# Generated by Django 3.0.3 on 2020-04-23 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='paragraph',
            field=models.IntegerField(choices=[(111, '111'), (112, '112'), (12, '12'), (13, '13'), (141, '141'), (142, '142'), (143, '143'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (31, '31'), (32, '32'), (33, '33'), (41, '41'), (42, '42'), (43, '43'), (51, '51'), (52, '52')]),
        ),
    ]
