# Generated by Django 3.0.6 on 2020-06-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0015_auto_20200625_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetrow',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
