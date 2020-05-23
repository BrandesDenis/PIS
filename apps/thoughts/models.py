import datetime
from django.db import models


class Paragraph(models.Model):
    number = models.PositiveIntegerField(max_length=4, unique=True, blank=False)
    title = models.CharField(max_length=100, unique=True, blank=False)


class Topic(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ["-paragraph"]


class Thought(models.Model):
    topics = models.ManyToManyField(Topic, related_name="thoughts")
    title = models.CharField(max_length=100, unique=True, blank=False)
    created = models.DateField(default=datetime.date.today)
    last_modified = models.DateField(auto_now=True)
    text = models.TextField()
    finished = models.BooleanField()

    class Meta:
        ordering = ["-created"]
