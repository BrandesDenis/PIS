import datetime
from django.db import models
from tinymce.models import HTMLField

from apps.core.models import PARAGRAPHS


class Topic(models.Model):
    paragraph = models.IntegerField(choices=PARAGRAPHS, verbose_name='Пункт')
    title = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ['paragraph', 'title']

    def __str__(self):
        return f'{self.title}({self.paragraph})'


class Thought(models.Model):
    topics = models.ManyToManyField(Topic, related_name="thoughts", verbose_name='Темы')
    title = models.CharField(max_length=100, unique=True,
                             blank=False, verbose_name='Заголовок')
    created = models.DateField(default=datetime.date.today, verbose_name='Создано')
    last_modified = models.DateField(auto_now=True, verbose_name='Последнее изменение')
    finished = models.BooleanField(default=False, verbose_name='Завершен')
    content = HTMLField(null=True)

    class Meta:
        ordering = ["-created"]

    @classmethod
    def get_grouped_thoughts(cls):
        grouped_thoughts = []
        current_paragraph = None
        current_paragraph_data = None
        for topic in Topic.objects.all():
            paragraph = topic.paragraph
            if paragraph != current_paragraph:
                current_paragraph = paragraph
                current_paragraph_data = []
                grouped_thoughts.append({
                    'name': paragraph,
                    'topics': current_paragraph_data,
                })

            current_paragraph_data.append({
                'name': topic.title,
                'thoughts': topic.thoughts.all(),
            })
        
        return grouped_thoughts
