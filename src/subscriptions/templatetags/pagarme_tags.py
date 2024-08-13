# from pagarmecoreapi.pagarmecoreapi_client import PagarmecoreapiClient
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from requests.api import request

from subscriptions.models import PagarmePlans, PagarmeSubscriptions, Subscription
from portal.templatetags.general_tags import translate

import requests
import urllib.request as ur
import json
from datetime import datetime


def getPagarmeTest():
    test_pagarme = False
    if settings.IS_LOCALHOST or settings.IS_DEV:
        test_pagarme = True
    return test_pagarme


def getPagarmeAPIKey(test):
    if test:
        api_key = settings.PAGARME_TEST_API_KEY
    else:
        api_key = settings.PAGARME_API_KEY

    return api_key


def getPagarmeSecretKey(test):
    if test:
        secret_key = settings.PAGARME_TEST_SECRET_KEY
    else:
        secret_key = settings.PAGARME_SECRET_KEY

    return secret_key


def setPagarmeData(test=True, controller_type='', payload={}, request_type='POST', controller_id=0):
    headers = {'content-type': 'application/json'}
    payload['api_key'] = getPagarmeAPIKey(test)

    pagarme_controllers = {
        'plans': 'plans',
        'subscriptions': 'subscriptions'
    }
    if settings.PAGARME_API_VERSION != 'v5':
        url = f"https://api.pagar.me/1/{pagarme_controllers[controller_type]}"
        if int(controller_id) > 0:
            url += f'/{str(controller_id)}'

        if request_type == 'PUT':
            response = requests.put(
                url, data=json.dumps(payload), headers=headers)
        else:
            response = requests.post(
                url, data=json.dumps(payload), headers=headers)

        if 'errors' in response.text:
            resp_json = json.loads(response.text)
            print(resp_json['errors'][0]['message'])
            return resp_json

        return json.loads(response.text)
    else:
        return {'error': 'Version wrong'}


def getPagarmePlan(test, payload):
    try:
        return PagarmePlans.objects.get(
            plan_pagarme_name=payload['name'], amount=payload['amount'], is_test=test, api_version=settings.PAGARME_API_VERSION)
    except ObjectDoesNotExist:
        pagarme_plan = setPagarmePlan(test, payload)
        if pagarme_plan['status'] == 200:
            return PagarmePlans.objects.get(plan_pagarme_id=pagarme_plan['id'], is_test=test, api_version=settings.PAGARME_API_VERSION)
        else:
            return pagarme_plan


def setPagarmePlan(test, payload):
    response = {'status': 200, 'msg': 'Plano criado com Sucesso', 'id': 0}
    json_pagarme = setPagarmeData(test, 'plans', payload)
    if 'errors' in json_pagarme:
        # TODO: erro de comunicação na pagarme, tente novamente, falta algum dado
        response = {'status': 400, 'msg': json_pagarme['errors']['message']}
    else:
        try:
            PagarmePlans.objects.create(
                plan_pagarme_id=json_pagarme['id'], amount=json_pagarme['amount'], plan_pagarme_name=json_pagarme['name'], is_test=test, api_version=settings.PAGARME_API_VERSION)
            response['id'] = json_pagarme['id']
        except Exception as e:
            response = {'status': 401, 'msg': str(
                e), 'obj_pagarme': json_pagarme}
    return response


def getPagarmeSubscription(test, client):
    try:
        return PagarmeSubscriptions.objects.get(
            client=client, is_test=test)
    except ObjectDoesNotExist:
        return {'status': 400, 'msg': 'Object not found'}


def setPagarmeSubscription(test, client, payload, language):
    response = {'status': 200, 'msg': 'Assinatura criada com Sucesso', 'id': 0}
    request_type = 'POST'

    json_pagarme = setPagarmeData(
        test, 'subscriptions', payload, request_type)
    print(json_pagarme)
    if 'errors' in json_pagarme:
        response = getPagarmeErrorJson(json_pagarme, language)
    else:
        # waiting_payment
        response = insertIntoPagarmeSubscription(
            test, client, payload['plan_id'], payload['payment_method'], json_pagarme, response)

    return response


def updatePagarmeSubscription(test, pagarme_subscription, payload, language):
    response = {'status': 200,
                'msg': 'Assinatura atualizada com Sucesso', 'id': 0}
    request_type = 'PUT'
    json_pagarme = setPagarmeData(
        test, 'subscriptions', payload, request_type, pagarme_subscription.get_pagarme_subscription_id())
    if 'errors' in json_pagarme:
        response = getPagarmeErrorJson(json_pagarme, language)
    else:
        pagarme_subscription.set_pagarme_subscription_plan_id(
            payload['plan_id'])

        json_period = getSubscriptionPeriodFromJson(json_pagarme)
        pagarme_subscription.set_current_period_start(
            json_period['start'])
        pagarme_subscription.set_current_period_end(
            json_period['end'])

        payment_method = 'credit_card'
        if 'payment_method' not in payload:
            payment_method = 'boleto'
        else:
            payment_method = payload['payment_method']
        pagarme_subscription.set_payment_type(payment_method)

        try:
            pagarme_subscription.save()
            response['id'] = json_pagarme['id']
            response = updateSubscriptionInfos(
                response, pagarme_subscription.client, json_pagarme, json_period)
        except Exception as e:
            print(
                f'error saving new plan subscription {str(pagarme_subscription.get_pagarme_subscription_id())}')
            response = {'status': 401, 'msg': str(
                e), 'id': pagarme_subscription.get_pagarme_subscription_id()}

    return response


def cancelPagarmeSubscription(id):
    response = {'status': 400}
    try:
        pagarme_subscription = PagarmeSubscriptions.objects.get(
            subscription_pagarme_id=id)
        try:
            subscription = Subscription.objects.get(
                client=pagarme_subscription.client)
            subscription.set_active(False)
            try:
                subscription.save()
                response = {'status': 200,
                            'msg': 'Subscription not active anymore'}
            except:
                response['msg'] = 'Error Saving subscription'

        except ObjectDoesNotExist:
            print('Subscription not found')
            response['msg'] = 'Subscription not found'
    except ObjectDoesNotExist:
        print('PagarmeSubscriptions not found')
        response['msg'] = 'PagarmeSubscriptions not found'
    finally:
        return response


def insertIntoPagarmeSubscription(test, client, plan_id, payment_type, json_pagarme, response):
    try:
        json_period = getSubscriptionPeriodFromJson(json_pagarme)
        PagarmeSubscriptions.objects.create(
            client=client, subscription_pagarme_id=json_pagarme['id'], plan_pagarme_id=plan_id, is_test=test, api_version=settings.PAGARME_API_VERSION, current_period_start=json_period['start'], current_period_end=json_period['end'], payment_type=payment_type)
        response['id'] = json_pagarme['id']
        response = updateSubscriptionInfos(
            response, client, json_pagarme, json_period)
    except Exception as e:
        response = {'status': 402, 'msg': str(
            e), 'obj_pagarme': json_pagarme}

    return response


def getSubscriptionPeriodFromJson(json_pagarme):
    current_period_start = None
    current_period_end = None
    if json_pagarme['current_period_start'] != None:
        current_period_start = datetime.strptime(
            json_pagarme['current_period_start'], '%Y-%m-%dT%H:%M:%S.%fZ')
        current_period_end = datetime.strptime(
            json_pagarme['current_period_end'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return {'end': current_period_end, 'start': current_period_start}


def updateSubscriptionInfos(response, client, json_pagarme, json_period):
    if json_pagarme['payment_method'] == 'boleto':
        json_period['end'] = datetime.strptime(
            json_pagarme['current_transaction']['boleto_expiration_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
    return Subscription.updateSubscriptionAfterPayment(response, client, json_period['start'],
                                                       json_period['end'], json_pagarme['current_transaction']['status'])


def calculatePagarmeSubscriptionUpdate(request, pagarme_subscription, plan_days):
    necessary_infos = {}
    subscription = request.subscription
    necessary_infos['plan_value_by_day'] = subscription.get_value() / \
        int(plan_days)
    today = datetime.today().date()
    necessary_infos['used_days'] = (
        today - pagarme_subscription.created_at).days

    return necessary_infos


def getPagarmeErrorJson(json_pagarme, language):
    msg = json_pagarme['errors'][0]['message']
    if json_pagarme['errors'][0]['type'] == 'invalid_parameter' and json_pagarme['errors'][0]['parameter_name'] == 'card_hash':
        msg = translate(
            'invalid_credit_card_are_you_sure_typed_it_correctly', language)
    return {'status': 400, 'msg': msg}
