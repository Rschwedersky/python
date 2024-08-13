from enum import auto
from http import client
from io import BytesIO
from cryptography.fernet import Fernet
import my_solutions.file_validator as file_validator
from types import SimpleNamespace
from typing import List
from time import time
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from rest_framework import status
from ansible_vault import Vault
from Crypto.Random import get_random_bytes
import hvac
from loguru import logger
import uuid
import pathlib
import random
import s3fs
import pandas as pd
import json
from dashboard.templatetags.dashboard_tags import get_automation_by_name, s3_remove_file, s3_presigned_url, getLanguage, isClientMainUser, get_all_months_object, getStandardVariables, getUsersfromClients
from portal.functions import get_client_from_request
from portal.templatetags.general_tags import check_if_automation_name_is_in_query, translate
from json.decoder import JSONDecodeError
import os
from django import template, utils
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models.aggregates import Max
from django.db.models import F, Q

from smt_orchestrator.models import Automation, InterestedInServiceUnderMaintenance, ScheduleExtraInfos, Schedule, Task
from subscriptions.models import AutomationsClients, Profile, Subscription, UsersPlans


register = template.Library()


@register.filter
def newCredential(schedule, login, password, link_results, extra_info, request, language):
    try:
        new_extrainfo = {}
        if len(extra_info) > 0:
            new_extrainfo = ScheduleExtraInfos(
                schedule=schedule, extra_info=extra_info)
            new_extrainfo.save()
        if createCredentialFile(request, schedule, login, password, link_results, extra_info):
            return {'msg': translate('execution_created_successfully', language), 'status': 200, 'new_extrainfo': new_extrainfo}
        else:
            return {'msg': translate('error_saving_credentials', language), 'status': 400}
    except KeyError:
        return {'msg': translate('error_saving_new_credential', language), 'status': 400}


@register.filter
def editExtraInfosAndCredentials(request, schedule, language, schedule_credential=None):
    infos = getRequestInfos(request, ['login', 'pass'])
    json = {
        'values': {'status': 200, 'msg': translate('execution_edited_successfully', language), 'input_path': getScheduleFileName(schedule.input_path)},
        'status': status.HTTP_201_CREATED
    }
    extra_infos = {'extra_info': ''}
    if schedule_credential != None:
        extra_infos = getRequestInfos(request, ['extra_info'])
        schedule_credential.extra_info = extra_infos['extra_info']
        schedule_credential.save()
        json['values']['extra_info'] = schedule_credential.extra_info
    result = createCredentialFile(
        request, schedule, infos['login'], infos['pass'], extra_infos['extra_info'])
    if not result:
        json = {
            'values': {'status': 400, 'msg': translate('error_saving_credentials', language)},
            'status': status.HTTP_400_BAD_REQUEST
        }
    return json


@register.filter
def getScheduleFileName(path):
    # path = "file_clients/1/cepom_rj/2/0be682a2-7160-4d69-a8ec-2def3d0bb07d.xlsx"
    if type(path) is str:
        path_array = path.split('/')
        return path_array[len(path_array) - 1]
    else:
        return False


@register.filter
def getRequestInfos(request, indexes=['login', 'pass', 'extra_info']):
    infos = {}
    try:
        infos = json.loads(request.body)
    except:
        if request.method == 'POST':
            for index in indexes:
                infos[index] = request.POST.get(index)
        else:
            for index in indexes:
                infos[index] = request.GET.get(index)
    return infos


@register.filter
def updateInputPath(schedule, request, filename, language, credentials=None):
    schedule.input_path = f"file_clients/{schedule.user.profile.client.id}/{schedule.automation.name}/{filename}"
    schedule.save()
    json = {'status': 200, 'msg': translate('execution_edited_successfully', language), 'schedule_id': schedule.id, 'name': schedule.name,
            'file_format': schedule.file_format, 'email_to_send_results': schedule.email_to_send_results, 'input_path': getScheduleFileName(schedule.input_path)}
    if credentials != None:
        created = createCredentialFile(
            request, schedule, credentials['login'], credentials['password'])
        if not created:
            json = {'status': 400, 'msg': translate(
                'error_saving_credentials', language)}
    else:
        encryption = encryptScheduleSensitiveInfos(request, schedule)
        if isinstance(encryption, tuple):
            # There was an error encrypting the schedule sensitive information
            json = {'status': 400, 'msg': encryption[1]}
        elif encryption:
            json['input_path'] = getScheduleFileName(schedule.input_path)
        else:
            json = {'status': 400, 'msg': translate(
                'there_was_problem_encrypting_your_file', language)}

    return json


@register.filter
def createCredentialFile(request, schedule, login, password, extra_infos=''):
    try:
        if schedule.input_path == None or len(schedule.input_path) == 0:
            path = f"file_clients/{schedule.user.profile.client.id}/{schedule.automation.name}"
            if password != None and len(password) > 0:
                credentials = [(login), (password)]
            else:
                credentials = [(login)]

            data = {'credentials': credentials}

            if extra_infos != '':
                dates = getDatesSepareted(extra_infos, 'DD_MM_YYYY')
                data['initial'] = [dates['date_from']]
                data['final'] = [dates['date_to']]

            credential_table = pd.DataFrame.from_dict(data, orient='index')
            credential_table = credential_table.transpose()
            # credential_table = pd.DataFrame(
            #     data=data
            # )
            schedule.input_path = f'{path}/{str(uuid.uuid4())}.enc'
            client_key = read_or_create_key(
                request.user.profile.client.id)
            encrypt_df(df=credential_table,
                       path=f'{settings.AWS_STORAGE_BUCKET_NAME}/{schedule.input_path}', key=client_key, sep=';')
            schedule.save()
            return True
        else:
            encryption = encryptScheduleSensitiveInfos(
                request, schedule, login, password, extra_infos)
            if isinstance(encryption, tuple):
                return False
            else:
                return encryption
    except KeyError:
        return False


@register.filter
def encryptScheduleSensitiveInfos(request, schedule, login='', password='', extra_infos=''):
    client_key = read_or_create_key(request.user.profile.client.id)
    automation_name = schedule.get_automation().get_name()
    required_columns = get_automation_fields(automation_name=automation_name)

    if '.csv' in schedule.input_path:
        s3file_path = s3_presigned_url(
            settings.AWS_STORAGE_BUCKET_NAME, schedule.input_path)
        if required_columns:
            file_validation = file_validator.validate_file(file=s3file_path,
                                                           fields=required_columns, language=getLanguage(request))
        else:
            file_validation = check_if_file_is_correct(
                file=s3file_path, language=getLanguage(request))

        file_is_valid = file_validation.get('success', False)

        if not file_is_valid:
            return (False, file_validation.get('payload', None))

        s3_df = pd.read_csv(s3file_path, na_values=";")
        removed = s3_remove_file(
            settings.AWS_STORAGE_BUCKET_NAME, schedule.input_path)
        if removed:
            if login != '':
                s3_df = addCredentials(
                    request, s3_df, login, password, extra_infos)
            schedule.input_path = schedule.input_path.replace('.csv', '.enc')
            encrypt_df(
                df=s3_df, path=f'{settings.AWS_STORAGE_BUCKET_NAME}/{schedule.input_path}', key=client_key, sep=';')
            schedule.save()
            return True
    elif '.xlsx' in schedule.input_path or '.xls' in schedule.input_path:
        extension = 'xlsx'
        if '.xls' in schedule.input_path:
            extension = 'xls'
        s3file_path = s3_presigned_url(
            settings.AWS_STORAGE_BUCKET_NAME, schedule.input_path)

        if required_columns:
            file_validation = file_validator.validate_file(file=s3file_path,
                                                           fields=required_columns, language=getLanguage(request))
        else:
            file_validation = check_if_file_is_correct(
                file=s3file_path, language=getLanguage(request))

        file_is_valid = file_validation.get('success', False)

        if not file_is_valid:
            return (False, file_validation.get('payload', None))

        s3_df = pd.read_excel(s3file_path)

        removed = s3_remove_file(
            settings.AWS_STORAGE_BUCKET_NAME, schedule.input_path)
        if removed:
            if login != '':
                s3_df = addCredentials(
                    request, s3_df, login, password, extra_infos, extension)
            schedule.input_path = schedule.input_path.replace(
                f'.{extension}', '.enc')
            encrypt_df(
                df=s3_df, path=f'{settings.AWS_STORAGE_BUCKET_NAME}/{schedule.input_path}', key=client_key, sep=';')
            schedule.save()
            return True
    elif '.enc' in schedule.input_path:
        s3_df = decrypt_df(f'{settings.AWS_STORAGE_BUCKET_NAME}/{schedule.input_path}',
                           'schedule_preview.csv', client_key, sep=';')
        if login != '':
            s3_df = addCredentials(request, s3_df, login,
                                   password, extra_infos)
        encrypt_df(
            df=s3_df, path=f'{settings.AWS_STORAGE_BUCKET_NAME}/{schedule.input_path}', key=client_key, sep=';')
        return True
    return False


def check_if_file_is_correct(file: str,  language: str) -> dict:
    data = {
        'success': None,
        'payload': None
    }
    if not isinstance(file, str) and file.name:
        file_extension = os.path.splitext(file.name)[1]
    elif '.xlsx' in file:
        file_extension = '.xlsx'
    elif '.xls' in file:
        file_extension = '.xls'
    elif '.csv' in file:
        file_extension = '.csv'
    try:
        if file_extension == '.xlsx' or file_extension == '.xls':
            s3_df = pd.read_excel(file)
        elif file_extension == '.csv':
            s3_df = pd.read_csv(file, na_values=";")
        data['success'] = True
        data['payload'] = s3_df
    except Exception as e:
        data['success'] = False
        data['payload'] = translate('unsupported_file', language)
    finally:
        return data


@register.filter
def addCredentials(request, df, login, password, extra_infos='', type='csv'):
    df = df.dropna(how='all')
    try:
        df.drop('credentials', axis=1, inplace=True)
        if extra_infos != '':
            df.drop('initial', axis=1, inplace=True)
            df.drop('final', axis=1, inplace=True)
        if type == 'csv':
            df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
    except KeyError as e:
        print('nothing to drop')
    df.credentials = ''
    df.at[0, 'credentials'] = login
    df.at[1, 'credentials'] = password
    if extra_infos != '':
        dates = getDatesSepareted(extra_infos, 'DD_MM_YYYY')
        df.initial = ''
        df.at[0, 'initial'] = dates['date_from']
        df.final = ''
        df.at[0, 'final'] = dates['date_to']
    return df


@register.filter
def getDatesSepareted(dates_on_string, type_format='DD_MM_YYYY'):
    # 2020-09-19|2021-09-19
    dates = dates_on_string.split('|')
    date_from = dates[0].split('-')
    date_to = dates[1].split('-')
    if type_format == 'DD_MM_YYYY':
        date_from = f'{date_from[2]}_{date_from[1]}_{date_from[0]}'
        date_to = f'{date_to[2]}_{date_to[1]}_{date_to[0]}'
    elif type_format == 'DD-MM-YYYY':
        date_from = f'{date_from[2]}-{date_from[1]}-{date_from[0]}'
        date_to = f'{date_to[2]}-{date_to[1]}-{date_to[0]}'

    return {'date_from': date_from, 'date_to': date_to}


@register.filter
def encrypt_df(df, path: str, key: str, sep=';'):
    print(df)
    logger.debug(f'save encrypted to "{path}"')
    s3 = s3fs.S3FileSystem(anon=False,)
    raw_data = df.to_csv(sep=sep, index=False)
    vault = Vault(key)
    vault.dump(raw_data, s3.open(path, mode='w'))


@register.filter
def decrypt_df(path, output, key, sep):
    vault = Vault(key)
    s3 = s3fs.S3FileSystem(anon=False,)
    data = vault.load(s3.open(path, mode='rb').read())

    with open(output, 'w') as f:
        f.write(data)

    df = pd.read_csv(output, sep=sep)
    print(df)
    return df


@register.filter
def read_or_create_key(user_id: str):
    root_token = settings.VAULT_TOKEN
    client = hvac.Client(
        url='https://vault.hub.smarthis.com.br:8200',
        token=root_token,
    )
    if not client.is_authenticated():
        raise Exception("hub must be authenticated to vault secrets")

    # as there is no way to know which client on back end we are using only one credential key
    path = f'/{user_id}'
    # path = '/rafael2'
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='hub/users',
        )
    except hvac.exceptions.InvalidPath:
        logger.warning("user-id not fould, creating new entrie")
        master_key = str(get_random_bytes(32))
        create_response = client.secrets.kv.v2.create_or_update_secret(
            path=path,
            mount_point='hub/users',
            secret=dict(MASTER_KEY=master_key),
        )
        print(create_response)
        return master_key

    master_key = read_response['data']['data']['MASTER_KEY']
    return master_key


def get_all_services_tabs(is_admin, active_tab, type_automations='all_automations'):
    all_services_tabs = [
        {'type': 'my_services', 'active_tab': active_tab,
            'template': type_automations, 'title': 'my_services'},
        {'type': 'processes_history', 'active_tab': active_tab,
            'template': 'processes_history', 'title': 'executed'},
        {'type': 'all_scheduled_automations', 'active_tab': active_tab,
            'template': 'all_scheduled_automations', 'title': 'scheduled_plural'},
    ]
    if is_admin:
        all_services_tabs.append(
            {'type': 'manage_permissions', 'active_tab': active_tab, 'template': 'manage_permissions', 'title': 'manage_licenses'})
    return all_services_tabs


def get_hired_user_services_and_solutions(is_admin, request, context, language, get_solutions=True):
    if is_admin:
        hired_services = AutomationsClients.objects.filter(
            client=request.user.profile.client)
        context = addManagePermissionInfos(request, context)
        if get_solutions:
            solutions = context['all_automations_contracted']
    else:
        hired_services = UsersPlans.objects.filter(
            user=request.user)
        if get_solutions:
            solutions = UsersPlans.objects.values('automation__id', 'automation__name', 'automation__active', 'automation__is_showcase').filter(
                user=request.user)

    if get_solutions:
        sorted_solutions = sort_automations_query(
            solutions, language, client=get_client_from_request(request))
        context['solutions'] = sorted_solutions

    context['hired_services'] = hired_services

    return context


@register.filter
def addManagePermissionInfos(request, context):
    client = get_client_from_request(request)
    if request.user.profile.role in [3, 4] and request.user.profile.client.name == 'Smarthis':
        language = getLanguage(request)
        all_automations = Automation.get_automations_with_ui(language, client)
        for automation in all_automations:
            ac = AutomationsClients.objects.filter(
                client=client, automation=automation)
            if len(ac) == 0:
                ac = AutomationsClients(
                    client=client, automation=automation, qnt_automations=3)
                ac.save()
        AutomationsClients.resetAutomationsClientsByClient(client)

    context = getAutomationsContractedByClient(
        context, client, request.subscription)
    return context


@register.filter
def getAutomationsContractedByClient(context, client, subscription):
    all_automations_contracted = AutomationsClients.getAutomationClientsByClient(
        client, 'automation__name')
    all_client_profiles = getUsersfromClients(False, client)
    all_automations_id = set([])
    all_users_allowed = {}
    licenses_info = {}
    permissions_available = subscription.get_number_of_hired_services()
    if subscription.get_dashboard():
        permissions_available -= 1
    for automations_contracted in all_automations_contracted:
        automation_name = automations_contracted['automation__name']
        qnt_licenses_hired = automations_contracted['qnt_automations']
        given_licenses = UsersPlans.objects.filter(
            client=client, automation__name=automation_name).count()

        licenses_info[automation_name] = {
            'available': qnt_licenses_hired - given_licenses, 'total':  qnt_licenses_hired}
        all_automations_id.add(automations_contracted['automation__id'])
        permissions_available -= qnt_licenses_hired
        if automation_name not in all_users_allowed:
            # como todos os schedules vão além do usersplans, seta inicialmente como 0 aqui e quem receber o resultado da função faz o for correto, como no caso da função getSettingsInfos
            all_users_allowed[automation_name] = {
                'items': {},
                'qnt': 0,
                'licenses': []
            }
        this_automation_schedules = Schedule.objects.filter(
            automation__name=automation_name, user__profile__in=all_client_profiles)

        for schedule in this_automation_schedules:
            user_id = schedule.user.id
            if not user_id in all_users_allowed[automation_name]['items']:
                all_users_allowed[automation_name]['items'][user_id] = {
                    'qnt': 0, 'name': schedule.user.get_full_name(), 'email': schedule.user.email}

            all_users_allowed[automation_name]['items'][user_id]['qnt'] += 1

    all_users_plans = UsersPlans.getUsersPlansByClientAndAutomationsIds(
        client, list(all_automations_id))
    for user_plan in all_users_plans:
        automation_name = user_plan.automation.name

        all_users_allowed[automation_name]['licenses'].append(user_plan.user)

        all_users_allowed[automation_name]['qnt'] += 1

    context['all_automations_contracted'] = all_automations_contracted
    context['all_users_allowed'] = all_users_allowed
    context['permissions_available'] = permissions_available
    context['licenses_info'] = licenses_info
    return context


@register.filter
def getUserSchedulesFewColumns(request, automation_name='', limit=0):
    language = getLanguage(request)
    if isClientMainUser(request.user):
        if automation_name != '':
            if limit != 0:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by('-updated_at').filter(
                    user__profile__client__id=request.user.profile.client.id, automation__name=automation_name)[:limit]
            else:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by('-updated_at').filter(
                    user__profile__client__id=request.user.profile.client.id, automation__name=automation_name)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            if limit != 0:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user__profile__client=request.user.profile.client, automation__in=allowed_automations)[:limit]
            else:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user__profile__client=request.user.profile.client, automation__in=allowed_automations)
    else:
        if automation_name != '':
            if limit != 0:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user=request.user, automation__name=automation_name)[:limit]
            else:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user=request.user, automation__name=automation_name)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            if limit != 0:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user=request.user, automation__in=allowed_automations)[:limit]
            else:
                schedules = Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                    '-updated_at').filter(user=request.user, automation__in=allowed_automations)

    tasks_results = get_tasks(schedules)

    return {'schedules': schedules, 'tasks': tasks_results}


@register.filter
def getUserSchedulesCompleteWithPagination(request, automation_name='', objects_per_page=5):
    language = getLanguage(request)
    if isClientMainUser(request.user):
        if automation_name != '':
            paginator = Paginator(Schedule.objects.values().order_by(
                '-updated_at').filter(user__profile__client=request.user.profile.client, automation__name=automation_name).annotate(automation__name=F('automation__name')), objects_per_page)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            paginator = Paginator(Schedule.objects.values().order_by(
                '-updated_at').filter(user__profile__client=request.user.profile.client, automation__in=allowed_automations), objects_per_page)
    else:
        if automation_name != '':
            paginator = Paginator(Schedule.objects.values().order_by('-updated_at').filter(
                user=request.user, automation__name=automation_name).annotate(automation__name=F('automation__name')), objects_per_page)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            paginator = Paginator(Schedule.objects.values().order_by(
                '-updated_at').filter(user=request.user, automation__in=allowed_automations), objects_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tasks_results = get_tasks(page_obj)

    return {'schedules': page_obj, 'tasks': tasks_results}


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def getUserSchedulesFewColumnsWithPagination(request, automation_name='', objects_per_page=5):
    language = getLanguage(request)

    if isClientMainUser(request.user):
        if automation_name != '':
            paginator = Paginator(Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by('-updated_at').filter(
                user__profile__client=request.user.profile.client, automation__name=automation_name), objects_per_page)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            paginator = Paginator(Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                '-updated_at').filter(user__profile__client=request.user.profile.client, automation__in=allowed_automations), objects_per_page)
    else:
        if automation_name != '':
            paginator = Paginator(Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by('-updated_at').filter(
                user=request.user, automation__name=automation_name), objects_per_page)
        else:
            allowed_automations = list(
                Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)))

            paginator = Paginator(Schedule.objects.values('id', 'automation__name', 'name', 'state', 'updated_at').order_by(
                '-updated_at').filter(user=request.user, automation__in=allowed_automations), objects_per_page)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    schedules_of_this_page = paginator.object_list

    tasks_results = get_tasks(schedules_of_this_page)

    return {'schedules': page_obj, 'tasks': tasks_results}


def get_last_date_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def get_first_date_of_month(date):
    previous_month = date.replace(day=28) + timedelta(days=4)
    return previous_month - timedelta(days=previous_month.day-1)


def getScheduledAutomations(is_admin, request, language, limit=0):
    # a página define os 2 meses em questão
    timezone_brazil = timezone(timedelta(hours=-3))
    brazil_now = datetime.now().astimezone(timezone_brazil)
    page_number = 1
    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))
    max_date = get_last_date_of_month(
        brazil_now + relativedelta(months=(2*page_number - 1)))
    min_date = get_first_date_of_month(
        max_date - relativedelta(months=2))
    if brazil_now > min_date:
        min_date = brazil_now

    # pegando os schedules recorrentes e só uma vez de acordo com as datas
    if is_admin:
        client = get_client_from_request(request)
        no_recurrence_schedules = Schedule.objects.values('name', 'automation__name', 'cron_expression', 'execution_date').filter(
            ~Q(execution_date=None), execution_date__lte=max_date, execution_date__gte=min_date, client=client).order_by('execution_date')
        recurrence_schedules = Schedule.objects.values('name', 'automation__name', 'cron_expression', 'execution_date').filter(
            ~Q(execution_date=None), Q(execution_date__lte=max_date), Q(client=client)).order_by('execution_date')
    else:
        no_recurrence_schedules = Schedule.objects.values('name', 'automation__name', 'cron_expression', 'execution_date').filter(
            ~Q(execution_date=None), execution_date__lte=max_date, execution_date__gte=min_date, user=request.user).order_by('execution_date')
        recurrence_schedules = Schedule.objects.values('name', 'automation__name', 'cron_expression', 'execution_date').filter(
            ~Q(execution_date=None), Q(execution_date__lte=max_date), Q(user=request.user)).order_by('execution_date')

    schedules_of_this_page = no_recurrence_schedules | recurrence_schedules

    all_standard_variables = getStandardVariables('', language, True)

    scheduled_automation = {}
    how_many_added = 0

    for schedule in schedules_of_this_page:
        if limit == 0 or how_many_added < limit:
            recurrence = get_recurrence_from_cron(schedule['cron_expression'])
            execution_date = schedule['execution_date']
            if recurrence == 30:
                schedule['recurrence_text'] = translate(
                    'repeats_every_day', language) + f' {execution_date.day}'
                date_index = min_date
                # caso a data de execução esteja muito anterior à recorrência, precisa atualizar pro mes atual
                updated_execution_date = execution_date
                if execution_date < brazil_now:
                    updated_execution_date.replace(month=date_index.month)
                    updated_execution_date.replace(year=date_index.year)
                remaining_days = (max_date - date_index).days
                while remaining_days > 0 or (remaining_days < 0 and date_index.month == max_date.month):
                    index_with_correct_day = date_index.replace(
                        day=execution_date.day)
                    if (index_with_correct_day >= execution_date and execution_date.day > date_index.day or date_index > brazil_now) and (limit == 0 or how_many_added < limit):

                        key_month = f'month_{date_index.month:02}'
                        if key_month not in scheduled_automation:
                            scheduled_automation[key_month] = {}

                        # updating month to get execution_text
                        if updated_execution_date.day not in scheduled_automation[key_month]:
                            weekday = translate(
                                f"week_{updated_execution_date.weekday()}", language).replace('-feira', '')
                            scheduled_automation[key_month][updated_execution_date.day] = {'weekday': weekday, 'execution_text': '', 'data': [
                            ]}

                        scheduled_automation[key_month][updated_execution_date.day]['data'].append(
                            insertScheduledAutomationExtraInfos(schedule, all_standard_variables, language, index_with_correct_day))
                        scheduled_automation[key_month][updated_execution_date.day]['execution_text'] = schedule['execution_text']
                        how_many_added += 1
                    elif how_many_added >= limit and limit > 0:
                        break
                    date_index += relativedelta(months=1)
                    updated_execution_date += relativedelta(months=1)
                    remaining_days = (max_date - date_index).days
            elif recurrence == 7:
                recurrence_text_variables = get_recurrence_text_variables(
                    recurrence, execution_date.weekday(), language)
                schedule['recurrence_text'] = f"{translate('weekly_capitalized', language)}, {recurrence_text_variables['every_text']} {recurrence_text_variables['week_day_text']}."
                days_until_now = (min_date - execution_date).days
                date_index = min_date
                if days_until_now % 7 != 0:
                    days_until_next_week = 7 - days_until_now % 7
                    date_index += timedelta(days=days_until_next_week)
                remaining_days = (max_date - date_index).days
                while remaining_days > 0 or (remaining_days < 0 and date_index.month == max_date.month):
                    if date_index >= execution_date and date_index > brazil_now and (limit == 0 or how_many_added < limit):
                        key_month = f'month_{date_index.month:02}'
                        if key_month not in scheduled_automation:
                            scheduled_automation[key_month] = {}
                        if date_index.day not in scheduled_automation[key_month]:
                            weekday = translate(
                                f"week_{date_index.weekday()}", language).replace('-feira', '')
                            scheduled_automation[key_month][date_index.day] = {'weekday': weekday, 'execution_text': '', 'data': [
                            ]}
                        scheduled_automation[key_month][date_index.day]['data'].append(
                            insertScheduledAutomationExtraInfos(schedule, all_standard_variables, language, date_index))
                        scheduled_automation[key_month][date_index.day]['execution_text'] = schedule['execution_text']
                        how_many_added += 1
                    elif how_many_added >= limit and limit > 0:
                        break
                    date_index += timedelta(days=7)
                    remaining_days = (max_date - date_index).days
            else:
                if execution_date > brazil_now:
                    executed_once_month = f'month_{execution_date.month:02}'
                    if executed_once_month not in scheduled_automation:
                        scheduled_automation[executed_once_month] = {}
                    if execution_date.day not in scheduled_automation[executed_once_month]:
                        weekday = translate(
                            f"week_{execution_date.weekday()}", language).replace('-feira', '')
                        scheduled_automation[executed_once_month][execution_date.day] = {'weekday': weekday, 'execution_text': '', 'data': [
                        ]}
                    schedule['recurrence_text'] = translate(
                        'does_not_repeat', language)
                    scheduled_automation[executed_once_month][execution_date.day]['data'].append(
                        insertScheduledAutomationExtraInfos(schedule, all_standard_variables, language, execution_date))
                    scheduled_automation[executed_once_month][execution_date.day]['execution_text'] = schedule['execution_text']
                    how_many_added += 1
        else:
            break

    keys = sorted(scheduled_automation.keys())
    sorted_scheduled_automation = {}
    for month in keys:
        sorted_scheduled_automation[month] = dict(
            sorted(scheduled_automation[month].items()))

    has_next = True
    if page_number == 12:
        has_next = False

    has_previous = True
    if page_number == 1:
        has_previous = False
    page_obj = {'has_other_pages': True, 'has_next': has_next, 'next_page_number': page_number + 1,
                'has_previous': has_previous, 'previous_page_number': page_number - 1, 'number': page_number, 'paginator': {'num_pages': 12}}
    return {'data': sorted_scheduled_automation, 'page_obj': page_obj, 'total_schedules': how_many_added}


def insertScheduledAutomationExtraInfos(schedule, all_standard_variables, language, execution_date):
    automation_name = schedule['automation__name']
    automation_obj = get_automation_by_name(automation_name)
    schedule['automation_type'] = translate(automation_obj.group, language)
    schedule['automation_title'] = all_standard_variables[schedule['automation__name']]['title']
    time = '16h'
    if language == 'en':
        time = '4 pm'

    day = str(execution_date.day)
    if len(day) == 1:
        day = f"0{day}"

    month = str(execution_date.month)
    if len(month) == 1:
        month = f"0{month}"
    schedule['execution_text'] = f"{translate('until', language)} {translate('week_'+str(execution_date.weekday()), language)}, {day}/{month} {translate('at', language)} {time}"
    return schedule


def get_recurrence_text_variables(recurrence, week_day, language):
    final_text = {'every_text': '', 'week_day_text': ''}
    if recurrence == 7:
        every_text = translate('every_female', language)
        male_days = {
            'pt-BR': [5, 6],
            'es': [3, 6]
        }
        week_day_text = translate('week_'+str(week_day), language)
        if language in male_days and week_day in male_days[language]:
            every_text = translate('every_male', language)
        final_text = {'every_text': every_text, 'week_day_text': week_day_text}
    return final_text


def get_tasks(schedules):
    all_schedules_ids = []
    for schedule in schedules:
        schedule_is_dict = isinstance(schedule, dict)
        all_schedules_ids.append(schedule.get(
            'id') if schedule_is_dict else schedule.id)

    tasks_results = {}
    if len(all_schedules_ids) > 0:
        tasks = Task.objects.filter(schedule__id__in=all_schedules_ids)
        all_tasks_filtered = tasks.values(
            'schedule__id', 'schedule__name', 'state', 'updated_at').annotate(task_id=Max('id'))

        for task in all_tasks_filtered:
            this_task_schedule_id = task['schedule__id']

            if this_task_schedule_id in tasks_results:
                newest_task = all_tasks_filtered.filter(
                    schedule__id=this_task_schedule_id).order_by('-updated_at').first()
                tasks_results[this_task_schedule_id] = {
                    'state': newest_task['state'], 'date': newest_task['updated_at']}
            else:
                tasks_results[this_task_schedule_id] = {
                    'state': task['state'], 'date': task['updated_at']}

    return tasks_results


def get_subscription(request):
    client = request.user.profile.client
    subscription = Subscription.getSubscriptionByClient(
        client=client)
    return subscription


@ register.filter
def getSettingsFilters(user, language):
    filters = {}
    number_of_total_services = 0
    hired_services = AutomationsClients.objects.filter(
        client=user.profile.client)

    for service in hired_services:
        automation_group = translate(service.automation.group, language)
        if not automation_group in filters:
            filters[automation_group] = 0

        filters[automation_group] += 1
        number_of_total_services += 1

    sorted_filters = sort_dict_by_key(filters)
    all_filters = {"all_male": number_of_total_services}

    filters_with_all_first = {**all_filters, **sorted_filters}

    return filters_with_all_first


@register.filter
def sort_automations_query(query, language, client):
    allowed_automations = Automation.get_automations_with_ui(
        language=language, client=client)

    hired_automations = []

    for item in query:
        hired_automations.append(item['automation__name'])

    return allowed_automations.filter(name__in=hired_automations)


@ register.filter
def check_if_free_trial_ended(subscription):
    start_of_free_trial = subscription.get_begin()
    now = utils.timezone.now().date()

    diff_in_days = (now - start_of_free_trial).days
    trial_period = subscription.get_trial_period()
    if not trial_period and trial_period != 0:
        trial_period = 14

    if diff_in_days > trial_period:
        return True
    else:
        return False


@ register.filter
def check_client_available_licenses(client):
    available_licenses = 0
    client_subscription = Subscription.getSubscriptionByClient(client)
    if client_subscription != None:
        client_licenses_limit = client_subscription.get_number_of_hired_services()
        all_automation_clients = AutomationsClients.objects.filter(
            client=client)

        used_licenses = 0

        for automation in all_automation_clients:
            used_licenses += int(automation.qnt_automations)

        if client_subscription.get_dashboard():
            used_licenses += 1

        available_licenses = client_licenses_limit - used_licenses

    return available_licenses


@ register.filter
def check_if_user_is_interested_in_fixed_automation(user, automation):
    try:
        InterestedInServiceUnderMaintenance.objects.get(
            user=user, automation=automation)
        return True
    except Exception as e:
        return False


@ register.filter
def check_if_user_has_service(user, automation):
    is_admin = isClientMainUser(user)
    try:
        if is_admin:
            # If is admin, we check if the client has the service

            AutomationsClients.objects.get(
                client=user.profile.client, automation=automation)
        else:
            UsersPlans.objects.get(
                user=user, automation=automation)

        return True
    except Exception as e:
        return False


def send_appropriate_email(request, class_instance):
    # Avoiding circular imports error
    def make_necessary_imports():
        from subscriptions.templatetags.subscriptions_tags import getHubUrl, sendEmail
        dict = {'getHubUrl': getHubUrl, 'sendEmail': sendEmail}
        # Getting dot notation
        transformed_dict = SimpleNamespace(**dict)
        return transformed_dict

    automation = class_instance.name
    active_state = class_instance.active
    people_to_send_email = set([])

    language = getLanguage(request)

    try:

        all_users_that_use_this_service = UsersPlans.objects.filter(
            automation=class_instance)
        for license in all_users_that_use_this_service:
            people_to_send_email.add(license.user.email)

        all_clients_admin_that_hired_this_service = AutomationsClients.objects.filter(
            automation=class_instance)
        for automation_client in all_clients_admin_that_hired_this_service:
            client = automation_client.client
            client_admin = Profile.objects.filter(
                client=client, role=4).first()
            if client_admin != None:
                people_to_send_email.add(client_admin.user.email)
    except Exception as e:
        return False

    imports = make_necessary_imports()

    if active_state == True:
        template = 'servicoConsertado'
        email_title = translate('your_service_has_been_updated', language)
        try:
            all_interested_users_emails = set([])
            all_instances_of_interested_users = InterestedInServiceUnderMaintenance.objects.filter(
                automation=class_instance)
            for instance in all_instances_of_interested_users:
                all_interested_users_emails.add(instance.user.email)

            list_of_interested_users_to_send_email = list(
                all_interested_users_emails)

            imports.sendEmail('interesseEmServicoConsertado', translate('service_available_for_contracting', language), list_of_interested_users_to_send_email, {
                'language': language, 'link_automation': f'{imports.getHubUrl()}discover/{automation}', 'automation': class_instance})

        except Exception as e:
            return False

    else:
        template = 'servicoEmManutencao'
        email_title = translate('your_service_is_under_maintenance', language)

    list_of_users_to_send_email = list(people_to_send_email)

    try:
        imports.sendEmail(template, email_title, list_of_users_to_send_email, {
            'language': language, 'link_automation': f'{imports.getHubUrl()}services/{automation}', 'automation': class_instance})
    except Exception as e:
        return False


@ register.filter
def sort_dict_by_key(dict):
    new_dict = {key: value for key, value in sorted(
        dict.items(), key=lambda item: item[0])}
    return new_dict


def get_filters_by_user(language: str, services, client, sort=True):
    number_of_total_services = 0
    filters = {}
    automations_with_frontend = Automation.get_automations_with_ui(
        language, client)
    for service in services:
        if isinstance(service, Automation):
            automation_name = service.name
        else:
            automation_name = service.automation.name
        automation_is_allowed = check_if_automation_name_is_in_query(
            automation_name=automation_name, query=automations_with_frontend)
        if automation_is_allowed:
            automation_obj = get_automation_by_name(automation_name)
            if language == 'en':
                automation_group = automation_obj.get_group_display()
            else:
                automation_group = translate(automation_obj.group, language)
            if not automation_group in filters:
                filters[automation_group] = 0
            filters[automation_group] += 1
            number_of_total_services += 1

    if sort:
        filters = sort_dict_by_key(filters)

    all_filters = {"all_male": number_of_total_services}

    filters_with_all_first = {**all_filters, **filters}

    return filters_with_all_first


@ register.filter
def get_hired_automation_by_automation_obj(request, automation_obj):
    # Avoiding circular imports error
    def make_necessary_imports():
        from portal.functions import get_client_from_request
        dict = {'get_client_from_request': get_client_from_request}
        # Getting dot notation
        transformed_dict = SimpleNamespace(**dict)
        return transformed_dict

    try:
        imports = make_necessary_imports()
        return AutomationsClients.objects.get(
            client=imports.get_client_from_request(request), automation=automation_obj)
    except ObjectDoesNotExist:
        return False


def get_automation_fields(automation_name: str) -> list:
    reference = get_all_automations_fields()
    return reference.get(automation_name, None)


def get_all_automations_fields():
    return {
        'aguas-rio': ['CPF/CNPJ', 'MATRICULA'],
        'cedae': ['MATRÍCULA', 'CPF/CNPJ'],
        'cepom-rj': ['NOME', 'CNPJ'],
        'certidao-mte': ['CNPJ'],
        'cnd': ['CNPJ MATRIZ', 'PERÍODO DE CONSULTA', 'SITUAÇÃO DA CERTIDÃO'],
        'cnd-rj': ['CPF/CNPJ'],
        'cnd-sp': ['CNPJ'],
        'comgas': ['CPF', 'CÓDIGO DO USUÁRIO'],
        'cpom-sp': ['CNPJ'],
        'divida-ativa-rj': ['CNPJ', 'NOME', 'CPF DO SOLICITANTE'],
        'fgts-crf': ['CNPJ'],
        # 'gnre-sp': ['TIPO DE DÉBITO-CONDICIONAL-GNRE-SP', 'INSCRIÇÃO ESTADUAL-CONDICIONAL', 'CNPJ', 'NOTA FISCAL ELETRÔNICA-CONDICIONAL', 'CNPJ DO REMETENTE-CONDICIONAL', 'INFORMAÇÕES COMPLEMENTARES', 'DATA DE VENCIMENTO', 'VALOR PRINCIPAL', 'JUROS-OPCIONAL', 'MULTA-OPCIONAL', 'ATUALIZAÇÃO MONETÁRIA-OPCIONAL'],
        # 'icms-rj': ['CPF/CNPJ', 'QUALIFICAÇÃO RECEITA', 'PERÍODO DE REFERÊNCIA', 'ICMS INFORMADO', 'FECP INFORMADO', 'DATA DE PAGAMENTO-OPCIONAL', 'INFORMAÇÕES COMPLEMENTARES-INDEPENDENTE'],
        # 'icms-sp': ['CPF/CNPJ', 'INSCRIÇÃO ESTADUAL', 'PERÍODO DE REFERÊNCIA', 'CNAE-OPCIONAL', 'VALOR PRINCIPAL', 'JUROS-OPCIONAL', 'MULTA-OPCIONAL', 'INFORMAÇÕES COMPLEMENTARES-INDEPENDENTE'],
        'inidoneos': ['CNPJ'],
        'inidoneos-ceis': ['CNPJ'],
        'ipva-rj': ['RENAVAM'],
        'ipva-sp': ['RENAVAM', 'PLACA DO VEÍCULO'],
        'iss-rj': ['CPF/CNPJ', 'VALOR TOTAL DA NOTA', 'DESCRIÇÃO INCONDICIONADOS', 'ISS RETIDO-OPCIONAL', 'TRIBUTAÇÃO DOS SERVIÇOS-OPCIONAL', 'ESTADO-OPCIONAL', 'CIDADE-OPCIONAL', 'ITEM-OPCIONAL', 'SUBITEM-OPCIONAL', 'SERVIÇO-OPCIONAL', 'DISCRIMINAÇÃO DOS SERVIÇOS-OPCIONAL', 'COFINS (R$)-OPCIONAL', 'CSL (R$)-OPCIONAL', 'INSS (R$)-OPCIONAL', 'IRPJ (R$)-OPCIONAL', 'PIS (R$)-OPCIONAL', 'OUTROS (R$)-OPCIONAL', 'TIPO DO RPS-OPCIONAL', 'NÚMERO DO RPS-OPCIONAL', 'SÉRIE DO RPS-OPCIONAL', 'DATA DE EMISSÃO DO RPS-OPCIONAL'],
        'iss-sp': ['CONTRIBUINTE', 'ANO DE EXERCÍCIO', 'MÊS DE EXERCÍCIO', 'SITUAÇÃO DA GUIA'],
        'naturgy': ['NUMERO DO CLIENTE', 'ANO', 'MÊS', 'CNPJ', 'CIDADE'],
        'notas-servico-sp': ['CPF/CNPJ', 'CÓDIGO DE VERIFICAÇÃO', 'NÚMERO DA NOTA'],
        'receita-federal-cnpj': ['CNPJ'],
        'receita-federal-cpf': ['CPF', 'DATA DE NASCIMENTO'],
        'sabesp': ['RGI'],
        'sefaz-rj': ['CPF', 'DATA DE NASCIMENTO', 'CEP', 'NÚMERO', 'COMPLEMENTO-INDEPENDENTE', 'DATA DO FATO GERADOR', 'VALOR DA DOAÇÃO'],
        'simples-nacional': ['CNPJ'],
        'trf2': ['CPF'],
        'trf3': ['NOME', 'CPF']
    }


@ register.filter
def check_and_maybe_encrypt_string(list_of_emails: json, language) -> json:
    def get_encryption_key():
        with open("/app/encryption/encryption_keys/keys.txt", "r") as file:
            line = file.readline()
            token = line.strip()
            return token

    def encrypt_string(key, string):
        cryptor = Fernet(key)
        string = string.replace('-no token', '')
        string_binary = string.encode('utf-8')
        token = cryptor.encrypt(string_binary)
        return token

    def save_encrypted_token(directory, token, random_id=random.getrandbits(32)):
        with open(f"{directory}/tokens{random_id}.txt", "w") as file:
            file.write(str(token.decode('utf-8')))
            return True

    try:
        converted_list_of_emails = json.loads(list_of_emails)
        result = []
        for string in converted_list_of_emails:
            if 'uipath' in string.lower():
                random_id = random.getrandbits(32)
                key = get_encryption_key()
                token = encrypt_string(key=key, string=string)
                directory_name = 'encryption_tokens'
                parent_dir = "/app/encryption/"
                directory_to_store_key = make_directory(
                    directory_to_store_key=directory_name, parent_dir=parent_dir)
                save_encrypted_token(
                    directory=directory_to_store_key, token=token, random_id=random_id)

                email_mask = translate(
                    'integrated_with_your_uipath_operation', language)
                result.append(f'{email_mask}-{random_id}')

            else:
                result.append(string)

        return json.dumps(result)
    except JSONDecodeError:
        # The list of emails is not a JSON
        result = []
        email = list_of_emails
        if isinstance(email, str) and 'uipath' in email.lower():
            random_id = random.getrandbits(32)
            key = get_encryption_key()
            token = encrypt_string(key=key, string=email)
            directory_name = 'encryption_tokens'
            parent_dir = "/app/encryption/"
            directory_to_store_key = make_directory(
                directory_to_store_key=directory_name, parent_dir=parent_dir)
            save_encrypted_token(
                directory=directory_to_store_key, token=token, random_id=random_id)

            email_mask = translate(
                'integrated_with_your_uipath_operation', language)
            result.append(f'{email_mask}-{random_id}')
        else:
            result.append(email)
        return json.dumps(result)

    except Exception:
        return list_of_emails


def make_directory(directory_to_store_key, parent_dir):
    path = os.path.join(parent_dir, directory_to_store_key)
    try:
        os.mkdir(path)
    except FileExistsError:
        for file_name in os.listdir(path):
            file_stats = pathlib.Path(f"{path}/{file_name}").stat()
            file_creation_timestamp = file_stats.st_mtime
            timestamp_now = time()
            file_is_older_than_one_minute = (
                timestamp_now - file_creation_timestamp) > 60
            if file_is_older_than_one_minute:
                os.remove(f"{path}/{file_name}")
    finally:
        return path


def decrypt_uipath_connection_string(emails_json):
    def get_encryption_key():
        file_path = f"/app/encryption/encryption_keys/keys.txt"
        with open(file_path, "rb") as file:
            line = file.readline()
            key = line.strip()
            return key

    def get_encryption_token(id):
        file_path = f"/app/encryption/encryption_tokens/tokens{id}.txt"
        with open(file_path, "rb") as file:
            line = file.readline()
            token = line.strip()
            os.remove(file_path)
            return token

    email_list = json.loads(emails_json)
    id = None
    index = None
    for email in email_list:
        if 'uipath' in email.lower():
            splitted = email.split('-')
            id = splitted[1]
            index = email_list.index(email)
            email_list[index] = 'replace'
            break
    if id and id != 'no token':
        key = get_encryption_key()
        token = get_encryption_token(id=id)
        try:
            cryptor = Fernet(key)
            decrypted = cryptor.decrypt(token)

            email_list[index] = decrypted.decode('utf-8')

        except Exception as e:
            print('error', e, e.__traceback__.tb_lineno)
        return json.dumps(email_list)
    else:
        return emails_json


def get_appointment_email_infos(language: str, execution_date: datetime, recurrence: int):
    week_day = execution_date.weekday()
    week_day_text = translate('week_'+str(week_day), language)

    all_months_obj = get_all_months_object(language)
    month_translated = all_months_obj[execution_date.month - 1]['month']

    date_text = f"{execution_date.date().day} {translate('of', language)} {month_translated} {translate('of', language)} {execution_date.year}"
    if language == 'en':
        date_text = f"{month_translated} {execution_date.date().day}, {execution_date.year}"
    date_text_with_week = f"{week_day_text}, {date_text}"

    recurrence_small_text = translate('does_not_repeat', language)
    execution_text = f"{translate('next_female', language)}"
    if recurrence == 30:
        recurrence_small_text = f"{translate('monthly_capitalized', language)}, {translate('every_day', language)} {execution_date.date().day}."
        execution_text = f"{translate('monthly', language)}, {translate('every_day', language)} {execution_date.date().day}, {translate('starting_in', language)} {date_text}"
    elif recurrence == 7:
        recurrence_text_variables = get_recurrence_text_variables(
            recurrence, week_day, language)
        recurrence_small_text = f"{translate('weekly_capitalized', language)}, {recurrence_text_variables['every_text']} {week_day_text}."
        execution_text = f"{translate('weekly', language)}, {recurrence_text_variables['every_text']} {week_day_text}, {translate('starting_in', language)} {date_text}"
    else:
        next_text = translate('next_female', language)
        male_days = {
            'pt-BR': ['sábado', 'domingo']
        }
        if language in male_days and week_day in male_days[language]:
            next_text = translate('in_next_male', language)

        execution_text = f"{next_text} {week_day_text}, {date_text}"

    return {'execution_text': execution_text, 'recurrence_small_text': recurrence_small_text, 'date_text_with_week': date_text_with_week}


def translate_schedule_appointment_into_cron_expression(date: datetime, recurrence: int):
    cron_expression = '0 11'  # executando às 11 horas

    if recurrence == 30:
        # como fica o caso do dia 29/02/2024?
        cron_expression = f"{cron_expression} {date.day} * *"
    elif recurrence == 7:
        # cron expression for week cases
        cron_expression = f"{cron_expression} * * {date.weekday()}"
    else:
        # cron expression for once execution
        cron_expression = f"{cron_expression} {date.day} {date.month} * {date.year}"
    return cron_expression


@register.filter
def translate_single_cron(cron_expression, language):
    final_text = ''
    cron_list = cron_expression.split(' ')
    if len(cron_list) == 6:
        # TODO: recurrence only once
        final_text = translate('does_not_repeat', language)
    elif cron_list[2] != '*':
        # is monthly
        final_text = translate('repeats_every_day',
                               language) + f' {cron_list[2]}'
    elif cron_list[4] != '*' and ',' not in cron_list[4]:
        # is weekly
        week_day = cron_list[4]
        week_day_text = translate('week_'+str(week_day), language)
        every_text = translate('every_female', language)
        male_days = {
            'pt-BR': [5, 6],
            'es': [3, 6]
        }
        if language in male_days and week_day in male_days[language]:
            every_text = translate('every_male', language)
        final_text = translate('repeats', language) + \
            f" {every_text} {week_day_text}"
    return final_text


@register.simple_tag
def get_template_cron_recurrence_text(cron_expression, execution_date, language):
    if execution_date:
        cron_expression = cron_expression
        final_text = translate('your_model_will_run', language)
        cron_list = cron_expression.split(' ')
        all_months_obj = get_all_months_object(language)
        date_text = ''
        month_translated = all_months_obj[execution_date.month - 1]['month']
        date_text = f"{execution_date.date().day} {translate('of', language)} {month_translated} {translate('of', language)} {execution_date.year}"
        if len(cron_list) == 6:
            # recurrence only once
            final_text += f" {translate('on', language)}"
        elif cron_list[2] != '*':
            # is monthly
            final_text += f" {translate('monthly', language)}, {translate('every_day', language)} {cron_list[2]}, {translate('starting_in', language)}"
        elif cron_list[4] != '*' and ',' not in cron_list[4]:
            # is weekly
            week_day = cron_list[4]
            week_day_text = translate('week_'+str(week_day), language)
            every_text = translate('every_female', language)
            male_days = {
                'pt-BR': [5, 6],
                'es': [3, 6]
            }
            if language in male_days and week_day in male_days[language]:
                every_text = translate('every_male', language)
            final_text += f" {translate('weekly', language)}, {every_text} {week_day_text}, {translate('from', language).lower()}"
        return final_text + f" {date_text}"
    else:
        return translate('no_starting_date_was_selected', language)


def get_recurrence_from_cron(cron_expression: str):
    recurrence = 0
    cron_list = cron_expression.split(' ')
    try:
        if len(cron_list) == 6:
            recurrence = 0
        elif cron_list[2] != '*':
            recurrence = 30
        elif cron_list[4] != '*':
            recurrence = 7

    except Exception as e:
        pass
    finally:
        return recurrence


def get_template_by_id(schedule_id, user_id, client):
    schedule = None
    try:
        schedule = Schedule.objects.get(id=schedule_id, client=client)
    except ObjectDoesNotExist:
        profiles = getUsersfromClients(False, client)
        all_users_ids = [user_id]
        for p in profiles:
            all_users_ids.append(p.user.id)
        try:
            schedule = Schedule.objects.get(
                id=schedule_id, user__id__in=all_users_ids)
        except ObjectDoesNotExist:
            pass
    finally:
        return schedule


def create_extrainfo_file(user_id, extra_infos: str):
    file_name = f"extrainfo_{user_id}.csv"
    data = {}
    dates = getDatesSepareted(extra_infos, 'DD-MM-YYYY')
    data['initial'] = [dates['date_from']]
    data['final'] = [dates['date_to']]
    credential_table = pd.DataFrame.from_dict(data, orient='index')
    credential_table = credential_table.transpose()
    credential_table.to_csv(file_name, sep=';', index=False)
    buf = None
    with open(file_name, 'rb') as fh:
        buf = BytesIO(fh.read())
    return buf


async def send_message_to_groups(groups: List[str], channel_layer, payload: dict):
    for group in groups:
        await channel_layer.group_send(str(group), payload)


@register.filter
def translate_relative_date(relative_date_text, language):
    if language == 'en':
        return relative_date_text

    if not relative_date_text:
        return ""

    if language == 'pt-BR':
        plurals_replaced = relative_date_text.replace('years', 'anos').replace(
            'months', 'meses').replace('weeks', 'semanas').replace('days', 'dias').replace('hours', 'horas').replace('minutes', 'minutos')
        singulars_replaced = plurals_replaced.replace('year', 'ano').replace(
            'month', 'mês').replace('week', 'semana').replace('day', 'dia').replace('hour', 'hora').replace('minute', 'minuto')

        cleaned_text = singulars_replaced.split(
            ',', 1)[0].replace('atrás', '').replace('ago', '').replace(r'\an\b', 'uma')

        if cleaned_text.lower() != 'agora':
            necessary_text = f"há {cleaned_text}"
        else:
            necessary_text = cleaned_text
    elif language == 'es':
        plurals_replaced = relative_date_text.replace('years', 'años').replace(
            'months', 'meses').replace('weeks', 'semanas').replace('days', 'días').replace('hours', 'horas').replace('minute', 'minutos')
        singulars_replaced = plurals_replaced.replace('year', 'año').replace(
            'month', 'mes').replace('week', 'semana').replace('day', 'día').replace('hour', 'hora').replace('minute', 'minuto')

        cleaned_text = singulars_replaced.split(
            ',', 1)[0].replace('atrás', '').replace('ago', '').replace(r'\an\b', 'una')

        necessary_text = f"hace {cleaned_text}"

    return necessary_text


@register.filter
def to_date(date: str):
    return datetime.fromisoformat(date)
