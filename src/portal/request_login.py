from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from dashboard.templatetags.dashboard_tags import setLanguage
from django.conf import settings
from my_solutions.templatetags.mysolutions_tags import check_if_free_trial_ended, get_subscription
from subscriptions.models import Subscription
from subscriptions.templatetags.subscriptions_tags import check_if_client_has_not_finished_registering


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_anonymous and ('register' not in request.META.get('PATH_INFO', None) and 'account' not in request.META.get('PATH_INFO', None) and 'services/check/model/' not in request.META.get('PATH_INFO', None) and 'api/v1/post_uipath_jobs_log' not in request.META.get('PATH_INFO', None) and 'pagarme/feedback' not in request.META.get('PATH_INFO', None)):
            return HttpResponseRedirect(reverse('login'))  # or http response
        elif not request.user.is_anonymous:
            request.is_prod = not settings.IS_LOCALHOST and not settings.IS_DEV

            subscription = get_subscription(request)
            request.subscription = subscription

            user = request.user
            user_profile = user.profile

            subscription_is_active = subscription.get_active()
            if not subscription_is_active and 'register' not in request.META.get('PATH_INFO', None):
                client_has_not_finished_registering = check_if_client_has_not_finished_registering(
                    subscription=subscription)
                if client_has_not_finished_registering:
                    return HttpResponseRedirect(reverse('conclude_registry'))
                else:
                    return HttpResponseRedirect(reverse('login'))

            if isinstance(subscription, Subscription):
                plan = subscription.get_subscription_plan()
            else:
                plan = None
            if plan and 'free trial' in plan.get_plan_name().lower():
                free_trial_ended = check_if_free_trial_ended(subscription)

                request.free_trial_ended = True if free_trial_ended else False
            else:
                request.free_trial_ended = False

            email_was_verified = user_profile.get_email_confirmed()
            request.email_was_verified = True if email_was_verified else False

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # setting language
        key = request.GET.get('key', '')
        value = request.GET.get('value', '')
        if key != '' and value != '' and key == 'language':
            response_withcookie = setLanguage(request, response)
            return response_withcookie['response']

        return response
