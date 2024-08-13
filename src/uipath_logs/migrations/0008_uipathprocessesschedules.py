# Generated by Django 3.2.10 on 2022-03-14 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uipath_logs', '0007_merge_0006_auto_20220217_1858_0006_auto_20220224_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='UiPathProcessesSchedules',
            fields=[
                ('Id', models.IntegerField(blank=True, null=True)),
                ('Key', models.SlugField(max_length=36, primary_key=True, serialize=False)),
                ('Enabled', models.CharField(blank=True, max_length=30, null=True)),
                ('ReleaseId', models.IntegerField(blank=True, null=True)),
                ('ReleaseKey', models.SlugField(blank=True, max_length=36, null=True)),
                ('ReleaseName', models.CharField(blank=True, max_length=150, null=True)),
                ('EnvironmentId', models.IntegerField(blank=True, null=True)),
                ('JobPriority', models.CharField(blank=True, max_length=150, null=True)),
                ('RuntimeType', models.CharField(blank=True, max_length=150, null=True)),
                ('StartProcessCron', models.CharField(blank=True, max_length=150, null=True)),
                ('StartProcessNextOccurrence', models.DateTimeField(blank=True, null=True)),
                ('StartStrategy', models.IntegerField(blank=True, null=True)),
                ('StopProcessExpression', models.CharField(blank=True, max_length=150, null=True)),
                ('StopStrategy', models.CharField(blank=True, max_length=150, null=True)),
                ('KillProcessExpression', models.CharField(blank=True, max_length=150, null=True)),
                ('ExternalJobKey', models.SlugField(blank=True, max_length=36, null=True)),
                ('ExternalJobKeyScheduler', models.SlugField(blank=True, max_length=36, null=True)),
                ('TimeZoneIana', models.CharField(blank=True, max_length=150, null=True)),
                ('UseCalendar', models.CharField(blank=True, max_length=30, null=True)),
                ('CalendarId', models.IntegerField(blank=True, null=True)),
                ('CalendarName', models.CharField(blank=True, max_length=150, null=True)),
                ('StopProcessDate', models.CharField(blank=True, max_length=150, null=True)),
                ('QueueDefinitionId', models.IntegerField(blank=True, null=True)),
                ('Context', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='uipath_logs.context')),
            ],
            options={
                'verbose_name': 'Uipath Process Schedules',
                'verbose_name_plural': 'Uipath Processes Schedules',
            },
        ),
    ]
