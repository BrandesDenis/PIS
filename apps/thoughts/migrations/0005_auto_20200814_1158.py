# Generated by Django 3.0.6 on 2020-08-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0004_auto_20200812_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='topic',
            options={'ordering': ['paragraph', 'title']},
        ),
        migrations.RemoveField(
            model_name='thought',
            name='text',
        ),
        migrations.AlterField(
            model_name='thought',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Заголовок'),
        ),
    ]
