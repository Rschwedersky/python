from rest_framework import serializers

from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'Context',
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
        )