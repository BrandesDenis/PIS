import datetime
from typing import Iterable, Tuple, Optional
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Sum
from django.http import QueryDict

from apps.tasks.models import Task
from apps.core.collect_request_data import collect_rows
from apps.core.dates import (month_end, month_start, quarter_end,
                             quarter_start, week_end, week_start)


class FinanceObject(models.Model):
    title = models.CharField(unique=True, max_length=100,
                             verbose_name='Название')
    is_positive = models.BooleanField(default=False, verbose_name='Это доход')
    need_description = models.BooleanField(default=False,
                                           verbose_name='Требуется указывать описание')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-is_positive', 'title')


class FinanceDocument(models.Model):
    total_income = models.DecimalField(default=0,
                                       blank=True,
                                       max_digits=15,
                                       decimal_places=2)

    total_outcome = models.DecimalField(default=0,
                                        blank=True,
                                        max_digits=15,
                                        decimal_places=2)

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    rows_added = models.BooleanField(default=False)

    class Meta:
        abstract = True


class FinanceDocumentRow(models.Model):
    document = models.ForeignKey(FinanceDocument,
                                 related_name="rows",
                                 on_delete=models.CASCADE)

    date = models.DateField(null=True)

    fin_object = models.ForeignKey(FinanceObject,
                                   on_delete=models.PROTECT)

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    additional_columns: Optional[Tuple[str]] = None

    class Meta:
        abstract = True

    @classmethod
    def add_rows_from_request(cls,
                              document: FinanceDocument,
                              request_data: QueryDict) -> None:

        document.rows.all().delete()

        total_income = 0.0
        total_outcome = 0.0

        columns = ('fin_object', 'total')

        for fin_object_pk, row_total in \
                collect_rows(request_data, columns):

            fin_object = FinanceObject.objects.get(pk=fin_object_pk)

            row_total = float(row_total)

            if fin_object.is_positive:
                total_income += row_total
            else:
                total_outcome += row_total

            cls(
                document=document,
                date=document.date,
                fin_object=fin_object,
                total=row_total,
            ).save()

        document.total_income = total_income
        document.total_outcome = total_outcome
        document.total = total_income - total_outcome
        document.rows_added = True
        document.save()


class DayReport(FinanceDocument):
    date = models.DateField(default=datetime.date.today,
                            unique=True,
                            verbose_name='Дата')
    p1 = models.PositiveIntegerField(verbose_name='П1',
                                     validators=(MaxValueValidator(10),))

    p13 = models.FloatField(verbose_name='П13',
                            validators=(MinValueValidator(0),))

    p3 = models.PositiveIntegerField(verbose_name='П3',
                                     validators=(MaxValueValidator(10),))
    p_union = models.PositiveIntegerField(verbose_name='Общая оценка',
                                          validators=(MaxValueValidator(10),))

    train = models.BooleanField(default=False, verbose_name='Тренировка')

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)


class DayReportRow(FinanceDocumentRow):

    document = models.ForeignKey(DayReport,
                                 related_name="rows",
                                 on_delete=models.CASCADE)

    fin_object = models.ForeignKey(FinanceObject,
                                   related_name="report_rows",
                                   on_delete=models.PROTECT)

    @classmethod
    def get_default_rows(cls) -> Iterable['DayReportRow']:
        default_row = cls()

        try:
            fin_object = FinanceObject.objects.get(title='Питание')
        except ObjectDoesNotExist:
            pass
        else:
            default_row.fin_object = fin_object

        return [default_row]


class FinanceRegister(models.Model):
    month = models.DateField(default=datetime.date.today,
                             unique=True,
                             verbose_name='Месяц')

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    balance = models.DecimalField(default=0,
                                  blank=True,
                                  max_digits=15,
                                  decimal_places=2)

    class Meta:
        get_latest_by = 'month'
        ordering = ('month',)

    @classmethod
    def calculate_month_balance(cls, date: datetime.date) -> None:
        # -1 день чтобы в последний день месяца не получить его же баланс
        previous_month_balance = cls._get_latest_balance(
            date-datetime.timedelta(days=1))

        month_start_ = month_start(date)
        month_end_ = month_end(date)
        month_total = cls._get_range_operations_total(
            month_start_, month_end_)

        if month_total:
            month_balance = previous_month_balance + month_total

            cls.objects.update_or_create(month=month_end_,
                                         defaults={
                                             'balance': month_balance,
                                             'total': month_total,
                                         })

            cls._recalculate_next_months_balances(month_end_, month_balance)

    @classmethod
    def recalculate_all(cls) -> None:
        # cls.objects.all().delete()
        pass

    @classmethod
    def _recalculate_next_months_balances(cls,
                                          date: datetime.date,
                                          start_balance: Decimal) -> None:

        balance = start_balance
        next_months = cls.objects.filter(month__gt=date).all()
        for month in next_months:
            balance += month.total
            month.balance = balance
            month.save()

    @classmethod
    def get_current_balance(cls) -> Decimal:
        latest_month = cls.objects.latest()

        return latest_month.balance if latest_month else Decimal(0)

    @classmethod
    def get_date_balance(cls, date: datetime.date) -> Decimal:
        latest_balance = cls._get_latest_balance(date)

        if date != month_end(date):
            month_start_ = month_start(date)
            range_total = cls._get_range_operations_total(month_start_, date)
        else:
            range_total = Decimal(0)

        return latest_balance + range_total

    @classmethod
    def _get_latest_balance(cls, date: datetime.date) -> Decimal:
        latest_month = cls.objects.filter(month__lte=date).order_by('-month').first()

        return latest_month.balance if latest_month else Decimal(0)

    @classmethod
    def _get_range_operations_total(cls,
                                    start_date: datetime.date,
                                    end_date: datetime.date) -> Decimal:

        return DayReport.objects\
            .filter(date__range=(start_date, end_date))\
            .aggregate(Sum('total')).get('total__sum') or Decimal(0)


class Budget(FinanceDocument):
    date = models.DateField(default=datetime.date.today,
                            unique=True,
                            verbose_name='Дата')

    total_income = models.DecimalField(default=0,
                                       blank=True,
                                       max_digits=15,
                                       decimal_places=2)

    total_outcome = models.DecimalField(default=0,
                                        blank=True,
                                        max_digits=15,
                                        decimal_places=2)

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)


class BudgetRow(FinanceDocumentRow):

    document = models.ForeignKey(Budget,
                                 related_name="rows",
                                 on_delete=models.CASCADE)

    fin_object = models.ForeignKey(FinanceObject,
                                   related_name="budget_rows",
                                   on_delete=models.PROTECT)

    @classmethod
    def get_default_rows(cls) -> Iterable['BudgetRow']:
        try:
            latest_bugdet = Budget.objects.latest()
            rows = latest_bugdet.rows.all()
        except ObjectDoesNotExist:
            rows = tuple()

        return rows


class PeriodicReport(models.Model):

    class ReportTypes():
        WEEK = 0
        MONTH = 1
        QUARTER = 2

        choises = (
            (WEEK, 'Недельный'),
            (MONTH, 'Месячный'),
            (QUARTER, 'Квартальный'),
        )

    report_type = models.IntegerField(choices=ReportTypes.choises,
                                      verbose_name='Тип отчета')

    date = models.DateField(default=datetime.date.today,
                            verbose_name='Дата')

    p1 = models.FloatField(verbose_name='П1',
                           validators=(MaxValueValidator(10.0),))

    p13 = models.FloatField(verbose_name='П13')

    p3 = models.FloatField(verbose_name='П3',
                           validators=(MaxValueValidator(10.0),))
    p_union = models.FloatField(verbose_name='Общая оценка',
                                validators=(MaxValueValidator(10.0),))

    total = models.DecimalField(default=0,
                                verbose_name='Итог ДС',
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    trains = models.PositiveIntegerField(verbose_name='Тренировок')

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)

        constraints = [
            models.UniqueConstraint(
                fields=['report_type', 'date'], name='unique report type'),
        ]

    def _get_report_period(self) -> Tuple[datetime.date]:
        if self.report_type == 0:
            period = (
                week_start(self.date),
                week_end(self.date),
            )
        elif self.report_type == 1:
            period = (
                month_start(self.date),
                month_end(self.date),
            )
        else:
            period = (
                quarter_start(self.date),
                quarter_end(self.date),
            )

        return period

    def _get_report_source(self) -> models.QuerySet:
        if self.report_type == 0:
            source = DayReport.objects
        elif self.report_type == 1:
            source = PeriodicReport.objects.filter(report_type=0)
        else:
            source = PeriodicReport.objects.filter(report_type=1)

        return source

    def collect_report_data(self):
        source = self._get_report_source()
        period = self._get_report_period()

        source = source.filter(date__range=period)

        aggregates = source.aggregate(
            Avg('p1'),
            Sum('p13'),
            Avg('p3'),
            Avg('p_union'),
            Sum('total'),
        )

        self.p1 = round(aggregates.get('p1__avg') or 0, 2)
        self.p13 = aggregates.get('p13__sum') or 0
        self.p3 = round(aggregates.get('p3__avg') or 0, 2)
        self.p_union = round(aggregates.get('p_union__avg') or 0, 2)
        self.total = aggregates.get('total__sum') or 0

        comments_list = [report.comment for report in source]
        self.comment = '\n'.join(comments_list)

    def get_reports_tasks(self):
        period = self._get_report_period()

        return Task.objects.filter(end__range=period)\
            .exclude(status=Task.TaskStatuses.IN_PROGRESS).all()
