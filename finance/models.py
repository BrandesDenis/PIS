from datetime import date
from typing import NoReturn

from django.db import models


class FinanceObjectType(models.Model):
    title = models.CharField(unique=True, max_length=100)
    is_positive = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FinanceObject(models.Model):
    object_type = models.ForeignKey(
        FinanceObjectType, on_delete=models.CASCADE, related_name='fin_objects')
    title = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.title


class DayReport(models.Model):
    date = models.DateField(default=date.today, unique=True)
    p1 = models.PositiveIntegerField()
    p13 = models.PositiveIntegerField()
    p3 = models.PositiveIntegerField()
    p_union = models.PositiveIntegerField()

    total = models.FloatField(default=0, blank=True)
    comment = models.TextField(blank=True)


class DayReportRow(models.Model):
    report = models.ForeignKey(DayReport, related_name='rows', on_delete=models.CASCADE)
    fin_object = models.ForeignKey(FinanceObject, on_delete=models.PROTECT)
    total = models.PositiveIntegerField()
