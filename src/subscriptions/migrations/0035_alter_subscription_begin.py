# Generated by Django 3.2.10 on 2022-02-22 15:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0034_auto_20220221_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='begin',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 2, 22, 15, 22, 56, 2284), null=True),
        ),
    ]
