from django.contrib.auth import views as auth_views

from django.urls import path

from subscriptions.views import password_reset_request
from .views import dashboard, dashboard_powerbi_detail, delete_process, get_uipath_api_monitoring_info, new_area, post_process, remove_area, get_settings_tab, get_manage_areas, get_manage_process, edit_area, invite_group


urlpatterns = [
    path('analytics', dashboard, name="dashboard"),
    path('areas', get_manage_areas, name="areas"),
    path('process', get_manage_process, name="process"),
    path('dashboard_view/<int:dashboard_id>',
         dashboard_powerbi_detail, name="powerbi_detail"),
    path('new/area', new_area, name="new_area"),
    path('remove/area/<int:area_id>', remove_area, name="remove_area"),
    path('edit/area/<int:area_id>', edit_area, name="edit_area"),
    path('post/process/<int:process_id>', post_process, name="post_process"),
    path('process/<int:process_id>',
         delete_process, name="post_process"),
    path('get/settings/tab', get_settings_tab, name="get_settings_tab"),
    path('dashboard/post/invite-group', invite_group, name='invite_group'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('setcookie', setcookie, name='setcookie'),
    # path('getcookie', getcookie, name='getcookie'),

    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/html_password_reset_email.html'), name='password_reset'),
    path('accounts/password_reset/request',
         password_reset_request, name='password_reset_request'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('monitor/uipath-api',
         get_uipath_api_monitoring_info, name='uipath_api_monitoring_info'),
]
