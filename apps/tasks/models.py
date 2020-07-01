from datetime import date

from django.db import models

from apps.core.models import PARAGRAPHS


class Task(models.Model):

    class TaskStatuses():
        IN_PROGRESS = 0
        FINISHED = 1
        FAILED = 2

        choises = (
            (IN_PROGRESS, 'В работе'),
            (FINISHED, 'Выполнено'),
            (FAILED, 'Провалено'),
        )

    title = models.CharField(unique=True, max_length=100, verbose_name='Заголовок')
    paragraph = models.IntegerField(choices=PARAGRAPHS, verbose_name='Пункт')
    start = models.DateField(default=date.today, verbose_name='Начало')
    end = models.DateField(verbose_name='Окончание')
    status = models.IntegerField(choices=TaskStatuses.choises,
                                 default=0, verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        ordering = ["end", "title"]

    def set_status(self, status: int) -> None:
        if status not in (0, 1, 2):
            raise ValueError("Некорректное значение статуса")

        self.status = status
        self.save()
