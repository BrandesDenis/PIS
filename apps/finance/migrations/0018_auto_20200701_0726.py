# Generated by Django 3.0.6 on 2020-07-01 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0017_auto_20200630_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayreport',
            name='p13',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='П13'),
        ),
    ]