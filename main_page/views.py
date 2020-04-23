from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


class IndexView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {1: 1}
        return render(request, 'main_page/index.html', context)
