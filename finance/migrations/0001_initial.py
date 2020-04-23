# Generated by Django 3.0.3 on 2020-04-23 05:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, unique=True)),
                ('p1', models.PositiveIntegerField()),
                ('p13', models.PositiveIntegerField()),
                ('p3', models.PositiveIntegerField()),
                ('p_union', models.PositiveIntegerField()),
                ('total', models.FloatField()),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinanceObjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('is_positive', models.BooleanField(default=False)),
                ('is_exchange', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FinanceObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('object_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fin_objects', to='finance.FinanceObjectType')),
            ],
        ),
    ]
