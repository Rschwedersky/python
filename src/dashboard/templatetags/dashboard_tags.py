from collections import defaultdict
from operator import not_
from django import template
from django.conf import settings
import logging
import boto3
from botocore.exceptions import ClientError
import unicodedata
import os
import uuid
import json
import re
from copy import deepcopy
from subscriptions.models import Client, Profile
from smt_orchestrator.models import Automation

import uipath_logs.models
from portal.functions import reset_cache
from portal.templatetags.general_tags import translate
from datetime import datetime, timedelta
from random import randint, uniform
from django.core.cache import cache


register = template.Library()


@register.filter
def remove_special_characters(string):
    return ''.join(e for e in string if e.isalnum())


@register.filter
def multiply(number_1, number_2):
    return number_1 * number_2


@register.filter
def multiply_int_result(number_1, number_2):
    return int(number_1 * number_2)


@register.filter
def get_new_id(service):
    service_without_spaces = service.replace(" ", "")
    random_identifier = uuid.uuid4()
    random_id = service_without_spaces + str(random_identifier)
    return random_id


@register.filter
def get_obj_attr(obj, attr):
    return obj[attr]


@register.filter
def exists_in_obj(attr, obj):
    return attr in obj


@register.filter
def comparing_variables(val1, val2):
    return val1 == val2


@register.filter
def subtract(n1, n2):
    return n1 - n2


@register.filter
def get_name_initials(full_name):
    number_of_words = len(full_name.split())
    if number_of_words == 0:
        return ''
    elif number_of_words == 1:
        initials = full_name[:2]
    else:
        first_name = full_name.split()[0]
        last_name = full_name.split()[-1]
        name_initial = first_name[0]
        last_name_initial = last_name[0]
        initials = name_initial + last_name_initial

    return initials.upper()


def s3_remove_file(bucket_name, file_name):
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        return True
    except Exception as e:
        return False


@register.filter
def s3_presigned_url(bucket_name, object_name, action='get_object', contentType=None, expiration=600):
    params = {'Bucket': bucket_name, 'Key': object_name}
    if contentType != None:
        params['ContentType'] = contentType

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    try:
        response = s3_client.generate_presigned_url(
            action,
            Params=params,
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


@register.filter
def get_s3_presigned_url_upload(infos, request, uniqid=0):
    try:
        oldfilename, file_extension = os.path.splitext(infos['filename'])
        oldfilename = re.sub('[^A-Za-z0-9]+', '-', oldfilename)

        complement_filename = uniqid
        if complement_filename == 0:
            complement_filename = str(uuid.uuid4())

        filename = f'{oldfilename}-{complement_filename}{file_extension}'
        contentType = infos['contentType']
        folder = infos['folder']
        subfolder = infos['subfolder']

        s3path = f"{folder}/{str(request.user.profile.client.id)}/{subfolder}/{filename}"
        presigned_url = s3_presigned_url(
            settings.AWS_STORAGE_BUCKET_NAME, s3path, 'put_object', contentType)

        result = {
            'method': 'PUT',
            'url': presigned_url,
            'fields': [],
            'headers': {
                'content-type': contentType
            },
            'status': 200
        }
        return result
    except KeyboardInterrupt:
        return {}


@register.filter
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


@register.filter
def get_automation_by_name(automation):
    automation_obj = Automation.objects.filter(name=automation)
    if len(automation_obj) == 0:
        automation_obj = Automation.objects.create(
            name=automation)
        automation_obj.save()
    else:
        automation_obj = automation_obj[0]
    return automation_obj


@register.filter
def getMinutesFromDates(endtime, starttime):
    return (endtime - starttime).total_seconds()/60


@register.filter
def getLanguage(request):
    try:
        language = str(request.user.profile.language)
    except Exception as e:
        # user not logged
        language = 'pt-BR'
    finally:
        key = request.GET.get('key', '')
        value = request.GET.get('value', '')
        allowed_languages = {'pt-BR': 1, 'en': 1, 'es': 1}
        if key != '' and value != '' and key == 'language' and value in allowed_languages:
            language = value
        elif request.COOKIES.get('language') != None:
            language = request.COOKIES.get('language')
        return language


@register.filter
def setLanguage(request, response):
    language = getLanguage(request)
    response.set_cookie('language', language)
    return {'response': response, 'language': language}


@register.filter
def days_passed(date):
    if isinstance(date, datetime):
        date = date.date()
    delta = datetime.now().date() - date
    return delta.days


@register.filter
def from_UTC(time):
    return time - timedelta(hours=3)


@register.filter
def getStandardVariables(automation_name, language, get_all_variables=False):
    standard_variables = {
        'cepom-rj': {
            'title': translate('cepom_rj_title_and_subtitle', language),
            'input_small': translate('cepom_rj_text_example_input', language),
            'subtitle_example_and_instructions': translate('cepom_rj_instructions', language),
            'title_text_solution': translate('cepom_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpom_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cepom_rj_title_about_the_service', language)
        },
        'cpom-sp': {
            'title': translate('cpom_sp_title_and_subtitle', language),
            'input_small': translate('cpom_sp_text_example_input', language),
            'subtitle_example_and_instructions': translate('cpom_sp_instructions', language),
            'title_text_solution': translate('cpom_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpom_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cpom_sp_title_about_the_service', language)
        },
        'sabesp': {
            'title': translate('sabesp_title_and_subtitle', language),
            'input_small': translate('cpom_sp_text_example_input', language),
            'subtitle_example_and_instructions': translate('sabesp_instructions', language),
            'title_text_solution': translate('sabesp_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('sabesp_discover_how_it_works_1', language),
            'how_it_works_2': translate('light_sabesp_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('sabesp_title_about_the_service', language)
        },
        'receita-federal-cpf': {
            'title': translate('receita_federal_cpf_title_and_subtitle', language),
            'input_small': translate('receita_federal_cpf_text_example_input', language),
            'subtitle_example_and_instructions': translate('receita_federal_cpf_instructions', language),
            'title_text_solution': translate('cpf_title_about_the_service', language),
            'subtitle_text_solution': translate('cpf_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpf_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_cnpj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cpf_title_about_the_service', language)
        },
        'enel-sp': {
            'title': translate('enel_sao_paulo_title_and_subtitle', language),
            'input_small': translate('enel_sp_text_example_input', language),
            'small_login': translate('same_login_used_on_enel_website', language),
            'small_password': translate('same_password_used_on_enel_website', language),
            'subtitle_example_and_instructions': translate('enel_sp_instructions', language),
            'title_text_solution': translate('enel_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('enel_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('enel_discover_how_it_works_1', language),
            'how_it_works_2': translate('enel_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('enel_sp_title_about_the_service', language)
        },
        'notas-servico-sp': {
            'title': translate('notas_servico_sp_title_and_subtitle', language),
            'input_small': translate('notas_servico_sp_example_input', language),
            'subtitle_example_and_instructions': translate('notas_servico_sp_instructions', language),
            'title_text_solution': translate('notas_servico_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('service_invoices_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('nfe_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate('nfe_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('notas_servico_sp_title_about_the_service', language)
        },
        'comgas': {
            'title': translate('comgas_title_and_subtitle', language),
            'input_small': translate('comgas_example_input', language),
            'subtitle_example_and_instructions': translate('comgas_instructions', language),
            'title_text_solution': translate('comgas_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('comgas_discover_how_it_works_1', language),
            'how_it_works_2': translate('comgas_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('comgas_title_about_the_service', language)
        },
        'trf2': {
            'title': translate('trf2_title_and_subtitle', language),
            'input_small': translate('trf2_example_input', language),
            'subtitle_example_and_instructions': translate('trf2_instructions', language),
            'title_text_solution': translate('trf2_title_about_the_service', language),
            'subtitle_text_solution': translate('cpf_certificates_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpf_trf2_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('trf2_title_about_the_service', language)
        },
        'trf3': {
            'title': translate('trf3_title_and_subtitle', language),
            'input_small': translate('trf3_example_input', language),
            'subtitle_example_and_instructions': translate('trf3_instructions', language),
            'title_text_solution': translate('trf3_title_about_the_service', language),
            'subtitle_text_solution': translate('cpf_certificates_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpf_trf3_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('trf3_title_about_the_service', language)
        },
        'inidoneos': {
            'title': translate('inidoneos_title_and_subtitle', language),
            'input_small': translate('inidoneos_example_input', language),
            'subtitle_example_and_instructions': translate('inidoneos_instructions', language),
            'title_text_solution': translate('inidoneos_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('inidoneos_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('inidoneos_title_about_the_service', language)
        },
        'comprot': {
            'title': translate('comprot_title_and_subtitle', language),
            'input_small': translate('comprot_text_input_small', language),
            'subtitle_example_and_instructions': translate('comprot_instructions', language),
            'title_text_solution': translate('comprot_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('comprot_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('comprot_title_about_the_service', language)
        },
        'vivo': {
            'title': translate('vivo_title_and_subtitle', language),
            'input_small': translate('vivo_example_input', language),
            'small_login': translate('same_login_used_on_vivo_website', language),
            'small_password': translate('same_password_used_on_vivo_website', language),
            'subtitle_example_and_instructions': translate('vivo_instructions', language),
            'title_text_solution': translate('vivo_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('vivo_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('vivo_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_cuts_and_fines', language),
            'advantages_3': translate('receive_all_information_and_tickets_in_one_place', language),
            'service_hover_text': translate('vivo_title_about_the_service', language)
        },
        'light': {
            'title': translate('light_title_and_subtitle', language),
            'input_small': translate('light_example_input', language),
            'small_login': translate('same_login_used_on_light_website', language),
            'small_password': translate('same_password_used_on_light_website', language),
            'subtitle_example_and_instructions': translate('light_instructions', language),
            'title_text_solution': translate('light_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('light_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('light_discover_how_it_works_1', language),
            'how_it_works_2': translate('light_sabesp_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('light_title_about_the_service', language)
        },
        'claro': {
            'title': translate('claro_title_and_subtitle', language),
            'input_small': translate('claro_example_input', language),
            'small_login': translate('same_login_used_on_claro_website', language),
            'small_password': translate('same_password_used_on_claro_website', language),
            'subtitle_example_and_instructions': translate('claro_instructions', language),
            'title_text_solution': translate('claro_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('claro_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('claro_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_cuts_and_fines', language),
            'advantages_3': translate('receive_all_information_and_tickets_in_one_place', language),
            'service_hover_text': translate('claro_title_about_the_service', language)
        },
        'iss-rj': {
            'title': translate('iss_rj_title_and_subtitle', language),
            'input_small': translate('iss_rj_example_input', language),
            'small_login': translate('same_login_used_on_nota_carioca_website', language),
            'small_password': translate('same_password_used_on_nota_carioca_website', language),
            'subtitle_example_and_instructions': translate('iss_rj_instructions', language),
            'title_text_solution': translate('iss_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_nota_carioca', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_rj_title_about_the_service', language)
        },
        'iss-sp': {
            'title': translate('iss_sp_title_and_subtitle', language),
            'input_small': translate('iss_sp_example_input', language),
            'small_login': translate('same_login_used_on_the_sao_paulo_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_sao_paulo_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_sp_instructions', language),
            'title_text_solution': translate('iss_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_city_hall_sp', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_sp_title_about_the_service', language)
        },
        'receita-federal-cnpj': {
            'title': translate('receita_federal_cnpj_title_and_subtitle', language),
            'input_small': translate('receita_federal_cnpj_example_input', language),
            'subtitle_example_and_instructions': translate('receita_federal_cnpj_instructions', language),
            'title_text_solution': translate('receita_federal_cnpj_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnpj_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_cnpj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('receita_federal_cnpj_title_about_the_service', language)
        },
        'icms-mg': {
            'title': translate('icms_mg_title_and_subtitle', language),
            'input_small': translate('icms_mg_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-sp': {
            'title': translate('icms_sp_title_and_subtitle', language),
            'input_small': translate('icms_sp_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-rj': {
            'title': translate('icms_rj_title_and_subtitle', language),
            'input_small': translate('icms_rj_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'ipva-rj': {
            'title': translate('ipva_rj_title_and_subtitle', language),
            'input_small': translate('ipva_rj_example_input', language),
            'subtitle_example_and_instructions': translate('ipva_instructions', language),
            'title_text_solution': translate('ipva_title_about_the_service', language),
            'subtitle_text_solution': translate('ipva_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('ipva_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('ipva_title_about_the_service', language)
        },
        'ipva-sp': {
            'title': translate('ipva_sp_title_and_subtitle', language),
            'input_small': translate('ipva_sp_example_input', language),
            'subtitle_example_and_instructions': translate('ipva_instructions', language),
            'title_text_solution': translate('ipva_title_about_the_service', language),
            'subtitle_text_solution': translate('ipva_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('ipva_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('ipva_title_about_the_service', language)
        },
        'notas-servicos-rj': {
            'title': translate('notas_servicos_rj_title_and_subtitle', language),
            'input_small': translate('notas_servicos_rj_example_input', language),
            'small_login': translate('same_login_used_on_nota_carioca_website', language),
            'small_password': translate('same_password_used_on_nota_carioca_website', language),
            'subtitle_example_and_instructions': translate('notas_servicos_rj_instructions', language),
            'title_text_solution': translate('notas_servicos_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('service_invoices_subtitle_about_the_service', language),
            'title_step2': translate('credentials_nota_carioca', language),
            'title_step3': translate('filter_notes', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('nfe_rj_discover_how_it_works_1', language),
            'how_it_works_2': translate('nfe_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('notas_servicos_rj_title_about_the_service', language)
        },
        'cnd': {
            'title': translate('cnd_federal_revenue_title_and_subtitle', language),
            'input_small': translate('cnd_federal_revenue_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'gnre-sp': {
            'title': translate('gnre_sp_title_and_subtitle', language),
            'input_small': translate('gnre_sp_example_input', language),
            'subtitle_example_and_instructions': translate('gnre_instructions', language),
            'title_text_solution': translate('gnre_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('gnre_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('gnre_discover_how_it_works_1', language),
            'how_it_works_2': translate('gnre_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('gnre_sp_title_about_the_service', language)
        },
        'gnre-rj': {
            'title': translate('gnre_title_and_subtitle', language),
            'input_small': translate('gnre_example_input', language),
            'subtitle_example_and_instructions': translate('gnre_instructions', language),
            'title_text_solution': translate('gnre_title_about_the_service', language),
            'subtitle_text_solution': translate('gnre_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('gnre_discover_how_it_works_1', language),
            'how_it_works_2': translate('gnre_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('gnre_title_about_the_service', language)
        },
        'cedae': {
            'title': translate('cedae_title_and_subtitle', language),
            'input_small': translate('cedae_example_input', language),
            'subtitle_example_and_instructions': translate('water_bill_instructions', language),
            'title_text_solution': translate('cedae_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': "",
            'advantages_2': "",
            'advantages_3': "",
            'service_hover_text': translate('cedae_title_about_the_service', language)
        },
        'naturgy': {
            'title': translate('naturgy_title_and_subtitle', language),
            'input_small': translate('naturgy_example_input', language),
            'subtitle_example_and_instructions': translate('naturgy_instructions', language),
            'title_text_solution': translate('naturgy_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': "",
            'advantages_2': "",
            'advantages_3': "",
            'service_hover_text': translate('naturgy_title_about_the_service', language)
        },
        'iss-rio-grande': {
            'title': translate('iss_rio_grande_title_and_subtitle', language),
            'input_small': translate('iss_rio_grande_example_input', language),
            'small_login': translate('same_ccm_used_on_the_rio_grande_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_website_of_the_municipality_of_rio_grande', language),
            'subtitle_example_and_instructions': translate('iss_rio_grande_instructions', language),
            'title_text_solution': translate('iss_rio_grande_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_city_hall_of_rio_grande', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'CCM',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_rio_grande_title_about_the_service', language)
        },
        'divida-ativa-rj': {
            'title': translate('divida_ativa_rj_title_and_subtitle', language),
            'input_small': translate('divida_ativa_rj_example_input', language),
            'subtitle_example_and_instructions': translate('divida_ativa_rj_instructions', language),
            'title_text_solution': translate('divida_ativa_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('divida_ativa_rj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('divida_ativa_rj_discover_how_it_works_1', language),
            'how_it_works_2': translate('divida_ativa_rj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('regularize_your_situation_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('divida_ativa_rj_title_about_the_service', language)
        },
        'divida-ativa-sp': {
            'title': translate('divida_ativa_sp_title_and_subtitle', language),
            'input_small': translate('divida_ativa_sp_example_input', language),
            'subtitle_example_and_instructions': translate('divida_ativa_sp_instructions', language),
            'title_text_solution': translate('divida_ativa_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('divida_ativa_rj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('divida_ativa_rj_discover_how_it_works_1', language),
            'how_it_works_2': translate('divida_ativa_rj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('regularize_your_situation_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('divida_ativa_rj_title_about_the_service', language)
        },
        'cnd-sp': {
            'title': translate('cnd_sp_title_and_subtitle', language),
            'input_small': translate('cnd_sp_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'cnd-rj': {
            'title': translate('cnd_rj_title_and_subtitle', language),
            'input_small': translate('cnd_rj_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_rj_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'iss-ipojuca-wilson': {
            'title': translate('iss_ipojuca_title_and_subtitle', language),
            'input_small': translate('iss_ipojuca_example_input', language),
            'small_login': translate('same_cpf_cnpj_used_on_the_ipojuca_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_ipojuca_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_ipojuca_wilson_instructions', language),
            'title_text_solution': translate('iss_ipojuca_wilson_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('ipojuca_city_hall_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'C.P.F./C.N.P.J.',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3',
                                      language),
            'service_hover_text': translate('iss_ipojuca_wilson_title_about_the_service', language)
        },
        'simples-nacional': {
            'title': translate('simples_nacional_title_and_subtitle', language),
            'input_small': translate('simples_nacional_example_input', language),
            'subtitle_example_and_instructions': translate('simples_nacional_instructions', language),
            'title_text_solution': translate('simples_nacional_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('simples_nacional_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('simples_nacional_title_about_the_service', language)
        },
        'iss-barcarena': {
            'title': translate('iss_barcarena_title_and_subtitle', language),
            'input_small': translate('iss_barcarena_example_input', language),
            'small_login': translate('same_cpf_used_on_the_website_of_the_municipality_of_barcarena', language),
            'small_password': translate('same_password_used_on_the_website_of_the_municipality_of_barcarena', language),
            'subtitle_example_and_instructions': translate('iss_barcarena_instructions', language),
            'title_text_solution': translate('iss_barcarena_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('barcarena_city_hall_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'CPF',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_barcarena_title_about_the_service', language)
        },
        'iss-oriximina': {
            'title': translate('iss_oriximina_title_and_subtitle', language),
            'input_small': translate('iss_oriximina_example_input', language),
            'small_login': translate('same_cpf_used_on_the_website_of_the_municipality_of_oriximina', language),
            'small_password': translate('same_password_used_on_the_website_of_the_municipality_of_oriximina', language),
            'subtitle_example_and_instructions': translate('iss_oriximina_instructions', language),
            'title_text_solution': translate('iss_oriximina_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_of_the_city_hall_of_oriximina', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'CPF',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_oriximina_title_about_the_service', language),
        },
        'sefaz-rj': {
            'title': translate('sefaz_rj_title_and_subtitle', language),
            'input_small': translate('sefaz_rj_example_input', language),
            'small_login': translate('same_user_used_on_the_sefaz_rio_de_janeiro_website', language),
            'small_password': translate('same_password_used_on_the_sefaz_rio_de_janeiro_website', language),
            'subtitle_example_and_instructions': translate('sefaz_rj_instructions', language),
            'title_text_solution': translate('sefaz_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('declaraciones_subtitle_about_the_service', language),
            'title_step2': translate('sefaz_credentials_rj', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': translate('user', language),
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('template_with_your_sefaz_rj_works_1', language),
            'how_it_works_2': translate('their_respective_itd_declaration_works_1', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('sefaz_rj_title_about_the_service', language)
        },
        'iss-cabedelo': {
            'title': translate('iss_cabedelo_title_and_subtitle', language),
            'input_small': translate('iss_cabedelo_example_input', language),
            'small_login': translate('same_cpf_cnpj_used_on_the_cabedelo_city_hall_website', language),
            'small_password': translate('same_password_used_on_cabedelo_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_cabedelo_instructions', language),
            'title_text_solution': translate('iss_cabedelo_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_of_cabedelo_city_hall', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'C.P.F./C.N.P.J.',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_cabedelo_title_about_the_service', language)
        },
        'certidao-mte': {
            'title': translate('certidao_mte_title_and_subtitle', language),
            'input_small': translate('certidao_mte_example_input', language),
            'subtitle_example_and_instructions': translate('certidao_mte_instructions', language),
            'title_text_solution': translate('certidao_mte_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('you_fill_in_the_upload_file_with_the_cnpj_that_you_want_to_issue_the_labor_debt_certificate_works_2', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('certidao_mte_title_about_the_service', language)
        },
        'inidoneos-ceis': {
            'title': translate('inidoneos_ceis_title_and_subtitle', language),
            'input_small': translate('inidoneos_ceis_example_input', language),
            'subtitle_example_and_instructions': translate('inidoneos_ceis_instructions', language),
            'title_text_solution': translate('inidoneos_ceis_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('inidoneos_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('inidoneos_ceis_title_about_the_service', language)
        },
        'cnd-fgts': {
            'title': translate('cnd_fgts_title_and_subtitle', language),
            'input_small': translate('cnd_fgts_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_fgts_instructions', language),
            'title_text_solution': translate('cnd_fgts_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('fgts_crf_discover_how_it_works_1', language),
            'how_it_works_2': translate('fgts_crf_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_fgts_title_about_the_service', language)
        },
        'aguas-rio': {
            'title': translate('aguas_rio_title_and_subtitle', language),
            'input_small': translate('aguas_rio_example_input', language),
            'subtitle_example_and_instructions': translate('aguas_rio_instructions', language),
            'title_text_solution': translate('aguas_rio_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('waters_of_the_river_works_1', language),
            'how_it_works_2': translate('waters_of_the_river_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('aguas_rio_title_about_the_service', language)
        },
        'iss-niteroi': {
            'title': translate('iss_niteroi_title_and_subtitle', language),
            'input_small': translate('iss_niteroi_example_input', language),
            'small_login': translate('same_cpf_cnpj_used_on_the_niteroi_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_niteroi_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_niteroi_instructions', language),
            'title_text_solution': translate('iss_niteroi_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_from_the_city_of_niteroi', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'C.P.F./C.N.P.J.',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('niteroi_city_hall_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_niteroi_title_about_the_service', language)
        },
        'iss-salvador': {
            'title': translate('iss_salvador_title_and_subtitle', language),
            'input_small': translate('iss_salvador_example_input', language),
            'small_login': translate('same_cpf_cnpj_used_on_the_salvador_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_salvador_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_salvador_instructions', language),
            'title_text_solution': translate('iss_salvador_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('salvador_city_hall_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'C.P.F./C.N.P.J.',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('iss_guides_in_salvador_city_hall_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_salvador_title_about_the_service', language)
        },
        'iss-maceio': {
            'title': translate('iss_maceio_title_and_subtitle', language),
            'input_small': translate('iss_maceio_example_input', language),
            'small_login': translate('same_login_used_on_the_maceio_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_maceio_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_maceio_instructions', language),
            'title_text_solution': translate('iss_maceio_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_of_the_municipality_of_maceio', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('iss_guides_in_maceio_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_maceio_title_about_the_service', language)
        },
        'iss-guaruja': {
            'title': translate('iss_guaruja_title_and_subtitle', language),
            'input_small': translate('iss_guaruja_example_input', language),
            'small_login': translate('same_login_used_on_the_guaruja_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_guaruja_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_guaruja_instructions', language),
            'title_text_solution': translate('iss_guaruja_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_of_the_city_hall_of_guaruja', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('iss_guides_in_guaruja_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_guaruja_title_about_the_service', language)
        },
        'iss-santos': {
            'title': translate('iss_santos_title_and_subtitle', language),
            'input_small': translate('iss_santos_example_input', language),
            'small_login': translate('same_login_used_on_the_santos_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_santos_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_santos_instructions', language),
            'title_text_solution': translate('iss_santos_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_of_the_municipality_of_santos', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('iss_guides_in_santos_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_santos_title_about_the_service', language)
        },
        'iss-santo-andre': {
            'title': translate('iss_santo_andre_title_and_subtitle', language),
            'input_small': translate('iss_santo_andre_example_input', language),
            'small_login': translate('same_login_used_on_the_santo_andre_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_santo_andre_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_santo_andre_instructions', language),
            'title_text_solution': translate('iss_santo_andre_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_from_the_city_of_santo_andre', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('iss_guides_in_santo_andre_works_1', language),
            'how_it_works_2': translate('iss_guides_in_salvador_city_hall_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_santo_andre_title_about_the_service', language)
        },
        'afip-argentina': {
            'title': translate('afip_argentina_title_and_subtitle', language),
            'input_small': translate('afip_argentina_example_input', language),
            'small_login': translate('same_cuit_cuil_used_on_the_afip_website', language),
            'small_password': translate('same_password_used_on_the_afip_website', language),
            'subtitle_example_and_instructions': translate('afip_argentina_instructions', language),
            'title_text_solution': translate('afip_argentina_title_about_the_service', language),
            'subtitle_text_solution': translate('afip_argentina_subtitle_about_the_service', language),
            'title_step2': translate('afip_credentials', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'CUIT/CUIL',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('afip_advantages_1', language),
            'how_it_works_2': translate('afip_advantages_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3':  translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('afip_argentina_title_about_the_service', language),
        },
        'arba-argentina': {
            'title': translate('arba_argentina_title_and_subtitle', language),
            'input_small': translate('arba_argentina_example_input', language),
            'small_login': translate('same_cuit_cuil_used_on_the_arba_website', language),
            'small_password': translate('same_password_used_on_the_arba_website', language),
            'subtitle_example_and_instructions': translate('arba_argentina_instructions', language),
            'title_text_solution': translate('arba_argentina_title_about_the_service', language),
            'subtitle_text_solution': translate('arba_argentina_subtitle_about_the_service', language),
            'title_step2': translate('arba_credentials', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'CUIT/CUIL',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('arba_advantages_1', language),
            'how_it_works_2': translate('arba_advantages_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3':  translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('arba_argentina_title_about_the_service', language),
        },
        'agip-argentina': {
            'title': translate('agip_argentina_title_and_subtitle', language),
            'input_small': translate('agip_argentina_example_input', language),
            'subtitle_example_and_instructions': translate('agip_argentina_instructions', language),
            'title_text_solution': translate('agip_argentina_title_about_the_service', language),
            'subtitle_text_solution': translate('agip_argentina_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('agip_how_it_works_1', language),
            'how_it_works_2': translate('agip_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('agip_argentina_title_about_the_service', language)
        },
        'copasa': {
            'title': translate('copasa_title_and_subtitle', language),
            'input_small': translate('copasa_text_example_input', language),
            'small_login': translate('same_login_used_on_copasa_website', language),
            'small_password': translate('same_password_used_on_copasa_website', language),
            'subtitle_example_and_instructions': translate('copasa_instructions', language),
            'title_text_solution': translate('copasa_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('copasa_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('copasa_title_about_the_service', language)
        },
        'iss-rj-wilson': {
            'title': translate('iss_rj_wilson_title_and_subtitle', language),
            'input_small': translate('iss_rj_example_input', language),
            'small_login': translate('same_login_used_on_nota_carioca_website', language),
            'small_password': translate('same_password_used_on_nota_carioca_website', language),
            'subtitle_example_and_instructions': translate('iss_rj_wilson_instructions', language),
            'title_text_solution': translate('iss_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('credentials_nota_carioca', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('iss_rj_title_about_the_service', language)
        },
        'integra-siafi': {
            'title': 'Administração Financeira do Tesouro Nacional | SIAFI',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversos documentos contábeis.'
        },
        'nfe-receita-federal': {
            'title': 'Emissão de Notas Fiscais (NFS-e) | Receita Federal',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': translate('service_invoices_subtitle_about_the_service', language),
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversas Nota Fiscal Eletrônica.'
        },
        'sintegra-sc': {
            'title': 'Verificação de Situação Cadastral | SINTEGRA-SC',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'conciliacao-bancaria': {
            'title': 'Consulta Conciliação Bancária | Interna',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversas conferências entre as suas contas bancárias.'
        },
        'santander': {
            'title': 'Emissão de Extrato Bancário | Santander',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber o extrato bancário, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversos extrato bancário.'
        },
        'itau': {
            'title': 'Emissão de Extrato Bancário | Itaú',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber o extrato bancário, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversos extrato bancário.'
        },
        'decretos-portarias': {
            'title': 'Consulta de Decretos e Portarias',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber decretos e portarias, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('text_verification_of_decrees_ordinances', language)
        },
        'processamento-documentos': {
            'title': 'Processamento Visual de Documentos',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber os documentos solicitados, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversos Documentos.'
        },
        'dashboards-ecommerce': {
            'title': 'Dashboard | Controle de Estoque',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber métricas, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Tome decisões para o seu e-commerce, acompanhando as principais métricas para gerir o seu negócio e impulsionar as suas vendas.'
        },
        'cemig': {
            'title': translate('cemig_title_and_subtitle', language),
            'input_small': translate('cemig_text_example_input', language),
            'small_login': translate('same_login_used_on_the_cemig_website', language),
            'small_password': translate('same_password_used_on_the_cemig_website', language),
            'subtitle_example_and_instructions': translate('cemig_instructions', language),
            'title_text_solution': translate('cemig_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('cemig_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('cemig_discover_how_it_works_1', language),
            'how_it_works_2': translate('light_sabesp_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('cemig_title_about_the_service', language)
        },
        'stone': {
            'title': 'Extrato de vendas | Stone',
            'input_small': '',
            'small_login': '',
            'small_password': '',
            'subtitle_example_and_instructions': '',
            'title_text_solution': '',
            'subtitle_text_solution': 'Ao final da execução do serviço, você irá receber o extrato bancário, assim como um arquivo de resumo das informações.',
            'title_step2': '',
            'title_step3': '',
            'input_form_login': '',
            'input_form_pass': '',
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': 'Com esse serviço você consegue consultar simultaneamente diversos extrato bancário.'
        },
        'extrato-bancario': {
            'title': translate('extrato_bancario_title_and_subtitle', language),
            'input_small': translate('extrato_bancario_text_example_input', language),
            'small_login': translate('same_login_used_on_the_bank_statement_website', language),
            'small_password': translate('same_password_used_on_the_bank_statement_website', language),
            'subtitle_example_and_instructions': translate('extrato_bancario_instructions', language),
            'title_text_solution': translate('extrato_bancario_title_about_the_service', language),
            'subtitle_text_solution': translate('extrato_bancario_subtitle_about_the_service', language),
            'title_step2': translate('banking_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('extrato_bancario_title_about_the_service', language)
        },
        'cnd-mg': {
            'title': translate('cnd_mg_title_and_subtitle', language),
            'input_small': translate('cnd_mg_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_mg_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'ibama': {
            'title': translate('ibama_title_and_subtitle', language),
            'input_small': translate('ibama_text_example_input', language),
            'subtitle_example_and_instructions': translate('ibama_instructions', language),
            'title_text_solution': translate('ibama_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('ibama_title_about_the_service', language)
        },
        'antecedentes-sp': {
            'title': translate('antecedentes_sp_title_and_subtitle', language),
            'input_small': translate('antecedentes_sp_text_example_input', language),
            'subtitle_example_and_instructions': translate('antecedentes_sp_instructions', language),
            'title_text_solution': translate('antecedentes_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('rg_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('rg_discover_how_it_works_1', language),
            'how_it_works_2': translate("rg_discover_how_it_works_2", language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('antecedentes_sp_title_about_the_service', language)
        },
        'antecedentes-federal': {
            'title': translate('antecedentes_federal_title_and_subtitle', language),
            'input_small': translate('antecedentes_federal_text_example_input', language),
            'subtitle_example_and_instructions': translate('antecedentes_federal_instructions', language),
            'title_text_solution': translate('antecedentes_federal_title_about_the_service', language),
            'subtitle_text_solution': translate('cpf_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpf_discover_how_it_works_1', language),
            'how_it_works_2': translate("cpf_cnpj_discover_how_it_works_2", language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('antecedentes_federal_title_about_the_service', language)
        },
        'cnd-pe': {
            'title': translate('cnd_pe_title_and_subtitle', language),
            'input_small': translate('cnd_pe_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_pe_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'cnd-bahia': {
            'title': translate('cnd_bahia_title_and_subtitle', language),
            'input_small': translate('cnd_bahia_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_pe_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'shopee': {
            'title': translate('shopee_title_and_subtitle', language),
            'input_small': translate('shopee_text_example_input', language),
            'subtitle_example_and_instructions': translate('shopee_instructions', language),
            'title_text_solution': translate('shopee_title_about_the_service', language),
            'subtitle_text_solution': translate('shopee_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('shopee_discover_how_it_works_1', language),
            'how_it_works_2': translate('shopee_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('shopee_title_about_the_service', language)
        },
        'der': {
            'title': translate('der_title_and_subtitle', language),
            'input_small': translate('der_text_example_input', language),
            'subtitle_example_and_instructions': translate('der_instructions', language),
            'title_text_solution': translate('der_title_about_the_service', language),
            'subtitle_text_solution': translate('der_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate("ipva_discover_how_it_works_1", language),
            'how_it_works_2': translate('der_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('der_title_about_the_service', language)
        },
        'mpf': {
            'title': translate('mpf_title_and_subtitle', language),
            'input_small': translate('mpf_text_example_input', language),
            'subtitle_example_and_instructions': translate('mpf_instructions', language),
            'title_text_solution': translate('mpf_title_about_the_service', language),
            'subtitle_text_solution': translate('mpf_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('shopee_discover_how_it_works_1', language),
            'how_it_works_2': translate('mpf_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('mpf_title_about_the_service', language)
        },
        'anvisa': {
            'title': translate('anvisa_title_and_subtitle', language),
            'input_small': translate('anvisa_text_example_input', language),
            'subtitle_example_and_instructions': translate('anvisa_instructions', language),
            'title_text_solution': translate('anvisa_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpom_discover_how_it_works_1', language),
            'how_it_works_2': translate('anvisa_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('anvisa_title_about_the_service', language)
        },
        'carf': {
            'title': translate('carf_title_and_subtitle', language),
            'input_small': translate('carf_example_input', language),
            'subtitle_example_and_instructions': translate('carf_instructions', language),
            'title_text_solution': translate('carf_title_about_the_service', language),
            'subtitle_text_solution': translate('cnpj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('carf_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('carf_title_about_the_service', language)
        },
        'divida-ativa-mg': {
            'title': translate('divida_ativa_mg_title_and_subtitle', language),
            'input_small': translate('divida_ativa_mg_example_input', language),
            'subtitle_example_and_instructions': translate('divida_ativa_mg_instructions', language),
            'title_text_solution': translate('divida_ativa_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('divida_ativa_mg_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnpj_discover_how_it_works_1', language),
            'how_it_works_2': translate('divida_ativa_mg_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('regularize_your_situation_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('divida_ativa_rj_title_about_the_service', language)
        },
        'cpfl-paulista': {
            'title': translate('cpfl_paulista_title_and_subtitle', language),
            'input_small': translate('cpfl_paulista_text_example_input', language),
            'subtitle_example_and_instructions': translate('cpfl_paulista_instructions', language),
            'title_text_solution': translate('cpfl_paulista_title_about_the_service', language),
            'subtitle_text_solution': translate('cpfl_paulista_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cpfl_paulista_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpfl_paulista_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cpfl_paulista_title_about_the_service', language)
        },
        'consulta-antt-rntrc': {
            'title': translate('consulta_antt_rntrc_title_and_subtitle', language),
            'input_small': translate('consulta_antt_rntrc_text_example_input', language),
            'subtitle_example_and_instructions': translate('consulta_antt_rntrc_instructions', language),
            'title_text_solution': translate('consulta_antt_rntrc_title_about_the_service', language),
            'subtitle_text_solution': translate('consulta_antt_rntrc_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('consulta_antt_rntrc_discover_how_it_works_1', language),
            'how_it_works_2': translate('consulta_antt_rntrc_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('consulta_antt_rntrc_title_about_the_service', language)
        },
        'correios': {
            'title': translate('correios_title_and_subtitle', language),
            'input_small': translate('correios_text_example_input', language),
            'subtitle_example_and_instructions': translate('correios_instructions', language),
            'title_text_solution': translate('correios_title_about_the_service', language),
            'subtitle_text_solution': translate('correios_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('correios_discover_how_it_works_1', language),
            'how_it_works_2': translate('correios_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('correios_title_about_the_service', language)
        },
        'omie': {
            'title': translate('omie_title_and_subtitle', language),
            'input_small': translate('omie_text_example_input', language),
            'small_login': translate('same_email_used_on_the_omie_website', language),
            'input_form_login': 'Email',
            'subtitle_example_and_instructions': translate('omie_instructions', language),
            'small_password': translate('same_password_used_on_omie_website', language),
            'input_form_pass': translate('password', language),
            'title_text_solution': translate('omie_title_about_the_service', language),
            'subtitle_text_solution': translate('omie_subtitle_about_the_service', language),
            'title_step2': translate('omie_credentials', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('omie_discover_how_it_works_1', language),
            'how_it_works_2': translate('omie_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('omie_title_about_the_service', language)
        },
        'antecedentes-rj': {
            'title': translate('antecedentes_rj_title_and_subtitle', language),
            'input_small': translate('antecedentes_rj_text_example_input', language),
            'subtitle_example_and_instructions': translate('antecedentes_rj_instructions', language),
            'title_text_solution': translate('antecedentes_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('rg_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('rg_discover_how_it_works_1', language),
            'how_it_works_2': translate("rg_discover_how_it_works_2", language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('antecedentes_rj_title_about_the_service', language)
        },
        'cnd-bocaina': {
            'title': translate('cnd_bocaina_title_and_subtitle', language),
            'input_small': translate('cnd_bocaina_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'cnd-ce': {
            'title': translate('cnd_ce_revenue_title_and_subtitle', language),
            'input_small': translate('cnd_ce_revenue_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'iss-ipojuca': {
            'title': translate('iss_ipojuca_title_and_subtitle', language),
            'input_small': translate('iss_ipojuca_example_input', language),
            'small_login': translate('same_cpf_cnpj_used_on_the_ipojuca_city_hall_website', language),
            'small_password': translate('same_password_used_on_the_ipojuca_city_hall_website', language),
            'subtitle_example_and_instructions': translate('iss_ipojuca_instructions', language),
            'title_text_solution': translate('iss_ipojuca_title_about_the_service', language),
            'subtitle_text_solution': translate('iss_subtitle_about_the_service', language),
            'title_step2': translate('ipojuca_city_hall_credentials', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'C.P.F./C.N.P.J.',
            'input_form_pass': translate('password', language),
            'how_it_works_1': "",
            'how_it_works_2': "",
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3',
                                      language),
            'service_hover_text': translate('iss_ipojuca_title_about_the_service', language)
        },
        'cnd-fortaleza': {
            'title': translate('cnd_fortaleza_revenue_title_and_subtitle', language),
            'input_small': translate('cnd_fortaleza_revenue_example_input', language),
            'subtitle_example_and_instructions': translate('cnd_instructions', language),
            'title_text_solution': translate('cnd_title_about_the_service', language),
            'subtitle_text_solution': translate('cnd_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('cnd_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_trf_inidoneos_cnd_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('cnd_title_about_the_service', language)
        },
        'energisa': {
            'title': translate('energisa_title_and_subtitle', language),
            'input_small': translate('energisa_text_example_input', language),
            'small_login': translate('same_login_used_on_energisa_website', language),
            'small_password': translate('same_password_used_on_energisa_website', language),
            'subtitle_example_and_instructions': translate('energisa_instructions', language),
            'title_text_solution': translate('energisa_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('energisa_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('energisa_discover_how_it_works_1', language),
            'how_it_works_2': translate('elektro_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('energisa_title_about_the_service', language)
        },
        'elektro': {
            'title': translate('elektro_title_and_subtitle', language),
            'input_small': translate('elektro_text_example_input', language),
            'small_login': translate('same_login_used_on_elektro_website', language),
            'small_password': translate('same_password_used_on_elektro_website', language),
            'subtitle_example_and_instructions': translate('elektro_instructions', language),
            'title_text_solution': translate('elektro_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('elektro_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('elektro_discover_how_it_works_1', language),
            'how_it_works_2': translate('elektro_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('elektro_title_about_the_service', language)
        },
        'correios-cas': {
            'title': translate('correios_cas_title_and_subtitle', language),
            'input_small': translate('correios_cas_text_example_input', language),
            'small_login': translate('same_login_used_on_the_correios_website_cas', language),
            'small_password': translate('same_password_used_on_the_correios_website_cas', language),
            'subtitle_example_and_instructions': translate('correios_cas_instructions', language),
            'title_text_solution': translate('correios_cas_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('postal_credentials_cas', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('correios_cas_discover_how_it_works_1', language),
            'how_it_works_2': translate('cpf_cnpj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('correios_cas_title_about_the_service', language)
        },
        'edp-brasil': {
            'title': translate('edp_brasil_title_and_subtitle', language),
            'input_small': translate('edp_brasil_text_example_input', language),
            'small_login': translate('same_login_used_on_the_edp_website', language),
            'small_password': translate('same_password_used_on_the_edp_website', language),
            'subtitle_example_and_instructions': translate('edp_brasil_instructions', language),
            'title_text_solution': translate('edp_brasil_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('edp_brasil_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('edp_brasil_discover_how_it_works_1', language),
            'how_it_works_2': translate('elektro_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_your_bills_in_one_place_advantages_3', language),
            'service_hover_text': translate('edp_brasil_title_about_the_service', language)
        },
        'solicitacao-notas-fiscais': {
            'title': translate('solicitacao_nf_title_and_subtitle', language),
            'input_small': translate('solicitacao_nf_text_example_input', language),
            'subtitle_example_and_instructions': translate('solicitacao_nf_instructions', language),
            'title_text_solution': translate('solicitacao_nf_title_about_the_service', language),
            'subtitle_text_solution': translate('solicitacao_nf_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('solicitacao_nf_discover_how_it_works_1', language),
            'how_it_works_2': translate('solicitacao_nf_subtitle_about_the_service', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('solicitacao_nf_title_about_the_service', language)
        },
        'tj-sp': {
            'title': translate('tj_sp_title_and_subtitle', language),
            'input_small': translate('tj_sp_text_example_input', language),
            'subtitle_example_and_instructions': translate('tj_sp_instructions', language),
            'title_text_solution': translate('tj_sp_title_about_the_service', language),
            'subtitle_text_solution': translate('tj_sp_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('tj_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate("tj_sp_discover_how_it_works_2", language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('tj_sp_title_about_the_service', language)
        },
        'tj-rj': {
            'title': translate('tj_rj_title_and_subtitle', language),
            'input_small': translate('tj_rj_text_example_input', language),
            'subtitle_example_and_instructions': translate('tj_rj_instructions', language),
            'title_text_solution': translate('tj_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('tj_rj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('tj_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate("tj_sp_discover_how_it_works_2", language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_results_in_one_place_advantages_3', language),
            'service_hover_text': translate('tj_rj_title_about_the_service', language)
        },
        'icms-alagoas': {
            'title': translate('icms_alagoas_title_and_subtitle', language),
            'input_small': translate('icms_alagoas_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-pr': {
            'title': translate('icms_pr_title_and_subtitle', language),
            'input_small': translate('icms_pr_example_input', language),
            'subtitle_example_and_instructions': translate('icms_pr_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'nfse-londrina': {
            'title': translate('nfse_londrina_title_and_subtitle', language),
            'input_small': translate('nfse_londrina_example_input', language),
            'small_login': translate('same_login_used_on_the_city_hall_of_londrina_pr_website', language),
            'small_password': translate('same_password_used_on_the_website_of_the_city_hall_of_londrina_pr', language),
            'subtitle_example_and_instructions': translate('nfse_londrina_instructions', language),
            'title_text_solution': translate('nfse_londrina_title_about_the_service', language),
            'subtitle_text_solution': translate('service_invoices_subtitle_about_the_service', language),
            'title_step2': translate('londrina_pr_credentials', language),
            'title_step3': translate('file_upload', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('nfse_londrina_discover_how_it_works_1', language),
            'how_it_works_2': translate('nfe_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('nfse_londrina_title_about_the_service', language)
        },
        'nfse-maringa': {
            'title': translate('nfse_maringa_title_and_subtitle', language),
            'input_small': translate('nfse_maringa_example_input', language),
            'small_login': translate('same_login_used_on_the_city_hall_of_maringa_pr_website', language),
            'small_password': translate('same_password_used_on_the_maringa_pr_city_hall_website', language),
            'subtitle_example_and_instructions': translate('nfse_maringa_instructions', language),
            'title_text_solution': translate('nfse_maringa_title_about_the_service', language),
            'subtitle_text_solution': translate('service_invoices_subtitle_about_the_service', language),
            'title_step2': translate('maringa_pr_credentials', language),
            'title_step3': translate('filter_notes', language),
            'title_step4': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('nfse_maringa_discover_how_it_works_1', language),
            'how_it_works_2': translate('nfe_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_mistakes_rework_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('nfse_maringa_title_about_the_service', language)
        },
        'icms-ce': {
            'title': translate('icms_ce_title_and_subtitle', language),
            'input_small': translate('icms_ce_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-sc': {
            'title': translate('icms_sc_title_and_subtitle', language),
            'input_small': translate('icms_sc_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-pe': {
            'title': translate('icms_pe_title_and_subtitle', language),
            'input_small': translate('icms_pe_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'nibo': {
            'title': translate('nibo_title_and_subtitle', language),
            'input_small': translate('nibo_example_input', language),
            'small_login': translate('email_used_on_the_nibo_website', language),
            'small_password': translate('password_used_on_the_nibo_website', language),
            'small_link': translate('onedrive_link_to_receive_the_file', language),
            'subtitle_example_and_instructions': translate('nibo_instructions', language),
            'title_text_solution': translate('nibo_title_about_the_service', language),
            'subtitle_text_solution': translate('nibo_subtitle_about_the_service', language),
            'title_step2': translate('nibo_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'E-mail',
            'input_form_pass': translate('password', language),
            'input_form_link': translate('onedrive_link', language),
            'how_it_works_1': translate('nibo_discover_how_it_works_1', language),
            'how_it_works_2': translate('nibo_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_cuts_and_fines', language),
            'advantages_3': translate('get_all_reports_in_one_place_advantages_3', language),
            'service_hover_text': translate('nibo_title_about_the_service', language)
        },
        'icms-pi': {
            'title': translate('icms_pi_title_and_subtitle', language),
            'input_small': translate('icms_pi_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-df': {
            'title': translate('icms_df_title_and_subtitle', language),
            'input_small': translate('icms_df_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'icms-pa': {
            'title': translate('icms_pa_title_and_subtitle', language),
            'input_small': translate('icms_pa_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'cremerj': {
            'title': translate('cremerj_title_and_subtitle', language),
            'input_small': translate('cremerj_example_input', language),
            'subtitle_example_and_instructions': translate('cremerj_instructions', language),
            'title_text_solution': translate('cremerj_title_about_the_service', language),
            'subtitle_text_solution': translate('cremerj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('tj_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate('cremerj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('cremerj_title_about_the_service', language)
        },
        'coren-rj': {
            'title': translate('coren_rj_title_and_subtitle', language),
            'input_small': translate('coren_rj_example_input', language),
            'subtitle_example_and_instructions': translate('coren_rj_instructions', language),
            'title_text_solution': translate('coren_rj_title_about_the_service', language),
            'subtitle_text_solution': translate('coren_rj_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('tj_sp_discover_how_it_works_1', language),
            'how_it_works_2': translate('coren_rj_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('coren_rj_title_about_the_service', language)
        },
        'embratel': {
            'title': translate('embratel_title_and_subtitle', language),
            'input_small': translate('embratel_example_input', language),
            'small_login': translate('same_login_used_on_embratel_website', language),
            'small_password': translate('same_password_used_on_embratel_website', language),
            'subtitle_example_and_instructions': translate('embratel_instructions', language),
            'title_text_solution': translate('embratel_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('embratel_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('embratel_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_cuts_and_fines', language),
            'advantages_3': translate('receive_all_information_and_tickets_in_one_place', language),
            'service_hover_text': translate('embratel_title_about_the_service', language)
        },
        'icms-to': {
            'title': translate('icms_to_title_and_subtitle', language),
            'input_small': translate('icms_to_example_input', language),
            'subtitle_example_and_instructions': translate('icms_instructions', language),
            'title_text_solution': translate('icms_title_about_the_service', language),
            'subtitle_text_solution': translate('icms_subtitle_about_the_service', language),
            'title_step2': translate('file_upload', language),
            'title_step3': translate('results_settings', language),
            'how_it_works_1': translate('icms_discover_how_it_works_1', language),
            'how_it_works_2': translate('icms_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_and_fines_advantages_2', language),
            'advantages_3': translate('get_all_guides_in_one_place_advantages_3', language),
            'service_hover_text': translate('icms_title_about_the_service', language)
        },
        'oi': {
            'title': translate('oi_title_and_subtitle', language),
            'input_small': translate('oi_example_input', language),
            'small_login': translate('same_login_used_on_oi_website', language),
            'small_password': translate('same_password_used_on_oi_website', language),
            'subtitle_example_and_instructions': translate('oi_instructions', language),
            'title_text_solution': translate('oi_title_about_the_service', language),
            'subtitle_text_solution': translate('consumption_accounts_subtitle_about_the_service', language),
            'title_step2': translate('oi_credentials', language),
            'title_step3': translate('results_settings', language),
            'input_form_login': 'Login',
            'input_form_pass': translate('password', language),
            'how_it_works_1': translate('oi_discover_how_it_works_1', language),
            'how_it_works_2': translate('telephony_ipva_discover_how_it_works_2', language),
            'advantages_1': translate('save_time_advantages_1', language),
            'advantages_2': translate('avoid_delays_cuts_and_fines', language),
            'advantages_3': translate('receive_all_information_and_tickets_in_one_place', language),
            'service_hover_text': translate('oi_title_about_the_service', language)
        },
    }
    if get_all_variables:
        return standard_variables

    if automation_name in standard_variables:
        return standard_variables[automation_name]
    return {}


@register.filter
def get_dashboard_infos(request, date_to, date_from, language):
    not_translated = False
    areas = uipath_logs.models.Areas.listAllColumnsTypes(
        request.user.profile.client)
    number_of_areas = len(areas['areas'])
    if str(request.user.profile.client) == 'Test' or str(request.user.profile.client) == 'Smarthis':
        date_from = date_to - timedelta(days=360)
        processes_registered = uipath_logs.models.Job.listAllColumnsTypes(
            date_from, date_to, 'processes', 'ReleaseName', request.user.profile.client)
        processes_translated = uipath_logs.models.Processos.listAllColumnsTypes(
            request.user.profile.client)
        processes_filter = {
            'title': translate('process', language),
            'inputs': processes_registered,
            'areas': areas,
        }
        force_test_client = Client.objects.get(
            name='Test', company__razao_social='Smarthis Test')
        fakejson = getFakeJson(force_test_client, date_to, date_from, language)
        infos_dashboard = {
            'fakejson': json.dumps(fakejson),
            'test': True,
            'language': language,
            'all_filters': fakejson['update_infos']['all_filters'],
            'date_to': date_to.strftime('%Y-%m-%d'),
            'date_from': date_from.strftime('%Y-%m-%d'),
            'not_translated': not_translated,
            'processes_filter': processes_filter,
            'processes_translated': processes_translated['dict'],
            'number_of_areas': number_of_areas
        }
    else:
        subprocess_registered = uipath_logs.models.SubProcessos.getSubProcessesInfosByClient(
            request.user.profile.client)
        processes_translated = uipath_logs.models.Processos.listAllColumnsTypes(
            request.user.profile.client)
        processes_filter = {
            'title': translate('process', language),
            'inputs': subprocess_registered,
            'areas': areas,
        }
        all_areas = areas['areas']
        all_status = uipath_logs.models.Job.listAllColumnsTypes(
            date_from, date_to, 'status', 'State', request.user.profile.client)
        all_robots = uipath_logs.models.Job.listAllColumnsTypes(
            date_from, date_to, 'robots', 'HostMachineName', request.user.profile.client)

        filters_processes_input = []
        for ReleaseName, subprocess in subprocess_registered.items():
            if subprocess['name'] not in filters_processes_input:
                filters_processes_input.append(
                    subprocess['name'])

        all_filters = {
            'area': {
                'title': translate('business_area', language),
                'inputs': all_areas,
            },
            'process': {
                'title': translate('process', language),
                'inputs': filters_processes_input,
            },
            'status': {
                'title': translate('status', language),
                'inputs': all_status,
            },
            'robot': {
                'title': translate('host_machine', language),
                'inputs': all_robots,
            }
        }

        not_translated = True
        if len(processes_translated['dict']) > len(processes_translated['incomplete_processes']):
            not_translated = False
        infos_dashboard = {
            'all_filters': all_filters,
            'processes_filter': processes_filter,
            'processes_translated': processes_translated['dict'],
            'language': language,
            'date_to': date_to.strftime('%Y-%m-%d'),
            'date_from': date_from.strftime('%Y-%m-%d'),
            'not_translated': not_translated,
            'number_of_areas': number_of_areas
        }

    return infos_dashboard


@register.filter
def getFakeJson(client, date_to, date_from, language):
    process_to_area = []
    processes_registered = uipath_logs.models.Job.listAllColumnsTypes(
        date_from, date_to, 'processes', 'ReleaseName', client)
    processes_translated = uipath_logs.models.Processos.listAllColumnsTypes(
        client)
    for index, p in enumerate(processes_registered):
        if p in processes_translated['dict']:
            process_to_area.append(
                {'name': processes_translated['dict'][p]['name'], 'area': processes_translated['dict'][p]['area']})
        else:
            process_to_area.append({'name': p, 'area': ''})

    # all_areas = {
    #     "areas":["Rebocadores", "Juridico", "Financeiro", "RH"],
    #     "id":[31, 32, 34, 35]
    # }
    all_areas = uipath_logs.models.Areas.listAllColumnsTypes(client)
    all_status = {
        0: "Faulted",
        1: "Faulted",
        2: "Stopped",
        3: "Successful",
        4: "Successful",
        5: "Successful",
        6: "Successful",
        7: "Successful",
        8: "Successful",
        9: "Successful",
        10: "Successful",
        11: "Successful",
        12: "Successful",
        13: "Successful",
        14: "Successful"
    }
    all_robots = ["AZBR-RPA-DESK1", "WSMZRPAROBNAT01"]
    res = {
        "all_areas": all_areas,
        "all_processes": {
            0: "BANCODOC_PROD01",
            1: "Boletos_Avulso_Contas",
            2: "CORP_PROJ_AVALARA_PROD01",
            3: "CORP_SUPRIMENTOS_ATUALIZACAO_MRP_PROD02",
            4: "CORP_TAX_ISS_RETIDO_PROD01",
            5: "DISPATCHER_TUG_DIGITACAO_SAMA_PROD02",
            6: "Manutencao_PROD01",
            7: "PERFORMER_TUG_DIGITACAO_SAMA_PROD01",
            8: "RDF_Dispatcher_Consumer_PROD01",
            9: "REBOCADORES_STATE_EMISSAO_NOTAS_PROD02",
            10: "Relatorio_Boletos_Avulso_PowerBI_Contas_a_Receber"
        },
        "all_status": all_status,
        "all_robots": all_robots,
        "all_average": ["12_AM", "01_AM", "02_AM", "03_AM", "04_AM", "05_AM", "06_AM", "07_AM", "08_AM", "09_AM", "10_AM", "11_AM", "12_PM", "01_PM", "02_PM", "03_PM", "04_PM", "05_PM", "06_PM", "07_PM", "08_PM", "09_PM", "10_PM", "11_PM"],
        "dates": {},
        "update_infos": {
            "all_filters": {
                'area': {
                    'title': translate('business_area', language),
                    'inputs': []
                },
                'process': {
                    'title': translate('process', language),
                    'inputs': []
                },
                'status': {
                    'title': translate('status', language),
                    'inputs': []
                },
                'robot': {
                    'title': translate('host_machine', language),
                    'inputs': []
                }
            },
            "date_from": date_from.strftime('%Y-%m-%d'),
            "date_to": date_to.strftime('%Y-%m-%d'),
            "language": language,
            "processes_filter": {
                'title': translate('process', language),
                'areas': {
                    'areas': [],
                    'id': []
                },
                'inputs': []
            }
        }
    }
    if len(process_to_area) > 0:
        i = 0
        # if isinstance(date_from, datetime):
        #     print(date_to , date_from.date(), date_from)
        #     days = (date_to - date_from.date()).days
        # else:
        days = (date_to - date_from).days
        while i < days:
            date_from = date_to - timedelta(days=i)
            dateindex = date_from.strftime('%Y_%m_%d')
            res['dates'][dateindex] = {
                'date': date_from.strftime('%Y-%m-%d'),
                'processes': {}
            }
            qntprocesses = randint(0, 10)
            j = 0
            while j < qntprocesses:
                processindex = randint(0, 10)
                robotindex = randint(0, 1)
                statusindex = randint(0, 14)
                area = ''
                if process_to_area[processindex]['area'] != '':
                    area = process_to_area[processindex]['area']
                    if area not in res['update_infos']['all_filters']['area']['inputs']:
                        res['update_infos']['all_filters']['area']['inputs'].append(
                            area)
                        res['update_infos']['processes_filter']['areas']['areas'].append(
                            area)
                        if area in all_areas['areas']:
                            index = all_areas['areas'].index(area)
                            res['update_infos']['processes_filter']['areas']['id'].append(
                                all_areas['id'][index])

                # adding to possible filters
                if process_to_area[processindex]['name'] not in res['update_infos']['all_filters']['process']['inputs']:
                    res['update_infos']['all_filters']['process']['inputs'].append(
                        process_to_area[processindex]['name'])
                    res['update_infos']['processes_filter']['inputs'].append(
                        process_to_area[processindex]['name'])

                if res['all_status'][statusindex] not in res['update_infos']['all_filters']['status']['inputs']:
                    res['update_infos']['all_filters']['status']['inputs'].append(
                        res['all_status'][statusindex])
                if res['all_robots'][robotindex] not in res['update_infos']['all_filters']['robot']['inputs']:
                    res['update_infos']['all_filters']['robot']['inputs'].append(
                        res['all_robots'][robotindex])

                res['dates'][dateindex]['processes'][res['all_processes'][processindex]] = {
                    'area': area,
                    'averageoccupation_byday': {},
                    'human_time': 0,
                    'process': process_to_area[processindex]['name'],
                    'qnt': 0,
                    'robot': res['all_robots'][robotindex],
                    'status': res['all_status'][statusindex],
                    'time': 0
                }
                this_process = res['dates'][dateindex]['processes'][res['all_processes'][processindex]]
                howmany_days = randint(1, 24)
                z = 0
                while z < howmany_days:
                    hour_index = randint(0, 23)
                    hour_index = res['all_average'][hour_index]
                    time = uniform(0, 1080)
                    qnt = randint(1, 64)
                    this_process['qnt'] += qnt
                    this_process['time'] += time
                    human_multiplier = uniform(1, 3)
                    this_process['human_time'] += human_multiplier * (time/60)
                    this_process['averageoccupation_byday'][hour_index] = {
                        'qnt': qnt, 'total_occupation_byhour': time}
                    z += 1
                print('-------------', res['dates'][dateindex]
                      ['processes'][res['all_processes'][processindex]])
                print('-------------')
                j += 1
            i += 1
    return res


@register.filter
def generateJobsFromJson(jobs_json, context_name):
    res = {}
    c = uipath_logs.models.Context.objects.get(customer__name=context_name)
    count = 0
    for job in jobs_json:
        nj = uipath_logs.models.Job(Context=c, Key=job['Key'], Id=job['Id'], ReleaseVersionId=job['ReleaseVersionId'], StartingScheduleId=job['StartingScheduleId'], StartTime=job['StartTime'], EndTime=job['EndTime'], CreationTime=job['CreationTime'], State=job['State'], Source=job['Source'], SourceType=job['SourceType'], BatchExecutionKey=job['BatchExecutionKey'],
                                    Info=job['Info'], ReleaseName=job['ReleaseName'], Type=job['Type'], OutputArguments=job['OutputArguments'], HostMachineName=job['HostMachineName'], HasMediaRecorded=job['HasMediaRecorded'], InputArguments=job['InputArguments'], PersistenceId=job['PersistenceId'], ResumeVersion=job['ResumeVersion'], StopStrategy=job['StopStrategy'])
        nj.save()
        count += 1
    return True


@register.filter
def generateFakeProcesses(client=None):
    fakeprocesses = {
        "BANCODOC_PROD01": "AZBR-RPA-DESK1",
        "Boletos_Avulso_Contas": "AZBR-RPA-DESK1",
        "CORP_PROJ_AVALARA_PROD01": "AZBR-RPA-DESK1",
        "CORP_SUPRIMENTOS_ATUALIZACAO_MRP_PROD02": "AZBR-RPA-DESK1",
        "CORP_TAX_ISS_RETIDO_PROD01": "WSMZRPAROBNAT01",
        "DISPATCHER_TUG_DIGITACAO_SAMA_PROD02": "WSMZRPAROBNAT01",
        "Manutencao_PROD01": "WSMZRPAROBNAT01",
        "PERFORMER_TUG_DIGITACAO_SAMA_PROD01": "WSMZRPAROBNAT01",
        "RDF_Dispatcher_Consumer_PROD01": "WSMZRPAROBNAT01",
        "REBOCADORES_STATE_EMISSAO_NOTAS_PROD02": "WSMZRPAROBNAT01",
        "Relatorio_Boletos_Avulso_PowerBI_Contas_a_Receber": "WSMZRPAROBNAT01"
    }
    customer_context = uipath_logs.models.Context.objects.filter(
        customer=client)
    for index, proc in enumerate(fakeprocesses):
        if index > 4:
            status = 'Successful'
        elif index == 2:
            status = 'Faulted'
        else:
            status = 'Stopped'
        nj = uipath_logs.models.Job(Context=customer_context[0], Key='026a2145-9b90-4f3b-te'+str(index)+'-ea81cbb1d04c', Id=(2400620 + index), ReleaseVersionId=23886, StartingScheduleId=3155, StartTime='2020-11-16 07:06:56.167000+00:00', EndTime='2020-11-16 07:07:27.010000+00:00', CreationTime='2020-11-16 07:00:18.460000+00:00', State=status,
                                    Source='Acordar', SourceType='Schedule', BatchExecutionKey='d5cc9507-8c01-438c-te'+str(index)+'-3715d51d67f6', Info='Job completed', ReleaseName=proc, Type='Unattended', OutputArguments={}, HostMachineName=fakeprocesses[proc], HasMediaRecorded=False, InputArguments=None, PersistenceId=None, ResumeVersion=None, StopStrategy=None)
        nj.save()


@register.filter
def isClientMainUser(user):
    return (user.profile.role == 4 or user.profile.role == 3)


@register.filter
def getUsersfromClients(request, client):
    if request == False:
        return Profile.objects.filter(client=client)
    else:
        return Profile.objects.filter(client=request.user.profile.client)


@register.filter
def getRoleDashboardAccess():
    return [3, 4, 5, 6]


@register.filter
def getAllDashboardUsersFromClient(request, client):
    all_dashboard_users = getRoleDashboardAccess()
    if request == False:
        return Profile.objects.filter(client=client, role__in=all_dashboard_users)
    else:
        return Profile.objects.filter(client=request.user.profile.client, role__in=all_dashboard_users)


@register.filter
def getClientMainUserInfo(request):
    main_user = Profile.objects.filter(
        client=request.user.profile.client, role=4)
    if len(main_user) > 0:
        return main_user.first().user
    else:
        return False


@register.filter
def getStringFromDictionary(item):
    return json.dumps(item)


@register.filter
def commaDecimalEnd(infos, language):
    # infos = number | howmany_decimal | force_decimal

    infos_splitted = infos.split(' | ')

    number = infos_splitted[0]
    if len(infos_splitted) == 3:
        howmany_decimal = int(infos_splitted[1])
        force_decimal = bool(infos_splitted[2])
    elif len(infos_splitted) == 2:
        howmany_decimal = int(infos_splitted[1])
        force_decimal = False
    else:
        howmany_decimal = 2
        force_decimal = False

    res = ""
    splitted = str(number).split(".")
    regex = "(\d)(?=(\d{3})+(?!\d))"
    if language == 'pt-BR':
        res = re.sub(regex, r"\1.", splitted[0])
        if len(splitted) > 1:
            res += f',{splitted[1][:howmany_decimal]}'
        elif force_decimal and howmany_decimal > 0:
            res += ','
            for i in range(0, howmany_decimal):
                res += '0'
    else:
        res = re.sub(regex, r"\1,", splitted[0])
        if len(splitted) > 1:
            res += f'.{splitted[1][:howmany_decimal]}'
        elif force_decimal and howmany_decimal > 0:
            res += '.'
            for i in range(0, howmany_decimal):
                res += '0'

    if force_decimal and len(splitted) > 1 and len(splitted[1]) < howmany_decimal:
        for i in range(0, (howmany_decimal - len(splitted[1]))):
            res += '0'

    return res


def get_all_months_object(language):
    return [
        {'month': translate('january', language),
         'active': False, 'number': '1'},
        {'month': translate('february', language),
         'active': False, 'number': '2'},
        {'month': translate('march', language),
         'active': False, 'number': '3'},
        {'month': translate('april', language),
         'active': False, 'number': '4'},
        {'month': translate('may', language), 'active': False, 'number': '5'},
        {'month': translate('june', language), 'active': False, 'number': '6'},
        {'month': translate('july', language), 'active': False, 'number': '7'},
        {'month': translate('august', language),
         'active': False, 'number': '8'},
        {'month': translate('september', language),
         'active': False, 'number': '9'},
        {'month': translate('october', language),
         'active': False, 'number': '10'},
        {'month': translate('november', language),
         'active': False, 'number': '11'},
        {'month': translate('december', language),
         'active': False, 'number': '12'},
    ]


@register.filter
def getAllowedYearsDashboard(language, date=''):
    initial_year = 2019
    all_years = []
    now = datetime.now()
    if date != '' and type(date) is datetime:
        now = date
    elif date != '':
        now = datetime.strptime(date, '%Y-%m-%d')

    while initial_year <= now.year:
        all_years.append(initial_year)
        initial_year += 1

    all_months = get_all_months_object(language)

    all_months[now.month - 1]['active'] = True

    return {'all_years': all_years, 'all_months': all_months, 'date': now.day, 'month_year': all_months[now.month-1]['month'] + ' ' + str(now.year), 'date_string': now.strftime('%d/%m/%Y')}


@register.filter
def getAllowedYearsDashboard(language, date=''):
    initial_year = 2019
    all_years = []
    now = datetime.now()
    if date != '' and type(date) is datetime:
        now = date
    elif date != '':
        now = datetime.strptime(date, '%Y-%m-%d')

    this_year = datetime.now()

    while initial_year <= this_year.year:
        all_years.append(initial_year)
        initial_year += 1

    all_months = [
        {'month': translate('january', language),
         'active': False, 'number': '1'},
        {'month': translate('february', language),
         'active': False, 'number': '2'},
        {'month': translate('march', language),
         'active': False, 'number': '3'},
        {'month': translate('april', language),
         'active': False, 'number': '4'},
        {'month': translate('may', language), 'active': False, 'number': '5'},
        {'month': translate('june', language), 'active': False, 'number': '6'},
        {'month': translate('july', language), 'active': False, 'number': '7'},
        {'month': translate('august', language),
         'active': False, 'number': '8'},
        {'month': translate('september', language),
         'active': False, 'number': '9'},
        {'month': translate('october', language),
         'active': False, 'number': '10'},
        {'month': translate('november', language),
         'active': False, 'number': '11'},
        {'month': translate('december', language),
         'active': False, 'number': '12'},
    ]

    all_months[now.month - 1]['active'] = True

    return {'all_years': all_years, 'all_months': all_months, 'date': now.day, 'month_year': all_months[now.month-1]['month'] + ' ' + str(now.year), 'date_string': now.strftime('%d/%m/%Y'), 'selected_year': now.year}


@register.filter
def getAllDashboardSelectOptions(language):
    select_options = {
        'all-occupation-robot-select-order': [
            {'value': 'hour', 'text': translate(
                'hour', language), 'selected': False},
            {'value': 'day', 'text': translate(
                'day', language), 'selected': True},
            {'value': 'week', 'text': translate(
                'week', language), 'selected': False},
            {'value': 'month', 'text': translate(
                'month_capital', language), 'selected': False},
        ],
        'rpa-execution-history-detail': [
            {'value': 'day', 'text': translate(
                'day', language), 'selected': False},
            {'value': 'month', 'text': translate(
                'month_capital', language), 'selected': True},
        ],
        'robot-occupation-time-band-select-order': [
            {'value': 'general', 'text': translate(
                'general_rate', language), 'selected': True},
            {'value': 'single', 'text': translate(
                'individual_rate', language), 'selected': False},
        ],
        'all-processes-select-order': [
            {'value': 'returnInHours', 'text': translate(
                'time_reduction', language), 'selected': True},
            {'value': 'operatorHours', 'text': translate(
                'employee_working_hours', language), 'selected': False},
            {'value': 'rpaHours', 'text': translate(
                'rpa_runtime', language), 'selected': False},
        ],
        'all-areas-select-order': [
            {'value': 'returnInHours', 'text': translate(
                'time_reduction', language), 'selected': True},
            {'value': 'operatorHours', 'text': translate(
                'employee_working_hours', language), 'selected': False},
            {'value': 'rpaHours', 'text': translate(
                'rpa_runtime', language), 'selected': False},
        ],
        'returned-hours-process-select': [
            {'value': 'smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'returned-hours-areas-select': [
            {'value': 'smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'hours-returned-history-select': [
            {'value': 'month', 'text': translate(
                "month", language).capitalize(), 'selected': True},
            {'value': 'day', 'text': translate(
                "day", language).capitalize(), 'selected': False},
        ],
        'rpa-history-select': [
            {'value': 'month', 'text': translate(
                "month", language).capitalize(), 'selected': True},
            {'value': 'day', 'text': translate(
                "day", language).capitalize(), 'selected': False},
        ],
        'rpa-process-select': [
            {'value': 'smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'rpa-area-select': [
            {'value': 'smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'roi-process-order': [
            {'value': 'roi_smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'roi_bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'roi-area-order': [
            {'value': 'roi_smaller', 'text': translate(
                "smallest", language), 'selected': True},
            {'value': 'roi_bigger', 'text': translate(
                "larger", language), 'selected': False},
        ],
        'roi-history-order': [
            {'value': 'roi_month', 'text': translate(
                "month", language).capitalize(), 'selected': True},
            {'value': 'roi_day', 'text': translate(
                "day", language).capitalize(), 'selected': False},
        ]
    }
    return select_options


def getAllFutureAutomations(language):
    return {
        'geracao-download-nfe': {
            'name': translate('nfe_generation_and_download', language),
            'info': translate('text_nfe_generation_and_download', language),
            'interested': False
        },
        'conciliacao-bancaria': {
            'name': translate('bank_reconciliation', language),
            'info': translate('text_bank_reconciliation', language),
            'interested': False
        },
        'verificacao-presenca-assinatura-documentos': {
            'name': translate('checking_presence_of_signature_on_documents', language),
            'info': translate('text_checking_presence_of_signature_on_documents', language),
            'interested': False
        },
        'processamento-inteligente-documentos': {
            'name': translate('intelligent_document_processing', language),
            'info': translate('text_intelligent_document_processing', language),
            'interested': False
        },
        'algoritmo-recomendacao-ecommerce': {
            'name': translate('recomendation_algorithm_ecommerce', language),
            'info': translate('text_recomendation_algorithm_ecommerce', language),
            'interested': False
        },
        'chatbot': {
            'name': 'Chatbot',
            'info': translate('text_chatbot', language),
            'interested': False
        },
        'verificacao-decretos-portarias': {
            'name': translate('verification_of_decrees_ordinances', language),
            'info': translate('text_verification_of_decrees_ordinances', language),
            'interested': False
        },
        'dashboards-integrados-ecommerce': {
            'name': translate('integrated_dashboards_ecommerce', language),
            'info': translate('text_integrated_dashboards_ecommerce', language),
            'interested': False
        }

    }


# @register.filter
# def merge_dicts(dict1, dict2):
#     new_dict = deepcopy(dict1)
#     new_dict.update(dict2)
#     return new_dict

def merge_dicts(dictionaries: list) -> dict:
    '''Merges dictionaries'''

    super_dict = defaultdict(set)
    for d in dictionaries:
        for k, v in d.items():
            super_dict[k] = v
    super_dict = dict(super_dict)
    return super_dict


@register.filter
def merge_lists(list1, list2):
    new_list = deepcopy(list1)
    new_list.extend(list2)
    return new_list


def get_people_to_send_email(type='product'):
    people = ['guilherme.favoreto@smarthis.com.br',
              'rodrigo.ferreira@smarthis.com.br', 'rayane.gomes@smarthis.com.br']
    if type == 'devs':
        people = ['bruno.marques@smarthis.com.br',
                  'mariana.reis@smarthis.com.br']
    return people


def reset_jobs_cache(client, date_from, date_to):
    all_areas_key = "all_areas_" + str(client).replace(' ', '_')
    reset_cache(all_areas_key)

    all_processes_key = "all_processes_" + str(client).replace(' ', '_')
    reset_cache(all_processes_key)

    all_subprocesses_key = "all_subprocesses_" + str(client).replace(' ', '_')
    reset_cache(all_subprocesses_key)

    sec_date_to = datetime.today().date()
    if str(client) == 'Elopar':
        sec_date_from = datetime.strptime('2020-01-01', '%Y-%m-%d')
    else:

        sec_date_from = sec_date_to - timedelta(days=90)

    jobs_key = "jobs_" + sec_date_from.strftime('%Y-%m-%d') + "_" + sec_date_to.strftime(
        '%Y-%m-%d') + "_" + str(client).replace(' ', '_')
    reset_cache(jobs_key)

    jobs_second_key = "jobs_" + date_from + "_" + date_to + \
        "_" + str(client).replace(' ', '_')
    reset_cache(jobs_second_key)

    return True


def get_dashboard_processes_info(subprocesses_info):
    data = {}
    for subprocess in subprocesses_info:
        process_id = subprocesses_info[subprocess].get('process_id')
        try:
            process = uipath_logs.models.Processos.objects.get(
                pk=process_id)
        except uipath_logs.models.Processos.DoesNotExist:
            continue
        investment = process.project_cost
        monthly_tasks = process.get_quantity_of_monthly_tasks(
        )
        minutes_in_task = process.get_duration_time()
        average_hour_value = process.get_average_hour_value()
        roi, manual_process_cost = calculate_process_roi(investment=investment, monthly_tasks=monthly_tasks,
                                                         minutes_in_task=minutes_in_task, average_hour_value=average_hour_value)
        if not roi or not manual_process_cost:
            continue
        info = {
            'investment': investment,
            'roi': roi,
            'manual_process_cost': manual_process_cost,
            'monthly_tasks': monthly_tasks,
            'minutes_in_task': minutes_in_task,
            'average_hour_value': average_hour_value
        }
        if not data.get(process.name, None):
            data[process.name] = info

    return data


def calculate_process_roi(investment, monthly_tasks, minutes_in_task, average_hour_value):
    if not monthly_tasks or not minutes_in_task or not average_hour_value or not investment:
        return (False, False)

    manual_process_cost = (
        (monthly_tasks * minutes_in_task) / 60) * float(average_hour_value)

    roi = (manual_process_cost - investment) / investment
    return (roi, manual_process_cost)
