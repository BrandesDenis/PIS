from typing import Dict

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.db.models import QuerySet

from apps.tasks.models import Task


class TaskCreate(CreateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task-all")
    template_name = "tasks/task/form.html"


class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("task-all")
    template_name = "tasks/task/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class TaskDelete(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        task = get_object_or_404(Task, pk=pk)
        task.delete()

        return HttpResponseRedirect(reverse("task-all"))


class TaskList(ListView):
    model = Task
    template_name = "tasks/task/list.html"

    def get_queryset(self) -> QuerySet:
        request_p = self.request.GET

        q = Task.objects

        status = request_p.get("status")
        if status:
            q = q.filter(status=status)

        return q.all()

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context['filter_status'] = self.request.GET.get("status")

        return context
