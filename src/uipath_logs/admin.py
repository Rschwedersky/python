from django.contrib import admin

from .models import Job, Context, UiPathProcessesSchedules, UipathApiMonitoring


class ContextAdmin(admin.ModelAdmin):
    list_display = ['customer', 'context']


admin.site.register(Context, ContextAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = [
        'Key',
        'Id',
        'ReleaseVersionId',
        'StartingScheduleId',
        'StartTime',
        'EndTime',
        'CreationTime',
        'State',
        'Source',
        'SourceType',
        'BatchExecutionKey',
        'Info',
        'ReleaseName',
        'Type',
        'OutputArguments',
        'HostMachineName',
        'HasMediaRecorded',
        'InputArguments',
        'PersistenceId',
        'ResumeVersion',
        'StopStrategy',
    ]


admin.site.register(Job, JobAdmin)


class UiPathProcessesSchedulesAdmin(admin.ModelAdmin):
    list_display = [
        'Context',
        'Id',
        'Key',
        'Enabled',
        'ReleaseId',
        'ReleaseKey',
        'ReleaseName',
        'EnvironmentId',
        'JobPriority',
        'RuntimeType',
        'StartProcessCron',
        'StartProcessNextOccurrence',
        'StartStrategy',
        'StopProcessExpression',
        'StopStrategy',
        'KillProcessExpression',
        'ExternalJobKey',
        'ExternalJobKeyScheduler',
        'TimeZoneIana',
        'UseCalendar',
        'CalendarId',
        'CalendarName',
        'StopProcessDate',
        'QueueDefinitionId',
    ]


admin.site.register(UiPathProcessesSchedules, UiPathProcessesSchedulesAdmin)


admin.site.register(UipathApiMonitoring)
