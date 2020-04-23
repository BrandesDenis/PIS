from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from finance.models import FinanceObjectType, FinanceObject, DayReport


class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'finance/index.html')


class FinanceObjectTypeCreate(CreateView):
    model = FinanceObjectType
    template_name = 'finance/fin_type_form.html'
    fields = '__all__'
    success_url = reverse_lazy('types-all')


class FinanceObjectTypeUpdate(UpdateView):
    model = FinanceObjectType
    template_name = 'finance/fin_type_form.html'
    fields = '__all__'
    success_url = reverse_lazy('types-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class FinanceObjectTypeDelete(View):

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(FinanceObjectType, pk=pk)
        task.delete()

        return HttpResponseRedirect(reverse('types-all'))


class FinanceObjectTypeList(ListView):
    model = FinanceObjectType
    template_name = 'finance/fin_types_list.html'


###

class FinanceObjectCreate(CreateView):
    model = FinanceObject
    template_name = 'finance/fin_object_form.html'
    fields = '__all__'
    success_url = reverse_lazy('objects-all')


class FinanceObjectUpdate(UpdateView):
    model = FinanceObject
    template_name = 'finance/fin_object_form.html'
    fields = '__all__'
    success_url = reverse_lazy('objects-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class FinanceObjectDelete(View):

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(FinanceObject, pk=pk)
        task.delete()

        return HttpResponseRedirect(reverse('objects-all'))


class FinanceObjectList(ListView):
    model = FinanceObject
    template_name = 'finance/fin_objects_list.html'

###


class DayReportCreate(CreateView):
    model = DayReport
    template_name = 'finance/day_report_form.html'
    fields = '__all__'
    success_url = reverse_lazy('day_reports-all')

    def post(self, request):
        a = 1


class DayReportUpdate(UpdateView):
    model = DayReport
    template_name = 'finance/day_report_form.html'
    fields = '__all__'
    success_url = reverse_lazy('day_reports-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class DayReportDelete(View):

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(DayReport, pk=pk)
        task.delete()

        return HttpResponseRedirect(reverse('day_reports-all'))


class DayReportList(ListView):
    model = DayReport
    template_name = 'finance/day_reports_list.html'
