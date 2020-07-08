from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

from apps.finance.reminders import get_finance_reminders
from apps.tasks.models import Task
from apps.finance.models import FinanceRegister


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        finance_balance = FinanceRegister.get_current_balance()
        report_reminders = get_finance_reminders()
        tasks = Task.get_current_tasks()

        context = {
            'finance_balance': finance_balance,
            'report_reminders': report_reminders,
            'tasks': tasks,
            'request': request,
        }

        return render(request, "main_page/index.html", context)
