import calendar
import datetime
from typing import Dict

from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.core.views import CreateUpdateView
from apps.finance.forms import (BudgetForm, BudgetRowForm, ReportForm,
                                ReportRowForm, PeriodicReportForm, NewPeriodicReportForm)
from apps.finance.models import (Budget, BudgetRow, DayReport, DayReportRow,
                                 FinanceObject, PeriodicReport)
from apps.finance.reports import report_data


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "finance/index.html")


class FinanceObjectCreate(CreateView):
    model = FinanceObject
    template_name = "finance/fin_object_form.html"
    fields = "__all__"
    success_url = reverse_lazy("objects-all")


class FinanceObjectUpdate(UpdateView):
    model = FinanceObject
    template_name = "finance/fin_object_form.html"
    fields = "__all__"
    success_url = reverse_lazy("objects-all")

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class FinanceObjectDelete(DeleteView):
    model = FinanceObject
    template_name = "finance/fin_objects_list.html"


class FinanceObjectList(ListView):
    model = FinanceObject
    template_name = "finance/fin_objects_list.html"


class DayReportView(CreateUpdateView):
    model = DayReport
    template_name = "finance/day_report_form.html"
    form_class = ReportForm
    success_url = reverse_lazy("day_reports-all")

    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        super().post(request, *args, **kwargs)

        errors = []
        form = self.form_class(request.POST, instance=self.object)

        success = form.is_valid()
        if success:
            report = form.save()
            success, errors = DayReportRow.add_rows_from_request(report, request.POST)
        else:
            for _, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)

        if success:
            return HttpResponseRedirect(reverse("day_reports-all"))
        else:
            transaction.rollback()
            context = self.get_context_data()
            context["errors"] = errors
            return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["row_form"] = ReportRowForm()

        if self.object:
            context["is_update"] = True
            rows = [row for row in self.object.rows.all()]
        else:
            rows = DayReportRow.get_default_rows()

        context["rows"] = [ReportRowForm(instance=row) for row in rows]

        return context


class DayReportDelete(DeleteView):
    model = DayReport
    success_url = reverse_lazy("day_reports-all")


class DayReportList(ListView):
    model = DayReport
    template_name = "finance/day_reports_list.html"


class BudgetView(CreateUpdateView):
    model = Budget
    template_name = "finance/budget_form.html"
    form_class = BudgetForm
    success_url = reverse_lazy("budgets-all")

    @transaction.atomic
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        super().post(request, *args, **kwargs)

        errors = []
        form = self.form_class(request.POST, instance=self.object)

        success = form.is_valid()
        if success:
            budget = form.save()
            success, errors = BudgetRow.add_rows_from_request(budget, request.POST)
        else:
            for _, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)

        if success:
            return HttpResponseRedirect(reverse("budgets-all"))
        else:
            transaction.rollback()
            context = self.get_context_data()
            context["errors"] = errors
            return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["row_form"] = BudgetRowForm()

        if self.object:
            context["is_update"] = True
            rows = [row for row in self.object.rows.all()]
        else:
            rows = BudgetRow.get_default_rows()

        context["rows"] = [ReportRowForm(instance=row) for row in rows]

        return context


class BudgetDelete(DeleteView):
    model = Budget
    success_url = reverse_lazy("budgets-all")


class BudgetList(ListView):
    model = Budget
    template_name = "finance/budgets_list.html"


class ReportView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        today = datetime.date.today()

        # from apps.core.utils import quarter_start, quarter_end

        # quarter_start(today)

        start_date = request.GET.get('start_date')
        if not start_date:
            start_date = today.replace(day=1)

        end_date = request.GET.get('end_date')
        if not end_date:
            end_date = today.replace(day=calendar.monthrange(today.year, today.month)[1])

        context = report_data(start_date, end_date)
        context['start_date'] = start_date
        context['end_date'] = end_date

        return render(request, "finance/report.html", context)


class PeriodicReportView(CreateUpdateView):
    model = PeriodicReport
    template_name = "finance/periodic_report/form.html"
    form_class = PeriodicReportForm
    success_url = reverse_lazy("periodic_reports-all")

    def post(self,
             request: HttpRequest,
             * args,
             **kwargs) -> HttpResponse:

        super().post(request, *args, **kwargs)

        errors = []
        form = self.form_class(request.POST, instance=self.object)

        success = form.is_valid()
        if success:
            form.save()
        else:
            for _, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)

        if success:
            return HttpResponseRedirect(reverse("periodic_reports-all"))
        else:
            transaction.rollback()
            context = self.get_context_data()
            context["errors"] = errors
            return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs) -> Dict:
        if self.object:
            context = super().get_context_data(**kwargs)
            context["is_update"] = True
        else:
            report_type_param = self.request.GET.get('report_type')
            report_type = int(report_type_param) if report_type_param else 0

            report_date_param = self.request.GET.get('date')
            if report_date_param:
                report_date = datetime.datetime.strptime(report_date_param,
                                                         '%d.%m.%Y').date()
            else:
                report_date = datetime.date.today()

            new_report = self.model()
            new_report.report_type = report_type
            new_report.date = report_date

            new_report.collect_report_data()

            self.object = new_report

            context = super().get_context_data(**kwargs)

        return context


class PeriodicReportDelete(DeleteView):
    model = PeriodicReport
    success_url = reverse_lazy("periodic_reports-all")


class PeriodicReportList(ListView):
    model = PeriodicReport
    template_name = "finance/periodic_report/list.html"

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['new_report_form'] = NewPeriodicReportForm()

        return context
