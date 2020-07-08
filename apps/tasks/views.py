from typing import Dict

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.db.models import QuerySet

from apps.tasks.models import Task
from apps.tasks.forms import TaskForm
from apps.core.views import NextRedirectMixin


class TaskCreate(NextRedirectMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-all")
    template_name = "tasks/task/form.html"


class TaskUpdate(NextRedirectMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task-all")
    template_name = "tasks/task/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class TaskDelete(NextRedirectMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task-all")


class TaskList(ListView):
    model = Task
    template_name = "tasks/task/list.html"

    def get_queryset(self) -> QuerySet:
        status_filter = self.request.GET.get('status')

        tasks = Task.objects

        if status_filter:
            tasks = tasks.filter(status=status_filter)

        return tasks.all()

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['filter_status'] = self.request.GET.get("status")

        return context
