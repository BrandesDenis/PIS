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

    title = models.CharField(unique=True, max_length=100)
    paragraph = models.IntegerField(choices=PARAGRAPHS)
    start = models.DateField(default=date.today)
    end = models.DateField()
    status = models.IntegerField(choices=TaskStatuses.choises, default=0)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["end", "title"]

    def set_status(self, status: int) -> None:
        if status not in (0, 1, 2):
            raise ValueError("Некорректное значение статуса")

        self.status = status
        self.save()
