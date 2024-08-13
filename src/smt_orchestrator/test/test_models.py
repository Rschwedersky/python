from unicodedata import name
from django.test import TestCase
import unittest
from smt_orchestrator.models import Automation, FutureAutomation
from subscriptions.models import User


class AutomationTestCase(TestCase):

    def setUp(self):
        Automation.objects.create(
            name='notas-servicos-rj',
            url='https://bot-cpom-sp_bot-api:5000',
            public_key='',
            active=True
        )

    def test_automation_str(self):
        return_automation = Automation.objects.get(name='notas-servicos-rj')
        self.assertEqual(return_automation.get_name(), 'notas-servicos-rj')


class FutureAutomationTestCase(TestCase):
    def setUp(self):

        test_user = User.objects.create(
            username='cris',
            email='chis.brown@smarthis.com'
        )

        FutureAutomation.objects.create(
            name='Conciliação bancária',
            user=test_user
        )

    def test_futureAutomation(self):
        return_future_automation = FutureAutomation.objects.get(
            name='Conciliação bancária', user__username='cris')
        self.assertEqual(return_future_automation.get_name(),
                         'Conciliação bancária')
