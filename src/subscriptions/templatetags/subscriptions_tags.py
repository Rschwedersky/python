from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.cache import cache
from django.template.loader import render_to_string
from django.db.models import Q
from portal.templatetags.general_tags import check_if_automation_name_is_in_query, get_automation_display_name
from subscriptions.models import Companies, Invites, Plan, Profile, User, UsersPlans, Subscription, Client, AutomationsClients
from smt_orchestrator.models import Automation, Schedule, Task

from dashboard.templatetags.dashboard_tags import remove_special_characters, s3_remove_file, translate, isClientMainUser, getUsersfromClients

import json
from datetime import datetime
from collections import Iterable
import requests

register = template.Library()


@register.filter
def getSettingsInfos(user, language):
    infos = {
        'active_tab': 'profile',
        'all_btns': [
            {'id': 'profile', 'name': translate('profile', language)},
        ],
    }

    if isClientMainUser(user):
        infos['all_btns'].append(
            {'id': 'plan', 'name': translate('plan', language)})
        infos['all_btns'].append(
            {'id': 'crew', 'name': translate('crew', language)})

        profile = Profile.objects.get(user=user)
        client = profile.client

        subscripted_in = Subscription.getSubscriptionByClient(client)
        infos['subscription'] = subscripted_in
        if (subscripted_in != None):
            infos['plan'] = subscripted_in.get_subscription_plan()
            infos['plan_value'] = str(subscripted_in.get_value())
        else:
            infos['plan'] = {'name': 'EMPTY', 'qnt_automations': 0, 'value': 0}
            infos['plan_value'] = 0

        profiles = getUsersfromClients(False, client)
        allinfos_profiles = {}
        all_users_ids = [user.id]
        for p in profiles:
            all_users_ids.append(p.user.id)
            allinfos_profiles[p.user.id] = {'user': p.user, 'services': {}}
        services_allocated_by_user = UsersPlans.objects.filter(
            user__id__in=all_users_ids)
        automations_translate = Automation.get_automations_with_ui(
            language=language, client=client)
        for service in services_allocated_by_user:
            allinfos_profiles[service.user.id]['services'][service.automation.name] = {
                'automation_name': service.automation.name,
                'display_name': get_automation_display_name(service.automation, language),
                'howmany_models_configured': 0
            }

        all_schedules_allocated = Schedule.objects.filter(
            user__id__in=all_users_ids)
        for schedule_allocated in all_schedules_allocated:
            # if aqui pra caso existam automações relacionadas, mas não exista o usersplans
            if schedule_allocated.user.id in allinfos_profiles and schedule_allocated.automation.name in allinfos_profiles[schedule_allocated.user.id]['services']:
                allinfos_profiles[schedule_allocated.user.id]['services'][
                    schedule_allocated.automation.name]['howmany_models_configured'] += 1
        infos['profiles'] = allinfos_profiles

        infos['automations_translate'] = automations_translate

    # Advanced por enquanto não vai
    # infos['all_btns'].append({ 'id':'advanced', 'name':translate('advanced',language) })

    return infos


@register.filter
def getAllClientCollaboratorsInfo(user):
    profile = Profile.objects.get(user=user)
    profiles = getUsersfromClients(False, profile.client)
    allinfos_profiles = {}
    all_users_ids = []
    for p in profiles:
        all_users_ids.append(p.user.id)
        allinfos_profiles[p.user.id] = {}
    services_allocated_by_user = UsersPlans.objects.filter(
        user__id__in=all_users_ids)
    for service in services_allocated_by_user:
        allinfos_profiles[service.user.id][service.automation.name] = {
            'howmany_models_configured': 0
        }

    all_schedules_allocated = Schedule.objects.filter(
        user__id__in=all_users_ids)
    for schedule_allocated in all_schedules_allocated:
        # if aqui pra caso existam automações relacionadas, mas não exista o usersplans
        if schedule_allocated.user.id in allinfos_profiles and schedule_allocated.automation.name in allinfos_profiles[schedule_allocated.user.id]:
            allinfos_profiles[schedule_allocated.user.id][schedule_allocated.automation.name]['howmany_models_configured'] += 1
    return allinfos_profiles


@register.filter
def getUserPlan(request):
    try:
        subscription = request.subscription
        plan = subscription.get_subscription_plan()
        return plan
    except ObjectDoesNotExist:
        return False


def delete_schedules_from_user(all_users_remove_list=[], automation_obj=None):
    if automation_obj != None:
        if isinstance(automation_obj, Iterable):
            schedules_to_be_deleted = Schedule.objects.filter(
                user__id__in=all_users_remove_list, automation__in=automation_obj)
        else:
            schedules_to_be_deleted = Schedule.objects.filter(
                user__id__in=all_users_remove_list, automation=automation_obj)
    else:
        schedules_to_be_deleted = Schedule.objects.filter(
            user__id__in=all_users_remove_list)
    for schedule in schedules_to_be_deleted:
        erase_schedule_in_s3_and_database(schedule)


@register.filter
def erase_schedule_in_s3_and_database(schedule, language='pt-BR'):
    emails_to_receive_notification = ['guilherme.favoreto@smarthis.com.br',
                                      'yuri.santana@smarthis.com.br', 'bruno.marques@smarthis.com.br']

    schedule_info = {'user': schedule.user.email, 'automation': schedule.automation.name, 'input_path': schedule.input_path,
                     'schedule_name': schedule.name, 'schedule_id': schedule.id, 'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'language': language}
    try:
        remove_s3_file = s3_remove_file(
            settings.AWS_STORAGE_BUCKET_NAME, schedule.input_path)
        if remove_s3_file == True:
            schedule.delete()
        else:
            sendEmail('errorErasingSchedule', 'Não foi possível apagar um Schedule',
                      emails_to_receive_notification, schedule_info)
    except:
        sendEmail('errorErasingSchedule', 'Não foi possível apagar um Schedule',
                  emails_to_receive_notification, schedule_info)


@register.filter
def sendEmail(template, title, to, email_params, testing_email_functionality=False):
    if not settings.TESTING or testing_email_functionality:
        try:
            email_params['title'] = title
            email_params['url'] = getHubUrl()

            msg_plain = render_to_string(
                f'email_templates/{template}.html', email_params)
            msg_html = render_to_string(
                f'email_templates/{template}.html', email_params)

            if type(to) is str:
                to = [to]

            if settings.IS_DEV or settings.IS_LOCALHOST:
                from_email = 'hub-contato@smarthis.com.br'
            else:
                from_email = 'contato@mail.hub.smarthis.com.br'

            send_mail(
                title,
                msg_plain,
                from_email,
                to,
                html_message=msg_html,
            )
            return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': str(e)}


@register.filter
def getHubUrl(consider_localhost=True):
    url = 'https://hub.smarthis.com.br/'
    if consider_localhost and settings.IS_DEV and settings.IS_LOCALHOST:
        url = 'http://localhost:8000/'
    elif settings.IS_DEV:
        url = 'https://hub.dev.smarthis.com.br/'
    return url


@register.filter
def get_users_from_client(client, count=False):
    profile = Profile.objects.filter(client=client)
    all_users = User.objects.filter(profile__in=profile)

    if count == True:
        return all_users.count()
    else:
        return all_users


@register.filter
def get_chosen_plan_name(plan, chosen_period,
                         with_extra_queries, with_dashboard):
    if plan == 'starter':
        if chosen_period == 'monthly':
            if with_extra_queries:
                if with_dashboard:
                    plan_name = 'starter_monthly_plus_with_dashboard'
                else:
                    plan_name = 'starter_monthly_plus'
            else:
                if with_dashboard:
                    plan_name = 'starter_monthly_with_dashboard'
                else:
                    plan_name = 'starter_monthly'
        else:
            if with_extra_queries:
                if with_dashboard:
                    plan_name = 'starter_anual_plus_with_dashboard'
                else:
                    plan_name = 'starter_anual_plus'
            else:
                if with_dashboard:
                    plan_name = 'starter_anual_with_dashboard'
                else:
                    plan_name = 'starter_anual'
    else:
        if chosen_period == 'monthly':
            if with_extra_queries:
                if with_dashboard:
                    plan_name = 'advanced_monthly_plus_with_dashboard'
                else:
                    plan_name = 'advanced_monthly_plus'
            else:
                if with_dashboard:
                    plan_name = 'advanced_monthly_with_dashboard'
                else:
                    plan_name = 'advanced_monthly'
        else:
            if with_extra_queries:
                if with_dashboard:
                    plan_name = 'advanced_anual_plus_with_dashboard'
                else:
                    plan_name = 'advanced_anual_plus'
            else:
                if with_dashboard:
                    plan_name = 'advanced_anual_with_dashboard'
                else:
                    plan_name = 'advanced_anual'

    return plan_name


@register.filter
def get_plan_info(plan=None):
    all_plans_obj = Plan.objects.filter(Q(name='Starter') | Q(name='Advanced'))
    all_plans = {}
    for single_plan in all_plans_obj:
        all_plans[single_plan.get_plan_name().lower()] = single_plan
    all_plans['business'] = {'name': 'Business', 'value': None, 'qnt_automations': None,
                             'available_queries': None, 'extra_queries': None,  'extra_price': None}

    if plan != None and plan in all_plans:
        return all_plans[plan]
    elif plan == None:
        return all_plans
    else:
        return False


def set_company_info_with_cnpj(client: Client, cnpj: str):
    print('client', client)
    print('cnpj', cnpj)
    cleaned_cnpj = remove_special_characters(cnpj)
    print('cleaned_cnpj', cleaned_cnpj)

    success = False
    try:
        print('try')
        client_company = Companies.objects.get(cnpj=cleaned_cnpj)
        client.set_company(client_company)
        client.save()
        return True

    except Companies.DoesNotExist:
        try:
            response = requests.get(
                f"https://www.receitaws.com.br/v1/cnpj/{cleaned_cnpj}")
            converted_response = json.loads(response.text)
            company_razao_social = converted_response.get(
                'nome', f'Client_{client.get_client_name()}_sem_nome')
            new_company = Companies.objects.create(
                cnpj=cleaned_cnpj, razao_social=company_razao_social)

            success = True
        except Exception:
            new_company = Companies.objects.create(
                cnpj=cleaned_cnpj, razao_social=f'Client_{client.get_client_name()}_sem_nome')
            success = False
        finally:
            client.set_company(new_company)
            client.save()
            return success


def get_hired_services_transformed_in_object(client, language):
    services = []
    hired_services = AutomationsClients.objects.filter(
        client=client)
    automation_objects = Automation.get_automations_with_ui(language, client)

    for automation_hired in hired_services:
        automation_name = automation_hired.automation.name
        automation_name_is_allowed = check_if_automation_name_is_in_query(
            automation_name=automation_name, query=automation_objects)

        if automation_name_is_allowed:
            for allocation in range(automation_hired.qnt_automations):
                services.append({'display_name': get_automation_display_name(automation_hired.automation, language),
                                'identifier': automation_name, 'utilizations': None, 'all_schedules': None, 'checked': None})

    return services


def get_client_services_and_utilizations(client, language, desired_plan, desired_plan_info, has_plan_negotiation, client_subscription, is_upgrade=False):
    services = get_hired_services_transformed_in_object(client, language)

    client_users = get_users_from_client(client)
    users_registry = {}
    utilizations = 0

    dashboard_checked = False
    if desired_plan == 'business':
        if (has_plan_negotiation != False and client_subscription.get_dashboard()) or (has_plan_negotiation == False and client_subscription.get_dashboard()):
            dashboard_checked = True
            utilizations += 1
    elif utilizations < desired_plan_info.get_plan_qnt_automations() and client_subscription.get_dashboard():
        dashboard_checked = True
        utilizations += 1

    if has_plan_negotiation == False:
        for service in services:
            all_service_schedules = Schedule.objects.filter(
                automation__name=service['identifier'], user__in=client_users)
            if len(all_service_schedules) > 0:
                if service['identifier'] in users_registry:
                    user_used_automation = Task.objects.filter(
                        schedule__in=all_service_schedules).exclude(Q(state=2) | Q(schedule__user__in=users_registry[service['identifier']]))

                else:
                    user_used_automation = Task.objects.filter(
                        schedule__in=all_service_schedules).exclude(state=2)
                if user_used_automation:
                    target_user = user_used_automation.first().schedule.user

                    if service['identifier'] not in users_registry.keys():
                        users_registry[service['identifier']] = [target_user]
                    else:
                        users_registry[service['identifier']].append(
                            target_user)
                    service['utilizations'] = target_user
                    if (desired_plan == 'business' or utilizations < desired_plan_info.get_plan_qnt_automations()):
                        utilizations += 1
                        service['checked'] = True
                    else:
                        service['checked'] = False
                elif is_upgrade and (isinstance(desired_plan_info, dict) or utilizations < desired_plan_info.qnt_automations):
                    service['checked'] = True
                    utilizations += 1
                service['all_schedules'] = all_service_schedules

    else:
        for service in services:
            utilizations += 1
            service['checked'] = True

    return {'services': services, 'licenses_used': utilizations, 'dashboard_checked': dashboard_checked}


@register.filter
def is_plan_upgrade(subscription, desired_plan, desired_period='monthly', desired_plus=None):
    desired_plan_value = 0
    desired_plan_qnt_automations = 0
    if isinstance(desired_plan, dict):
        if desired_plan['value']:
            desired_plan_value = desired_plan['value']
            if desired_plus != None and desired_plus:
                desired_plan_value += desired_plan['extra_price']
        desired_plan_qnt_automations = desired_plan['qnt_automations']
    else:
        desired_plan_value = desired_plan.value
        if desired_plus != None and desired_plus:
            desired_plan_value += desired_plan.get_extra_price()
        desired_plan_qnt_automations = desired_plan.qnt_automations

    if desired_period == 'yearly':
        desired_plan_value *= 10

    is_more_expensive = desired_plan_value > subscription.get_value()
    is_upgrade = False
    if desired_plan_qnt_automations != None and desired_plan_qnt_automations > subscription.get_number_of_hired_services():
        is_upgrade = True
    elif desired_plan_qnt_automations == None:
        is_upgrade = True

    return is_more_expensive or is_upgrade


def update_plans_to_starter_and_advanced():
    old_user_plans = Plan.objects.filter(
        name__startswith='user')
    for plan in old_user_plans:
        new_name = plan.get_plan_name().replace('user', 'starter')
        plan.set_plan_name(new_name)
        plan.save()

    old_area_plans = Plan.objects.filter(
        name__startswith='area')
    for plan in old_area_plans:
        new_name = plan.get_plan_name().replace('area', 'advanced')
        plan.set_plan_name(new_name)
        plan.save()


def check_if_client_has_not_finished_registering(subscription):
    plan_name_is_trial = subscription.get_subscription_plan().get_plan_name() == 'Free Trial'
    subscription_value_is_default = subscription.get_value() == 200.0
    subscription_trial_period_is_default = subscription.get_trial_period() == 14
    subscription_dashboard_is_default = subscription.get_dashboard() == False
    subscription_hired_services_is_default = subscription.get_number_of_hired_services() == 1
    subscription_payment_period_is_default = subscription.get_payment_period() == 'MONTHLY'
    subscription_queries_limit_is_default = subscription.get_queries_limit() == 0
    subscription_extra_queries_is_default = subscription.get_extra_queries() == False

    if plan_name_is_trial and subscription_value_is_default and subscription_trial_period_is_default and subscription_dashboard_is_default and subscription_hired_services_is_default and subscription_payment_period_is_default and subscription_queries_limit_is_default and subscription_extra_queries_is_default:
        return True
    else:
        return False


def create_new_client_subscription(client):
    try:
        free_trial_plan = Plan.objects.get(name='Free Trial')
    except Plan.DoesNotExist:
        free_trial_plan = Plan.objects.create(name='Free Trial',  qnt_automations=0,
                                              qnt_queries=0, qnt_extra_queries=0, extra_price=0)

    subscription = Subscription.objects.create(
        client=client, plan=free_trial_plan, active=False)


def get_progress_points(request):
    subscription = request.subscription
    user = request.user
    client = user.profile.client
    dashboard = request.subscription.get_dashboard()

    try:
        has_any_task = Task.objects.get(schedule__client=client)
    except:
        has_any_task = None

    total_points = 0

    reference = {
        'confirm_email': {'points': 15, 'completed': False, 'alerted': cache.get(f"confirm_email_{user.id}", False)},
        'use_service': {'points': 40, 'completed': False, 'alerted': cache.get(f"use_service_{user.id}", False)},
        'new_service': {'points': 30, 'completed': False, 'alerted': cache.get(f"new_service_{user.id}", False)},
        'invite_crew': {'points': 15, 'completed': False, 'alerted': cache.get(f"invite_crew_{user.id}", False)},
    }

    all_automation_clients = AutomationsClients.objects.filter(
        client=client).values('qnt_automations')
    number_of_hired_services = 0

    for hired_service in all_automation_clients:
        number_of_hired_services += hired_service.get('qnt_automations', 0)

    client_invites = Invites.objects.filter(client=client)

    if has_any_task:
        total_points += reference['use_service']['points']
        reference['use_service']['completed'] = True

    if subscription.get_number_of_hired_services() < number_of_hired_services or (subscription.get_number_of_hired_services() == number_of_hired_services and dashboard == True):
        total_points += reference['new_service']['points']
        reference['new_service']['completed'] = True

    if len(client_invites) > 0:
        total_points += reference['invite_crew']['points']
        reference['invite_crew']['completed'] = True

    if request.email_was_verified == True:
        total_points += reference['confirm_email']['points']
        reference['confirm_email']['completed'] = True

    for key, value in reference.items():
        if value.get('completed', None) and not value.get('alerted', None):
            cache_key = f"{key}_{user.id}"
            cache.set(cache_key, True, 1814400)

    return (total_points, reference)


def check_email_domain(email_domain: str) -> bool:
    standard_domains = ['gmail', 'yahoo', 'hotmail',
                        'aol', 'live', 'outlook', 'protonmail', 'dukeoo', 'icloud']
    domain_is_standard = False

    for domain in standard_domains:
        if domain in email_domain:
            domain_is_standard = True

    return domain_is_standard
