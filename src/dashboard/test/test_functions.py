import unittest
from django.test import TestCase
from portal.templatetags.general_tags import translate
from dashboard.templatetags.dashboard_tags import merge_dicts, comparing_variables, merge_lists, multiply, remove_special_characters, subtract, get_obj_attr, remove_accents


class TestMainDashboardFunctionsTestCase(unittest.TestCase):
    def test_translate_with_correct_info(self):
        self.assertEqual(translate('licenses', 'en'), 'licenses')
        self.assertEqual(translate('licenses', 'pt-BR'), 'licenças')

    @unittest.expectedFailure
    def test_translate_with_missing_key(self):
        self.assertRaises(translate('key_not_in_dict', KeyError))


class TestDashboardHelperFunctionsTestCase(unittest.TestCase):
    def test_remove_special_characters(self):
        self.assertEqual(remove_special_characters(
            'olá! meu nome é [Bruno], e o seu?'), 'olámeunomeéBrunoeoseu')

    def test_multiply(self):
        self.assertEqual(multiply(20, 10), 200)
        self.assertNotEqual(multiply(5, 2), 18)

    def test_merge_dicts(self):
        first_dict = {'a': 1, 'b': 2}
        second_dict = {'c': 3, 'd': 4}
        merged = merge_dicts([first_dict, second_dict])

        self.assertEqual(merged,
                         {'a': 1, 'b': 2, 'c': 3, 'd': 4})

        ''' Testing if order is correct '''
        dict_keys = list(merged.keys())

        self.assertEqual(dict_keys[0],
                         'a')
        self.assertEqual(dict_keys[3],
                         'd')

    def test_merge_lists(self):
        first_list = ['bruno']
        second_list = ['germano', 'mari']
        merged = merge_lists(first_list, second_list)

        self.assertEqual(merged,
                         ['bruno', 'germano', 'mari'])

        ''' Testing if order is correct '''

        self.assertEqual(merged[1], 'germano')
        self.assertNotEqual(merged[2], 'bruno')

    def test_comparing_variables(self):
        self.assertEqual(comparing_variables(2, 1), False)
        self.assertEqual(comparing_variables(5, 3), False)

    def test_subtract(self):
        self.assertEqual(subtract(1, 2), -1)
        self.assertEqual(subtract(5, 8), -3)
        self.assertNotEqual(subtract(6, 4), -2)

    def test_get_obj_attr(self):
        test_get = {'gallahad': 'the pure', 'robin': 'the brave'}
        result = 'the brave'
        self.assertEqual(get_obj_attr(test_get, 'robin'), result)

    @unittest.expectedFailure
    def test_get_obj_attr_with_missing_key(self):
        test_get = {'gallahad': 'the pure', 'robin': 'the brave'}
        key_error = test_get['the']
        self.assertRaises(get_obj_attr(key_error, KeyError))

    def test_remove_accents(self):
        self.assertEqual(remove_accents('marí'), 'mari')
        self.assertNotEqual(remove_accents('brocólis'), 'brocólis')
