from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

from apps.finance.reminders import get_finance_reminders
from apps.tasks.models import Task


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        report_reminders = get_finance_reminders()
        tasks = Task.get_current_tasks()

        context = {
            'report_reminders': report_reminders,
            'tasks': tasks,
        }

        return render(request, "main_page/index.html", context)
