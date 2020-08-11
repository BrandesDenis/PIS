import datetime
from django.db import models
from tinymce import HTMLField


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
    topics = models.ManyToManyField(Topic, related_name="thoughts", verbose_name='Темы')
    title = models.CharField(max_length=100, unique=True,
                             blank=False, verbose_name='Темы')
    created = models.DateField(default=datetime.date.today, verbose_name='Создано')
    last_modified = models.DateField(auto_now=True, verbose_name='Последнее изменение')
    text = models.TextField(verbose_name='Содержание')
    finished = models.BooleanField(default=False, verbose_name='Завершен')
    content = HTMLField(null=True)

    class Meta:
        ordering = ["-created"]

    @classmethod
    def get_grouped_thoughts(cls):
        paragraphs = {}
        # thoughts = cls.objects.select_related('topics').all()
        thoughts = cls.objects.all()
        for thought in thoughts:
            paragraph = thought.topics.paragraph
            paragraph_data = paragraphs.setdefault(paragraph, {})

            topic_title = thought.topic.title
            topic_data = paragraph_data.setdefault(
                topic_title, [])
            topic_data.append(thought)

        grouped_data = []
        for paragraph_name, paragraph_data in paragraphs.items():
            topics = []
            grouped_data.append({'paragraph': paragraph_name, 'topics': topics})
            for topic_name, topic_data in paragraph_data.items():
                topics.append({'topic': topic_name, 'thoughts': topic_data})

        return grouped_data
