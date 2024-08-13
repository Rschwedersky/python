# Generated by Django 3.2.10 on 2022-02-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smt_orchestrator', '0017_schedule_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='client',
        ),
        migrations.AlterField(
            model_name='schedule',
            name='recurrence',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'WITHOUT-REPEAT'), (30, 'MONTHLY'), (7, 'WEEKLY')], default=0, null=True),
        ),
    ]
