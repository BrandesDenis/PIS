from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

from apps.finance.reminders import get_finance_reminders


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        report_reminders = get_finance_reminders()

        context = {'report_reminders': report_reminders}

        return render(request, "main_page/index.html", context)
