# Generated by Django 3.2.10 on 2022-05-02 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smt_orchestrator', '0024_schedule_execution_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SchedulesAppointments',
        ),
    ]
