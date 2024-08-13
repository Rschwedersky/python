from .views import chosen_plan_feedback, email_confirmation, email_confirmed_view, end_of_trial_choose_plan, end_of_trial_summary, help_center, generate_authetication_token, conclude_registry, save_chosen_plan, save_login_infos, send_email_confirmation, submit_registry, exclude_user, get_user_by_email_and_client, pay_subscription, edit_profile_user, faq_doubts, update_plan, pagarme_feedback, registration
from tabnanny import check
from django.urls import path

from dashboard.views import save_dashboard_infos

urlpatterns = [
    path('help-center', help_center, name='help_center'),
    path('help_center/faq_doubts', faq_doubts, name='faq_doubts'),
    path('iam/authenticate', generate_authetication_token),
    path('register', registration, name='registration'),
    path('register/<uuid:token>', registration, name='invite_collaborator'),
    path('register/conclude', conclude_registry, name='conclude_registry'),
    path('register/conclude/submit', submit_registry, name='submit_registry'),
    path('accounts/user/exclude', exclude_user, name='exclude_user'),
    path('accounts/user/edit_profile_user', edit_profile_user,
         name='edit_profile_user'),
    path('get/user', get_user_by_email_and_client,
         name='get_user_by_email_and_client'),
    path('metrics/login', save_login_infos, name='save_login_infos'),
    path('metrics/dashboard', save_dashboard_infos, name='save_dashboard_infos'),
    path('trial/summary', end_of_trial_summary, name='end_of_trial_summary'),
    path('trial/choose-plan/conclude', save_chosen_plan,
         name='save_chosen_plan'),
    path('trial/choose-plan/feedback', chosen_plan_feedback,
         name='chosen_plan_feedback'),
    path('trial/choose-plan/<str:desired_plan>', end_of_trial_choose_plan,
         name='end_of_trial_choose_plan'),
    path('trial/choose-plan/<str:desired_plan>/<str:period>', end_of_trial_choose_plan,
         name='end_of_trial_choose_plan'),
    path('pay/subscription', pay_subscription,
         name='pay_subscription'),
    path('pagarme/feedback', pagarme_feedback,
         name='pagarme_feedback'),
    path('update/plan/<str:desired_plan>/<str:period>', update_plan,
         name='update_plan'),
    path('update/plan/<str:desired_plan>/<str:period>/<str:plus>', update_plan,
         name='update_plan'),
    path('accounts/email-confirmation/<uidb64>/<token>',
         email_confirmation, name='email_confirmation'),
    path('accounts/send-email-confirmation',
         send_email_confirmation, name='send_email_confirmation'),
    path('email-confirmed',
         email_confirmed_view, name='email_confirmed_view'),

]
