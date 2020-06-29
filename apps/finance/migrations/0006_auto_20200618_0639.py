# Generated by Django 3.0.6 on 2020-06-18 06:39

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_delete_financeobjecttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, unique=True, verbose_name='Дата')),
                ('total_income', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
                ('total_outcome', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
            ],
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='date',
            field=models.DateField(default=datetime.date.today, unique=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='p1',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='П1'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='p13',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='П13'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='p3',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='П3'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='p_union',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(10)], verbose_name='Общая оценка'),
        ),
        migrations.AlterField(
            model_name='dayreport',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='dayreportrow',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='financeobject',
            name='is_positive',
            field=models.BooleanField(default=False, verbose_name='Это доход'),
        ),
        migrations.AlterField(
            model_name='financeobject',
            name='need_description',
            field=models.BooleanField(default=False, verbose_name='Требуется указывать описание'),
        ),
        migrations.AlterField(
            model_name='financeobject',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='BudgetRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=15)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='finance.Budget')),
                ('fin_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.FinanceObject')),
            ],
        ),
    ]