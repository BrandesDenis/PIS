import datetime
from typing import Dict

from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.core.collect_request_data import collect_start_end_dates_reports
from apps.core.dates import date_pretty_format, html_date_format, today
from apps.core.views import CreateUpdateView, NextRedirectMixin
from apps.finance.forms import (BudgetForm, BudgetRowForm,
                                NewPeriodicReportForm, PeriodicReportForm,
                                ReportForm, ReportRowForm)
from apps.finance.models import (Budget, BudgetRow, DayReport, DayReportRow,
                                 FinanceObject, PeriodicReport)
from apps.finance.reports.fin_object_detalization import \
    fin_object_detalization
from apps.finance.reports.finance_report import finance_report


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "finance/index.html")


class FinanceObjectCreate(CreateView):
    model = FinanceObject
    template_name = "finance/fin_object/form.html"
    fields = "__all__"
    success_url = reverse_lazy("objects-all")


class FinanceObjectUpdate(UpdateView):
    model = FinanceObject
    template_name = "finance/fin_object/form.html"
    fields = "__all__"
    success_url = reverse_lazy("objects-all")

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class FinanceObjectDelete(DeleteView):
    model = FinanceObject
    success_url = reverse_lazy("objects-all")


class FinanceObjectList(ListView):
    model = FinanceObject
    template_name = "finance/fin_object/list.html"


class DayReportView(NextRedirectMixin, CreateUpdateView):
    model = DayReport
    template_name = "finance/day_report/form.html"
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
            DayReportRow.add_rows_from_request(report, request.POST)
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

            report_date_param = self.request.GET.get('date')
            if report_date_param:
                report_date = datetime.datetime.strptime(report_date_param,
                                                         '%d.%m.%Y').date()
            else:
                report_date = today()

            context['form'].initial['date'] = date_pretty_format(report_date)

        context["rows"] = [ReportRowForm(instance=row) for row in rows]

        return context


class DayReportDelete(NextRedirectMixin, DeleteView):
    model = DayReport
    success_url = reverse_lazy("day_reports-all")


class DayReportList(ListView):
    paginate_by = 15
    model = DayReport
    template_name = "finance/day_report/list.html"


class BudgetView(NextRedirectMixin, CreateUpdateView):
    model = Budget
    template_name = "finance/budget/form.html"
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
            BudgetRow.add_rows_from_request(budget, request.POST)
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

            report_date_param = self.request.GET.get('date')
            if report_date_param:
                report_date = datetime.datetime.strptime(report_date_param,
                                                         '%d.%m.%Y').date()
            else:
                report_date = today()

            context['form'].initial['date'] = date_pretty_format(report_date)

        context["rows"] = [ReportRowForm(instance=row) for row in rows]

        return context


class BudgetDelete(NextRedirectMixin, DeleteView):
    model = Budget
    success_url = reverse_lazy("budgets-all")


class BudgetList(ListView):
    model = Budget
    template_name = "finance/budget/list.html"


class ReportView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        start_date, end_date = collect_start_end_dates_reports(request.GET)

        context = finance_report(start_date, end_date)

        context['start_date'] = html_date_format(start_date)
        context['end_date'] = html_date_format(end_date)

        return render(request, "finance/reports/report.html", context)


class FinObjectDetalizationReportView(View):

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:

        fin_object = get_object_or_404(FinanceObject, pk=pk)

        start_date, end_date = collect_start_end_dates_reports(request.GET)

        context = fin_object_detalization(start_date, end_date, fin_object)

        context['start_date'] = date_pretty_format(start_date)
        context['end_date'] = date_pretty_format(end_date)
        context['title'] = fin_object.title

        return render(request, "finance/reports/fin_object_detalization.html", context)


class PeriodicReportView(NextRedirectMixin, CreateUpdateView):
    model = PeriodicReport
    template_name = "finance/periodic_report/form.html"
    form_class = PeriodicReportForm
    success_url = reverse_lazy("periodic_reports-all")

    def post(self,
             request: HttpRequest,
             *args,
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
                report_date = today()

            new_report = self.model()
            new_report.report_type = report_type
            new_report.date = report_date

            new_report.collect_report_data()

            self.object = new_report

            context = super().get_context_data(**kwargs)

        context['tasks'] = self.object.get_reports_tasks()

        return context


class PeriodicReportDelete(NextRedirectMixin, DeleteView):
    model = PeriodicReport
    success_url = reverse_lazy("periodic_reports-all")


class PeriodicReportList(ListView):
    model = PeriodicReport
    template_name = "finance/periodic_report/list.html"

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['new_report_form'] = NewPeriodicReportForm()

        return context
