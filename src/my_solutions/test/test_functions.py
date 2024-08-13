import unittest
from django.test import TestCase

from portal.templatetags.general_tags import translate
from my_solutions.templatetags.mysolutions_tags import sort_dict_by_key, get_all_automations_fields, get_automation_fields
import my_solutions.file_validator as file_validator

import os
from io import TextIOWrapper


class TestMainDashboardFunctionsTestCase(unittest.TestCase):
    pass


class TestDashboardHelperFunctionsTestCase(unittest.TestCase):
    language = 'pt-BR'

    def test_sort_dict_by_key(self):
        dict = {'energy': 'Energia', 'telephony': 'Telefonia',
                'cpf': 'CPF', 'cnpj': 'CNPJ'}
        sorted = sort_dict_by_key(dict)
        sorted_keys = list(sorted.keys())
        self.assertEqual(sorted_keys[0], 'cnpj')
        self.assertNotEqual(sorted_keys[3], 'cpf')

    def test_all_automations_validation(self):
        # all_automations = get_all_automations_fields()
        all_automations = {'aguas-rio': '', 'cedae': '', 'cepom-rj': '',
                           'certidao-mte': '', 'cnd': '', 'cnd-rj': '', 'cnd-sp': '', 'comgas': '', 'cpom-sp': '', 'divida-ativa-rj': '', 'icms-rj': '', 'icms-sp': '', 'inidoneos-ceis': '', 'inidoneos': '', 'ipva-rj': '', 'ipva-sp': '', 'iss-rj': '', 'iss-sp': '', 'naturgy': '', 'notas-servico-sp': '', 'receita-federal-cnpj': '', 'receita-federal-cpf': '', 'sabesp': '', 'trf3': ''}
        failed_column_name_changed_automations = []
        failed_empty_value_automations = []
        for automation in all_automations.keys():
            required_columns = get_automation_fields(
                automation_name=automation)
            file_name = f'example_{automation}_teste.xlsx'

            column_name_changed = get_file(
                '/test_files/automations/not_assert/column_validation/column_name_changed', file_name)
            file_validated_not_assert = file_validator.validate_file(
                file=column_name_changed.name, fields=required_columns, language=self.language)

            if len(required_columns) == 1:
                self.assertEqual(translate('spreadsheet_entered_does_not_belong_to_service',
                                           self.language) in file_validated_not_assert['payload'], True)
            elif not translate('not_all_columns_are_filled',
                               self.language) in file_validated_not_assert['payload']:
                failed_column_name_changed_automations.append(file_name)
            else:
                self.assertEqual(translate('not_all_columns_are_filled',
                                           self.language) in file_validated_not_assert['payload'], True)

            column_empty = get_file(
                '/test_files/automations/not_assert/column_validation/column_empty', file_name)
            file_validated_not_assert = file_validator.validate_file(
                file=column_empty.name, fields=required_columns, language=self.language)
            self.assertEqual(translate('spreadsheet_entered_does_not_belong_to_service',
                                       self.language) in file_validated_not_assert['payload'], True)

            invalid_file = get_file(
                '/test_files/automations/not_assert/invalid_file', file_name)
            file_validated_not_assert = file_validator.validate_file(
                file=invalid_file.name, fields=required_columns, language=self.language)
            self.assertEqual(translate('unsupported_file',
                             self.language) in file_validated_not_assert['payload'], True)

            try:
                field_error = get_file(
                    '/test_files/automations/not_assert/field_validation', file_name)
                file_validated_not_assert = file_validator.validate_file(
                    file=field_error.name, fields=required_columns, language=self.language)
                self.assertEqual(translate('there_were_problems_with_the_following_fields',
                                           self.language) in file_validated_not_assert['payload'], True)
            except Exception as e:
                print('--------------- Error Getting Field Error File --------------')
                print(str(e))

            field_empty = get_file(
                '/test_files/automations/not_assert/field_empty', file_name)
            file_validated_not_assert = file_validator.validate_file(
                file=field_empty.name, fields=required_columns, language=self.language)
            if not translate('not_all_columns_are_filled',
                             self.language) in file_validated_not_assert['payload']:
                failed_empty_value_automations.append(file_name)
            else:
                self.assertEqual(translate('not_all_columns_are_filled',
                                           self.language) in file_validated_not_assert['payload'], True)

            valid_file = get_file(
                '/test_files/automations/assert', file_name)
            file_validated_assert = file_validator.validate_file(
                file=valid_file.name, fields=required_columns, language=self.language)
            self.assertEqual(file_validated_assert['success'], True)

        if len(failed_column_name_changed_automations) > 0:
            print(
                '\n \n' + '-------------- Error Getting Column Name Changed File --------------')
            for failed_automation in failed_column_name_changed_automations:
                print(failed_automation + '\n')

        if len(failed_empty_value_automations) > 0:
            print(
                '\n \n' + '-------------- Error Empty Value Automations --------------')
            for failed_automation in failed_empty_value_automations:
                print(failed_automation + '\n')


def get_file(dir: str, file_name: str) -> TextIOWrapper:
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(
        module_dir + dir, file_name)
    with open(file_path, 'r') as f:
        return f
