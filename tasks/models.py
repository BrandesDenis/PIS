from datetime import date
from typing import NoReturn

from django.db import models


class Task(models.Model):

    paragraphs = (
        (111, '111'),
        (112, '112'),
        (12, '12'),
        (13, '13'),
        (141, '141'),
        (142, '142'),
        (143, '143'),
        (21, '21'),
        (22, '22'),
        (23, '23'),
        (24, '24'),
        (31, '31'),
        (32, '32'),
        (33, '33'),
        (41, '41'),
        (42, '42'),
        (43, '43'),
        (51, '51'),
        (52, '51'),
    )

    statuses = (
        (0, 'in progress'),
        (1, 'finished'),
        (2, 'failed'),
    )

    title = models.CharField(unique=True, max_length=100)
    paragraph = models.IntegerField(choices=paragraphs)
    start = models.DateField(default=date.today)
    end = models.DateField()
    status = models.IntegerField(choices=statuses, default=0)
    description = models.TextField(default='')

    class Meta:
        ordering = ['end', 'title']

    def set_status(self, status: int) -> NoReturn:
        if status not in (0, 1, 2):
            raise ValueError('Статус должен быть в списке (0,1,2)')

        self.status = status
        self.save()
