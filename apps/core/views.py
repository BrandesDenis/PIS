import json
from typing import Optional, Dict

from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin
from django.http import HttpRequest, HttpResponse
from django.db.models import Model


class CreateUpdateView(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    def get_object(self, queryset=None) -> Optional[Model]:
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()

    def get_context_data(self, **kwargs) -> Dict:
        return super().get_context_data(**kwargs)


class NextRedirectMixin(FormMixin):
    def get_success_url(self, **kwargs) -> str:
        success_url = super().get_success_url(**kwargs)
        next_redirect = self.request.POST.get('next')

        return next_redirect if next_redirect else success_url

    def get_context_data(self, **kwargs) -> Dict:
        context = super().get_context_data(**kwargs)
        next_redirect = self.request.GET.get('next')
        if next_redirect:
            context['next'] = next_redirect

        return context
