from cryptography.fernet import Fernet
from django.conf import settings as django_settings
from django import utils
from django.core.validators import validate_email
from datetime import datetime, timedelta
from celery import task
from celery.task import periodic_task
from celery.schedules import crontab

import requests
import pytz
from dashboard.templatetags.dashboard_tags import getLanguage

from my_solutions.templatetags.mysolutions_tags import make_directory
from portal.templatetags.general_tags import translate
from smt_orchestrator.models import Schedule
from subscriptions.models import Profile, Subscription
from subscriptions.templatetags.subscriptions_tags import getHubUrl, sendEmail

from .models import Settings

HTTP_200_OK = 200  # mimics rest_framework status helper pattern


@task(name='task start tj bot')
def task_start_tj_bot():
    print("[DEBUG] running 'task_start_tj_bot'")

    app_name = django_settings.APP_URL_TRIBUNAL_DE_JUSTICA_RJ  # 'bot-api' # or 'bot-api
    app_url = f'http://{app_name}:5000/safe_run'

    # get a list of process marked to auto run
    try:
        processes_to_run = Settings.objects.filter(auto_run=True)
    except Settings.DoesNotExist:
        print('nothing to run, skipping!')
        return

    for process in processes_to_run:

        # throttle guard
        run_interval = timedelta(minutes=2)
        next_run = process.last_run + run_interval
        if next_run > datetime.now(tz=pytz.utc):
            print("skipping process because is too soon to run")
            continue

        # read credentials from db
        print("reading credentials from db")
        data = {
            'login': process.login,
            'password': process.password,
            'emailToSendResults': process.email_to_send_results,
            'encrypted_key': process.encrypted_key,
        }

        print("making api request to bot")
        response = requests.post(url=app_url, json=data)

        if not response.ok:
            # TODO: Log error to start
            print(
                f"error running task, status code was {response.status_code}")
            continue  # go to next process

        print("updating last_run info")
        process.last_run = datetime.utcnow()
        process.save()


# Execute at midnight (UTC)
@periodic_task(name='Change UiPath connection string encryption key', run_every=crontab(hour=0, minute=0))
def update_uipath_connection_string_encryption_key():
    def create_file_and_store_key(directory, key):
        with open(f"{directory}/keys.txt", "w") as file:
            file.write(str(key.decode('utf-8')))
            return True

    key = Fernet.generate_key()
    directory_name = 'encryption_keys'
    parent_dir = "/app/encryption/"
    directory_to_store_key = make_directory(
        directory_to_store_key=directory_name, parent_dir=parent_dir)
    create_file_and_store_key(
        directory=directory_to_store_key, key=key)


# Execute at 12:00 everyday (UTC)
@periodic_task(name='Send free trial follow-up emails', run_every=crontab(hour=12, minute=00))
def check_and_send_follow_up_emails():
    subscriptions_in_trial_period = Subscription.objects.filter(
        plan__name='Free Trial')

    for subscription in subscriptions_in_trial_period:
        profiles = []
        language = "pt-BR"

        start_of_free_trial = subscription.get_begin()
        now = utils.timezone.now().date()
        client = subscription.get_client()

        client_used_hub = Schedule.objects.filter(client=client).exists()
        client_signed_up_on_hub = subscription.get_subscription_plan(
        ).get_plan_name() != 'Free Trial'

        if 'smarthis' in client.get_client_name().lower():
            continue

        client_admins = Profile.objects.filter(client=client, role=4)
        for admin_profile in client_admins:
            # In case there is more than one client admin
            admin_email = admin_profile.get_user().get_email()
            email_is_valid = validate_email(admin_email)
            if email_is_valid:
                profiles.append(admin_profile)

        trial_period = subscription.get_trial_period()
        if not trial_period:
            trial_period = 14

        diff_in_days = (now - start_of_free_trial).days

        if diff_in_days == 5:
            email_template = 'trialFirstFeedback'
            email_context = {'language': 'pt-BR', 'hub_url': getHubUrl(),
                             'number_of_days_left': trial_period - diff_in_days, 'user': {}}
        elif diff_in_days == 8 and not client_used_hub:
            email_template = 'trialDidNotUseHub8Days'
            email_context = {'language': 'pt-BR', 'user': {}, 'services_link': f'{getHubUrl()}services',
                             'discover_link': f'{getHubUrl()}discover'
                             }
        elif diff_in_days == trial_period - 2:
            email_template = 'trial2DaysLeft'
            email_context = {
                'language': 'pt-BR', 'link': f'{getHubUrl()}services?modal="plans-modal--upgrade-button"', 'user': {}}
        elif diff_in_days == (trial_period + 1):
            email_template = 'endOfTrial'
            email_context = {
                'language': 'pt-BR', 'link': f'{getHubUrl()}services?modal="plans-modal--upgrade-button"', 'user': {}}
        elif diff_in_days == (trial_period + 3) and not client_signed_up_on_hub:
            email_template = 'postMortemTrialEmail'
            email_context = {'language': 'pt-BR', 'user': {}}

        if email_template != '':
            for profile in profiles:
                user = profile.get_user()
                language = profile.getLanguage()
                if email_template == 'trialFirstFeedback':
                    email_title = f"{translate('so', language)} {user.first_name} {translate('hows_your_smarthis_hub_experience', language)}"
                elif email_template == 'trialDidNotUseHub8Days':
                    email_title = f"{user.first_name} {translate('can_we_help_you', language)}"
                elif email_template == 'trial2DaysLeft':
                    email_title = {translate(
                        'weve_set_up_important_information_for_you_to_enjoy_the_last_days_of_testing', language)}
                elif email_template == 'endOfTrial':
                    email_title = {
                        translate('next_steps_what_to_do_now_that_the_trial_period_is_over', language)}
                elif email_template == 'postMortemTrialEmail':
                    email_title = f"{user.first_name} {translate('can_we_talk_to_you', language)}"
                else:
                    return

                email_context['user'] = user
                email_context['language'] = language
                sendEmail(email_template, email_title,
                          user.get_email(), email_context)

        else:
            continue
