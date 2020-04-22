# Generated by Django 3.0.5 on 2020-04-22 12:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('paragraph', models.IntegerField(choices=[(111, '111'), (112, '112'), (12, '12'), (13, '13'), (141, '141'), (142, '142'), (143, '143'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (31, '31'), (32, '32'), (33, '33'), (41, '41'), (42, '42'), (43, '43'), (51, '51'), (52, '51')])),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField()),
                ('status', models.IntegerField(choices=[(0, 'in progress'), (1, 'finished'), (2, 'failed')], default=0)),
                ('description', models.TextField(default='')),
            ],
            options={
                'ordering': ['end', 'title'],
            },
        ),
    ]
