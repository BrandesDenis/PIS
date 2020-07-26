from datetime import date

from django.db import models


class Reading(models.Model):
    title = models.CharField(unique=True, max_length=100, verbose_name='Название')
    autor = models.CharField(max_length=100, verbose_name='Автор')
    start = models.DateField(default=date.today, verbose_name='Начало')
    end = models.DateField(verbose_name='Окончание', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    files_dir = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Путь к прикрепленным файлам')

    class Meta:
        ordering = ["end", "title"]
