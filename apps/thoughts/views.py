from typing import Dict, Optional

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views import View

from apps.core.views import CreateUpdateView
from apps.thoughts.forms import ThoughtForm, TopicRowForm
from apps.thoughts.models import Thought, Topic


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "thoughts/index.html")


class TopicCreate(CreateView):
    model = Topic
    template_name = "thoughts/topic/form.html"
    fields = "__all__"
    success_url = reverse_lazy("topics-list")


class TopicUpdate(UpdateView):
    model = Topic
    template_name = "thoughts/topic/form.html"
    fields = "__all__"
    success_url = reverse_lazy("topics-list")

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class TopicDelete(DeleteView):
    model = Topic
    success_url = reverse_lazy("topics-list")


class TopicList(ListView):
    model = Topic
    template_name = "thoughts/topic/list.html"


class ThoughtView(CreateUpdateView):
    model = Thought
    template_name = "thoughts/thought/form.html"
    form_class = ThoughtForm
    success_url = reverse_lazy("thoughts-list")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        super().post(request, *args, **kwargs)

        errors = []

        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            thought = form.save()

            thought.topics.clear()
            has_topics = False
            for key, value in request.POST.items():
                if "topic" in key:
                    topic = get_object_or_404(Topic, pk=value)
                    thought.topics.add(topic)
                    has_topics = True

            if not has_topics:
                errors.append("Нельзя записать объект без темы")
        else:
            for _, error_list in form.errors.items():
                for error in error_list:
                    errors.append(error)

        if errors:
            context = self.get_context_data()
            context["errors"] = errors
            return render(request, self.template_name, context=context)
        else:
            return HttpResponseRedirect(reverse("thoughts-list"))

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        context["topic_row_form"] = TopicRowForm()

        if self.object:
            context["is_update"] = True
            topics = [
                TopicRowForm(initial={"topic": topic})
                for topic in self.object.topics.all()
            ]
            context["topics"] = topics

        return context


class ThoughtDeleteView(DeleteView):
    model = Thought
    success_url = reverse_lazy("thoughts-list")


class ThoughtListView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        thoughts_data = Thought.get_grouped_thoughts()

        context = {
            'thoughts_data': thoughts_data,
        }

        return render(request, "thoughts/thought/list.html", context)
