from celery import task, Task
from datetime import datetime
from loguru import logger

from .models import Context, UiPathProcessesSchedules, UipathApiMonitoring
from .uipath.client import CloudClient
from .serializers import JobSerializer

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


@task(name='sync uipath logs')
def sync_uipath_logs():
    print("[DEBUG] running 'sync_uipath_logs'")

    try:
        logs_to_update = Context.objects.filter(auto_update=True)
    except Context.DoesNotExist:
        return

    for context in logs_to_update:
        # mount credentials object
        credentials = {
            'url': context.orchestrator_url,
            'tenant_name': context.tenant_name,
            'refresh_token': context.refresh_token,
            'client_id': context.client_id
        }
        # instantiate uipath client
        uipath_client = CloudClient(credentials)
        try:
            uipath_client.authenticate()
        except Exception:
            logger.debug("Invalid Credentials")
            continue

        try:
            # guard valid odata pattern
            folder_response = uipath_client.get_folders()
            uipath_folders_data = get_uipath_response(
                'Folders', folder_response, context)
            if uipath_folders_data['status'] == 200:
                for single_folder in uipath_folders_data['values']:
                    print(get_and_sync_processschedules(
                        uipath_client, context, single_folder['Id']))

            print(get_and_sync_jobs(uipath_client, context))
        except Exception as e:
            print(str(e))
            print('Problem with ', context.customer.name, credentials)


def get_uipath_response(type, response, context):
    print('----GETTING UIPATH RESPONSE-----')
    uipath_data = {'status': 400}
    try:
        data = response.json()
    except Exception as e:
        print('PROBLEM GETTING RESPONSE JSON')
        print(str(e))
        return uipath_data
    try:
        uipath_data = {'status': 200,
                       'values': data['value'], 'count': data['@odata.count'], 'context': data['@odata.context']}
    except Exception as e:
        # TODO: mudar o estado no banco de dados?
        print('ERROR ON DATA')
        print(str(e))
        return uipath_data

    # guard valid odata context
    try:
        url_divided = uipath_data['context'].split('$metadata#')
        orchestrator_url = f'{context.orchestrator_url}odata/'
        if context.orchestrator_url[-1] != '/':
            orchestrator_url = f'{context.orchestrator_url}/odata/'
        if orchestrator_url != url_divided[0] and type != url_divided[1]:
            uipath_data = {'status': 401}
    except Exception as e:
        uipath_data = {'status': 404}

    return uipath_data


def get_and_sync_processschedules(uipath_client, context, folder_id):
    print('SYNC PROCESSSCHEDULES')
    response = uipath_client.get_processes_schedules(
        folder_id)
    uipath_data = get_uipath_response(
        'ProcessSchedules', response, context)
    if uipath_data['status'] == 200:
        data = []
        for entrie in uipath_data['values']:
            entrie['Context'] = context.id
            data.append(entrie)
        if context.customer.name == 'Saphyr':
            print(data)
        response = {'status': 200}
        for uipath_process in uipath_data['values']:
            try:
                single_uipath_process = UiPathProcessesSchedules.objects.get(
                    ReleaseName=uipath_process['ReleaseName'])
            except Exception as e:
                single_uipath_process = UiPathProcessesSchedules()
            single_uipath_process.Context = context
            single_uipath_process.Id = uipath_process['Id']
            single_uipath_process.Key = uipath_process['Key']
            single_uipath_process.Enabled = uipath_process['Enabled']
            single_uipath_process.ReleaseId = uipath_process['ReleaseId']
            single_uipath_process.ReleaseKey = uipath_process['ReleaseKey']
            single_uipath_process.ReleaseName = uipath_process['ReleaseName']
            if uipath_process['EnvironmentId'] == '':
                single_uipath_process.EnvironmentId = None
            else:
                single_uipath_process.EnvironmentId = uipath_process['EnvironmentId']
            single_uipath_process.JobPriority = uipath_process['JobPriority']
            single_uipath_process.RuntimeType = uipath_process['RuntimeType']
            single_uipath_process.StartProcessCron = uipath_process['StartProcessCron']
            single_uipath_process.StartProcessNextOccurrence = uipath_process[
                'StartProcessNextOccurrence']
            single_uipath_process.StartStrategy = uipath_process['StartStrategy']
            single_uipath_process.StopProcessExpression = uipath_process[
                'StopProcessExpression']
            single_uipath_process.StopStrategy = uipath_process['StopStrategy']
            single_uipath_process.KillProcessExpression = uipath_process[
                'KillProcessExpression']
            single_uipath_process.ExternalJobKey = uipath_process['ExternalJobKey']
            single_uipath_process.ExternalJobKeyScheduler = uipath_process[
                'ExternalJobKeyScheduler']
            single_uipath_process.TimeZoneIana = uipath_process['TimeZoneIana']
            single_uipath_process.UseCalendar = uipath_process['UseCalendar']
            single_uipath_process.CalendarId = uipath_process['CalendarId']
            single_uipath_process.CalendarName = uipath_process['CalendarName']
            single_uipath_process.StopProcessDate = uipath_process['StopProcessDate']
            single_uipath_process.QueueDefinitionId = uipath_process['QueueDefinitionId']

            try:
                single_uipath_process.save()
            except Exception as e:
                response = {'status': 407}
                print('PROBLEM SAVING: ',
                      uipath_process['ReleaseName'])
                print(str(e))
    else:
        # error getting response
        response = {'status': 403}
    return response


def get_and_sync_jobs(uipath_client, context):
    print('SYNC JOBS')
    client = context.customer
    response = None
    error_message = None
    error_code = None

    try:
        response = uipath_client.get_jobs(
            from_datetime=context.last_update)
        if not response.ok:
            raise Exception('Problem getting jobs from ui path client')

    except Exception as e:
        error_message = str(e) or 'Problem getting jobs from ui path client'
        error_code = response.status_code
    finally:
        if client:
            UipathApiMonitoring.objects.update_or_create(client=client, defaults={
                'error_message': error_message or 'Sucesso',
                'error_code': error_code
            })
        if error_message or error_code:
            return {'status': error_code or 402}

    uipath_data = get_uipath_response('Jobs', response, context)
    if uipath_data['status'] == 200:
        # serialize input
        data = []
        for entrie in uipath_data['values']:
            entrie['Context'] = context.id
            data.append(entrie)

        # last update will be the most recent data entrie as fallback
        if len(data) > 0:
            context.last_update = datetime.strptime(
                data[-1]['StartTime'], DATETIME_FORMAT)
        resp = {'status': 200}
        retry = 1
        print(len(data))
        while retry >= 0:
            serializer = JobSerializer(data=data, many=True)
            # guard valid serialized data
            if not serializer.is_valid():
                resp['status'] = 405
                filtered_jobs_values = []
                for index, error_line in enumerate(serializer.errors):
                    try:
                        if error_line["Key"][0] != "Job log with this Key already exists.":
                            filtered_jobs_values.append(data[index])
                    except KeyError:
                        filtered_jobs_values.append(data[index])
                        continue
                    except TypeError:
                        break
                data = filtered_jobs_values

                retry -= 1
                continue
            break
        # last update will be the last recent data entrie the could be saved, this is because data to be save is modified in retry block
        if serializer.is_valid():
            if len(serializer.data) > 0:
                context.last_update = datetime.strptime(
                    serializer.data[-1]['StartTime'], DATETIME_FORMAT)
                resp['datetime'] = context.last_update
            try:
                serializer.save()
                resp['status'] = 200
            except Exception as e:
                print(str(e))
                resp['status'] = 406

        context.save()
        return resp
    else:
        # error getting response
        return {'status': 403}
