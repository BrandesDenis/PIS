# Generated by Django 3.0.6 on 2020-06-24 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_auto_20200624_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayreportrow',
            name='date',
            field=models.DateField(blank=True),
        ),
    ]
