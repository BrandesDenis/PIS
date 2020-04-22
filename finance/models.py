from datetime import date
from typing import NoReturn

from django.db import models


class FinanceObjectType(models.Model):
    title = models.CharField(unique=True, max_length=100)
    is_positive = models.BooleanField(default=False)
    is_exchange = models.BooleanField(default=False)


class FinanceObject(models.Model):
    object_type = models.ForeignKey(
        FinanceObjectType, on_delete=models.CASCADE, related_name='fin_objects')
    title = models.CharField(unique=True, max_length=100)


class DayReport(models.Model):
    date = models.DateField(default=date.today, unique=True)
    p1 = models.PositiveIntegerField()
    p13 = models.PositiveIntegerField()
    p3 = models.PositiveIntegerField()
    p_union = models.PositiveIntegerField()

    total = models.FloatField()
    comment = models.TextField(blank=True)
