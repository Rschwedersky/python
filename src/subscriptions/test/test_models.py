from unicodedata import name
from django.core.exceptions import ValidationError
from django.test import TestCase
import unittest
from subscriptions.models import AutomationsClients, Profile, Client, Companies, Plan, User, Service, Plan
# from subscriptions.models import AutomationsClients, Client, Plan, User, Service, Plan, Profile
from smt_orchestrator.models import Automation


class CompaniesTestCase(TestCase):
    def setUp(self):
        """ Populates DB before testing """
        Companies.objects.create(razao_social='test', cnpj='96127625000198')

    def test_if_company_is_created(self):
        test_company = Companies.objects.get(cnpj='96127625000198')
        self.assertEqual(test_company.get_razao_social(), "test")
        self.assertEqual(test_company.get_cnpj(), "96127625000198")

    def test_if_cnpj_is_validated_correctly(self):
        test_company_with_valid_cnpj = Companies.objects.get(
            cnpj='96127625000198')
        self.assertTrue(test_company_with_valid_cnpj.validate_cnpj(
            test_company_with_valid_cnpj.get_cnpj()))

    def test_if_cnpj_is_formatted_correctly(self):
        test_company = Companies.objects.get(cnpj='96127625000198')

        self.assertEqual(test_company.get_formatted_cnpj(),
                         '96.127.625/0001-98')

    def test_if_company_raises_error_when_created_with_invalid_cnpj(self):
        with self.assertRaises(ValidationError):
            Companies.objects.create(
                razao_social='test with invalid cnpj', cnpj='01234567890123')

    def test_if_cnpj_is_cleaned_correctly(self):
        test_company = Companies.objects.get(cnpj='96127625000198')
        test_company.set_cnpj('90.766.979/0001-04')

        self.assertEqual(test_company.get_cnpj(), '90766979000104')


class ClientTestCase(TestCase):
    def setUp(self):
        """ Populates DB before testing """
        Client.objects.create(name='client_test')

    def test_if_client_is_created(self):
        """ Client Instance can be created and its attributes retrieved"""
        test_client = Client.objects.get(name="client_test")
        self.assertEqual(test_client.get_client_name(), "client_test")

    def test_if_client_can_be_created_with_repeated_name(self):
        """ Client Instance can be created if there is another with the same name"""
        client_with_same_name = Client.objects.create(name="client_test")
        self.assertEqual(
            client_with_same_name.get_client_name(), "client_test")
        self.assertEqual(client_with_same_name.get_company(), None)


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            username='mariana',
            email='mariana.reis@smarthis.com'
        )

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)


class ServiceTestCase(TestCase):
    # check the return of the name method is the same
    def setUp(self):
        Service.objects.create(
            name='cpom',
            description='consulta cpom'
        )

    def test_service_str(self):
        return_name = Service.objects.get(name='cpom')
        return_desc = Service.objects.get(description='consulta cpom')
        self.assertEqual(return_name.get_name(), 'cpom')
        self.assertEqual(return_desc.get_description(), 'consulta cpom')


class PlanTestCase(TestCase):
    def setUp(self):
        Plan.objects.create(
            name='free_trial',
            with_dashboard=False,
            qnt_automations='3',
            value='0.00',
            qnt_queries='0',
            qnt_extra_queries='0',
            extra_price='0.00'
        )

    def test_plan_str(self):
        return_plan = Plan.objects.get(name='free_trial')
        self.assertEqual(return_plan.get_plan_name(), 'free_trial')


class ProfileTestCase(TestCase):
    def setUp(self):

        User.objects.create(
            username='beyonce',
            email='beyonce.hip@gmail.com.br'
        )

        Client.objects.create(
            name='Smarthis'
        )

    def test_profile(self):
        return_profile = Profile.objects.get(
            user__email='beyonce.hip@gmail.com.br')
        return_profile.set_department('RH')
        return_profile.set_role(3)
        self.assertEqual(return_profile.get_department(), 'RH')
        self.assertEqual(return_profile.get_role(), 3)
        self.assertEqual(return_profile.get_user().get_email(),
                         'beyonce.hip@gmail.com.br')


class AutomationsClientsTestCase(TestCase):
    def setUp(self):

        cliente_test = Client.objects.create(
            name='Elopar'
        )

        automation_test = Automation.objects.create(
            name='notas-servicos-rj',
            url='https://bot-cpom-sp_bot-api:5000',
            public_key='',
            active=True
        )

        AutomationsClients.objects.create(
            client=cliente_test,
            automation=automation_test,
            qnt_automations=5
        )

    def test_automations_clients(self):
        return_automation = AutomationsClients.objects.get(
            client__name='Elopar', automation__name='notas-servicos-rj')
        self.assertEqual(return_automation.get_qnt_automations(), 5)
        self.assertNotEqual(return_automation.get_qnt_automations(), 1)
