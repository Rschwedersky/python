import json
from django.test import Client as DjangoClient, TestCase
from subscriptions.models import AutomationsClients, Plan, Subscription, User, Client
from django.urls import reverse


class TestRegistration(TestCase):

    def setUp(self):
        self.client = DjangoClient()
        self.plan = Plan.objects.create(name='test')
        self.test_client = Client.objects.create(name='test')
        self.subscription = Subscription.objects.create(
            client=self.test_client, plan=self.plan)

    def test_if_user_can_register(self):
        # Registering
        response = self.client.post(reverse('new_account'), {
            'name': 'Registration Test',
            'email': 'testecadastro@testecadastro.com.br',
            'client': 'Company that tests registration',
            'password': 'senhaforte123A!',
            'department': 'RH',
            'job_title': 'Director',
            'user_role': 4
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)

        created_user = User.objects.get(
            email='testecadastro@testecadastro.com.br')

        created_client = created_user.profile.get_client()

        # Choosing services
        response = self.client.post(reverse('submit_registry'), {
            'with_dashboard': 1,
            'automations_allocated': json.dumps({
                'simples-nacional': 2,
                'iss-rj': 1
            })
        })

        # subscription = Subscription.objects.get(client=created_client)
        subscription = Subscription.getSubscriptionByClient(created_client)
        plan_name = 'Free Trial'

        self.assertEqual(
            subscription.get_subscription_plan().get_plan_name(), plan_name)
        self.assertTrue(
            subscription.get_dashboard())

        simples_nacional = AutomationsClients.objects.get(
            client=created_client, automation__name='simples-nacional')
        iss_rj = AutomationsClients.objects.get(
            client=created_client, automation__name='iss-rj')

        self.assertEqual(simples_nacional.get_qnt_automations(), 2)
        self.assertEqual(iss_rj.get_qnt_automations(), 1)

    def test_if_user_fails_to_register_with_invalid_email(self):
        response = self.client.post(reverse('new_account'), {
            'name': 'Registration Test',
            'email': 'testecadastro@testecadastro',
            'client': 'Company that tests registration',
            'password': 'senhaforte123A!',
            'department': 'RH',
            'job_title': 'Director',
            'user_role': 4
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
