# Generated by Django 3.2.13 on 2022-07-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smt_orchestrator', '0030_schedule_link_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='scheduled_for',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
