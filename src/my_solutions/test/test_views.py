import json
from django.test import Client as DjangoClient, TestCase
from django.test.testcases import SimpleTestCase, TransactionTestCase
from smt_orchestrator.models import Automation
from subscriptions.models import Invites, Plan, Subscription, User, Client, UsersPlans
from django.urls import reverse


class TestHomeViewTestCase(TestCase):
    def setUp(self):
        self.client = DjangoClient()
        self.user = User.objects.create(
            email='test@test.com', password='senhaforte123!', username="teste")
        self.test_client = Client.objects.create(name='test')
        self.user.profile.set_client(self.test_client)
        self.plan = Plan.objects.create(name='test')
        self.subscription = Subscription.objects.create(
            client=self.test_client, plan=self.plan)

    def test_if_anonymous_user_is_redirected_to_login(self):

        self.client.force_login(user=self.user)
        response = self.client.get('/', follow=True)
        '''Checking if logged user can access home '''
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        self.client.logout()
        response = self.client.get('/')
        '''Checking if anonymous user is redirected to login '''
        self.assertRedirects(response, reverse('login'))

    def test_if_get_user_works(self):
        self.client.force_login(user=self.user)

        response = self.client.generic('POST', reverse(
            'get_user_by_email_and_client'), json.dumps({'email': self.user.get_email()}))

        converted_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(converted_response['id'], self.user.get_id())


class TestInviteFromWithinPlatform(TransactionTestCase):
    def setUp(self):
        self.client = DjangoClient()

        self.admin_test_user = User.objects.create(
            email='test@testadmin.com', password='senhaforte123!', username="testeadmin")

        self.first_user = User.objects.create(
            email='test@test.com', password='senhaforte123!', username="teste1")

        self.second_user = User.objects.create(
            email='test@testagain.com', password='senhaforte123!', username="teste2")

        self.third_user = User.objects.create(
            email='test@testagainagain.com', password='senhaforte123!', username="teste3")

        self.test_client = Client.objects.create(name='test')

        self.test_automation = Automation.objects.create(name='cepom-rj')

        self.first_user.profile.set_client(self.test_client)
        self.second_user.profile.set_client(self.test_client)
        self.third_user.profile.set_client(self.test_client)
        self.admin_test_user.profile.set_client(self.test_client)

        self.plan = Plan.objects.create(name='test')
        self.subscription = Subscription.objects.create(
            client=self.test_client, plan=self.plan)

        self.first_user.profile.save()
        self.second_user.profile.save()
        self.third_user.profile.save()
        self.admin_test_user.profile.save()

        UsersPlans.objects.create(user=self.second_user, client=self.test_client,
                                  automation=self.test_automation)

        UsersPlans.objects.create(user=self.third_user, client=self.test_client,
                                  automation=self.test_automation)

        self.client.force_login(user=self.admin_test_user)

        self.response = self.client.post(reverse('manage_client_permissions'), {
            'all_users_add': json.dumps([self.first_user.id, 'testinvite@testinvite.com.br', self.third_user.id]),
            'all_users_remove': json.dumps([self.second_user.id]),
            'automation_name': self.test_automation.get_name()
        })

    def test_if_user_was_invited_and_license_added(self):
        invite = Invites.objects.get(
            email='testinvite@testinvite.com.br', client=self.test_client)
        self.assertTrue(invite)
        user_plan = UsersPlans.objects.get(
            user__email='testinvite@testinvite.com.br', client=self.test_client, automation=self.test_automation)

        self.assertTrue(user_plan)

    def test_if_license_was_added(self):
        user_plan = UsersPlans.objects.get(
            user=self.first_user, client=self.test_client, automation=self.test_automation)

        self.assertTrue(user_plan)

    def test_if_license_was_removed(self):
        with self.assertRaises(UsersPlans.DoesNotExist):
            UsersPlans.objects.get(
                user=self.second_user, client=self.test_client,
                automation=self.test_automation)

    def test_if_license_was_not_added_again_to_user_that_already_have_it(self):
        number_of_user_plans_of_third_user = UsersPlans.objects.filter(
            user=self.third_user, client=self.test_client, automation=self.test_automation).count()

        self.assertEqual(number_of_user_plans_of_third_user, 1)
