from . import models
# from celery import task
import requests
import json
from urllib.parse import urljoin
from celery.schedules import crontab
from celery.task import periodic_task
from dashboard.templatetags.dashboard_tags import getAllFutureAutomations
from smt_orchestrator.models import FutureAutomation

# @task(name = 'start automation task')


def start_task(task_id):
    '''
    start_task start the execution of an automation
    '''

    task = models.Task.objects.get(pk=task_id)
    automation = task.schedule.automation

    base_url = automation.url
    target_url = urljoin(base_url, '/run')

    data = json.dumps({
        'input_path': task.schedule.input_path,
        'file_format': task.schedule.file_format,
        'email_to_send_results': task.schedule.email_to_send_results,
    })

    print(f'debug {data}')

    r = requests.post(url=target_url,
                      data=data,
                      headers={
                          'content-type': 'application/json'
                      })

    if not r.ok:
        task.state = 3  # FAULTED

    task.state = 2  # PROCESSING
    task.save()
    task.schedule.state = task.state
    task.schedule.save()


@periodic_task(name='Clean FutureAutomation Database', run_every=crontab(hour=2, minute=0, day_of_month=1))
def clean_future_automations_database():
    services_to_erase = set([])

    all_registered_future_automations = getAllFutureAutomations(
        language='pt-BR')
    all_future_automations_in_database = FutureAutomation.objects.all()
    for automation in all_future_automations_in_database:
        if automation.name not in all_registered_future_automations:
            services_to_erase.add(automation.name)

    FutureAutomation.objects.filter(name__in=services_to_erase).delete()
