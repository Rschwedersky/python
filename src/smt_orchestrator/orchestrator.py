from copyreg import constructor
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from typing import Tuple, Optional
import requests
import logging


def get_orchestrator_credentials() -> Tuple[str, str, str]:
    '''select proper credentials based on environment'''
    if settings.IS_DEV or settings.IS_LOCALHOST:
        return(
            settings.ORCHESTRATOR_API_TEST_URL,
            settings.ORCHESTRATOR_API_TEST_USERNAME,
            settings.ORCHESTRATOR_API_TEST_PASSWORD
        )
    else:
        return (
            settings.ORCHESTRATOR_API_URL,
            settings.ORCHESTRATOR_API_USERNAME,
            settings.ORCHESTRATOR_API_PASSWORD
        )


def get_auth_token() -> str:
    orchestrator_url, username, password = get_orchestrator_credentials()
    data = {
        'username': username,
        'password': password
    }
    res = requests.post(
        f'{orchestrator_url}/iam/authenticate', data=data)
    if not res.ok:
        raise Exception(f"{res.json()}")
    return res.json()['token_type'].title() + ' ' + res.json()['access_token']


def start_schedule(schedule_id: int) -> bool:
    '''start schedule using an privileged account, 
    should only be called after checking credentials'''
    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/schedules/start'
    res = requests.post(
        url=url,
        data={'ids': [schedule_id]},
        headers=headers
    )
    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def read_automation(client_id: int, start_date: int, end_date: int) -> dict:
    '''start schedule using an privileged account, 
    should only be called after checking credentials'''

    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/dashboard_tasks/{client_id}'
    data = {
        'client_id': client_id,
        'start_date': start_date,
        'end_date': end_date
    }
    res = requests.get(
        url=url,
        headers=headers,
        params=data,
    )

    return {
        'success': res.ok,
        'data': res.json()
    }


def read_monitoring_dashboard_data(start_skip: int, end_limit: int) -> dict:
    '''start schedule using an privileged account, 
    should only be called after checking credentials'''

    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }

    url = f'{orchestrator_url}/dashboard_tasks/data/monitoring_dashboard'
    data = {
        'skip': start_skip,
        'limit': end_limit,
    }
    print("data", data)
    res = requests.get(
        url=url,
        headers=headers,
        params=data,
    )

    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def stop_schedule(schedule_id: int) -> bool:
    '''stop schedule using an privileged account, 
    should only be called after checking credentials'''
    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/schedules/stop/{schedule_id}'
    res = requests.post(
        url=url,
        headers=headers
    )
    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def new_model(
    user_id: int,
    input_file,
    schedule_name: str,
    automation_name: str,
    output_file_format: str,
    link_results: str,
    email_to_send_results: str,
    attachments=None,
    credentials: str = ''
) -> dict:
    '''creates new model using an privileged account, 
    should only be called after checking credentials'''
    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/schedules/'

    data = {'user_id': user_id,
            'attachments': attachments,
            'credentials': credentials,
            'schedule_name': schedule_name,
            'automation_name': automation_name,
            'output_file_format': output_file_format,
            'link_results': link_results,
            'email_to_send_results': email_to_send_results
            }

    res = requests.post(
        url=url,
        headers=headers,
        data=data,
        files={'input_file': input_file}
    )
    logging.debug(data)
    logging.debug(res)

    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def edit_model(
    user_id: int,
    model_id: int,
    input_file=None,
    attachments=None,
    credentials=None,
    schedule_name: Optional[str] = None,
    automation_name: Optional[str] = None,
    output_file_format: Optional[str] = None,
    link_results: Optional[str] = None,
    email_to_send_results: Optional[str] = None
) -> dict:
    '''edits existing model using an privileged account, 
    should only be called after checking credentials'''
    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/schedules/{model_id}'

    data = {
        'user_id': user_id,
        'attachments': None,
        'credentials': credentials,
        'schedule_name': schedule_name,
        'automation_name': automation_name,
        'output_file_format': output_file_format,
        'link_results': link_results,
        'email_to_send_results': email_to_send_results
    }

    res = requests.put(
        url=url,
        headers=headers,
        data=data,
        files={'input_file': input_file}
    )

    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def delete_model(user_id: int, model_id: int) -> bool:
    '''deletes existing model using an privileged account, 
    should only be called after checking credentials'''
    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    url = f'{orchestrator_url}/schedules/{model_id}'

    data = {
        'user_id': user_id,
    }

    res = requests.delete(
        url=url,
        headers=headers,
        params=data
    )
    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def create_appointment_on_backend(schedule):
    '''
    create appointment of a template
    '''

    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    target_url = orchestrator_url + '/appointments/'

    data = {
        'schedule_id': schedule.id,
        'execution_cron': schedule.get_cron_expression(),
        'start_date': schedule.get_execution_date(format='%s'),
    }

    res = requests.post(url=target_url,
                        data=data,
                        headers=headers)

    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def edit_appointment_on_backend(schedule):
    '''
    edit appointment of a template
    '''

    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    target_url = orchestrator_url + f"/appointments/{schedule.id}"

    data = {
        'execution_cron': schedule.get_cron_expression(),
        'start_date': schedule.get_execution_date(format='%s'),
    }

    res = requests.put(url=target_url,
                       data=data,
                       headers=headers)

    return {
        'success': res.ok,
        'data': res.json(),
        'status': res.status_code
    }


def delete_appointment_on_backend(template_id):
    '''
    delete appointment of a template
    '''

    orchestrator_url, _, _ = get_orchestrator_credentials()
    headers = {
        'Authorization': get_auth_token()
    }
    target_url = orchestrator_url + f"/appointments/{template_id}"

    res = requests.delete(url=target_url, headers=headers)

    return {
        'success': res.ok,
        'status': res.status_code
    }
