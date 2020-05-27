from typing import Optional, Dict

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    ModelFormMixin,
    ProcessFormView,
)
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from apps.finance.models import (
    FinanceObject,
    DayReport,
    DayReportRow,
)
from apps.finance.forms import ReportForm, ReportRowForm


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


class DayReportView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = DayReport
    template_name = "finance/day_report_form.html"
    form_class = ReportForm
    success_url = reverse_lazy("day_reports-all")

    def get_object(self, queryset=None) -> Optional[DayReport]:
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()

        errors = []

        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            report = form.save()
            report.rows.all().delete()

            report_total = 0.0
            for key, value in request.POST.items():
                if "fin_object" in key:
                    fin_object = get_object_or_404(FinanceObject, pk=value)
                if "description" in key:
                    description = value
                if "total" in key:
                    total = float(value)

                    if fin_object.is_positive:
                        report_total += total
                    else:
                        report_total -= total

                    DayReportRow(
                        report=report,
                        fin_object=fin_object,
                        description=description,
                        total=total,
                    ).save()

            report.total = report_total
            report.save()

        else:
            for _, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)

        if errors:
            context = self.get_context_data()
            context["errors"] = errors
            return render(request, self.template_name, context=context)
        else:
            return HttpResponseRedirect(reverse("day_reports-all"))

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["row_form"] = ReportRowForm()

        if self.object:
            context["is_update"] = True
            rows = [ReportRowForm(instance=row) for row in self.object.rows.all()]
            context["rows"] = rows

        return context


class DayReportDelete(DeleteView):
    model = DayReport
    template_name = "finance/day_reports_list.html"


class DayReportList(ListView):
    model = DayReport
    template_name = "finance/day_reports_list.html"
