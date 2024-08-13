from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import reverse
from rest_framework import status
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings

from .serializers import JobSerializer
from .models import Job, Context, UiPathProcessesSchedules
from dashboard.templatetags.dashboard_tags import getLanguage, get_dashboard_infos

from datetime import datetime, timedelta


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uipath_logs(request):
    try:
        date_to = datetime.strptime(request.GET['date_to'], '%Y-%m-%d')
    except KeyError:
        date_to = datetime.today().date()
    try:
        date_from = datetime.strptime(request.GET['date_from'], '%Y-%m-%d')
    except KeyError:
        date_from = date_to - timedelta(days=90)
    data = {}

    try:
        json = Job.get_json_from_db(
            date_from, date_to, request.user.profile.client)
        data = json
        data['totalhours_rpa'] = int(json['totalhours_rpa'])
        language = getLanguage(request)
        data['update_infos'] = get_dashboard_infos(
            request, date_to, date_from, language)
    except Exception as e:
        print('error', e, e.__traceback__.tb_lineno)

    return Response(data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uipath_logs_calendar(request):
    try:
        date_to = datetime.strptime(request.GET['date_to'], '%Y-%m-%d')
    except KeyError:
        date_to = datetime.today().date()
    try:
        date_from = datetime.strptime(request.GET['date_from'], '%Y-%m-%d')
    except KeyError:
        date_from = date_to - timedelta(days=90)
    language = getLanguage(request)
    data = Job.get_calendar_json_from_db(
        request.user.profile.client, date_from, date_to, language)
    data = {'status': 200, 'processes_by_day': data}
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_future_uipath_logs_calendar(request):
    try:
        date_to = datetime.strptime(request.GET['date_to'], '%Y-%m-%d')
    except KeyError:
        date_to = datetime.today().date()
    try:
        date_from = datetime.strptime(request.GET['date_from'], '%Y-%m-%d')
    except KeyError:
        date_from = date_to - timedelta(days=90)
    data = UiPathProcessesSchedules.get_processes_scheduled_by_context(
        request.user.profile.client, date_from, date_to)
    data = {'status': 200, 'processes_by_day': data}
    return JsonResponse(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_uipath_jobs_log(request):
    # insert a new record for a job log
    if request.method == 'POST':
        # read data from request
        try:
            context = request.data['@odata.context']
            count = request.data['@odata.count']
            raw_data = request.data['value']
        except KeyError:
            return Response({
                'error': 'Body is not matching odata pattern.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # guard valid count
        check_count_valid = (count == len(raw_data))
        if not check_count_valid:
            return Response({
                'error': 'Integrity error. OData count is not matching.'
            },
                status=status.HTTP_400_BAD_REQUEST)

        # guard valid odata context
        try:
            context = Context.objects.get(context=context)
        except Exception:
            return Response({
                'error': 'Log context must be registered before push data.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # serialize input
        data = []
        for entrie in raw_data:
            entrie['Context'] = context.id
            data.append(entrie)

        serializer = JobSerializer(data=data, many=True)

        # guard valid serialized data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # save
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_post_uipath_jobs_log(request):
    if settings.IS_LOCALHOST or settings.IS_DEV:
        from uipath_logs.tasks import sync_uipath_logs
        sync_uipath_logs()
        return Response({}, status=status.HTTP_201_CREATED)
    else:
        return HttpResponseRedirect(reverse('onboarding'))
