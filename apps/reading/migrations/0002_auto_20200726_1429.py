# Generated by Django 3.0.6 on 2020-07-26 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reading', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='files_dir',
            field=models.CharField(blank=True, max_length=500, verbose_name='Путь к прикрепленным файлам'),
        ),
    ]
