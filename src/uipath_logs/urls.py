from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^api/v1/post_uipath_jobs_log/$',
        views.post_uipath_jobs_log, name='post_uipath_jobs_log'),
    url(r'^api/v1/get_uipath_logs/$',
        views.get_uipath_logs, name='get_uipath_logs'),
    url(r'^api/v1/get/uipathlogs/calendar/future',
        views.get_future_uipath_logs_calendar, name='get_future_uipath_logs_calendar'),
    url(r'^api/v1/get/uipathlogs/calendar',
        views.get_uipath_logs_calendar, name='get_uipath_logs_calendar'),
    url(r'^api/v1/teste/post_uipath_jobs_log/$',
        views.test_post_uipath_jobs_log, name='test_post_uipath_jobs_log'),
]
