from typing import Union
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.query_utils import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
import uuid
from portal.functions import reset_cache
from subscriptions.validators import validate_cnpj_when_created
import re
from datetime import datetime
from validate_docbr import CNPJ
import json
import urllib.request as ur
import pytz
import uuid


class Companies(models.Model):
    cnpj = models.CharField(max_length=14, unique=True,
                            validators=[validate_cnpj_when_created])
    razao_social = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        if not self.validate_cnpj(self.cnpj):
            raise ValidationError("The CNPJ informed is invalid")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.razao_social

    def get_cnpj(self) -> str:
        return self.cnpj

    def get_formatted_cnpj(self) -> str:
        cnpj_util = CNPJ()
        return cnpj_util.mask(self.cnpj)

    def set_cnpj(self, value: str) -> Union[None, Exception]:
        if self.validate_cnpj(value):
            self.cnpj = self.clean_cnpj(value)

        else:
            raise ValidationError("The CNPJ informed is invalid")

    def get_razao_social(self) -> str:
        return self.razao_social

    def set_razao_social(self, value: str) -> None:
        self.razao_social = value.strip()

    def validate_cnpj(self=None, cnpj: str = '') -> bool:
        cnpj_util = CNPJ()
        return cnpj_util.validate(cnpj)

    def clean_cnpj(self, cnpj: str) -> str:
        cleaned = re.sub('[^0-9]', '', cnpj.strip())
        return cleaned


class Client(models.Model):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(
        Companies, on_delete=models.DO_NOTHING, null=True, blank=True)
    domain = models.CharField(max_length=100, default='-')
    identifier = models.CharField(
        max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_client_name(self):
        return self.name

    def set_name(self, name):
        self.name = name.trim()

    def get_company(self):
        return self.company

    def set_company(self, company):
        self.company = company


class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class Plan(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # TODO: depois que atualizar os planos em prod apagar esse campo (with_dashboard)
    with_dashboard = models.BooleanField(default=False)
    qnt_automations = models.IntegerField(null=False, blank=False, default=10)
    value = models.DecimalField(decimal_places=2, max_digits=10, default=200)
    qnt_queries = models.IntegerField(null=False, blank=False, default=0)
    qnt_extra_queries = models.IntegerField(null=False, blank=False, default=0)
    extra_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=50)

    def __str__(self):
        return self.name

    def get_plan_name(self):
        return self.name

    def set_plan_name(self, name):
        self.name = name

    def get_plan_qnt_automations(self):
        return self.qnt_automations

    def get_value(self) -> str:
        return self.value

    def get_plan_qnt_queries(self):
        return self.qnt_queries

    def get_plan_qnt_extra_queries(self):
        return self.qnt_extra_queries

    def get_extra_price(self) -> str:
        return self.extra_price

    def set_value(self, new_value):
        self.value = new_value

    def update_plans():
        try:
            new_starter_plan = Plan.objects.get(name='Starter')
        except Plan.DoesNotExist:
            new_starter_plan = Plan.objects.create(name='Starter', qnt_automations=1, value=149.0,
                                                   qnt_queries=3000, qnt_extra_queries=6000, extra_price=50)

        try:
            new_advanced_plan = Plan.objects.get(name='Advanced')
        except Plan.DoesNotExist:
            new_advanced_plan = Plan.objects.create(name='Advanced', qnt_automations=3, value=499.0,
                                                    qnt_queries=9000, qnt_extra_queries=11000, extra_price=200)

        try:
            new_business_plan = Plan.objects.get(name='Business')

        except Plan.DoesNotExist:
            new_business_plan = Plan.objects.create(name='Business',  qnt_automations=0, value=0,
                                                    qnt_queries=0, qnt_extra_queries=0, extra_price=0)

        try:
            new_free_trial_plan = Plan.objects.get(name='Free Trial')
        except Plan.DoesNotExist:
            new_free_trial_plan = Plan.objects.create(name='Free Trial',  qnt_automations=0, value=0,
                                                      qnt_queries=0, qnt_extra_queries=0, extra_price=0)

        try:
            new_business_trial_plan = Plan.objects.get(name='Business Trial')

        except Plan.DoesNotExist:
            new_business_trial_plan = Plan.objects.create(name='Business Trial',  qnt_automations=0, value=0,
                                                          qnt_queries=0, qnt_extra_queries=0, extra_price=0)

        old_plans = Plan.objects.filter(Q(name__startswith='starter') | Q(
            name__startswith='advanced') | Q(name__startswith='business') | Q(name__startswith='free_trial'))

        for plan in old_plans:
            if 'starter' in plan.name:
                desired_plan = new_starter_plan
            elif 'advanced' in plan.name:
                desired_plan = new_advanced_plan
            elif 'business_trial' in plan.name:
                desired_plan = new_business_trial_plan
            elif 'business' in plan.name:
                desired_plan = new_business_plan
            elif 'free_trial' in plan.name:
                desired_plan = new_free_trial_plan

            subscriptions = Subscription.objects.filter(plan=plan)
            for subscription in subscriptions:
                subscription.set_subscription_plan(desired_plan)
                subscription.set_number_of_hired_services(
                    plan.qnt_automations)
                subscription.set_dashboard(plan.with_dashboard)
                subscription.set_value(plan.value)

                if 'monthly' in plan.name:
                    subscription.set_payment_period('MONTHLY')
                elif 'anual' in plan.name or 'annual' in plan.name:
                    subscription.set_payment_period('YEARLY')

                if 'plus' in plan.name:
                    subscription.set_extra_queries(True)

                subscription.save()

        # Melhor não deletar caso dê algum problema
        # old_plans.delete()


class Subscription(models.Model):
    class Period(models.TextChoices):
        MONTHLY = 'MONTHLY', "Monthly"
        YEARLY = 'YEARLY', "Yearly"

    begin = models.DateField(default=datetime.now)
    end = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    value = models.DecimalField(decimal_places=2, max_digits=10, default=200)
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, db_index=True)
    client = models.OneToOneField(
        Client, on_delete=models.DO_NOTHING, db_index=True)
    trial_period = models.SmallIntegerField(default=14)
    with_dashboard = models.BooleanField(default=False)
    number_of_hired_services = models.IntegerField(
        null=False, blank=False, default=1)
    payment_period = models.CharField(
        choices=Period.choices, default=Period.MONTHLY, max_length=10)
    queries_limit = models.IntegerField(null=False, blank=False, default=0)
    extra_queries = models.BooleanField(default=False)
    status = models.CharField(default='trialing', max_length=30)

    def __str__(self):
        return "%s - [%s] " % (self.client, self.plan.name)

    def get_begin(self):
        return self.begin

    def set_begin(self, time):
        if isinstance(time, datetime):
            if time.tzinfo is None:
                brasa_timezone = pytz.timezone('America/Sao_Paulo')
                time = brasa_timezone.localize(time)
            self.begin = time

    def get_end(self):
        return self.end

    def set_end(self, time):
        if isinstance(time, datetime):
            if time.tzinfo is None:
                brasa_timezone = pytz.timezone('America/Sao_Paulo')
                time = brasa_timezone.localize(time)
            self.end = time
        elif time == None:
            self.end = time

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_subscription_plan(self):
        return self.plan

    def set_subscription_plan(self, plan):
        self.plan = plan

    def get_client(self):
        return self.client

    def get_trial_period(self):
        return self.trial_period

    def set_trial_period(self, trial_period):
        self.trial_period = trial_period

    def get_dashboard(self):
        return self.with_dashboard

    def set_dashboard(self, dashboard):
        self.with_dashboard = dashboard

    def get_number_of_hired_services(self):
        return self.number_of_hired_services

    def set_number_of_hired_services(self, number_of_hired_services):
        self.number_of_hired_services = number_of_hired_services

    def get_payment_period(self):
        return self.payment_period

    def set_payment_period(self, period):
        self.payment_period = period

    def get_queries_limit(self):
        return self.queries_limit

    def set_queries_limit(self, queries_limit):
        self.queries_limit = queries_limit

    def get_extra_queries(self):
        return self.extra_queries

    def set_extra_queries(self, extra_queries):
        self.extra_queries = extra_queries

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def getSubscriptionByClient(client):
        try:
            key = f'subscription_client_{str(client.id)}'
            subscription = cache.get(key)
            if subscription == None:
                subscription = Subscription.objects.get(client=client)
                cache.set(key, subscription, 86400)
        except ObjectDoesNotExist:
            subscription = None
        finally:
            return subscription

    def resetSubscriptionByClient(client):
        key = f'subscription_client_{str(client.id)}'
        return reset_cache(key, 86400)

    def updateSubscriptionAfterPayment(response, client, begin, end, status):
        subscription = Subscription.getSubscriptionByClient(client)
        if subscription:
            subscription.set_end(end)
            subscription.set_begin(begin)
            subscription.set_status(status)
            try:
                subscription.save()
            except Exception as e:
                response = {'status': 403,
                            'msg': 'Error saving subscription', 'error': str(e)}
            finally:
                return response
        else:
            return {'status': 404, 'msg': 'Subscription not found'}

    def save(self, *args, **kwargs):
        key = f'subscription_client_{str(self.client.id)}'
        reset_cache(key, 86400)
        super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        # username besides of beeing used or not is inherited from AbstractUser,
        # so to avoid mistakes where someone query for a specific username em have,
        # all dataset, we are duplicating info username=email.
        username = uuid.uuid4()

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Auto generated uuid field'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    email = models.EmailField(
        ('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email


class Profile(models.Model):
    USER_ROLES = (
        (1, 'Service Account'),
        (2, 'Client'),
        (3, 'Admin'),
        (4, 'Main'),
        (5, 'Editor Account'),
        (6, 'View Account'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, null=True, blank=False, db_index=True)
    phone = models.CharField(null=True, max_length=100, blank=True)
    language = models.CharField(max_length=10, default='pt-BR')
    department = models.CharField(max_length=100, default='RH')
    job_title = models.CharField(max_length=100, default='Not provided')
    role = models.PositiveSmallIntegerField(
        choices=USER_ROLES, default=1, blank=False)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return ""

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def get_client(self):
        return self.client

    def set_client(self, client):
        self.client = client

    def get_phone(self):
        return self.phone

    def set_phone(self, phone):
        self.phone = phone

    def get_language(self):
        return self.language

    def set_language(self, language):
        self.language = language

    def get_department(self):
        return self.department

    def set_department(self, department):
        self.department = department

    def get_job_title(self):
        return self.job_title

    def set_job_title(self, job_title):
        self.job_title = job_title

    def get_role(self):
        return int(self.role)

    def set_role(self, role):
        self.role = role

    def get_email_confirmed(self):
        return self.email_confirmed

    def set_email_confirmed(self, confirmed):
        self.email_confirmed = confirmed

    def set_verified_emails():
        all_profiles = Profile.objects.all()
        for profile in all_profiles:
            profile.set_email_confirmed(True)
            profile.save()

    def get_user_by_email_and_client(email, client):
        profile = Profile.objects.filter(user__email=email, client=client)
        if len(profile) > 0:
            return profile.first()
        else:
            return {}


class AutomationsClients(models.Model):
    class Meta:
        verbose_name_plural = 'Automation clients'

    CREATE_MODEL_STATES = (
        (1, 'LIBERADO'),
        (2, 'AGUARDANDO'),
        (3, 'NÃO-LIBERADO'),
    )

    client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, null=True, blank=False, db_index=True)
    automation = models.ForeignKey(
        'smt_orchestrator.Automation', on_delete=models.DO_NOTHING, db_index=True)
    qnt_automations = models.IntegerField(null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    can_create_model = models.PositiveSmallIntegerField(
        choices=CREATE_MODEL_STATES, default=1, blank=False)

    def get_qnt_automations(self):
        return self.qnt_automations

    def subtract_qnt_automations(self, quantity=None):
        if quantity is None:
            self.qnt_automations -= 1
        else:
            self.qnt_automations -= quantity

    def get_can_create_model(self):
        return int(self.can_create_model)

    def getAutomationClientsByClient(client, order_by='automation__name'):
        key = f'automations_clients_order_by_{order_by}_{str(client.id)}'
        all_automations_contracted = cache.get(key)
        if not all_automations_contracted:
            all_automations_contracted = AutomationsClients.objects.values('automation__id', 'automation__name', 'qnt_automations', 'automation__active', 'automation__is_showcase').filter(
                client=client).order_by(order_by)
            cache.set(key, all_automations_contracted, 900)
        return all_automations_contracted

    def resetAutomationsClientsByClient(client):
        all_order_by = ['automation__name']
        all_done = True
        for order_by in all_order_by:
            try:
                key = f'automations_clients_order_by_{order_by}_{str(client.id)}'
                cache.set(key, None, 900)
            except Exception as e:
                all_done = False

        return all_done


class UsersPlans(models.Model):
    class Meta:
        verbose_name_plural = 'User plans'

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False, db_index=True)
    client = models.ForeignKey(
        Client, on_delete=models.DO_NOTHING, null=True, blank=False, db_index=True)
    automation = models.ForeignKey(
        'smt_orchestrator.Automation', on_delete=models.DO_NOTHING, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getUsersPlansByClientAndAutomationsIds(client, all_automations_id):
        key = f'all_users_plans_by_client_{str(client.id)}'
        all_users_plans = cache.get(key)
        if not all_users_plans:
            all_users_plans = UsersPlans.objects.filter(
                client=client, automation__id__in=all_automations_id)
            cache.set(key, all_users_plans, 900)
        return all_users_plans

    def resetUsersPlansByClientAndAutomationsIds(client):
        key = f'all_users_plans_by_client_{str(client.id)}'
        return reset_cache(key, 900)


class Invites(models.Model):
    class Meta:
        verbose_name_plural = 'Invites'

    email = models.EmailField(
        ('email address'),
        blank=False,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    token = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_email(self):
        return self.email

    def get_client(self):
        return self.client


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class SessionInfo(models.Model):
    session_start = models.DateTimeField(auto_now_add=False)
    session_end = models.DateTimeField(auto_now_add=False)
    session_duration = models.TimeField(auto_now_add=False)
    user_id = models.IntegerField(null=False, blank=False, default=0)
    user_ip_address = models.GenericIPAddressField(
        default=None, blank=True, null=True)


class PagarmePlans(models.Model):
    class Meta:
        verbose_name_plural = 'PagarmePlans'

    plan_pagarme_id = models.CharField(max_length=200)
    amount = models.DecimalField(
        decimal_places=2, max_digits=15, default=14900)  # amount is in pagarme format
    plan_pagarme_name = models.CharField(max_length=200)
    is_test = models.BooleanField(default=False)
    api_version = models.CharField(max_length=10, default='v4')
    created_at = models.DateTimeField(
        auto_now_add=True)

    def get_pagarme_plan_id(self):
        return self.plan_pagarme_id

    def get_pagarme_plan_name(self):
        return self.plan_pagarme_name

    def get_all_pagarme_plans_from_api(api_key, payload):
        array_payload = []
        for key, value in payload.items():
            array_payload.append(f'{key}={value}')

        url = f"https://api.pagar.me/1/plans?api_key={api_key}"

        if len(array_payload) > 0:
            join_string = '&'
            url += f"&{join_string.join(array_payload)}"

        response = ur.urlopen(url)
        plans = json.loads(response.read())
        for plan in plans:
            print(plan['name'], plan['amount'], plan['id'])
        return plans

    def update_all_plans_on_db_from_api(api_key):
        # TODO caso os planos já estejam criados na pagarme, atualizar essa tabela com os mesmos
        return {}


class PagarmeSubscriptions(models.Model):
    class Meta:
        verbose_name_plural = 'PagarmeSubscriptions'

    class PaymentTypes(models.TextChoices):
        credit_card = 'credit_card'
        boleto = 'boleto'

    client = models.OneToOneField(
        Client, on_delete=models.DO_NOTHING, db_index=True)
    subscription_pagarme_id = models.CharField(max_length=200)
    plan_pagarme_id = models.CharField(max_length=200)
    is_test = models.BooleanField(default=False)
    api_version = models.CharField(max_length=10, default='v4')
    created_at = models.DateTimeField(
        auto_now_add=True)
    current_period_start = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    current_period_end = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    payment_type = models.CharField(
        choices=PaymentTypes.choices, null=True, blank=True, default='credit_card', max_length=15)

    def get_pagarme_subscription_id(self):
        return self.subscription_pagarme_id

    def get_pagarme_subscription_plan_id(self):
        return self.plan_pagarme_id

    def set_pagarme_subscription_id(self, id):
        self.subscription_pagarme_id = id

    def set_pagarme_subscription_plan_id(self, plan_id):
        self.plan_pagarme_id = plan_id

    def get_current_period_start(self):
        return self.current_period_start

    def set_current_period_start(self, time):
        if isinstance(time, datetime):
            if time.tzinfo is None:
                brasa_timezone = pytz.timezone('America/Sao_Paulo')
                time = brasa_timezone.localize(time)
            self.current_period_start = time
        elif time == None:
            self.current_period_start = time

    def get_current_period_end(self):
        return self.current_period_end

    def set_current_period_end(self, time):
        if isinstance(time, datetime):
            if time.tzinfo is None:
                brasa_timezone = pytz.timezone('America/Sao_Paulo')
                time = brasa_timezone.localize(time)
            self.current_period_end = time
        elif time == None:
            self.current_period_end = time

    def get_payment_type(self):
        return self.payment_type

    def set_payment_type(self, payment_type):
        self.payment_type = payment_type

    def get_client(self):
        return self.client
