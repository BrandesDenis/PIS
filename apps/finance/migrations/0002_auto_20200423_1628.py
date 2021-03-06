# Generated by Django 3.0.3 on 2020-04-23 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financeobjecttype',
            name='is_exchange',
        ),
        migrations.CreateModel(
            name='DayReportRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField()),
                ('fin_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='finance.FinanceObject')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='finance.DayReport')),
            ],
        ),
    ]
