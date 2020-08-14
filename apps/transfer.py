import datetime
import json
import os

from django.db.utils import IntegrityError

from apps.finance.models import DayReport, DayReportRow, FinanceObject, Budget, BudgetRow, PeriodicReport
from apps.tasks.models import Task
from apps.reading.models import Reading
from apps.thoughts.models import Thought, Topic


def transfer(_):
    load_thoughts()
    load_day_reports()
    load_budgets()
    load_periodic_reports()
    load_tasks()
    load_readings()
    load_thoughts()


not_loading_objects = {
    'Перераспределение(Д)',
    'Перераспределение(Р)',
    'Долг(Д)',
}

finance_objects_matching = {
    'Ипотека': 'Ипотека',
    'Долг бате по ипотеке': 'Долг бате по ипотеке',
    'Отдых': 'Отдых',
    'Кино': 'Отдых',
    # 'Рубашки,свитера,футболки': '',
    # 'Обувь и аксессуары': '',
    # 'Спортпит': '',
    # 'Тренажерный зал': '',
    # 'Штаны': '',
    # 'Стрижка и прочее': '',
    # 'Куртки и подобное': '',
    # 'Прочая одежда': '',
    # 'Брюки, штаны, шорты': '',
    # 'Танго': '',
    # 'Штаны, шорты': '',
    # 'Пиджак': '',
    # 'Гантели': '',
    # 'Парфюм': '',
    # 'Спортивная сумка': '',
    # 'Аксессуары': '',
    # 'Гигиенические принадлежности': '',
    # 'Турник': '',
    # 'Груша': '',
    # 'Пр. расходы на п14': '',
    # 'Химчистка одежды': '',
    # 'Перчатки для груши': '',
    # 'Витамины,лекарства...': '',
    # 'Селфи палка': '',
    # 'Средства личной гигиены': '',
    # 'Прочие(спорт)': '',
    'Питание': 'Питание',

    'Погрешность(расход)': 'Прочий расход',
    'Подарки девушке': 'Прочий расход',
    'Подарки родителям': 'Прочий расход',
    'Подарки(старая статья)': 'Прочий расход',
    'Подарки прочие': 'Прочий расход',
    'Подарки друзьям': 'Прочий расход',
    'Ранний расход': 'Прочий расход',
    'Прочий расход': 'Прочий расход',


    'Бензин': 'Машина',
    'Страховка': 'Машина',
    'Ремонт автомобиля': 'Машина',
    'Шины': 'Машина',
    'Налоги,штрафы - машина': 'Машина',
    'Аккумулятор': 'Машина',
    'Машинное масло': 'Машина',
    'Ремонт крыши': 'Машина',
    'Прочие расходы на машину': 'Машина',
    'Сцепление': 'Машина',
    'Автомойка': 'Машина',
    'бампер': 'Машина',
    'Перебортовка': 'Машина',
    'Амортизаторы передние': 'Машина',
    'Прочие детали(машина)': 'Машина',
    'Антифриз': 'Машина',
    'Диски': 'Машина',
    "Амортизаторы": 'Машина',
    'Техосмотр': 'Машина',
    'Глушитель': 'Машина',
    'Крышки амотризаторов': 'Машина',
    'Тормозные шланги': 'Машина',
    'Лючок бензобака': 'Машина',
    'тормозные колодки': 'Машина',
    'Одеяло для двигателя': 'Машина',
    'Термостат': 'Машина',
    'Огнетушитель': 'Машина',
    "Шнур регистратора": 'Машина',
    'Воздушный фильтр': 'Машина',
    'Щетка': 'Машина',
    'Рамка для номера': 'Машина',
    'Тормозная жидкость': 'Машина',

    'Квартплата': 'Бытовые расходы',
    'Связь и интернет': 'Бытовые расходы',
    'Коммуналка': 'Бытовые расходы',
    'Прочие бытовые расходы': 'Бытовые расходы',
    'Средства личной гигиены': 'Бытовые расходы',
    'Прочие материалы ремонт': 'Бытовые расходы',

    # 'Расходы на операцию ПКС': '',
    # 'Лечение': '',
    # 'Лекарства': '',
    # 'Очки для компьютера': '',
    # 'Лечение зубов': '',
    # 'Фиксатор осанки': '',

    # 'Транспорт': '',
    # 'Такси': '',
    # 'Налоги': '',
    'Переоценка актива(Доход)': 'Прочий доход',
    'Фриланс': 'Фриланс',

    'Кэшбек': 'Кэшбек',
    'Рост вклада': 'Рост вклада',

    'Возмещение за машину': 'Прочий доход',
    'Возврат покупок': 'Прочий доход',
    'Прочий доход': 'Прочий доход',
    'Погрешность(доход)': 'Прочий доход',
    'Подарки денежные(мне)': 'Прочий доход',
    'Возмещение НДФЛ': 'Прочий доход',

    'Подарки родителей': 'Подарки родителей',
    'Помощь родителей по ипотеке и ремонту': 'Помощь родителей по ипотеке и ремонту',

    'Зарплата': 'Зарплата',
}

not_mathing_object = FinanceObject.objects.get(title='Разовые расходы')
# not_mathing_object = None


def load_day_reports():
    source_path = 'Z:\\перенос ПИС\\Ежотчеты'

    files = os.listdir(source_path)

    not_mathing_object_names = set()

    for file in files:
        if '.ini' in file:
            continue
        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            report_data_str = f.read().decode('utf-8-sig')

        report_data = json.loads(report_data_str)

        report = DayReport(
            date=datetime.datetime.strptime(report_data['date'], '%d.%m.%Y'),
            p1=int(report_data['p11']),
            p13=int(report_data['p13']),
            p3=int(report_data['p3']),
            p_union=int(report_data['union']),
            train=report_data['train'],
            comment=report_data['comment']
        )

        try:
            report.save()
        except IntegrityError:
            print(f'Отчет за {report.date} в файле {file} имеет дубль!')
            continue

        # rows
        total_income = 0.0
        total_outcome = 0.0
        for row in report_data['rows']:
            fin_object_ = row['object']
            if fin_object_ in not_loading_objects:
                continue
            row_total = float(row['total'])
            if not row_total:
                continue

            description = None
            if fin_object_ == '':
                fin_object = not_mathing_object
                description = 'Нет описания'
                print(
                    f'В отчете за {report.date} строка на сумму {row_total} не имеет описания!')
            else:
                fin_object_match = finance_objects_matching.get(fin_object_)
                if fin_object_match is None:
                    fin_object = not_mathing_object
                    if fin_object_ not in not_mathing_object_names:
                        not_mathing_object_names.add(fin_object_)
                        print(f'{fin_object_} связано с разовым расходом')
                else:
                    fin_object = FinanceObject.objects.get(title=fin_object_match)

                if fin_object.need_description:
                    description = fin_object_

            if fin_object.is_positive == True:
                total_income += row_total
            else:
                total_outcome += row_total

            DayReportRow(
                document=report,
                date=report.date,
                fin_object=fin_object,
                description=description,
                total=row_total,
            ).save()

        report.total_income = total_income
        report.total_outcome = total_outcome
        report.total = total_income - total_outcome
        report.rows_added = True
        report.save()


def load_budgets():
    source_path = 'Z:\\перенос ПИС\\Бюджеты'

    not_mathing_object_names = set()

    salary_object = FinanceObject.objects.get(title='Зарплата')

    files = os.listdir(source_path)

    for file in files:
        if '.ini' in file:
            continue
        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            data_str = f.read().decode('utf-8-sig')

        data = json.loads(data_str)

        budget = Budget(
            date=datetime.datetime.strptime(data['date'], '%d.%m.%Y'),
        )

        budget.save()

        # rows
        incomes = int(data['incomes_plan'])
        if incomes:
            BudgetRow(
                document=budget,
                date=budget.date,
                fin_object=salary_object,
                total=incomes,
            ).save()

        total_income = incomes
        total_outcome = 0.0
        for row in data['rows_budget']:
            fin_object_ = row['object']
            if fin_object_ in not_loading_objects:
                continue
            row_total = float(row['total'])
            if not row_total:
                continue

            description = None
            if fin_object_ == '':
                fin_object = not_mathing_object
                description = 'Нет описания'
                print(
                    f'В бюджете за {budget.date} строка на сумму {row_total} не имеет описания!')
            else:
                fin_object_match = finance_objects_matching.get(fin_object_)
                if fin_object_match is None:
                    fin_object = not_mathing_object
                    if fin_object_ not in not_mathing_object_names:
                        not_mathing_object_names.add(fin_object_)
                        print(f'{fin_object_} связано с разовым расходом')
                else:
                    fin_object = FinanceObject.objects.get(title=fin_object_match)

                if fin_object.need_description:
                    description = fin_object_

            if fin_object.is_positive == True:
                total_income += row_total
            else:
                total_outcome += row_total

            BudgetRow(
                document=budget,
                date=budget.date,
                fin_object=fin_object,
                description=description,
                total=row_total,
            ).save()

        budget.total_income = total_income
        budget.total_outcome = total_outcome
        budget.total = total_income - total_outcome
        budget.rows_added = True
        budget.save()


def load_periodic_reports():
    source_path = 'Z:\\перенос ПИС\\Периодические отчеты'

    files = os.listdir(source_path)

    for file in files:
        if '.ini' in file:
            continue

        if file.startswith('week'):
            report_type = 0
        elif file.startswith('month'):
            report_type = 1
        elif file.startswith('quarter'):
            report_type = 2

        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            data_str = f.read().decode('utf-8-sig')

        data = json.loads(data_str)

        PeriodicReport(
            date=datetime.datetime.strptime(data['date'], '%d.%m.%Y'),
            report_type=report_type,
            p1=float(data['p11']),
            p13=float(data['p13']),
            p3=float(data['p3']),
            p_union=float(data['union']),
            trains=int(data['trains']),
            comment=data['comment'],
            total=float(data['finance_total']),
        ).save()


def load_tasks():
    source_path = 'Z:\\перенос ПИС\\Задачи'

    files = os.listdir(source_path)

    for file in files:
        if '.ini' in file:
            continue

        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            data_str = f.read().decode('utf-8-sig')

        data = json.loads(data_str)

        data_status = data['result']
        if data_status == 'Успешно':
            status = 1
        elif data_status == 'Провалено':
            status = 2
        else:
            status = 0

        paragraph_ = data['paragraph'].replace('П', '')
        if paragraph_:
            paragraph = int(paragraph_)
        else:
            paragraph = 52

        task = Task(
            start=datetime.datetime.strptime(data['start'], '%d.%m.%Y').date(),
            end=datetime.datetime.strptime(data['end'], '%d.%m.%Y').date(),
            description=data['text'],
            title=data['title'],
            paragraph=paragraph,
            status=status
        )

        try:
            task.save()
        except IntegrityError:
            task.title += data['end']
            task.save()


def load_readings():
    source_path = 'Z:\\перенос ПИС\\\Чтения'

    files = os.listdir(source_path)

    for file in files:
        if '.ini' in file:
            continue

        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            data_str = f.read().decode('utf-8-sig')

        data = json.loads(data_str)

        end_ = data['finished']
        if end_ != '':
            end = datetime.datetime.strptime(end_, '%d.%m.%Y').date()
        else:
            end = None

        reading = Reading(
            start=datetime.datetime.strptime(data['created'], '%d.%m.%Y').date(),
            end=end,
            description=data['text'],
            title=data['title'],
            autor=data['autor'],
        )

        reading.save()


def load_thoughts():
    source_path = 'Z:\\перенос ПИС\\Исследования'

    files = os.listdir(source_path)

    for file in files:
        if '.ini' in file:
            continue

        path = os.path.join(source_path, file)

        with open(path, 'rb') as f:
            data_str = f.read().decode('utf-8-sig')

        data = json.loads(data_str)

        thought = Thought(
            created=datetime.datetime.strptime(data['created'], '%d.%m.%Y').date(),
            finished=data['finished'],
            title=data['title'],
            content=data['html'],
        )

        thought.save()

        for topic_data in data['topics']:
            topic, _ = Topic.objects.get_or_create(
                title=topic_data['title'],
                defaults={'paragraph': int(topic_data['paragraph'].replace('П', ''))}
            )
            topic.save()
            thought.topics.add(topic)

        thought.save()
