from django.conf import settings
from django.db import models
from django.db.models import Count
import datetime
from datetime import datetime, timedelta
from croniter import croniter
import pytz
import unicodedata
import time

from django.core.cache import cache

from dashboard.templatetags.dashboard_tags import get_dashboard_processes_info


class Context(models.Model):
    customer = models.ForeignKey(
        settings.CUSTOMER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    context = models.CharField(max_length=150)
    auto_update = models.BooleanField(default=False)
    orchestrator_url = models.CharField(max_length=150, null=True, blank=True)
    tenant_name = models.CharField(max_length=150, null=True, blank=True)
    refresh_token = models.CharField(max_length=150, null=True, blank=True)
    client_id = models.CharField(max_length=150, null=True, blank=True)
    last_update = models.DateTimeField(
        default=datetime(2020, 1, 1, tzinfo=pytz.UTC))

    def __str__(self):
        return f"{self.customer} - {self.context}"


class Job(models.Model):
    '''
    UiPath Job Log Model
    Define the attributes of an uipath job log
    '''
    class Meta:
        verbose_name = 'Job log'
        verbose_name_plural = 'Jobs logs'

    Context = models.ForeignKey(
        Context, on_delete=models.DO_NOTHING, db_index=True)

    # "53d7873a-9401-42b1-93b6-39364a7da241",
    Key = models.SlugField(max_length=36, primary_key=True)
    Id = models.IntegerField(null=True, blank=True)  # 25057
    ReleaseVersionId = models.IntegerField(null=True, blank=True)  # 140,
    StartingScheduleId = models.IntegerField(null=True, blank=True)  # 2,
    StartTime = models.DateTimeField(
        null=True, blank=True)  # "2020-07-29T11:00:00.557Z",
    # "2020-07-29T11:01:49.48Z",
    EndTime = models.DateTimeField(null=True, blank=True)
    CreationTime = models.DateTimeField(
        null=True, blank=True)  # "2020-07-29T11:00:00.253Z",
    State = models.CharField(max_length=150, null=True,
                             blank=True)  # "Successful",
    # "Processo_Boletos_Avulso_2_Minutos",
    Source = models.CharField(max_length=150, null=True, blank=True)
    SourceType = models.CharField(
        max_length=150, null=True, blank=True)  # "Schedule",
    # "38309dbd-6a29-4f88-ab53-ea34ecc1f941",
    BatchExecutionKey = models.CharField(max_length=150, null=True, blank=True)
    Info = models.TextField(null=True, blank=True)  # "Tarefa concluída",
    # "Boletos_Avulso_Contas_a_Receber",
    ReleaseName = models.CharField(
        max_length=150, null=True, blank=True, db_index=True)
    Type = models.CharField(max_length=150, null=True,
                            blank=True)  # "Unattended",
    OutputArguments = models.TextField(null=True, blank=True)  # "{}",
    HostMachineName = models.CharField(
        max_length=150, null=True, blank=True)  # "AZBR-RPA-DESK1",
    HasMediaRecorded = models.BooleanField(
        default=False, null=True, blank=True)  # false,
    InputArguments = models.TextField(null=True, blank=True)  # null,
    PersistenceId = models.CharField(
        max_length=150, null=True, blank=True)  # null,
    ResumeVersion = models.CharField(
        max_length=150, null=True, blank=True)  # null,
    StopStrategy = models.CharField(
        max_length=150, null=True, blank=True)  # null,

    def listAllColumnsTypes(date_from, date_to, columnkey, columnname, client):
        key = "all_" + columnkey + "_" + date_from.strftime(
            '%m_%d') + "_" + date_to.strftime('%m_%d') + "_" + str(client).replace(' ', '_')
        alltypes = cache.get(key)
        # alltypes = []
        if not alltypes:
            alltypes = []
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            alltypes_object = Job.objects.values(columnname).filter(Context__customer=client, StartTime__range=[date_from.strftime(date_format), date_to.strftime(date_format)], EndTime__range=[
                date_from.strftime(date_format), date_to.strftime(date_format)]).annotate(dcount=Count(columnname)).exclude(ReleaseName__contains='Teste').order_by(columnname)
            not_allowed_processes = ['Boleto_Avulso_EloPar_Contas_a_Receber',
                                     'ProcessoEmBranco_Contas_a_Receber', 'Logins_PROD01']
            for type in alltypes_object:
                if (columnname == 'ReleaseName' and type[columnname] in not_allowed_processes) or (str(client) == 'Elopar' and columnname == 'HostMachineName' and type[columnname] != 'AZBR-RPA-DESK1') or (columnname == 'HostMachineName' and (type[columnname] == None or type[columnname] == '' or len(type[columnname]) == 0)):
                    continue
                elif (type[columnname] == None or type[columnname] == 'None') and columnname != 'HostMachineName':
                    alltypes.append('Vazia')
                elif (columnname == 'ReleaseName' and type[columnname] != 'Boleto_Avulso_EloPar_Contas_a_Receber' and type[columnname] != 'ProcessoEmBranco_Contas_a_Receber') or (str(client) == 'Elopar' and columnname == 'HostMachineName' and type[columnname] == 'AZBR-RPA-DESK1') or (columnname in type):
                    alltypes.append(type[columnname])
            cache.set(key, alltypes, 900)
        return alltypes

    def get_json_from_db(date_from, date_to, client):
        key = "jobs_" + date_from.strftime('%Y-%m-%d') + "_" + date_to.strftime(
            '%Y-%m-%d') + "_" + str(client).replace(' ', '_')

        cached_value = cache.get(key)
        if cached_value:
            return cached_value

        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        all_jobs = Job.objects.filter(Context__customer=client, StartTime__range=[date_from.strftime(date_format), date_to.strftime(
            date_format)], EndTime__range=[date_from.strftime(date_format), date_to.strftime(date_format)]).values('StartTime', 'EndTime', 'ReleaseName', 'HostMachineName', 'State').exclude(ReleaseName__contains='Teste')
        subprocesses_infos = SubProcessos.getSubProcessesInfosByClient(client)

        json = Job.setJsonReturn(date_from, date_to)
        for j in all_jobs:
            if j['StartTime'] == None or j['EndTime'] == None or (j['ReleaseName'] == 'Boleto_Avulso_EloPar_Contas_a_Receber' or j['ReleaseName'] == 'ProcessoEmBranco_Contas_a_Receber') or (str(client) == 'Elopar' and j['HostMachineName'] != 'AZBR-RPA-DESK1') or (str(client) == 'Wilson' and j['ReleaseName'] == 'Logins_PROD01') or (str(client) == 'Nidec' and (j['HostMachineName'] == None or j['HostMachineName'] == '' or len(j['HostMachineName']) == 0)):
                continue
            duration = (j['EndTime'] - j['StartTime']).seconds
            json['totalhours_rpa'] += duration

            execution_time_in_seconds = (
                j['EndTime'] - j['StartTime']).total_seconds()
            machinename = j['HostMachineName']
            if j['HostMachineName'] == None:
                machinename = 'Vazia'
            process_key = j['ReleaseName'] + machinename + j['State']
            process_key = Job.strip_accents(process_key.replace('-', '_'))

            process_info = {'area': '',
                            'process': j['ReleaseName'], 'duration_time': 0}
            if j['ReleaseName'] in subprocesses_infos:
                human_duration_time = subprocesses_infos[j['ReleaseName']
                                                         ]['duration_time']

                process_info = {'area': subprocesses_infos[j['ReleaseName']]['area'], 'process': subprocesses_infos
                                [j['ReleaseName']]['name'], 'duration_time': human_duration_time}

            if process_key not in json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes']:
                json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key] = {
                    'area': process_info['area'], 'process': process_info['process'], 'robot': machinename, 'status': j['State'], 'qnt': 0, 'time': 0, 'averageoccupation_byday': {}, 'human_time': 0}
            json['dates'][j['StartTime'].strftime(
                '%Y_%m_%d')]['processes'][process_key]['time'] += execution_time_in_seconds
            json['dates'][j['StartTime'].strftime(
                '%Y_%m_%d')]['processes'][process_key]['human_time'] += process_info['duration_time']
            json['dates'][j['StartTime'].strftime(
                '%Y_%m_%d')]['processes'][process_key]['qnt'] += 1

            initialdate = j['StartTime']
            delta = timedelta(hours=1)
            next_hour = (initialdate + delta)
            seconds_next_hour = (next_hour - initialdate).seconds

            done = False
            while not done:
                if initialdate.strftime('%I_%p') not in json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday']:
                    json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime(
                        '%I_%p')] = {'qnt': 0, 'total_occupation_byhour': 0}
                if seconds_next_hour >= execution_time_in_seconds:
                    # minutos para a proxima hora é 22 e diferença de minutos é 22
                    done = True
                    json['dates'][j['StartTime'].strftime(
                        '%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime('%I_%p')]['qnt'] += 1
                    json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime(
                        '%I_%p')]['total_occupation_byhour'] += execution_time_in_seconds
                elif execution_time_in_seconds > 3600:
                    # minutos para a proxima hora é 43 e diferença de minutos é 120
                    json['dates'][j['StartTime'].strftime(
                        '%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime('%I_%p')]['qnt'] += 1
                    json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime(
                        '%I_%p')]['total_occupation_byhour'] += seconds_next_hour
                    initialdate = initialdate + \
                        timedelta(seconds=seconds_next_hour)
                    execution_time_in_seconds -= seconds_next_hour
                    seconds_next_hour = 3600
                else:
                    # minutos para a próxima hora é 29 e diferença de minutos é 53
                    json['dates'][j['StartTime'].strftime(
                        '%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime('%I_%p')]['qnt'] += 1
                    json['dates'][j['StartTime'].strftime('%Y_%m_%d')]['processes'][process_key]['averageoccupation_byday'][initialdate.strftime(
                        '%I_%p')]['total_occupation_byhour'] += seconds_next_hour
                    seconds_next_hour = execution_time_in_seconds - seconds_next_hour
                    execution_time_in_seconds = seconds_next_hour

        processes_registered = get_dashboard_processes_info(
            subprocesses_info=subprocesses_infos)
        all_robots = Job.listAllColumnsTypes(
            date_from, date_to, 'robots', 'HostMachineName', client)
        all_status = Job.listAllColumnsTypes(
            date_from, date_to, 'status', 'State', client)
        all_areas = Areas.listAllColumnsTypes(client)

        json['all_robots'] = all_robots
        json['all_processes'] = processes_registered
        json['all_status'] = all_status
        json['all_areas'] = all_areas

        cache.set(key, json, 900)
        return json

    def get_calendar_json_from_db(client, date_from, date_to, language):
        from dashboard.templatetags.dashboard_tags import translate
        key = "calendar_jobs_" + date_from.strftime('%Y-%m-%d') + "_" + date_to.strftime(
            '%Y-%m-%d') + "_" + str(client).replace(' ', '_')
        json = cache.get(key)
        if json:
            return json

        json = {}

        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        all_jobs = Job.objects.filter(Context__customer=client, StartTime__range=[date_from.strftime(date_format), date_to.strftime(
            date_format)], EndTime__range=[date_from.strftime(date_format), date_to.strftime(date_format)]).values('StartTime', 'EndTime', 'ReleaseName', 'HostMachineName', 'State').exclude(ReleaseName__contains='Teste')
        dict_processes = Processos.listAllColumnsTypes(client)
        for j in all_jobs:
            if j['StartTime'] == None or j['EndTime'] == None or (j['ReleaseName'] == 'Boleto_Avulso_EloPar_Contas_a_Receber' or j['ReleaseName'] == 'ProcessoEmBranco_Contas_a_Receber') or (str(client) == 'Elopar' and j['HostMachineName'] != 'AZBR-RPA-DESK1') or (str(client) == 'Wilson' and j['ReleaseName'] == 'Logins_PROD01') or (str(client) == 'Nidec' and (j['HostMachineName'] == None or j['HostMachineName'] == '' or len(j['HostMachineName']) == 0)):
                continue

            title = j['ReleaseName']
            if j['ReleaseName'] in dict_processes['dict']:
                title = dict_processes['dict'][j['ReleaseName']]['name']

            duration = (j['EndTime'] - j['StartTime']).seconds
            text_duration = f'{str(duration)} segundos'
            if duration > 60:
                duration_seconds = duration % 60
                seconds_text = translate('seconds', language)
                if duration_seconds == 1:
                    seconds_text = translate('second', language)
                duration_minutes = str(int((duration - duration_seconds) / 60))
                minutes_text = translate('minutes', language)
                if duration_minutes == 1:
                    minutes_text = translate('minute', language)
                text_duration = f'{duration_minutes} {minutes_text} ' + \
                    translate('and', language) + \
                    f' {duration_seconds} {seconds_text}'

            calendar_event = {
                'title': title,
                'description': translate('process_took', language) + f' {text_duration} ' + translate('to_be_executed', language),
                'start': j['StartTime'],
                'end': j['EndTime'],
                'className': 'fc-bg-default',
                'allDay': False,
            }
            if j['StartTime'].strftime('%Y-%m-%d') not in json:
                json[j['StartTime'].strftime('%Y-%m-%d')] = []
            json[j['StartTime'].strftime('%Y-%m-%d')].append(calendar_event)

        cache.set(key, json, 900)
        return json

    def setJsonReturn(date_from, date_to):
        json = {
            'totalhours_rpa': 0,
            'dates': {},
        }

        populate_days = (date_to - date_from).days
        while populate_days >= 0:
            mydate = date_to - timedelta(days=populate_days)
            json['dates'][mydate.strftime('%Y_%m_%d')] = {'processes': {}, 'robots': {
            }, 'areas': {}, 'status': {}, 'date': mydate.strftime('%Y-%m-%d')}
            populate_days -= 1

        return json

    def strip_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii.decode("utf-8")


class UiPathProcessesSchedules(models.Model):
    '''
    UiPath Process Schedules Model
    Define the attributes of an uipath process schedules
    '''
    class Meta:
        verbose_name = 'Uipath Process Schedules'
        verbose_name_plural = 'Uipath Processes Schedules'

    Context = models.ForeignKey(
        Context, on_delete=models.DO_NOTHING, db_index=True)
    Id = models.IntegerField(null=True, blank=True)  # 44146,
    # 'a1124254-ee6d-465b-944e-1834f64a2f41'
    Key = models.SlugField(max_length=36, primary_key=True)
    Enabled = models.CharField(max_length=30, blank=True, null=True)  # False
    ReleaseId = models.IntegerField(null=True, blank=True)  # 83800
    # 'd8d9e73c-0ddb-4736-b96a-73572598ea18'
    ReleaseKey = models.SlugField(max_length=36, blank=True, null=True)
    ReleaseName = models.CharField(max_length=150, null=True,
                                   blank=True)  # 'CORP_FOPAG_FGTS_DISPATCHER_PROD01'
    EnvironmentId = models.IntegerField(null=True, blank=True)  # '2809'
    JobPriority = models.CharField(max_length=150, null=True,
                                   blank=True)  # None
    RuntimeType = models.CharField(max_length=150, null=True,
                                   blank=True)  # None
    StartProcessCron = models.CharField(
        max_length=150, null=True, blank=True)  # '0 0 20 3-7 * ? *'
    StartProcessNextOccurrence = models.DateTimeField(
        null=True, blank=True)  # None
    StartStrategy = models.IntegerField(null=True, blank=True)  # 1
    StopProcessExpression = models.CharField(max_length=150, null=True,
                                             blank=True)  # ''
    StopStrategy = models.CharField(max_length=150, null=True,
                                    blank=True)  # None
    KillProcessExpression = models.CharField(max_length=150, null=True,
                                             blank=True)  # None
    ExternalJobKey = models.SlugField(
        max_length=36, null=True, blank=True)  # None
    ExternalJobKeyScheduler = models.SlugField(
        max_length=36, null=True, blank=True)  # None
    TimeZoneIana = models.CharField(max_length=150, null=True,
                                    blank=True)  # 'America/Sao_Paulo'
    # False (keeping charfield because of how the value comes from uipath api)
    UseCalendar = models.CharField(max_length=30, blank=True, null=True)
    CalendarId = models.IntegerField(null=True, blank=True)  # 44146
    CalendarName = models.CharField(max_length=150, null=True,
                                    blank=True)  # None
    StopProcessDate = models.CharField(max_length=150, null=True,
                                       blank=True)  # None
    QueueDefinitionId = models.IntegerField(null=True, blank=True)  # None

    def get_processes_scheduled_by_context(client, date_from, date_to):
        processes_scheduled = UiPathProcessesSchedules.objects.values(
            'ReleaseName', 'StartProcessCron', 'QueueDefinitionId').filter(Enabled='True', Context__customer=client)
        json = {'data': {}, 'every_minute': []}
        populate_days = (date_to - date_from).days
        while populate_days >= 0:
            mydate = date_to - timedelta(days=populate_days)
            json['data'][mydate.strftime('%Y-%m-%d')] = []
            populate_days -= 1

        dict_processes = Processos.listAllColumnsTypes(client)
        for process in processes_scheduled:
            if (process['ReleaseName'] == 'Boleto_Avulso_EloPar_Contas_a_Receber' or process['ReleaseName'] == 'ProcessoEmBranco_Contas_a_Receber') or (str(client) == 'Elopar' and process['HostMachineName'] != 'AZBR-RPA-DESK1') or (str(client) == 'Wilson' and process['ReleaseName'] == 'Logins_PROD01'):
                continue
            final_name = process['ReleaseName']
            if process['ReleaseName'] in dict_processes['dict']:
                final_name = dict_processes['dict'][process['ReleaseName']]['name']
            json = UiPathProcessesSchedules.add_cron_to_calendar_json(
                process['StartProcessCron'], date_from, date_to, final_name, process, json)
        return json

    def add_cron_to_calendar_json(expression, from_date, to_date, final_name, process, json):
        expression = expression.replace('?', '*').lower()
        expression_list = expression.split(' ')
        try:
            expression_to_croniter = f'{expression_list[1]} {expression_list[2]} {expression_list[3]} {expression_list[4]} {expression_list[5]}'
            iter = croniter(expression_to_croniter,
                            (from_date - timedelta(days=1)))  # -1 day because of get_next

            days_until = (to_date - from_date).days
            already_added = []
            try:
                if '0 0/1 * 1/1' not in expression:
                    while days_until >= 0:
                        next_date = iter.get_next(datetime)
                        next_date += timedelta(hours=3)
                        calendar_event = {
                            'title': final_name,
                            'description': '',
                            'start': next_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            'end': (next_date + timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                            'className': 'fc-bg-default',
                            'allDay': False,
                        }
                        if next_date.strftime('%Y-%m-%d') not in json['data']:
                            json['data'][next_date.strftime('%Y-%m-%d')] = []
                        json['data'][next_date.strftime(
                            '%Y-%m-%d')].append(calendar_event)
                        days_until = (to_date - next_date).days
                elif process['ReleaseName'] not in already_added and process['QueueDefinitionId']:
                    next_date = iter.get_next(datetime)
                    next_date += timedelta(hours=3)
                    calendar_event = {
                        'title': final_name,
                        'description': '',
                        'start': next_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        'end': (next_date + timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                        'className': 'fc-bg-default',
                        'allDay': False

                    }
                    json['every_minute'].append(calendar_event)
                    already_added.append(process['ReleaseName'])
                else:
                    print('IS QUEUE, NEED BETTER UNDERSTANDING',
                          process['ReleaseName'])
            except Exception as e:
                print('PROBLEM ON WHILE')
                print(str(e))
            finally:
                return json
        except Exception as e:
            print('PROBLEM EXPRESSION', str(e))
            return json


class Areas(models.Model):
    '''
    Areas Log Model
    Define the attributes of an Areas log
    '''
    class Meta:
        verbose_name = 'Areas log'
        verbose_name_plural = 'Areas logs'

    area = models.TextField(null=False, blank=False)
    customer = models.ForeignKey(
        settings.CUSTOMER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def get_area_name(self):
        return self.area

    def get_customer(self):
        return self.customer

    def listAllColumnsTypes(client):
        key = "all_areas_" + str(client).replace(' ', '_')
        alltypes = cache.get(key)
        if not alltypes:
            alltypes = {'areas': [], 'id': []}
            alltypes_object = Areas.objects.filter(
                customer__name=client).order_by('area')
            for single_type in alltypes_object:
                alltypes['areas'].append(single_type.area)
                alltypes['id'].append(single_type.id)
            cache.set(key, alltypes, 900)
        return alltypes


class Processos(models.Model):
    class Meta:
        verbose_name = 'Processos'
        verbose_name_plural = 'Processos'

    # depois de rodar a função remover as 2 colunas
    process = models.CharField(max_length=150, null=True, blank=True)
    ReleaseName = models.CharField(
        max_length=150, null=True, blank=True, db_index=True)
    # depois de rodar a função remover as 2 colunas
    name = models.CharField(max_length=150, default='Not provided')
    duration_time = models.FloatField(null=True, blank=True)  # Time in minutes
    area = models.ForeignKey(
        Areas, on_delete=models.CASCADE, null=True, blank=True)
    salary_collaborator = models.FloatField(null=True, blank=True)
    hours_collaborator = models.IntegerField(null=True, blank=True)  # 6 or 8
    # per process, how many collaborators evolved
    howmany_collaborators = models.IntegerField(null=True, blank=True)
    project_cost = models.FloatField(null=True, blank=True)
    client = models.ForeignKey(
        settings.CUSTOMER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None, db_index=True)
    average_hour_value = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    quantity_of_monthly_tasks = models.IntegerField(null=True, blank=True)

    def get_process(self):
        return self.name

    def set_process(self, name):
        if (name and name.strip()) or name == '':
            self.name = name

    def get_duration_time(self):
        return self.duration_time

    def set_duration_time(self, duration_time):
        if duration_time or duration_time == 0:
            self.duration_time = duration_time

    def get_area(self):
        return self.area

    def set_area(self, area):
        self.area = area

    def get_salary_collaborator(self):
        return self.salary_collaborator

    def set_salary_collaborator(self, salary_collaborator):
        if salary_collaborator or salary_collaborator == 0:
            self.salary_collaborator = salary_collaborator

    def get_hours_collaborator(self):
        return self.hours_collaborator

    def set_hours_collaborator(self, hours_collaborator):
        if hours_collaborator or hours_collaborator == 0:
            self.hours_collaborator = hours_collaborator

    def get_howmany_collaborators(self):
        return self.howmany_collaborators

    def set_howmany_collaborators(self, howmany_collaborators):
        if howmany_collaborators or howmany_collaborators == 0:
            self.howmany_collaborators = howmany_collaborators

    def get_project_cost(self):
        return self.project_cost

    def set_project_cost(self, project_cost):
        if project_cost or project_cost == 0:
            self.project_cost = project_cost

    def get_client(self):
        return self.client

    def set_client(self, client):
        if client:
            self.client = client

    def get_average_hour_value(self):
        return self.average_hour_value

    def set_average_hour_value(self, value):
        self.average_hour_value = value

    def get_quantity_of_monthly_tasks(self):
        return self.quantity_of_monthly_tasks

    def set_quantity_of_monthly_tasks(self, value):
        self.quantity_of_monthly_tasks = value

    def listAllColumnsTypes(client):
        key = "all_processes_" + str(client).replace(' ', '_')
        alltypes = cache.get(key)
        if not alltypes:
            alltypes = {'processes': [], 'dict': {},
                        'subprocesses_registered': [], 'incomplete_processes': []}
            allprocesses_ids = Processos.objects.order_by('name').filter(
                client=client).values_list('id', flat=True)

            if len(allprocesses_ids):
                all_client_subprocesses = SubProcessos.objects.filter(
                    process__id__in=allprocesses_ids)

                ignored_jobs = [
                    'Boleto_Avulso_EloPar_Contas_a_Receber', 'ProcessoEmBranco_Contas_a_Receber']
                for single_type in all_client_subprocesses:
                    if single_type.ReleaseName not in ignored_jobs:
                        if single_type.process.name not in alltypes['dict']:
                            alltypes['processes'].append(
                                single_type.process.area)
                            alltypes['dict'][single_type.process.name] = Processos.get_process_infos_formated(
                                single_type.process)
                        alltypes['subprocesses_registered'].append(
                            single_type.ReleaseName)
                        alltypes['dict'][single_type.process.name]['subprocesses'].append(SubProcessos.get_subprocess_infos_formated(
                            single_type.ReleaseName, single_type.id))
                        for key, value in alltypes['dict'][single_type.process.name].items():
                            if not value:
                                alltypes['dict'][single_type.process.name]['completed'] = False
                                alltypes['incomplete_processes'].append(
                                    single_type.process.name)
                                break
            cache.set(key, alltypes, 900)
        return alltypes

    def get_process_infos_formated(process):
        completed = True
        if not (process.area and process.area.area) or not(process.duration_time) or not(process.quantity_of_monthly_tasks) or not(process.average_hour_value) or not(process.project_cost):
            completed = False
        return {
            'area': process.area.area if process.area and process.area.area else '',
            'name': process.name,
            'process_id': process.id,
            'duration_time': process.duration_time if process.duration_time else 0,
            'area_id': process.area.id if process.area else 0,
            'quantity_of_monthly_tasks': process.quantity_of_monthly_tasks if process.quantity_of_monthly_tasks else 0,
            'average_hour_value': process.average_hour_value if process.average_hour_value else 0,
            'project_cost': process.project_cost if process.project_cost else 0,
            'completed': completed,
            'subprocesses': []
        }

    def get_fields(self, ignore_fields=[]):
        # return [field.value_from_object(self) for field in self.__class__._meta.fields]
        fields_values = []
        for field in self.__class__._meta.fields:
            if field.name not in ignore_fields:
                fields_values.append(field.value_from_object(self))
        return fields_values

    def set_default_clients():
        # function created to update client on processes and allow empty departments, as we changed form inputs
        instances_without_client = Processos.objects.filter(client=None)

        for instance in instances_without_client:
            if instance.get_area() and instance.get_area().get_customer():
                instance.set_client(instance.get_area().get_customer())
                instance.save()

    def generate_new_subprocesses_for_each_client():
        all_processes = Processos.objects.all()
        for single_process in all_processes:
            if single_process.ReleaseName and single_process.ReleaseName != '':
                single_process.name = single_process.process
                single_process.save()
                subprocess = SubProcessos.objects.create(
                    process=single_process, ReleaseName=single_process.ReleaseName)
                subprocess.save()


class SubProcessos(models.Model):
    process = models.ForeignKey(
        Processos, on_delete=models.CASCADE, null=True, blank=True)
    ReleaseName = models.CharField(
        max_length=150, null=True, blank=True, db_index=True)

    def get_ReleaseName(self):
        return self.ReleaseName

    def set_ReleaseName(self, ReleaseName):
        if ReleaseName and ReleaseName.strip():
            self.ReleaseName = ReleaseName

    def getSubProcessesInfosByClient(client):
        key = "all_subprocesses_" + str(client).replace(' ', '_')
        response = cache.get(key)
        if not response:
            response = {}
            all_client_subprocesses = SubProcessos.objects.filter(
                process__client=client)
            ignored_jobs = [
                'Boleto_Avulso_EloPar_Contas_a_Receber', 'ProcessoEmBranco_Contas_a_Receber']
            for subprocess in all_client_subprocesses:
                if subprocess.ReleaseName not in ignored_jobs:
                    response[subprocess.ReleaseName] = {
                        'name': subprocess.process.name,
                        'duration_time': subprocess.process.duration_time if subprocess.process.duration_time else 0,
                        'area': subprocess.process.area.area if subprocess.process.area and subprocess.process.area.area else '',
                        'process_id': subprocess.process_id
                    }
            cache.set(key, response, 900)
        return response

    def get_subprocess_infos_formated(releasename, id):
        return {
            'releasename': releasename,
            'id': id
        }


class UipathApiMonitoring(models.Model):
    client = models.ForeignKey(
        settings.CUSTOMER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    error_message = models.CharField(max_length=300, blank=True, null=True)
    error_code = models.IntegerField(blank=True, null=True)
