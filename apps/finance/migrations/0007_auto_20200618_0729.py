# Generated by Django 3.0.6 on 2020-06-18 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20200618_0639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dayreport',
            options={'ordering': ('date',)},
        ),
    ]
