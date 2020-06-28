from datetime import date
from typing import Iterable, Tuple

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg, Sum
from django.http import QueryDict
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.core import utils


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


class DayReport(models.Model):
    date = models.DateField(default=date.today,
                            unique=True,
                            verbose_name='Дата')
    p1 = models.PositiveIntegerField(verbose_name='П1',
                                     validators=(MaxValueValidator(10),))

    p13 = models.PositiveIntegerField(verbose_name='П13')

    p3 = models.PositiveIntegerField(verbose_name='П3',
                                     validators=(MaxValueValidator(10),))
    p_union = models.PositiveIntegerField(verbose_name='Общая оценка',
                                          validators=(MaxValueValidator(10),))

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)


class DayReportRow(models.Model):
    report = models.ForeignKey(DayReport,
                               related_name="rows",
                               on_delete=models.CASCADE)

    date = models.DateField(null=True)

    fin_object = models.ForeignKey(FinanceObject,
                                   related_name='reports',
                                   on_delete=models.PROTECT)
    description = models.CharField(max_length=500, blank=True)
    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    @staticmethod
    @receiver(pre_save, sender='finance.DayReportRow')
    def set_row_date(sender, instance, *args, **kwargs):
        instance.date = instance.report.date

    @classmethod
    def get_default_rows(cls) -> Iterable['BudgetRow']:
        default_row = cls()

        try:
            fin_object = FinanceObject.objects.get(title='Питание')
        except ObjectDoesNotExist:
            pass
        else:
            default_row.fin_object = fin_object

        return [default_row]

    @classmethod
    def add_rows_from_request(cls, report: DayReport, request_data: QueryDict) -> Tuple:
        errors = []
        success = True

        report.rows.all().delete()

        report_total = 0.0

        columns = ('fin_object', 'total', 'description')
        for fin_object_pk, total, description in \
                utils.collect_rows_from_request(request_data, columns):

            try:
                fin_object = FinanceObject.objects.get(pk=fin_object_pk)
            except ObjectDoesNotExist:
                errors.append(f'Не удалось найти fin_object с pk {fin_object_pk}')
                success = False
                break

            total = float(total)

            if fin_object.is_positive:
                report_total += total
            else:
                report_total -= total

            cls(
                report=report,
                fin_object=fin_object,
                description=description,
                total=total,
            ).save()

        if success:
            report.total = report_total
            report.save()

        return success, errors


class Budget(models.Model):
    date = models.DateField(default=date.today,
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

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)


class BudgetRow(models.Model):
    budget = models.ForeignKey(Budget, related_name="rows",
                               on_delete=models.CASCADE)

    date = models.DateField(null=True)

    fin_object = models.ForeignKey(FinanceObject,
                                   related_name='budgets',
                                   on_delete=models.PROTECT)
    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    @staticmethod
    @receiver(pre_save, sender='finance.BudgetRow')
    def set_row_date(sender, instance, *args, **kwargs):
        instance.date = instance.budget.date

    @classmethod
    def get_default_rows(cls) -> Iterable['BudgetRow']:
        try:
            latest_bugdet = Budget.objects.latest()
            rows = latest_bugdet.rows.all()
        except ObjectDoesNotExist:
            rows = tuple()

        return rows

    @classmethod
    def add_rows_from_request(cls, budget: Budget, request_data: QueryDict) -> Tuple:

        errors = []
        success = True

        budget.rows.all().delete()

        total_income = 0.0
        total_outcome = 0.0

        columns = ('fin_object', 'total')
        for fin_object_pk, total in utils.collect_rows_from_request(request_data,
                                                                    columns):

            try:
                fin_object = FinanceObject.objects.get(pk=fin_object_pk)
            except ObjectDoesNotExist:
                errors.append(f'Не удалось найти fin_object с pk {fin_object_pk}')
                success = False
                break

            total = float(total)

            if fin_object.is_positive:
                total_income += total
            else:
                total_outcome += total

            cls(
                budget=budget,
                fin_object=fin_object,
                total=total,
            ).save()

        if success:
            budget.total_income = total_income
            budget.total_outcome = total_outcome
            budget.save()

        return success, errors


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

    date = models.DateField(default=date.today,
                            verbose_name='Дата')

    p1 = models.FloatField(verbose_name='П1',
                           validators=(MaxValueValidator(10.0),))

    p13 = models.FloatField(verbose_name='П13')

    p3 = models.FloatField(verbose_name='П3',
                           validators=(MaxValueValidator(10.0),))
    p_union = models.FloatField(verbose_name='Общая оценка',
                                validators=(MaxValueValidator(10.0),))

    total = models.DecimalField(default=0,
                                blank=True,
                                max_digits=15,
                                decimal_places=2)

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        get_latest_by = 'date'
        ordering = ('date',)

        constraints = [
            models.UniqueConstraint(
                fields=['report_type', 'date'], name='unique report type'),
        ]

    def collect_report_data(self):
        if self.report_type == 0:
            source = DayReport.objects
            period = (
                utils.week_start(self.date),
                utils.week_end(self.date),
            )
        elif self.report_type == 1:
            source = PeriodicReport.objects.filter(report_type=0)
            period = (
                utils.month_start(self.date),
                utils.month_end(self.date),
            )
        else:
            source = PeriodicReport.objects.filter(report_type=1)
            period = (
                utils.quarter_start(self.date),
                utils.quarter_end(self.date),
            )

        source = source.filter(date__range=period)

        aggregates = source.aggregate(
            Avg('p1'),
            Avg('p13'),
            Avg('p3'),
            Avg('p_union'),
            Sum('total'),
        )

        self.p1 = aggregates.get('p1__avg', 0)
        self.p13 = aggregates.get('p13__avg', 0)
        self.p3 = aggregates.get('p3__avg', 0)
        self.p_union = aggregates.get('p_union__avg', 0)
        self.total = aggregates.get('total__sum', 0)

        comments_list = [report.comment for report in source]
        self.comment = '\n'.join(comments_list)
