import pytz
from portal.functions import get_client_from_request
from portal.templatetags.general_tags import translate
from .templatetags.dashboard_tags import reset_jobs_cache, get_dashboard_infos, getLanguage, getAllDashboardSelectOptions, getRoleDashboardAccess, isClientMainUser
import json
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime,  timedelta, time
from subscriptions.models import Profile
from django.http.response import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import HttpResponseForbidden, Http404, JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, reverse
from django.contrib.gis.geoip2 import GeoIP2
from my_solutions.templatetags.mysolutions_tags import getRequestInfos
from django.core.paginator import Paginator

from .models import Dashboard, DashboardSessionInfo
from uipath_logs.models import Job, Areas, Processos, SubProcessos, UipathApiMonitoring

from decimal import Decimal


def dashboard(request):
    language = getLanguage(request)
    role_users_access = getRoleDashboardAccess()
    client_subscription = request.subscription
    if client_subscription.get_dashboard() and request.user.profile.role in role_users_access:
        date_to = datetime.today().date()
        if str(request.user.profile.client) == 'Elopar':
            date_from = datetime.strptime('2020-01-01', '%Y-%m-%d')
        else:
            date_from = date_to - timedelta(days=90)

        context = get_dashboard_infos(request, date_to, date_from, language)
        context['active_page'] = 'dashboard'
        if not context['not_translated']:
            context['all_processes_translated'] = True
        sincebegin_processes_registered = Job.listAllColumnsTypes(datetime.strptime(
            '2020-01-01', '%Y-%m-%d'), date_to, 'processes', 'ReleaseName', request.user.profile.client)
        context['sincebegin_processes_registered'] = {
            'title': translate('process', language),
            'inputs': sincebegin_processes_registered
        }
        context['allow_dashboard'] = True
        if request.user.profile.role == 6:
            context['view_type'] = 'view'
        else:
            context['view_type'] = 'editor'
        context['hide_warnings'] = True
        # g = GeoIP2()
        client_ip = request.META['REMOTE_ADDR']
        print(client_ip)
        # print(g.country(client_ip))
    else:
        context = {
            'allow_dashboard': False,
            'language': language,
            'active_page': 'dashboard',
        }
    context['all_select_options'] = getAllDashboardSelectOptions(language)

    context['free_trial_ended'] = request.free_trial_ended

    return render(request, "dashboard/index.html", context)

# @api_view(['POST'])


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_settings_tab(request):
    date_to = datetime.today().date()
    processes_translated = Processos.listAllColumnsTypes(
        request.user.profile.client)
    language = getLanguage(request)
    sincebegin_processes_registered = Job.listAllColumnsTypes(datetime.strptime(
        '2020-01-01', '%Y-%m-%d'), date_to, 'processes', 'ReleaseName', request.user.profile.client)
    context = {
        'processes_translated': processes_translated['dict'],
        'language': language,
        'sincebegin_processes_registered': {
            'title': translate('process', language),
            'inputs': sincebegin_processes_registered
        }
    }
    return render(request, "dashboard/manage_settings_tab.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_manage_areas(request):
    language = getLanguage(request)

    processes_in_areas = {}
    areas = Areas.listAllColumnsTypes(request.user.profile.client)
    for area in areas['areas']:
        processes_in_areas[area] = 0
    dict_processes = Processos.listAllColumnsTypes(request.user.profile.client)
    for process in dict_processes['dict']:
        desired_area = dict_processes['dict'][process]['area']

        if desired_area:
            processes_in_areas[desired_area] += 1

    processes_filter = {
        'title': translate('process', language),
        'areas': areas,
    }

    context = {
        'language': language,
        'active_page': 'dashboard',
        'processes_in_areas': processes_in_areas,
        'processes_filter': processes_filter,
    }

    return render(request, "dashboard/components/manage_areas_tab.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_manage_process(request):
    language = getLanguage(request)

    # If you change these two texts, also see processes filters, since they use the text content inside its logic
    filters = {
        translate('data_complete', language): None,
        translate('incomplete_data', language): None
    }

    processes_in_areas = {}

    areas = Areas.listAllColumnsTypes(request.user.profile.client)
    for area in areas['areas']:
        processes_in_areas[area] = 0
        filters[area] = None

    processes_translated = Processos.listAllColumnsTypes(
        request.user.profile.client)
    for process in processes_translated['dict']:
        desired_area = processes_translated['dict'][process]['area']
        if desired_area:
            processes_in_areas[processes_translated['dict']
                               [process]['area']] += 1

    processes_filter = {
        'title': translate('process', language),
        'areas': areas,
    }

    date_to = datetime.today().date()
    sincebegin_processes_registered = Job.listAllColumnsTypes(datetime.strptime(
        '2020-01-01', '%Y-%m-%d'), date_to, 'processes', 'ReleaseName', request.user.profile.client)
    processes_not_registered = []
    for process in sincebegin_processes_registered:
        if process not in processes_translated['subprocesses_registered']:
            processes_not_registered.append(
                SubProcessos.get_subprocess_infos_formated(process, 0))
    context = {
        'language': language,
        'active_page': 'dashboard',
        'processes_in_areas': processes_in_areas,
        'processes_filter': processes_filter,
        'processes_translated': processes_translated['dict'],
        'sincebegin_processes_registered': {
            'title': translate('process', language),
            'inputs': sincebegin_processes_registered
        },
        'processes_not_registered': processes_not_registered,
        'filters': filters,
        'is_admin': isClientMainUser(request.user)
    }

    return render(request, "dashboard/settings/manage_processes_tab.html", context)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def new_area(request):
    language = getLanguage(request)
    result = {'status': 'erro', 'msg': translate(
        'informations_came_empty', language)}

    try:
        area_name = request.data['area']
        customer = request.user.profile.client
        if customer is None:
            result['msg'] = result['msg'] = translate(
                'are_you_sure_this_is_your_account', language)
            return Response(result, status.HTTP_204_NO_CONTENT)
        p = Areas(area=area_name, customer=customer)
        p.save()
        id_area = p.id
        reset_jobs_cache(
            customer, request.data['date_from'], request.data['date_to'])
        result = {'status': 'sucesso', 'msg': translate(
            'department_saved_successfully', language), 'id': id_area}
        return Response(result, status.HTTP_201_CREATED)
    except KeyError:
        return Response(result, status.HTTP_204_NO_CONTENT)
    except Exception as e:
        result['msg'] = translate('unable_to_save_department', language)
        return Response(result, status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def remove_area(request, area_id):
    language = getLanguage(request)
    result = {'status': 'erro', 'msg': translate(
        'informations_came_empty', language)}
    try:
        customer = request.user.profile.client
        a = Areas.objects.get(id=area_id)
        if customer is None:
            result['msg'] = translate(
                'are_you_sure_this_is_your_account', language)
            return Response(result, status.HTTP_204_NO_CONTENT)
        a = Areas.objects.filter(customer=customer, id=area_id)
        if len(a) > 0:
            a = a.first()
            a.delete()
            reset_jobs_cache(
                customer, request.data['date_from'], request.data['date_to'])
            result = {'status': 'sucesso', 'msg': translate(
                'department_removed_successfully', language)}
        else:
            result = {'status': 'erro', 'msg': translate(
                'department_not_found', language)}
        return Response(result, status.HTTP_201_CREATED)
    except KeyError:
        return Response(result, status.HTTP_204_NO_CONTENT)
    except Exception as e:
        result['msg'] = translate('unable_to_save_department', language)
        result['error'] = str(e)
        return Response(result, status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def edit_area(request, area_id):

    language = getLanguage(request)
    result = {'status': 'erro', 'msg': translate(
        'informations_came_empty', language)}
    infos = getRequestInfos(request, ['area'])
    try:

        customer = request.user.profile.client
        a = Areas.objects.get(customer=customer, id=area_id)
        if customer is None:
            result['msg'] = translate(
                'are_you_sure_this_is_your_account', language)
            return Response(result, status.HTTP_204_NO_CONTENT)
        a = Areas.objects.filter(customer=customer, id=area_id)
        if len(a) > 0:
            a = a.first()
            a.area = infos['area']
            a.save()
            reset_jobs_cache(
                customer, request.data['date_from'], request.data['date_to'])
            result = {'status': 'sucesso',
                      'msg': translate('successfully_edited_area', language), 'area': a.area, 'id': area_id}
        else:
            result = {'status': 'erro', 'msg': translate(
                'department_not_found', language)}
        return Response(result, status.HTTP_201_CREATED)
    except KeyError:
        return Response(result, status.HTTP_204_NO_CONTENT)
    except Exception as e:
        result['msg'] = translate('unable_to_save_department', language)
        result['error'] = str(e)
        return Response(result, status.HTTP_204_NO_CONTENT)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def post_process(request, process_id):
    language = getLanguage(request)
    client = get_client_from_request(request)
    data = {}

    converted_request_body = json.loads(request.body)

    process_name = converted_request_body.get('process_name', None)

    area_id = int(converted_request_body.get('area', 0))

    quantity_of_monthly_tasks = int(
        converted_request_body.get('quantity_of_monthly_tasks', 0))

    project_cost = Decimal(converted_request_body.get(
        'project_cost', 0))

    average_time_spent = float(converted_request_body.get(
        'average_time_spent', 0))

    average_hour_value = Decimal(converted_request_body.get(
        'average_hour_value', 0))

    subprocesses = converted_request_body.get(
        'subprocesses', [])

    date_from = converted_request_body.get('date_from', None)

    date_to = converted_request_body.get('date_to', None)

    try:
        if area_id:
            try:
                area_obj = Areas.objects.get(id=area_id)
            except Areas.DoesNotExist:
                area_obj = None
        else:
            area_obj = None

        old_subprocesses_list = []
        new_subprocesses_list = []
        if process_id > 0:
            try:
                process_to_be_edited = Processos.objects.get(id=process_id)
                process_to_be_edited.set_process(process_name)

                process_to_be_edited.set_area(area_obj)

                process_to_be_edited.set_project_cost(project_cost)

                process_to_be_edited.set_average_hour_value(average_hour_value)

                process_to_be_edited.set_quantity_of_monthly_tasks(
                    quantity_of_monthly_tasks)

                process_to_be_edited.set_duration_time(average_time_spent)
                try:
                    old_subprocesses = SubProcessos.objects.filter(
                        process=process_to_be_edited)
                    for old_subprocess in old_subprocesses:
                        if old_subprocess.ReleaseName in subprocesses:
                            old_subprocesses_list.append(
                                old_subprocess.ReleaseName)
                            subprocess_dict = SubProcessos.get_subprocess_infos_formated(
                                old_subprocess.ReleaseName, old_subprocess.id)
                            new_subprocesses_list.append(subprocess_dict)

                    if len(old_subprocesses_list) > 0:
                        old_subprocesses = old_subprocesses.exclude(
                            ReleaseName__in=old_subprocesses_list)
                    old_subprocesses.delete()

                except Exception as e:
                    print(str(e))

            except Processos.DoesNotExist:
                process_to_be_edited = Processos.objects.create(
                    process=process_name, name=process_name, duration_time=average_time_spent, area=area_obj, average_hour_value=average_hour_value, quantity_of_monthly_tasks=quantity_of_monthly_tasks, project_cost=project_cost, client=client)
        else:
            process_to_be_edited = Processos.objects.create(
                process=process_name, name=process_name, duration_time=average_time_spent, area=area_obj, average_hour_value=average_hour_value, quantity_of_monthly_tasks=quantity_of_monthly_tasks, project_cost=project_cost, client=client)

        process_to_be_edited.save()

        subprocesses_creation_list = []
        if len(subprocesses) > 0:
            for subprocess in subprocesses:
                if subprocess not in old_subprocesses_list:
                    subprocesses_creation_list.append(SubProcessos(
                        process=process_to_be_edited, ReleaseName=subprocess))
            if len(subprocesses_creation_list) > 0:
                SubProcessos.objects.bulk_create(subprocesses_creation_list)

            # getting subprocesses ids
            subprocesses_created = SubProcessos.objects.values(
                'id', 'ReleaseName').filter(process=process_to_be_edited)
            for subprocess in subprocesses_created:
                if subprocess['ReleaseName'] not in old_subprocesses_list:
                    subprocess_dict = SubProcessos.get_subprocess_infos_formated(
                        subprocess['ReleaseName'], subprocess['id'])
                    new_subprocesses_list.append(subprocess_dict)

        if date_from and date_to:
            reset_jobs_cache(
                client, date_from, date_to)

        process_formated = Processos.get_process_infos_formated(
            process_to_be_edited)
        process_formated['subprocesses'] = subprocesses_creation_list
        context = {
            'process': process_formated,
            'language': language,
            'subprocesses': new_subprocesses_list
        }
        return render(request, "dashboard/settings/single_process_registered.html", context, status=status.HTTP_200_OK)

    except Exception as e:
        print('error', e)
        data['error'] = f"""{translate(
            'there_was_a_problem_saving_your_process', language)} {translate("hub_contact_email", language)}"""
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def invite_group(request):
    language = getLanguage(request)
    invite_group = request.data['invite_group']
    deleted_group = request.data['deleted_group']

    all_invite_users_by_group = {'editor': [], 'leitor': [], 'admin': []}
    for user_id, edition_type in invite_group.items():
        all_invite_users_by_group[edition_type].append(user_id)

    errors = []
    try:
        if (len(all_invite_users_by_group['editor']) > 0):
            Profile.objects.filter(
                client=request.user.profile.client, user__id__in=all_invite_users_by_group['editor']).update(role=5)
    except Exception as e:
        errors.append(translate['editor'][language])

    try:
        if (len(all_invite_users_by_group['leitor']) > 0):
            Profile.objects.filter(
                client=request.user.profile.client, user__id__in=all_invite_users_by_group['leitor']).update(role=6)
    except Exception as e:
        errors.append(translate['can_view'][language])

    try:
        if (len(deleted_group) > 0):
            Profile.objects.filter(
                client=request.user.profile.client, user__id__in=deleted_group).update(role=1)
    except Exception as e:
        errors.append('deleted')

    if len(errors) == 0:
        return JsonResponse({'status': 200}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'status': 400, 'msg': translate['error_updating_users'][language] + ', '.join(errors)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tribunal_justica(request):
    context = {}
    return render(request, "dashboard/tribunal_justica.html", context)


def dashboard_powerbi_detail(request, dashboard_id):
    try:
        dashboard = Dashboard.objects.get(id=dashboard_id)
    except Dashboard.DoesNotExist:
        raise Http404("Dashboard does not exist")

    if dashboard.customer != request.user.profile.client:
        return HttpResponseForbidden()

    context = {'dashboard': dashboard}
    return render(request, "dashboard/powerbi.html", context)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def save_dashboard_infos(request):
    data = {}
    converted_request_body = json.loads(request.body)
    session_start = converted_request_body.get('session_start')
    session_end = converted_request_body.get('session_end')

    def get_duration(duration):
        hours = int(duration / 3600)
        minutes = int(duration % 3600 / 60)
        seconds = int((duration % 3600) % 60)
        return [hours, minutes, seconds]

    try:
        user_id = request.user.id
        converted_session_start = datetime.fromtimestamp(
            session_start/1000, tz=pytz.utc)
        converted_session_end = datetime.fromtimestamp(
            session_end/1000, tz=pytz.utc)
        if converted_session_end > converted_session_start:
            difference_between_dates = (
                converted_session_end - converted_session_start).total_seconds()

            session_duration = get_duration(difference_between_dates)

            converted_session_duration = time(
                session_duration[0], session_duration[1], session_duration[2])
            new_session_info_entry = DashboardSessionInfo.objects.create(
                user_id=user_id, session_start=converted_session_start, session_end=converted_session_end, session_duration=converted_session_duration)

            new_session_info_entry.save()

            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["DELETE"])
def delete_process(request, process_id):
    try:
        process = Processos.objects.get(pk=process_id)
        process.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    except Processos.DoesNotExist:
        return HttpResponseNotFound('Resource not found')
    except Exception as e:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET"])
def get_uipath_api_monitoring_info(request):
    client = get_client_from_request(request)
    if not client.identifier == "smarthis.com.br":
        return HttpResponseRedirect(reverse('services'))

    language = getLanguage(request)
    client_id = client.id

    infos = UipathApiMonitoring.objects.all().order_by('-updated_at')

    paginator = Paginator(infos, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    headings = [
        'Cliente',
        'Última Atualização',
        'Mensagem de Erro',
        'Código do Erro',
    ]

    context = {
        'language': language,
        'client_id': client_id,
        'page_number': page_number,
        'page_obj': page_obj,
        'headings': headings
    }

    return render(request, "dashboard/uipath_api_monitoring.html", context)
