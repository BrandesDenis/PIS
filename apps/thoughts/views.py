from typing import Optional

from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from apps.thoughts.models import Thought


class ThoughtCreateView(CreateView):
    model = Thought
    template_name = "thought.html"
    fields = "__all__"
    success_url = reverse_lazy("day_reports-all")

    def post(self, request):
        a = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["row_form"] = ReportRowForm

        return context


class ThoughtUpdateView(UpdateView):
    model = Thought
    template_name = "thought.html"
    fields = "__all__"
    success_url = reverse_lazy("day_reports-all")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class ThoughtDeleteView(DeleteView):
    model = Thought
    success_url = reverse_lazy("day_reports-all")


class ThoughtListView(ListView):
    model = Thought
    template_name = "thoughts_list.html"
