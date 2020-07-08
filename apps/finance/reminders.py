from typing import List, Dict
from datetime import date, timedelta


from apps.finance.models import DayReport, PeriodicReport, Budget
from apps.core.dates import now, today, week_end, month_end, quarter_end


REMINDERS_START = date(day=1, month=7, year=2020)
REMINDERS_DEPTH = 30


def get_finance_reminders() -> List[Dict[str, date]]:
    reminders = []

    start_date = _get_start_date()

    day_report_dates = DayReport.objects\
        .filter(date__gte=start_date)\
        .values('date').all()

    week_report_dates = PeriodicReport.objects\
        .filter(report_type=PeriodicReport.ReportTypes.WEEK)\
        .filter(date__gte=start_date)\
        .values('date').all()

    month_report_dates = PeriodicReport.objects\
        .filter(report_type=PeriodicReport.ReportTypes.MONTH)\
        .filter(date__gte=start_date)\
        .values('date').all()

    quarter_report_dates = PeriodicReport.objects\
        .filter(report_type=PeriodicReport.ReportTypes.QUARTER)\
        .filter(date__gte=start_date)\
        .values('date').all()

    budget_dates = Budget.objects\
        .filter(date__gte=start_date)\
        .values('date').all()

    check_date = start_date
    day_delta = timedelta(days=1)

    day_report_index = 0
    week_report_index = 0
    month_report_index = 0
    quarter_report_index = 0
    budget_index = 0

    day_report_dates_iteration = True
    week_report_dates_iteration = True
    month_report_dates_iteration = True
    quarter_report_dates_iteration = True
    budget_dates_iteration = True

    today_date = today()
    end_date = today_date if now().hour > 20 else today_date - day_delta

    while check_date <= end_date:
        try:
            day_report_date = day_report_dates[day_report_index].get('date')
        except IndexError:
            day_report_dates_iteration = False

        if day_report_dates_iteration and check_date == day_report_date:
            day_report_index += 1
        else:
            reminders.append({'type': 'day_report', 'date': check_date})

        if check_date == week_end(check_date):
            try:
                week_report_date = week_report_dates[week_report_index].get('date')
            except IndexError:
                week_report_dates_iteration = False

            if week_report_dates_iteration and check_date == week_report_date:
                week_report_index += 1
            else:
                reminders.append(
                    {'type':
                     'periodic_report',
                     'report_type': PeriodicReport.ReportTypes.WEEK,
                     'date': check_date})

        if check_date == month_end(check_date):
            try:
                month_report_date = month_report_dates[month_report_index].get('date')
            except IndexError:
                month_report_dates_iteration = False

            if month_report_dates_iteration and check_date == month_report_date:
                month_report_index += 1
            else:
                reminders.append(
                    {'type':
                     'periodic_report',
                     'report_type': PeriodicReport.ReportTypes.MONTH,
                     'date': check_date})

            try:
                budget_date = budget_dates[budget_index].get('date')
            except IndexError:
                budget_dates_iteration = False

            # Бюджет на месяц заводится в последний день пред. месяца
            # Бюджет всегда заводится первым числом
            budget_check_date = check_date + day_delta
            if budget_dates_iteration and budget_check_date == budget_date:
                budget_index += 1
            else:
                reminders.append({'type': 'budget', 'date': budget_check_date})

        if check_date == quarter_end(check_date):
            try:
                quarter_report_date = quarter_report_dates[quarter_report_index].get(
                    'date')
            except IndexError:
                quarter_report_dates_iteration = False

            if quarter_report_dates_iteration and check_date == quarter_report_date:
                quarter_report_index += 1
            else:
                reminders.append(
                    {'type':
                     'periodic_report',
                     'report_type': PeriodicReport.ReportTypes.QUARTER,
                     'date': check_date})

        check_date += day_delta

    return reminders


def _get_start_date() -> date:
    depth_date = date.today() - timedelta(days=REMINDERS_DEPTH)

    return max(depth_date, REMINDERS_START)
