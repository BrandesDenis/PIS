from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from apps.reading.models import Reading
from apps.reading.forms import ReadingForm


class ReadingCreate(CreateView):
    model = Reading
    form_class = ReadingForm
    success_url = reverse_lazy("reading-list")
    template_name = "reading/form.html"


class ReadingUpdate(UpdateView):
    model = Reading
    form_class = ReadingForm
    success_url = reverse_lazy("reading-list")
    template_name = "reading/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context


class ReadingDelete(DeleteView):
    model = Reading
    success_url = reverse_lazy("reading-list")


class ReadingList(ListView):
    model = Reading
    template_name = "reading/list.html"
