import datetime
import json
import os
from apps.finance.models import DayReport, DayReportRow, FinanceObject, Budget, PeriodicReport

finance_objects_matching = {
}

not_mathing_object = FinanceObject.objects.get(title='Разовые расходы')

'''
нужно учесть описание для разовых
нужно добавить тренировки в отчеты и периодчиеские отчеты
'''


def load_day_reports():
    source_path = ''

    files = os.listdir(source_path)

    for file in files:
        path = os.path.join(source_path, file)

        with open(path) as f:
            report_data_str = f.read()

        report_data = json.loads(report_data_str)

        report = DayReport(
            date=datetime.datetime.strptime(report_data['date'], '%d.%m.%y'),
            p1=int(report_data['p1']),
            p13=int(report_data['p13']),
            p3=int(report_data['p3']),
            p_union=int(report_data['p_union']),
            train=report_data['train'],
            comment=report_data['comment']
        )

        report.save()

        # rows
        total_income = 0.0
        total_outcome = 0.0
        for row in report_data['rows']:
            fin_object = finance_objects_matching.get(row['object'])
            if fin_object is None:
                fin_object = not_mathing_object
                print(f'{row["object"]} связано с разовым расходом')

            row_total = float(row['object'])

            DayReportRow(
                document=report,
                date=report.date,
                fin_object=fin_object,
                total=row_total,
            ).save()

            if fin_object.is_positive:
                total_income += row_total
            else:
                total_outcome += row_total

        report.total_income = total_income
        report.total_outcome = total_outcome
        report.total = total_income - total_outcome
        report.rows_added = True
        report.save()


def load_budgets():
    source_path = ''

    salary_object = FinanceObject.objects.get(title='Зарплата')

    files = os.listdir(source_path)

    for file in files:
        path = os.path.join(source_path, file)

        with open(path) as f:
            data_str = f.read()

        data = json.loads(data_str)

        budget = Budget(
            date=datetime.datetime.strptime(data['date'], '%d.%m.%y'),
        )

        budget.save()

        # rows
        total_income = 0.0
        total_outcome = 0.0

        incomes = int(data['incomes_plan'])
        if incomes:
            DayReportRow(
                document=budget,
                date=budget.date,
                fin_object=salary_object,
                total=incomes,
            ).save()

        for row in data['rows']:
            fin_object = finance_objects_matching.get(row['object'])
            if fin_object is None:
                fin_object = not_mathing_object
                print(f'{row["object"]} связано с разовым расходом')

            row_total = float(row['object'])

            DayReportRow(
                document=budget,
                date=budget.date,
                fin_object=fin_object,
                total=row_total,
            ).save()

            if fin_object.is_positive:
                total_income += row_total
            else:
                total_outcome += row_total

        budget.total_income = total_income
        budget.total_outcome = total_outcome
        budget.total = total_income - total_outcome
        budget.rows_added = True
        budget.save()


def load_priodic_reports():
    source_path_week = ''
    source_path_month = ''
    source_path_quarter = ''

    for report_type, source_path in enumerate((source_path_week, source_path_month, source_path_quarter)):
        files = os.listdir(source_path)

        for file in files:
            path = os.path.join(source_path, file)

            with open(path) as f:
                data_str = f.read()

            data = json.loads(data_str)

            PeriodicReport(
                date=datetime.datetime.strptime(data['date'], '%d.%m.%y'),
                report_type=report_type,
                p1=float(data['p1']),
                p13=float(data['p13']),
                p3=float(data['p3']),
                p_union=float(data['p_union']),
                trains=int(data['trains']),
                comment=data['comment'],
                total=float(data['total']),
            ).save()


def load_tasks():
    source_path = ''

    files = os.listdir(source_path)

    for file in files:
        path = os.path.join(source_path, file)

        with open(path) as f:
            data_str = f.read()

        data = json.loads(data_str)

        data_status = data['result']
        if data_status == 'Успешно':
            status = 1
        elif data_status == 'Провалено':
            status = 2
        else:
            status = 0

        PeriodicReport(
            start=datetime.datetime.strptime(data['start'], '%d.%m.%y'),
            end=datetime.datetime.strptime(data['end'], '%d.%m.%y'),
            description=data['text'],
            title=data['title'],
            paragraph=int(data['paragraph'].replace('П', '')),
            status=status
        ).save()
