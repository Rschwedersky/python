from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from smt_orchestrator.orchestrator import create_appointment_on_backend, edit_appointment_on_backend, delete_appointment_on_backend
from portal.functions import get_client_from_request
from django.db.models import Q
from django.db.utils import IntegrityError
from .models import Settings
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
import uuid
import json as JSON
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.decorators.http import require_http_methods
from django.http.response import HttpResponse
from .security.rsa import urlsafe_encrypt as rsa_urlsafe_encrypt
from .security.aes import urlsafe_encrypt as aes_urlsafe_encrypt
from Crypto.Random import get_random_bytes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.decorators import permission_classes, authentication_classes
from django.core.validators import validate_email
from types import SimpleNamespace
from .models import Settings

from subscriptions.models import User, AutomationsClients, UsersPlans, Profile, Invites
from smt_orchestrator.orchestrator import delete_model, edit_model, new_model, start_schedule, stop_schedule, read_automation

from dashboard.templatetags.dashboard_tags import getAllFutureAutomations, getClientMainUserInfo, get_s3_presigned_url_upload, get_automation_by_name, getLanguage, getStandardVariables, isClientMainUser, get_people_to_send_email
from smt_orchestrator.models import Automation, FutureAutomation, InterestedInServiceUnderMaintenance, Schedule, ScheduleExtraInfos
from .templatetags.mysolutions_tags import check_if_file_is_correct, get_automation_fields, get_filters_by_user, get_template_by_id, getUserSchedulesCompleteWithPagination, getUserSchedulesFewColumnsWithPagination, getRequestInfos, send_message_to_groups, sort_dict_by_key, addManagePermissionInfos, check_client_available_licenses, get_hired_user_services_and_solutions, get_all_services_tabs, getScheduledAutomations, translate_schedule_appointment_into_cron_expression, get_appointment_email_infos, check_if_free_trial_ended, create_extrainfo_file
from portal.templatetags.general_tags import check_if_automation_name_is_in_query, translate, get_automation_display_name
from subscriptions.templatetags.subscriptions_tags import delete_schedules_from_user, get_progress_points, getUserPlan, sendEmail, getHubUrl
import my_solutions.file_validator as file_validator
from smt_orchestrator.orchestrator import create_appointment_on_backend, edit_appointment_on_backend, delete_appointment_on_backend, delete_model, edit_model, new_model, start_schedule, stop_schedule, read_automation, read_monitoring_dashboard_data

from datetime import datetime


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def get_upload_presigned_url(request):
    try:
        infos = JSON.loads(request.body)
        result = get_s3_presigned_url_upload(infos, request)
        return JsonResponse(data=result, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({}, status.HTTP_204_NO_CONTENT)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def onboarding_user(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))

    language = getLanguage(request)
    is_admin = isClientMainUser(request.user)
    subscription = request.subscription
    plan = subscription.get_subscription_plan()

    if plan and 'free trial' in plan.get_plan_name().lower():
        if is_admin:
            free_trial_ended = check_if_free_trial_ended(subscription)
            request.free_trial_ended = True if free_trial_ended else False

            if free_trial_ended:
                return HttpResponseRedirect(reverse('services'))

            total_points, _ = get_progress_points(request)
            trial_period = subscription.get_trial_period()

            if total_points == 100:
                if trial_period == 14:
                    sendEmail('userOnboardingCompletion', translate('congratulations_youve_earned_6_extra_days', language),
                              request.user.get_email(), {'hub_url': getHubUrl(), 'language': 'pt-BR', 'user': request.user})
                    trial_period = subscription.set_trial_period(
                        trial_period=20)
                    subscription.save()
            else:
                trial_period = subscription.set_trial_period(trial_period=14)
                subscription.save()

            context = {
                'active_page': 'onboarding',
                'body_class': 'body_api',
                'language': language,
                'subscription': subscription.get_subscription_plan().get_plan_name()
            }

            return render(request, "onboardingContent.html", context)
        else:
            return HttpResponseRedirect(reverse('services'))
    else:
        request.free_trial_ended = False
        return HttpResponseRedirect(reverse('services'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def services(request, active_tab=''):
    language = getLanguage(request)
    client = get_client_from_request(request)

    is_admin = isClientMainUser(request.user)
    allowed_automations = Automation.get_automations_with_ui(
        language=language, client=client)

    context = {
        'language': language,
        'active_page': 'services',
        'automations_translate': allowed_automations,
        'is_admin': is_admin,
        'subscription': request.subscription,
        'free_trial_ended': request.free_trial_ended,
    }

    if active_tab == '':
        active_tab = 'my_services'
    context['active_tab'] = active_tab
    context['all_services_tabs'] = get_all_services_tabs(
        is_admin, active_tab, 'all_automations')

    if active_tab == 'processes_history':
        schedule_info = getUserSchedulesFewColumnsWithPagination(
            request, objects_per_page=5)

        context['schedules'] = schedule_info['schedules']
        context['tasks'] = schedule_info['tasks']
    elif active_tab == 'all_scheduled_automations':
        scheduled_automations = getScheduledAutomations(
            is_admin, request, language)
        context['scheduled_automations'] = scheduled_automations['data']
        context['page_obj_scheduled_automations'] = scheduled_automations['page_obj']
    else:

        if request.method == 'GET' and request.GET.get('q', None):
            context = get_hired_user_services_and_solutions(
                is_admin, request, context, language, False)

            query = request.GET.get('q')

            query = query.strip()

            automations = allowed_automations.filter(
                Q(name__icontains=query) | Q(type__icontains=query) | Q(group__icontains=query) | Q(display_name_pt_br__icontains=query) | Q(display_name_en__icontains=query) | Q(display_name_es__icontains=query))

            if is_admin:
                query = AutomationsClients.objects.filter(
                    client=client).values('automation__name')
            else:
                query = UsersPlans.objects.filter(
                    user=request.user).values('automation__name')

            allowed_automations = set()
            for q in query:
                automation_name = q.get('automation__name')
                automation_is_allowed = check_if_automation_name_is_in_query(
                    automation_name=automation_name, query=automations)
                if automation_is_allowed:
                    allowed_automations.add(automation_name)

            if automations:
                context['solutions'] = automations.filter(
                    name__in=allowed_automations)
            else:
                context['solutions'] = Automation.objects.none()

            context['filters'] = get_filters_by_user(
                language, context['solutions'], client=get_client_from_request(request), sort=True)
        else:
            context = get_hired_user_services_and_solutions(
                is_admin, request, context, language)

            context['filters'] = get_filters_by_user(
                language, context['hired_services'], client=get_client_from_request(request), sort=True)

    return render(request, "services.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def services_singletab(request, tab='my_services'):
    template = 'services_tabs/single_tab_content/'
    language = getLanguage(request)
    is_admin = isClientMainUser(request.user)
    allowed_tabs = ['processes_history', 'my_services',
                    'manage_permissions', 'all_scheduled_automations']

    context = {
        'language': language,
        'is_admin': is_admin,
        'automations_translate': Automation.get_automations_with_ui(language=language, client=get_client_from_request(request)),
        'active_tab': tab
    }
    if tab == 'processes_history':
        template += f'{tab}.html'
        schedule_info = getUserSchedulesFewColumnsWithPagination(
            request, objects_per_page=5)
        context['schedules'] = schedule_info['schedules']
        context['tasks'] = schedule_info['tasks']
    elif tab == 'all_scheduled_automations':
        template += f'{tab}.html'
        # TODO: get all scheduled automations
        scheduled_automations = getScheduledAutomations(
            is_admin, request, language)
        context['scheduled_automations'] = scheduled_automations['data']
        context['page_obj_scheduled_automations'] = scheduled_automations['page_obj']
    elif tab in allowed_tabs:
        context = get_hired_user_services_and_solutions(
            is_admin, request, context, language)
        context['filters'] = get_filters_by_user(
            language, context['hired_services'], client=get_client_from_request(request), sort=True)

        if tab == 'my_services':
            template += 'all_automations.html'
        elif tab == 'manage_permissions':
            template += f'{tab}.html'

    return render(request, template, context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def automations(request, automation_name, active_tab=''):
    language = getLanguage(request)
    client = get_client_from_request(request)

    allowed_automations = Automation.get_automations_with_ui(
        language=language, client=client)
    automation_name_is_allowed = check_if_automation_name_is_in_query(
        automation_name=automation_name, query=allowed_automations)

    if automation_name_is_allowed:
        automation_obj = get_automation_by_name(automation_name)
        automation_type = automation_obj.type
        is_showcase = automation_obj.get_is_showcase()
        is_admin = isClientMainUser(request.user)

        if is_showcase:
            return HttpResponseRedirect(reverse('services'))

        if is_admin:
            allowed_user_automations = AutomationsClients.objects.filter(
                client=client, automation__name=automation_name)
        else:
            allowed_user_automations = UsersPlans.objects.filter(
                user=request.user, automation__name=automation_name)
        if len(allowed_user_automations) > 0:
            schedule_info = getUserSchedulesCompleteWithPagination(
                request=request, automation_name=automation_name, objects_per_page=5)
            can_create_model = AutomationsClients.objects.get(
                client=client, automation=automation_obj)

            context = {
                'can_create_model': can_create_model.get_can_create_model(),
                'language': language,
                'automation_name': automation_name,
                'schedules': schedule_info['schedules'],
                'tasks': schedule_info['tasks'],
                'active_page': 'services',
                'standard_variables': getStandardVariables(automation_name, language),
                'automation_type': automation_type,
                'automations_translate': allowed_automations,
                'is_admin': is_admin,
                'subscription': request.subscription,
                'free_trial_ended': request.free_trial_ended,
                'is_automation_active': automation_obj.active,
                'email_was_verified': request.email_was_verified,
                'automation_obj': automation_obj
            }

            if automation_type == 'upload_and_credential' or automation_type == 'credential_and_filter_notes':
                allschedules_ids = Schedule.objects.order_by('created_at').filter(
                    user=request.user, automation__name=automation_name).values_list('id', flat=True)
                allschedule_extrainfos = ScheduleExtraInfos.objects.filter(
                    schedule__id__in=allschedules_ids)
                allschedule_extrainfos_obj = {}
                for schedule_extrainfos in allschedule_extrainfos:
                    allschedule_extrainfos_obj[schedule_extrainfos.schedule.id] = schedule_extrainfos.extra_info
                context['allschedule_credentials'] = allschedule_extrainfos_obj

            if active_tab == '':
                active_tab = 'my_services'
            context['active_tab'] = active_tab
            context['all_services_tabs'] = get_all_services_tabs(
                is_admin, active_tab, 'my_automations')

            return render(request, "components/standard_solution.html", context)
        else:
            # não contratou esse tipo de automação
            return HttpResponseRedirect(reverse('services'))
    else:
        return HttpResponseRedirect(reverse('services'))


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def discover(request):
    # Avoiding circular imports error
    def make_necessary_imports():
        from .templatetags.mysolutions_tags import getAutomationsContractedByClient
        dict = {'getAutomationsContractedByClient': getAutomationsContractedByClient}
        # Getting dot notation
        transformed_dict = SimpleNamespace(**dict)
        return transformed_dict

    client = get_client_from_request(request)
    is_admin = isClientMainUser(request.user)

    language = getLanguage(request)

    available_licenses = check_client_available_licenses(
        request.user.profile.client)

    all_future_automations = getAllFutureAutomations(language)
    saved_future_automations = FutureAutomation.objects.filter(
        user=request.user)
    for automation in saved_future_automations:
        try:
            if automation.name in all_future_automations:
                all_future_automations[automation.name]['interested'] = True
        except KeyError as e:
            continue

    all_permitted_automations = Automation.get_automations_with_ui(
        language=language, client=client)

    if request.method == 'GET' and request.GET.get('q', None):
        query = request.GET.get('q')

        query = query.strip()

        automations = all_permitted_automations.filter(
            Q(name__icontains=query) | Q(type__icontains=query) | Q(group__icontains=query) | Q(display_name_pt_br__icontains=query) | Q(display_name_en__icontains=query) | Q(display_name_es__icontains=query))

        if automations:
            services = automations
        else:
            services = Automation.objects.none()
    else:
        services = all_permitted_automations

    filters = {}
    number_of_total_services = 0
    for automation in services:
        if automation.active:
            automation_group = translate(automation.group, language)
            if not automation_group in filters:
                filters[automation_group] = 0

            filters[automation_group] += 1
            number_of_total_services += 1

    sorted_filters = sort_dict_by_key(filters)

    all_filters = {"all_male": number_of_total_services}

    filters_with_all_first = {**all_filters, **sorted_filters}

    context = {
        'language': language,
        'active_page': 'discover',
        'automations_translate': services,
        'filters': filters_with_all_first,
        'subscription': request.subscription,
        'all_future_automations': all_future_automations,
        'available_licenses': available_licenses,
        'free_trial_ended': request.free_trial_ended,
    }

    imports = make_necessary_imports()
    context = imports.getAutomationsContractedByClient(
        context, get_client_from_request(request), request.subscription)

    if is_admin:
        context['is_admin'] = True
    else:
        context['is_admin'] = False
        context['admin_info'] = getClientMainUserInfo(request)

    return render(request, "discover.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def register_for_future_service(request):
    language = getLanguage(request)

    allowed_future_automations = getAllFutureAutomations(language)

    converted_request_body = JSON.loads(request.body)
    automation_name = converted_request_body.get('automation_name')
    interested = int(converted_request_body.get('interested'))

    if automation_name in allowed_future_automations:
        try:
            if interested == 1:
                new_future_automation_obj = FutureAutomation(
                    name=automation_name, user=request.user)
                new_future_automation_obj.save()
                return HttpResponse(status=status.HTTP_201_CREATED)
            else:
                FutureAutomation.objects.filter(
                    name=automation_name, user=request.user).delete()
                return HttpResponse(status=status.HTTP_200_OK)
        except Exception as e:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def discover_service(request, automation_name):
    # Avoiding circular imports error
    def make_necessary_imports():
        from .templatetags.mysolutions_tags import getAutomationsContractedByClient
        dict = {'getAutomationsContractedByClient': getAutomationsContractedByClient}
        # Getting dot notation
        transformed_dict = SimpleNamespace(**dict)
        return transformed_dict

    is_admin = isClientMainUser(request.user)

    language = getLanguage(request)
    client = get_client_from_request(request)
    available_licenses = check_client_available_licenses(client)

    allowed_automations = Automation.get_automations_with_ui(language, client)
    automation_name_is_allowed = check_if_automation_name_is_in_query(
        automation_name=automation_name, query=allowed_automations)

    if automation_name_is_allowed:

        automation_obj = get_automation_by_name(automation_name)
        is_automation_active = automation_obj.active

        if is_automation_active or request.user.profile.client.name == 'Smarthis':
            context = {
                'language': language,
                'automations_translate': allowed_automations,
                'automation_name': automation_name,
                'active_page': 'discover',
                'standard_variables': getStandardVariables(automation_name, language),
                'automation_type': automation_obj.type,
                'subscription': request.subscription,
                'available_licenses': available_licenses,
                'free_trial_ended': request.free_trial_ended,
            }

            imports = make_necessary_imports()
            context = imports.getAutomationsContractedByClient(
                context, get_client_from_request(request), request.subscription)

            if is_admin:
                context['is_admin'] = True
            else:
                context['is_admin'] = False
                context['admin_info'] = getClientMainUserInfo(request)
        else:
            return HttpResponseRedirect(reverse('discover'))
    else:
        return HttpResponseRedirect(reverse('discover'))

    return render(request, "discover/discover_service_page.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET"])
def get_switch_services_modal(request, automation_name):
    language = getLanguage(request)

    all_permitted_automations = Automation.get_automations_with_ui(
        language=language, client=get_client_from_request(request), column='name')
    automation_name_is_allowed = check_if_automation_name_is_in_query(
        automation_name=automation_name, query=all_permitted_automations)
    if not automation_name_is_allowed:
        return HttpResponseRedirect(reverse('discover'))

    automation_obj = get_automation_by_name(automation_name)

    heading = get_automation_display_name(automation_obj, language)

    context = {
        'language': language,
        'active_page': 'discover',
        'automations_translate': all_permitted_automations,
        'subscription': request.subscription,
        'heading': heading,
        'logo': f"img/logo_{automation_name}.png",
    }

    context = addManagePermissionInfos(request, context)

    return render(request, "discover/switch_services_step_modal.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def create_new_model(request):

    language = getLanguage(request)
    json = {'status': 400, 'msg': translate(
        "could_not_save_execution", language)}
    try:
        infos = getRequestInfos(
            request, ['name', 'file_format', 'email_to_send_results', 'automation', 'pass', 'login', 'extra_info', 'link_results'])
        file_wrapper = request.FILES.get('input_file', None)
        credentials = f"{infos['login']},{infos['pass']}"

        if file_wrapper:
            file = file_wrapper.file
            file.seek(0)
        elif infos['extra_info']:
            # is credential_extrainfos_type, need file
            file = create_extrainfo_file(request.user.id, infos['extra_info'])
        else:
            file = None

        response = new_model(user_id=request.user.id, input_file=file, schedule_name=infos['name'], automation_name=infos[
                             'automation'], output_file_format=infos['file_format'], email_to_send_results=infos['email_to_send_results'], link_results=infos['link_results'], credentials=credentials)

        if not response.get('success', False):
            return JsonResponse(json, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))

        new_model_info = response.get('data', {})
        new_model_id = new_model_info.get('id')

        new_model_obj = Schedule.objects.get(pk=new_model_id)
        automation_obj = get_automation_by_name(infos['automation'])

        standard_variables = getStandardVariables(
            infos['automation'], language)
        automation_pattern_type = automation_obj.type
        automation_obj = get_automation_by_name(infos['automation'])

        box_context = {'schedule': new_model_obj, 'automation_type': automation_pattern_type, 'automation_description': standard_variables[
            'title'], 'language': language, 'is_automation_active': automation_obj.active, 'schedule_automation_name': infos['automation'], 'email_was_verified': request.email_was_verified}

        if infos['extra_info']:
            try:
                new_extrainfo = ScheduleExtraInfos(
                    schedule=new_model_obj, extra_info=infos['extra_info'])
                new_extrainfo.save()
                allschedule_extrainfos_obj = {}
                allschedule_extrainfos_obj[new_model_obj.id] = infos['extra_info']
                box_context['allschedule_credentials'] = allschedule_extrainfos_obj
            except ObjectDoesNotExist:
                print('ERROR saving extra_info on DB')
                pass

        new_model_component = render_to_string(
            "components/box_automation.html", box_context)

        json = {'status': 201, 'msg': translate(
            "execution_created_successfully", language), 'model_component': new_model_component}

        return HttpResponse(JSON.dumps(json, ensure_ascii=False), content_type="application/json", status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse(json, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def edit_existing_model(request, model_id):

    language = getLanguage(request)
    json = {'status': 400, 'msg': translate(
        "could_not_save_execution", language)}

    try:
        infos = getRequestInfos(request, [
                                'name', 'file_format', 'login', 'pass', 'email_to_send_results', 'extra_info', 'filename', 'automation', 'link_results'])
        file_wrapper = request.FILES.get('input_file', None)

        if file_wrapper:
            file = file_wrapper.file
            file.seek(0)
        else:
            file = None

        credentials = f"{infos['login']},{infos['pass']}"

        response = edit_model(model_id=model_id, user_id=request.user.id, input_file=file, schedule_name=infos['name'], automation_name=infos['automation'],
                              output_file_format=infos['file_format'], email_to_send_results=infos['email_to_send_results'], credentials=credentials, link_results=infos['link_results'])
        if not response.get('success', None):
            return JsonResponse(json, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))

        json = {'status': 200, 'msg': translate(
            "execution_edited_successfully", language), 'data': response.get('data', {})}
        return JsonResponse(json, status=response.get('status', status.HTTP_200_OK))
    except KeyError as e:
        print('ERROR', e)
        return JsonResponse(json, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["DELETE"])
def remove_model(request, model_id):

    language = getLanguage(request)
    json = {'status': 400, 'msg': translate(
        'unable_to_remove_execution_please_try_again', language)}

    try:
        response = delete_model(
            model_id=model_id, user_id=request.user.id)

        if not response.get('success', None):
            return JsonResponse(json, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))

        json = {'status': 200, 'msg': translate(
            'execution_removed_successfully', language)}
        return JsonResponse(json, status=response.get('status', status.HTTP_200_OK))
    except KeyError as e:
        return JsonResponse(json, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def manage_client_permissions(request):
    language = getLanguage(request)

    client = get_client_from_request(request)

    allowed_automations = Automation.get_automations_with_ui(language, client)
    all_showcase = {}

    if len(request.POST) == 0 and JSON.loads(request.body).get('page') == 'discover':
        data = {}
        all_users_add = []
        converted_request_body = JSON.loads(request.body)
        all_users_remove = converted_request_body.get('all_users_remove')
        automation_name = converted_request_body.get('automation_name', '')
        automation_to_remove_permissions_name = converted_request_body.get(
            'automation_to_remove_permissions', '')
        number_of_permissions_to_add = converted_request_body.get(
            'number_of_permissions_to_add')

        automation_name_is_allowed = check_if_automation_name_is_in_query(
            automation_name=automation_name, query=allowed_automations)

        if automation_name_is_allowed:
            automation_obj = get_automation_by_name(automation_name)
            source_automation_obj = get_automation_by_name(
                automation_to_remove_permissions_name)

            if automation_obj.get_is_showcase() and automation_name not in all_showcase:
                all_showcase[automation_name] = number_of_permissions_to_add
            elif automation_name in all_showcase:
                all_showcase[automation_name] += number_of_permissions_to_add

            try:
                if len(all_users_remove) > 0:
                    UsersPlans.objects.filter(
                        user__id__in=all_users_remove, automation=source_automation_obj).delete()
                    delete_schedules_from_user(
                        all_users_remove_list=all_users_remove, automation_obj=source_automation_obj)
                source_service = AutomationsClients.objects.get(
                    client=client, automation=source_automation_obj)
                source_service.qnt_automations -= number_of_permissions_to_add
                if source_service.get_qnt_automations() == 0:
                    source_service.delete()
                else:
                    source_service.save()

                try:
                    target_service = AutomationsClients.objects.get(
                        client=client, automation=automation_obj)
                    target_service.qnt_automations += number_of_permissions_to_add

                except ObjectDoesNotExist:
                    target_service = AutomationsClients(
                        client=client, automation=automation_obj, qnt_automations=number_of_permissions_to_add)

                if automation_name == 'extrato-bancario':
                    target_service.can_create_model = 3

                target_service.save()
                AutomationsClients.resetAutomationsClientsByClient(client)
                UsersPlans.resetUsersPlansByClientAndAutomationsIds(client)

                target_service_available_permissions = int(target_service.get_qnt_automations()) - len(UsersPlans.objects.filter(
                    client=client, automation=automation_obj))

                source_service_available_permissions = int(source_service.get_qnt_automations()) - len(UsersPlans.objects.filter(
                    client=client, automation=source_automation_obj))

                data['source_service_permissions'] = source_service_available_permissions
                data['target_service_permissions'] = target_service_available_permissions

                if bool(all_showcase):
                    email_context = {
                        'language': language,
                        'user': request.user,
                        'all_showcase': all_showcase,
                    }

                    sendEmail('showcaseRequest', '[Troca de Serviço] Solicitação de Automação Vitrine' + ' Smarthis Hub',
                              get_people_to_send_email('product'), email_context)
                return JsonResponse(data, status=status.HTTP_200_OK)
            except:
                return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        all_users_add = JSON.loads(request.POST.get('all_users_add'))
        all_users_remove = JSON.loads(request.POST.get('all_users_remove'))
        automation_name = request.POST.get('automation_name', '')
        json = {'status': 400, 'msg': translate(
            'automation_not_found', language)}

    automation_name_is_allowed = check_if_automation_name_is_in_query(
        automation_name=automation_name, query=allowed_automations)

    if automation_name_is_allowed:
        automation_obj = get_automation_by_name(automation_name)
        try:
            for user_id in all_users_add:
                user_is_already_invited = (
                    type(user_id) is str and user_id.isdigit()) or type(user_id) is int
                if user_is_already_invited:
                    profile = Profile.objects.get(user__id=user_id)
                    try:
                        UsersPlans.objects.get(user=profile.get_user(
                        ), client=profile.get_client(), automation=automation_obj)
                    except UsersPlans.DoesNotExist:
                        UsersPlans.objects.create(
                            user=profile.get_user(), client=profile.get_client(), automation=automation_obj)
                        UsersPlans.resetUsersPlansByClientAndAutomationsIds(
                            profile.get_client())
                        sendEmail('conviteServico', translate('new_service_available', language), profile.get_user().get_email(), {
                            'language': language, 'user': profile.get_user(), 'link_automation': f'{getHubUrl()}services/{automation_obj.get_name()}', 'automation': automation_obj})
                    except UsersPlans.MultipleObjectsReturned:
                        ''' There is more than one UserPlan created for that user and that automation. Since we don't know which one to delete we pass for now'''
                        pass
                else:
                    # needs to invite user
                    try:
                        validate_email(user_id)
                    except ValidationError:
                        return JsonResponse({'status': 400, 'msg': translate('invalid_email', language)}, status=status.HTTP_400_BAD_REQUEST)
                    token = uuid.uuid4()
                    new_invite_id = 0
                    try:
                        new_invite = Invites.objects.create(
                            email=user_id, client=client, token=token, active=True)
                        new_invite_id = new_invite.id
                        new_user = User.objects.create_user(
                            email=user_id, password=str(uuid.uuid4()))
                        new_user.save()
                        new_user_profile = Profile.objects.get(
                            user=new_user)
                        new_user_profile.set_client(client)
                        new_user_profile.set_role(1)
                        new_user_profile.save()
                        new_user_services = UsersPlans.objects.create(
                            user=new_user, client=client, automation=automation_obj)
                        UsersPlans.resetUsersPlansByClientAndAutomationsIds(
                            client)

                        sendEmail('convitePlataforma', translate('you_have_been_invited_to_smarthis_hub', language), user_id, {
                                  'language': language, 'user': request.user, 'link_invite': f'{getHubUrl()}cadastro/{token}'})
                    except IntegrityError as e:
                        # error happened, need to undo things
                        if new_invite_id != 0:
                            Invites.objects.filter(id=new_invite_id).delete()
                        return JsonResponse({'status': 400, 'msg': translate('there_is_already_an_email_for_this_invite', language), 'user_repeated_email': user_id}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            if len(all_users_remove) > 0:
                UsersPlans.objects.filter(
                    user__id__in=all_users_remove).delete()
                UsersPlans.resetUsersPlansByClientAndAutomationsIds(client)

            users = []
            collaborators = UsersPlans.objects.filter(
                client=request.user.profile.client, automation=automation_obj).select_related('user')
            for collaborator in collaborators:
                users.append(collaborator.user)
            return render(request, "components/permissions_box_content.html", {'collaborators': users, 'language': language})

        except KeyError:
            json['msg'] = translate(
                'problem_deleting_old_licenses', language)

    return JsonResponse(json, status=status.HTTP_201_CREATED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def delete_client_permissions(request):
    language = getLanguage(request)
    automation_name = request.POST.get('automation_name', '')
    json = {'status': 400, 'msg': translate('automation_not_found', language)}
    client = get_client_from_request(request)
    allowed_automations = Automation.get_automations_with_ui(language, client)
    automation_name_is_allowed = check_if_automation_name_is_in_query(
        automation_name=automation_name, query=allowed_automations)

    if automation_name_is_allowed:
        try:
            user_id = request.POST.get('user_id', 0)
            if int(user_id) == 0:
                UsersPlans.objects.filter(
                    client=client, automation__name=automation_name).delete()
                UsersPlans.resetUsersPlansByClientAndAutomationsIds(client)
                json = {'status': 200, 'msg': translate(
                    'licenses_reset_successfully', language)}
            else:
                UsersPlans.objects.filter(
                    user__id=user_id, automation__name=automation_name).delete()
                collaborators = UsersPlans.objects.filter(
                    client=client, automation__name=automation_name).select_related('user')
                users = []
                for collaborator in collaborators:
                    users.append(collaborator.user)
                UsersPlans.resetUsersPlansByClientAndAutomationsIds(client)
                return render(request, "components/permissions_box_content.html", {'collaborators': users, 'language': language})
        except IntegrityError:
            json['msg'] = translate(
                'problem_deleting_old_licenses', language)
    return JsonResponse(json, status=status.HTTP_201_CREATED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET", "POST"])
def cancel_automation(request, schedule_id):
    return stop_automation(request, schedule_id)


@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def start_automation(request, schedule_id):
    language = getLanguage(request)
    json = {'status': 400, 'msg': translate(
        'unable_to_start_execution_please_try_again', language)}
    try:
        response = start_schedule(schedule_id)
        if not response.get('success', None):
            return JsonResponse(json, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))

        json = {'status': 200, 'msg': translate('execution_started', language)}
        return JsonResponse(json, status=response.get('status', status.HTTP_200_OK))
    except KeyError:
        return JsonResponse(json, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def stop_automation(request, schedule_id):
    language = getLanguage(request)
    json = {'status': 400, 'msg': translate(
        'unable_to_cancel_execution_please_try_again', language)}

    try:
        response = stop_schedule(schedule_id=schedule_id)
        if not response.get('success', None):
            return JsonResponse(json, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))
        json = {'status': 200, 'msg': translate(
            'execution_canceled', language)}
        return JsonResponse(json, status=response.get('status', status.HTTP_200_OK))
    except KeyError:
        return JsonResponse(json, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# tj options
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET", "POST"])
def update_settings(request):
    # TODO: Form validation on server side

    def encrypt(login, password, email_to_send_results):
        key = get_random_bytes(16)
        # TODO: Read from app configuration
        # I think that the best way to implement this is use a table with apps configuration
        binary_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCqjGVQ8Gga6LeZHgMSUTzqypRQtgXKzIO4aIlQi+Bxoe1LkOaEag7IAJM1bj8KrEFWB7wwigL95sOMqnZWzDPssx2vQLQxvuVUvgBiP1wJ33q91qZ0T8sQUMA7NCiUbJI8AGDCCq3Ewn2mszKvh5BFvEiIjGhZ81CMX6Nf5b4WRjgVy2Tcagskee8zA7ftsfxuJsbGA3hzN1hvVm/xm1+GN+Jafsyn+gLg8t8r02kALPT3libzdl61cmBFFdeJeVRYzoMsSAEhQsjvYJeEwpgfaAwSAHB2SkIZfG0Gpk/SYigNAOoU8QRFrJxhSBXc8aQLLAu+ZQCMeSTg63A5eDvqyjhe1LN4QkOrEUEhXnJiSKaATtW6Xt83lYzn09TkXqqrexwo0WXb873X/8L84spiSRuAC6G6a9z8zbZbVYpgkp/BHQG+XRcvqUfXJ8l96Nt8KatrdRrfOjezuMeWU66xFGlFTiwpJTBJM9EgtQ0XsDbloSxC2+3sbOSfOxcS1fs= Rafael@DESKTOP-NPATGGP"

        s_login = aes_urlsafe_encrypt(login, key)
        s_password = aes_urlsafe_encrypt(password, key)
        s_email_to_send_results = aes_urlsafe_encrypt(
            email_to_send_results, key)
        s_key = rsa_urlsafe_encrypt(key, binary_public_key)

        return {
            'login': s_login,
            'password': s_password,
            'email_to_send_results': s_email_to_send_results,
            'encrypted_key': s_key,
        }

    def save_settings_to_db(user, login, password, email_to_send_results, encrypted_key):
        try:
            settings = Settings.objects.get(user=user)
            settings.login = login
            settings.password = password
            settings.email_to_send_results = email_to_send_results
            settings.encrypted_key = encrypted_key
            settings.save()
        except Settings.DoesNotExist:
            settings = Settings(
                user=user,
                login=login,
                password=password,
                email_to_send_results=email_to_send_results,
                encrypted_key=encrypted_key,
            )
            settings.save()

    context = None
    template = 'tribunal_justica/index.html'

    if request.method == 'POST':

        try:
            user = request.user
            login = request.POST.get('login', "")
            password = request.POST.get('password', "")
            email_to_send_results = request.POST.get('email', "")

            secret = encrypt(login=login, password=password,
                             email_to_send_results=email_to_send_results)

            save_settings_to_db(
                user=user,
                login=secret['login'],
                password=secret['password'],
                email_to_send_results=secret['email_to_send_results'],
                encrypted_key=secret['encrypted_key'],
            )
            context = {
                'success': 'Settings saved with success'
            }

        except ValueError:
            context = {
                'error': 'Invalid settings, try again'
            }

    return render(request, template, context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def save_single_service_to_database(request):
    language = getLanguage(request)

    data = {}
    all_showcase = {}

    converted_request_body = JSON.loads(request.body)
    service_to_add = converted_request_body.get('service')
    number_of_permissions_to_add = converted_request_body.get('quantity')
    automation_obj = get_automation_by_name(service_to_add)

    if automation_obj.get_is_showcase() and service_to_add not in all_showcase:
        all_showcase[service_to_add] = number_of_permissions_to_add
    elif service_to_add in all_showcase:
        all_showcase[service_to_add] += number_of_permissions_to_add

    client_plan = getUserPlan(request)
    client_is_in_trial = 'trial' in client_plan.get_plan_name().lower()

    if client_is_in_trial:
        client_can_add_service = True
    else:
        client_can_add_service = check_client_available_licenses(
            request.user.profile.client) > 0

    if (client_can_add_service):
        client = get_client_from_request(request)
        try:
            service_to_add_licenses = AutomationsClients.objects.get(
                client=client, automation=automation_obj)
            service_to_add_licenses.qnt_automations += number_of_permissions_to_add or 1
            service_to_add_licenses.save()
            AutomationsClients.resetAutomationsClientsByClient(client)

            if bool(all_showcase):
                email_context = {
                    'language': language,
                    'user': request.user,
                    'all_showcase': all_showcase,
                }

                sendEmail('showcaseRequest', '[Adicionando Licença] Solicitação de Automação Vitrine' + ' Smarthis Hub',
                          get_people_to_send_email('product'), email_context)
            return JsonResponse(data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            if service_to_add == 'extrato-bancario':
                new_service = AutomationsClients.objects.create(
                    client=client, automation=automation_obj, qnt_automations=number_of_permissions_to_add or 1, can_create_model=3)
                new_service.save()
            else:
                new_service = AutomationsClients.objects.create(
                    client=client, automation=automation_obj, qnt_automations=number_of_permissions_to_add or 1)
                new_service.save()
            AutomationsClients.resetAutomationsClientsByClient(client)

            return JsonResponse(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        data['error'] = translate('you_have_no_licenses_available', language)
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def interested_in_service_under_maintenance(request):

    language = getLanguage(request)
    data = {}

    converted_request_body = JSON.loads(request.body)
    automation = converted_request_body.get('automation')
    user = request.user
    automation_obj = {}

    try:
        automation_obj = get_automation_by_name(automation)
    except Exception as e:
        data['error'] = f"""{translate('requested_automation_does_not_exist', language)}. {translate(
            'please_try_again', language)}"""

        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    try:
        interested_obj = InterestedInServiceUnderMaintenance.objects.get(
            user=user, automation=automation_obj)
        interested_obj.delete()

        return JsonResponse(data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        interest = InterestedInServiceUnderMaintenance.objects.create(
            user=user, automation=automation_obj)
        interest.save()

        return JsonResponse(data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def check_upload_file(request):
    language = getLanguage(request)

    request_files_body = request.FILES
    request_post_body = request.POST
    file = request_files_body.get('file', None)
    automation = request_post_body.get('automation', None)
    if file:
        file_name = file.name
    else:
        file_name = None

    data = {
        'success': None,
        'payload': None
    }

    if not automation or automation.lower() == 'undefined':
        data['success'] = False
        data['payload'] = translate('file_was_not_received_error', language)
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    required_columns = get_automation_fields(
        automation_name=automation)

    if not required_columns:
        file_checking = check_if_file_is_correct(file=file, language=language)
        file_is_valid = file_checking.get('success', False)

        if not file_is_valid:
            data['success'] = False
            data['payload'] = file_is_valid.get('payload', None)
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

        data['success'] = True
        data['payload'] = 'Não existe validação para esta automação'
        return JsonResponse(data, status=status.HTTP_200_OK)
    if file and file_name:
        try:
            file_validation = file_validator.validate_file(file=file,
                                                           fields=required_columns, language=language)
            if file_validation.get('success', None):
                data['success'] = True
                return JsonResponse(data, status=status.HTTP_200_OK)
            else:
                data['success'] = False
                data['payload'] = file_validation.get('payload', None)

                return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            data['success'] = False
            data['payload'] = translate('unsupported_file', language)

            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('exception', e)
            data['success'] = False
            data['payload'] = translate(
                'there_was_problem_encrypting_your_file', language)
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data['success'] = False
        data['payload'] = translate('file_was_not_received_error', language)
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def api_hub(request):
    language = getLanguage(request)

    context = {
        'hidehole_navbar': 1,
        'language': language,
        'body_class': 'body_api',
    }

    return render(request, "hub_api/api_menu.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def api_hub_request_email(request):
    email_context = {
        'language': 'pt-BR',
        'user': request.user
    }

    sendEmail('apiAccessRequest', 'Solicitação Acesso API' + ' Smarthis Hub',
              get_people_to_send_email('product'), email_context)

    return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["PUT", "POST"])
def appointment(request):
    language = getLanguage(request)
    json_body = JSON.loads(request.body)
    try:
        recurrence = int(json_body.get('recurrence'))
        execution_date = datetime.strptime(
            json_body.get('executionDate'), '%Y-%m-%d')
        schedule_id = int(json_body.get('id'))
    except Exception as e:
        return JsonResponse({'status': 400, 'msg': translate(
            'incomplete_data', language)}, status=status.HTTP_400_BAD_REQUEST)
    finally:
        client = get_client_from_request(request)
        schedule = get_template_by_id(schedule_id, request.user.id, client)
        if schedule:
            old_cron_expression = schedule.get_cron_expression()

            new_cron_expression = translate_schedule_appointment_into_cron_expression(
                execution_date, recurrence)
            schedule.set_execution_date(execution_date)
            schedule.set_cron_expression(new_cron_expression)

            if old_cron_expression and old_cron_expression != '':
                response = edit_appointment_on_backend(schedule)
            else:
                response = create_appointment_on_backend(schedule)

            if response.get('success', None):
                try:
                    schedule.save()
                    email_infos = get_appointment_email_infos(
                        language, execution_date, recurrence)
                    email_context = {
                        'language': language,
                        'user': request.user,
                        'schedule': schedule,
                        'automation_name': schedule.automation.name,
                        'date_text': email_infos['date_text_with_week'],
                        'recurrence_small_text': email_infos['recurrence_small_text'],
                        'execution_text': email_infos['execution_text']
                    }
                    sendEmail('sendAppointment', translate('template_schedule', language),
                              [request.user.email], email_context)

                    product_language = 'pt-BR'
                    if language != 'pt-BR':
                        email_context['language'] = product_language
                        email_infos = get_appointment_email_infos(
                            product_language, execution_date, recurrence)
                        email_context['date_text'] = email_infos['date_text_with_week']
                        email_context['recurrence_small_text'] = email_infos['recurrence_small_text']
                        email_context['execution_text'] = email_infos['execution_text']

                    sendEmail('sendAppointment', translate('template_schedule', product_language),
                              get_people_to_send_email('product'), email_context)

                    automation_type = schedule.automation.type
                    standard_variables = getStandardVariables(
                        schedule.automation.name, language)
                    return render(request, "components/box_automation.html", {'schedule': schedule, 'automation_description': standard_variables['title'], 'automation_type': automation_type, 'language': language, 'is_automation_active': True, 'schedule_automation_name': schedule.automation.name, 'email_was_verified': request.email_was_verified})
                except ValidationError:
                    return JsonResponse({'status': 402, 'msg': translate('template_not_found', language)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'status': 403, 'msg': translate('unable_to_start_scheduling', language)}, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))
        else:
            return JsonResponse({'status': 401, 'msg': translate('template_not_found', language)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["DELETE"])
def delete_appointment(request, id):
    language = getLanguage(request)
    client = get_client_from_request(request)
    schedule = get_template_by_id(id, request.user.id, client)
    if schedule:
        response = delete_appointment_on_backend(schedule.id)
        if response.get('success', None):
            schedule.set_cron_expression(None)
            schedule.set_execution_date(None)
            try:
                schedule.save()
                automation_type = schedule.automation.type
                standard_variables = getStandardVariables(
                    schedule.automation.name, language)
                return render(request, "components/box_automation.html", {'schedule': schedule, 'automation_description': standard_variables['title'], 'automation_type': automation_type, 'language': language, 'is_automation_active': True, 'schedule_automation_name': schedule.automation.name, 'email_was_verified': request.email_was_verified})
            except Exception as e:
                return JsonResponse({'status': 401, 'msg': translate('unable_to_remove_appointment', language)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'status': 402, 'msg': translate('unable_to_remove_appointment', language)}, status=response.get('status', status.HTTP_500_INTERNAL_SERVER_ERROR))
    else:
        return JsonResponse({'status': 400, 'msg': translate('incomplete_data', language)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def request_modal_creation(request, automation_name):

    try:
        client = get_client_from_request(request)
        can_create_model = AutomationsClients.objects.get(
            client=client, automation__name=automation_name)

        if can_create_model.get_can_create_model() == 3:
            email_context = {
                'language': 'pt-BR',
                'user': request.user
            }
            sendEmail('requestModalCreation', '[Extrato Bancário] Solicitação de configuração de modelo' + ' Smarthis Hub',
                      get_people_to_send_email('product'), email_context)
            can_create_model.can_create_model = 2
            can_create_model.save()
            return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({}, status.HTTP_204_NO_CONTENT)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET"])
def get_dashboard_automations_info(request):

    language = getLanguage(request)
    client_id = request.user.profile.client.id
    start_date = int(datetime.strptime('2020-01-01', '%Y-%m-%d').timestamp())
    end_date = int(datetime.today().timestamp())

    tasks = read_automation(client_id=client_id,
                            start_date=start_date, end_date=end_date)

    infos = tasks['data']['tasks']

    all_services = set()
    all_model = set()
    all_status = set()

    for value in infos.values():
        for v in value:
            service = v.get('automation_name', None)
            model = v.get('schedule_name', None)
            status = v.get('task_status', None)

            if service:
                all_services.add(service)
            if model:
                all_model.add(model)
            if status:
                all_status.add(status)

    all_services = list(all_services)
    all_model = list(all_model)
    all_status = list(all_status)

    all_filters = {
        'services': {
            'title': 'Serviços',
            'inputs': all_services,
        },
        'model': {
            'title': 'Modelos',
            'inputs': all_model,
        },
        'status': {
            'title': translate('status', language),
            'inputs': all_status,
        },
    }

    context = {
        'hidehole_navbar': 1,
        'language': language,
        'body_class': 'body_dash-automation',
        'all_filters': all_filters,
        'client_id': client_id,
        'tasks': tasks
    }

    return render(request, "dashboard_automation/dash_content.html", context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def check_running_model_state(request):
    request_body = JSON.loads(request.body)
    new_state = request_body.get('state', False)
    message = request_body.get('message', '')
    model_id = request_body.get('model_id', '')

    if not model_id:
        return HttpResponse(status.HTTP_400_BAD_REQUEST)

    channel_layer = get_channel_layer()

    try:
        model = Schedule.objects.get(pk=model_id)
        model_owner_id = model.user.id
        this_client_admins = list(Profile.objects.filter(
            client=model.client).filter(Q(role=3) | Q(role=4)))
        this_client_admins_ids = [
            profile.user.id for profile in this_client_admins]

        groups = [
            model_owner_id] + this_client_admins_ids

        async_to_sync(send_message_to_groups)(groups, channel_layer, {
            "type": "model.update",
            "model_id": model_id,
            "state": new_state,
            "message": message,
        })

    except Exception:
        return HttpResponse(status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status.HTTP_200_OK)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET"])
def get_executions_monitoring_info(request):
    client = get_client_from_request(request)
    if not client.identifier == "smarthis.com.br":
        return HttpResponseRedirect(reverse('services'))

    page = int(request.GET.get('page', 1))
    language = getLanguage(request)
    client_id = client.id
    start_skip = (page-1)*10
    end_limit = page*10
    response = read_monitoring_dashboard_data(
        start_skip=start_skip, end_limit=end_limit)
    tasks = response.get('data', [])

    headings = [
        'Cliente',
        'Automação',
        'Modelo',
        'Horário Agendado',
        'Rodou?',
        'Horário de Execucao',
        '% de sucesso',
        '% business exception',
        '% application exception',
    ]

    context = {
        'language': language,
        'client_id': client_id,
        'tasks': tasks,
        'is_first_page': page == 1,
        'page': page,
        'headings': headings
    }

    return render(request, "monitoring_dashboard/monitoring_dashboard.html", context)
