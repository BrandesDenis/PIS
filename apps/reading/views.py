import subprocess

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView, View

from apps.reading.forms import ReadingForm
from apps.reading.models import Reading


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


class ReadingFiles(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:

        reading = get_object_or_404(Reading, pk=pk)
        path = reading.get_files_path()

        subprocess.call(["xdg-open", path])

        return HttpResponseRedirect(reverse("reading-detail", args=(pk,)))
