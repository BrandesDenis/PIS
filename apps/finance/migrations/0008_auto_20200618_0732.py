# Generated by Django 3.0.6 on 2020-06-18 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0007_auto_20200618_0729'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={'get_latest_by': 'date', 'ordering': ('date',)},
        ),
        migrations.AlterModelOptions(
            name='dayreport',
            options={'get_latest_by': 'date', 'ordering': ('date',)},
        ),
    ]
