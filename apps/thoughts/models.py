import datetime
from django.db import models


class Paragraph(models.Model):
    number = models.PositiveIntegerField(unique=True, blank=False)
    title = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ["number"]


class Topic(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ["paragraph"]

    def __str__(self):
        return f'{self.title}({self.paragraph.number})'


class Thought(models.Model):
    topics = models.ManyToManyField(Topic, related_name="thoughts")
    title = models.CharField(max_length=100, unique=True, blank=False)
    created = models.DateField(default=datetime.date.today)
    last_modified = models.DateField(auto_now=True)
    text = models.TextField()
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
