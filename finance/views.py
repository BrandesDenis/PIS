from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from finance.models import FinanceObjectType


class FinanceObjectTypeCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-all')


class FinanceObjectTypeUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class FinanceObjectTypeDelete(View):

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.delete()

        return HttpResponseRedirect(reverse('task-all'))


class FinanceObjectTypeList(ListView):
    model = Task

    def get_queryset(self):
        request_p = self.request.GET

        q = Task.objects

        status = request_p.get('status')
        if status:
            q = q.filter(status=status)

        return q.all()
