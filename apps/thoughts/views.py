from typing import Dict, Optional

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import (
    DeleteView,
    ModelFormMixin,
    ProcessFormView,
)
from django.views.generic.list import ListView

from apps.thoughts.forms import ThoughtForm, TopicRowForm
from apps.thoughts.models import Thought, Topic


# TODO - транзакция
# TODO - подумать, над наиболее правильным View
class ThoughtView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = Thought
    template_name = "thought.html"
    form_class = ThoughtForm
    success_url = reverse_lazy("thoughts-list")

    def get_object(self, queryset=None) -> Optional[Thought]:
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


class ThoughtListView(ListView):
    model = Thought
    template_name = "thoughts_list.html"
