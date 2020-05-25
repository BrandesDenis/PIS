from typing import Dict

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from apps.thoughts.models import Thought, Topic
from apps.thoughts.forms import ThoughtForm, TopicRowForm


class ThoughtCreateView(CreateView):
    model = Thought
    template_name = "thought.html"
    form_class = ThoughtForm
    success_url = reverse_lazy("thoughts-list")

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save()

            for k, v in request.POST.items():
                if "topic" in k:
                    topic = Topic.objects.get(pk=v)
                    thought.topics.add(topic)

            return HttpResponseRedirect(reverse("thoughts-list"))

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["topic_row_form"] = TopicRowForm
        return context


class ThoughtUpdateView(UpdateView):
    model = Thought
    template_name = "thought.html"
    form_class = ThoughtForm
    success_url = reverse_lazy("thoughts-list")

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["topic_row_form"] = TopicRowForm
        context["is_update"] = True
        context["topics"] = self.object.topics.all()
        return context


class ThoughtDeleteView(DeleteView):
    model = Thought
    success_url = reverse_lazy("thoughts-list")


class ThoughtListView(ListView):
    model = Thought
    template_name = "thoughts_list.html"
