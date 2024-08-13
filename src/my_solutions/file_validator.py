import os
from typing import Union

import pandas as pd
from datetime import datetime
from collections.abc import Iterable
import copy

from portal.templatetags.general_tags import translate
from dashboard.templatetags.dashboard_tags import remove_accents, remove_special_characters
from validate_docbr import CPF, CNPJ, RENAVAM


def validate_file(file, fields: list, language: str) -> dict:
    # Fields to identify conditional files
    conditional_fields = ['TIPO DE DÉBITO-CONDICIONAL-GNRE-SP']
    is_conditional_file = bool(set(conditional_fields).intersection(fields))

    def _read_file() -> Union[dict, bool]:
        '''Reads input file and returns the fields that we are interested'''
        def _check_if_every_field_has_value_in_line(line: tuple) -> bool:
            '''Returns True if every item in the Tuple is not null or nan'''
            for index, item in enumerate(line):
                try:
                    # Checking if exists an empty column
                    getattr(line, 'EMPTY')
                    line_length = len(line)
                    is_last = index == line_length - 1
                    if not is_last and pd.isnull(item):
                        return False
                except AttributeError:
                    if pd.isnull(item):
                        return False

            return True

        def _check_if_line_is_all_empty(line: tuple) -> bool:
            '''Returns True if every item in the Tuple is null or nan'''
            for index, item in enumerate(line):
                if index != 0 and not pd.isnull(item) and (remove_special_characters(item) if isinstance(item, str) else True):
                    return False
            return True

        def _get_list_of_letters_corresponding_to_numbers(list_of_fields: list) -> list:
            '''Gets the length of the fields list and returns the columns to read in the form of letters, as in, A,B,C,D'''
            length_of_fields = len(list_of_fields)
            result = []
            for number in range(length_of_fields):
                number += 1
                result.append(chr(ord('@')+number))

            return ",".join(str(x) for x in sorted(result))

        def _flatten(list_to_flatten: list) -> list:
            flat_list = []
            for sublist in list_to_flatten:
                if isinstance(sublist, Iterable) and not isinstance(sublist, (str, bytes)):
                    for item in sublist:
                        flat_list.append(item)
                else:
                    flat_list.append(sublist)
            return flat_list

            # return [item for sublist in list_to_flatten for item in sublist if isinstance(item, Iterable)]

        try:
            if not isinstance(file, str) and file.name:
                file_extension = os.path.splitext(file.name)[1]
            elif '.xlsx' in file:
                file_extension = '.xlsx'
            elif '.xls' in file:
                file_extension = '.xls'
            elif '.csv' in file:
                file_extension = '.csv'
            try:
                if file_extension == '.xlsx' or file_extension == '.xls':
                    # 'A,B,C,D'
                    columns_to_read = _get_list_of_letters_corresponding_to_numbers(
                        fields)
                    s3_df = pd.read_excel(
                        file, usecols=columns_to_read)
                elif file_extension == '.csv':
                    # [0,1,2,3]
                    csv_columns_to_read = range(len(fields))
                    s3_df = pd.read_csv(file, na_values=";",
                                        usecols=csv_columns_to_read)
                else:
                    raise ValueError("File not supported")
            except Exception as e:
                print('error', e, e.__traceback__.tb_lineno)
                return {
                    'success': False,
                    'payload': translate('unsupported_file', language)
                }
            try:
                s3_df.columns = fields
            except ValueError:
                fields_copy = fields.copy()
                fields_copy.append('EMPTY')
                s3_df.columns = fields_copy

            dict_result = {}
            found_heading = False
            line_by_line_result = {}
            try:
                for line in s3_df.itertuples():
                    line_is_empty = _check_if_line_is_all_empty(
                        line)
                    if line_is_empty and found_heading:
                        break

                    line_has_been_read = False
                    for field in fields:
                        # The index 0 is the line that we are on. For now we are not interested so we add 1 to get to the real values
                        desired_index = fields.index(field) + 1
                        # Have to add 2 lines in Pandas to get real line
                        this_line = line[0] + 2
                        field_has_already_been_mapped = dict_result.get(
                            field, None)
                        if not found_heading or not field_has_already_been_mapped:
                            interested_line = str(line[desired_index])
                            if not pd.isnull(interested_line):
                                fields_to_match_entire_word = [
                                    'CPF', 'CNPJ', 'RGI', 'CPF/CNPJ', 'RENAVAM']
                                if field in fields_to_match_entire_word:
                                    cleaned_line = None
                                    if '\n' in interested_line:
                                        cleaned_line = interested_line.lower().split('\n')[
                                            0].strip()

                                    elif ' ' in interested_line.strip() and ' ' not in field:
                                        cleaned_line = interested_line.lower().split(' ')[
                                            0].strip()
                                    else:
                                        cleaned_line = interested_line.lower().strip()
                                    field_name_exists_in_line = field.lower(
                                    ) == cleaned_line
                                elif 'OPCIONAL' in field or "CONDICIONAL" in field or "INDEPENDENTE" in field:
                                    field_name_exists_in_line = field.split('-')[0].lower(
                                    ).replace('\n', '') in interested_line.lower()
                                else:
                                    cleaned_field = remove_accents(
                                        input_str=field)
                                    cleaned_line = remove_accents(
                                        input_str=interested_line)
                                    field_name_exists_in_line = cleaned_field.lower() in cleaned_line.lower()

                                if field_name_exists_in_line and _check_if_every_field_has_value_in_line(
                                        line):
                                    # Checking if it is the heading, because it is mandatory that every column in it have a value (otherwise there wouldn't be no heading)
                                    found_heading = True
                                    dict_result[field] = {
                                        'value': [],
                                        'field': interested_line.strip()
                                    }
                        else:
                            if not isinstance(line[desired_index], datetime):
                                if not isinstance(line[desired_index], str) or line[desired_index].strip():
                                    # Line is not just a line break (\n)
                                    value = str(line[desired_index])
                                    dict_result[field]['value'].append(
                                        (value, this_line))
                                    line_has_been_read = True
                            else:
                                # If it is a datetime instance we have to check its type to validate it, so we don't convert it to string
                                value = line[desired_index]
                                dict_result[field]['value'].append(
                                    (value, this_line))
                    if is_conditional_file and line_has_been_read:
                        # Conditional automation to check results line by line

                        updated_dict = _check_and_adjust_conditionals(
                            dict_result)

                        line_is_filled = _check_if_all_columns_were_filled(
                            dict_with_results=updated_dict)

                        if not line_is_filled.get('success', None):
                            fields_not_filled = line_is_filled.get(
                                'payload', [])
                            formatted_columns_not_filled = "\n".join(
                                str(item) for item in fields_not_filled)

                            error_message = f"{translate('not_all_columns_are_filled', language)}:\n\n{formatted_columns_not_filled}"

                            return {
                                'success': False,
                                'payload': error_message
                            }

                        line_is_valid = _validate_columns(
                            updated_dict)

                        if not line_is_valid.get('success', None):
                            list_of_errors = line_is_valid.get('payload', [])
                            for error in list_of_errors:
                                field_with_error = error[0]
                                lines_with_error = error[1]
                                field_has_been_mapped = line_by_line_result.get(
                                    field_with_error, None)
                                if not field_has_been_mapped:
                                    line_by_line_result[field_with_error] = []

                                line_by_line_result[field_with_error].append(
                                    lines_with_error)
                                line_by_line_result[field_with_error] = _flatten(
                                    line_by_line_result[field_with_error])

                        for key, value in dict_result.items():
                            # Cleaning the values for next line
                            value['value'] = []

                if is_conditional_file:
                    data = {
                        'success': False,
                        'payload': None
                    }
                    errors = []
                    if line_by_line_result:
                        for key, value in line_by_line_result.items():
                            formatted_lines_with_error = ",".join(
                                str(x) for x in value)
                            field_name_without_whitespace = ' '.join(
                                key.splitlines())

                            formatted_error_result = f"{field_name_without_whitespace} ({translate('line' if len(lines_with_error) == 1 else 'lines', language)}: {formatted_lines_with_error})"
                            errors.append(
                                formatted_error_result)

                        formatted_columns_with_errors = "\n".join(
                            str(item) for item in errors)
                        data['payload'] = f"{translate('there_were_problems_with_the_following_fields', language)}:\n\n{formatted_columns_with_errors}"
                    else:
                        data['success'] = True
                        data['payload'] = file
                    return data
                else:
                    return dict_result
            except Exception as e:
                print('error', e, e.__traceback__.tb_lineno)
                return {
                    'success': False,
                    'payload': translate('unsupported_file', language)
                }

        except Exception as e:
            print('error', e, e.__traceback__.tb_lineno)
            return {
                'success': False,
                'payload': translate('unsupported_file', language)
            }

    def _check_and_adjust_conditionals(dict_with_results: dict) -> dict:
        '''This function returns a new dict with the necessary fields marked as obligatory and optional (don't need to be filled) '''
        def _conditional_gnre_sp(dict_copy: dict) -> dict:
            try:
                for key in dict_with_results.keys():
                    if 'GNRE-SP' in key:
                        # Ruler is the field that will change the way we process the file
                        ruler = dict_copy.get(key)
                        ruler_value = ruler.get('value')[0][0]
                        if ruler_value == '(ICMS) Apuração':
                            dict_copy['INSCRIÇÃO ESTADUAL'] = dict_copy['INSCRIÇÃO ESTADUAL-CONDICIONAL']
                            dict_copy['NOTA FISCAL ELETRÔNICA-OPCIONAL'] = dict_copy['NOTA FISCAL ELETRÔNICA-CONDICIONAL']
                            dict_copy['CNPJ DO REMETENTE-OPCIONAL'] = dict_copy['CNPJ DO REMETENTE-CONDICIONAL']

                        elif ruler_value == '(ICMS) Apuração - Simples Nacional' or ruler_value == 'Outros Recolhimentos':
                            dict_copy['INSCRIÇÃO ESTADUAL-OPCIONAL'] = dict_copy['INSCRIÇÃO ESTADUAL-CONDICIONAL']
                            dict_copy['NOTA FISCAL ELETRÔNICA-OPCIONAL'] = dict_copy['NOTA FISCAL ELETRÔNICA-CONDICIONAL']
                            dict_copy['CNPJ DO REMETENTE-OPCIONAL'] = dict_copy['CNPJ DO REMETENTE-CONDICIONAL']

                        elif ruler_value == '(ICMS) Operação/Prestação' or ruler_value == '(ICMS) Operação/Prestação - Simples Nacional':
                            dict_copy['INSCRIÇÃO ESTADUAL-OPCIONAL'] = dict_copy['INSCRIÇÃO ESTADUAL-CONDICIONAL']
                            dict_copy['NOTA FISCAL ELETRÔNICA'] = dict_copy['NOTA FISCAL ELETRÔNICA-CONDICIONAL']
                            dict_copy['CNPJ DO REMETENTE-OPCIONAL'] = dict_copy['CNPJ DO REMETENTE-CONDICIONAL']

                        elif ruler_value == 'Recolhimento Antecipado':
                            dict_copy['INSCRIÇÃO ESTADUAL'] = dict_copy['INSCRIÇÃO ESTADUAL-CONDICIONAL']
                            dict_copy['NOTA FISCAL ELETRÔNICA-OPCIONAL'] = dict_copy['NOTA FISCAL ELETRÔNICA-CONDICIONAL']
                            dict_copy['CNPJ DO REMETENTE'] = dict_copy['CNPJ DO REMETENTE-CONDICIONAL']

                        dict_copy['TIPO DE DÉBITO'] = dict_copy['TIPO DE DÉBITO-CONDICIONAL-GNRE-SP']
                        del dict_copy['TIPO DE DÉBITO-CONDICIONAL-GNRE-SP']
                        del dict_copy['INSCRIÇÃO ESTADUAL-CONDICIONAL']
                        del dict_copy['NOTA FISCAL ELETRÔNICA-CONDICIONAL']
                        del dict_copy['CNPJ DO REMETENTE-CONDICIONAL']

                        return dict_copy

            except Exception:
                return dict_with_results
        try:
            dict_copy = copy.deepcopy(dict_with_results)
            if 'TIPO DE DÉBITO-CONDICIONAL-GNRE-SP' in fields:
                return _conditional_gnre_sp(dict_copy)
            else:
                return dict_with_results
        except Exception:
            return dict_with_results

    def _check_if_all_columns_were_filled(dict_with_results: dict) -> bool:
        '''Checking if every field is in dictionary with results. If the length is different means that not every field was found, so it returns False'''
        try:
            errors = []
            # All fields. When they are checked they are removed of the list.
            # If in the end there is an item in this list, means that this item
            # was not filled
            fields_copy = fields.copy()
            for key, info in dict_with_results.items():
                if 'OPCIONAL' not in key and 'INDEPENDENTE' not in key:
                    field_value = info.get('value', None)
                    field_name = info.get('field', None)

                    if field_value:
                        field_lines_not_filled = set()
                        for tuple in field_value:
                            forbidden_values = ['nan', '\n']
                            tuple_value = tuple[0]
                            tuple_line = tuple[1]
                            if tuple_value in forbidden_values:
                                field_name_without_whitespace = ' '.join(
                                    field_name.splitlines() if field_name else key.splitlines())

                                field_lines_not_filled.add(tuple_line)
                            else:
                                if key in fields_copy:
                                    fields_copy.remove(key)

                        if field_lines_not_filled:
                            field_name_without_whitespace = ' '.join(
                                field_name.splitlines() if field_name else key.splitlines())
                            formatted_lines_with_error = ",".join(
                                str(x) for x in field_lines_not_filled)

                            field_with_line = f"{field_name_without_whitespace} ({translate('line' if len(field_lines_not_filled) == 1 else 'lines', language)}: {formatted_lines_with_error})"

                            errors.append(field_with_line)
                    else:
                        field_name_without_whitespace = ' '.join(
                            field_name.splitlines() if field_name else key.splitlines())

                        errors.append(field_name_without_whitespace)
                else:
                    fields_copy.remove(key)
                    continue

            # Checks if the fields that were not filled are optional
            not_all_columns_were_found = len(
                list(filter(lambda x: 'OPCIONAL' not in x and 'INDEPENDENTE' not in x, fields_copy))) > 0

            if not_all_columns_were_found:
                result = {
                    'success': False,
                    'payload': translate('not_all_columns_are_filled', language)
                }
            else:
                result = {
                    'success': True if len(errors) == 0 else False,
                    'payload': errors
                }

            return result
        except Exception as e:
            print('error', e, e.__traceback__.tb_lineno)
            return False

    def _validate_columns(dict_with_results: dict) -> bool:
        '''Loops through dict with results to validate all the values that were sent'''
        def check_if_list_with_values_is_ok(list_with_values: list) -> bool:
            # Sometimes there is a space in a cell and that can't count as a value that the user sent
            list_without_line_breaks = list(
                filter(lambda x: x[0] != '\n', list_with_values))
            for value in list_without_line_breaks:
                if pd.isnull(value):
                    return False

            return True

        errors = []
        try:
            for key, field_info in list(dict_with_results.items()):
                field_value = field_info.get('value', ())
                field_name = field_info.get('field', '')

                if 'OPCIONAL' in key:
                    filtered_field_value = list(
                        filter(lambda x: not isinstance(x[0], str) or x[0] != 'nan' and x[0] != '\n' and remove_special_characters(x[0].strip()), field_value))
                    if filtered_field_value:
                        dict_with_results[key]['value'] = filtered_field_value
                        dict_with_results[key.split(
                            '-')[0]] = dict_with_results[key]
                        del dict_with_results[key]
                        field_value = filtered_field_value
                        key = key.split('-')[0]
                    else:
                        continue
                elif 'INDEPENDENTE' in key:
                    continue

                are_all_fields_valid = check_if_list_with_values_is_ok(
                    field_value)

                if not are_all_fields_valid:
                    is_valid = False
                else:
                    desired_function = _get_field_validator(key)

                    validator_feedback = desired_function(field_value)
                    is_valid = validator_feedback.get('status', False)

                if not is_valid:
                    field_name_without_whitespace = ' '.join(
                        field_name.splitlines())

                    lines_with_error = validator_feedback.get('errors', [])

                    if is_conditional_file:
                        errors.append(
                            (field_name, lines_with_error))
                    else:
                        formatted_lines_with_error = ",".join(
                            str(x) for x in lines_with_error)

                        formatted_error_result = f"{field_name_without_whitespace} ({translate('line' if len(lines_with_error) == 1 else 'lines', language)}: {formatted_lines_with_error})"

                        errors.append(
                            formatted_error_result)

            return {
                'success': True if len(errors) == 0 else False,
                'payload': errors
            }
        except Exception as e:
            print('error', e, e.__traceback__.tb_lineno)
            return {
                'success': False,
                'payload': errors
            }

##### EXECUTABLE CODE #####
    try:
        if is_conditional_file:
            columns_validation = _read_file()
            return columns_validation
        else:
            reading_analysis = _read_file()

            reading_analysis_is_empty = len(reading_analysis) == 0

            if 'success' in reading_analysis and not reading_analysis.get('success'):
                return {
                    'success': False,
                    'payload': reading_analysis.get('payload')
                }
            elif reading_analysis_is_empty:
                return {
                    'success': False,
                    'payload': translate('spreadsheet_entered_does_not_belong_to_service', language)
                }

            all_columns_have_been_filled = _check_if_all_columns_were_filled(
                dict_with_results=reading_analysis)

            if not all_columns_have_been_filled.get('success', None):
                fields_not_filled = all_columns_have_been_filled.get(
                    'payload', [])
                if isinstance(fields_not_filled, list):
                    formatted_columns_not_filled = "\n".join(
                        str(item) for item in fields_not_filled)

                    error_message = f"{translate('not_all_columns_are_filled', language)}:\n\n{formatted_columns_not_filled}"
                else:
                    error_message = fields_not_filled

                return {
                    'success': False,
                    'payload': error_message
                }

            columns_validation = _validate_columns(reading_analysis)

            if not columns_validation.get('success', None):
                formatted_columns_with_errors = "\n".join(
                    str(item) for item in columns_validation.get('payload', None))
                return {
                    'success': False,
                    'payload': f"{translate('there_were_problems_with_the_following_fields', language)}:\n\n{formatted_columns_with_errors}"
                }
            else:
                return {
                    'success': True,
                    'payload': file
                }

    except Exception as e:
        print('error', e, e.__traceback__.tb_lineno)
        return {
            'success': False,
            'payload': None
        }
##### END OF EXECUTABLE CODE #####


def _get_field_validator(field: str):
    def include_zeros_to_the_left(string: str, desired_length: int) -> str:
        difference = desired_length - len(string)
        new_string = string
        for _ in range(difference):
            new_string = f"0{new_string}"
        return new_string

    def check_if_it_is_cpf_or_cnpj(values: list):
        values_tuple = values[0]
        value = values_tuple[0]
        cleaned_value = remove_special_characters(value)
        if len(cleaned_value) <= 11:
            return _validate_cpf(values)
        elif len(cleaned_value) <= 14:
            return _validate_cnpj(values)
        else:
            # Doesn't matter which one, will throw error anyway
            return _validate_cnpj(values)

    def _validate_cep(ceps: list) -> dict:
        data = {'status': True, 'errors': set()}
        for cep in ceps:
            cep_value = cep[0]
            cep_line = cep[1]
            cleaned_cep = remove_special_characters(cep_value)
            if not len(cleaned_cep) == 8:
                data['status'] = False
                data['errors'].add(cep_line)

        return data

    def _validate_cnae(cnaes: list) -> bool:
        data = {'status': True, 'errors': set()}
        for cnae in cnaes:
            cnae_value = cnae[0]
            cnae_line = cnae[1]
            cleaned_cnae = remove_special_characters(cnae_value)
            if not len(cleaned_cnae) == 5 and not len(cleaned_cnae) == 7:
                data['status'] = False
                data['errors'].add(cnae_line)

        return data

    def _validate_cpf(cpfs: list) -> dict:
        data = {'status': True, 'errors': set()}
        cpf_util = CPF()
        for cpf in cpfs:
            cpf_value = cpf[0]
            cpf_line = cpf[1]
            desired_length = 11
            if len(cpf_value) < desired_length:
                cpf_value = include_zeros_to_the_left(
                    string=cpf_value, desired_length=desired_length)
            is_valid = cpf_util.validate(cpf_value)
            if not is_valid:
                data['status'] = False
                data['errors'].add(cpf_line)
        return data

    def _validate_cnpj(cnpjs: list) -> dict:
        data = {'status': True, 'errors': set()}
        cnpj_util = CNPJ()
        for cnpj in cnpjs:
            cnpj_value = cnpj[0]
            cnpj_line = cnpj[1]
            desired_length = 14
            if len(cnpj_value) < desired_length:
                cnpj_value = include_zeros_to_the_left(
                    string=cnpj_value, desired_length=desired_length)

            is_valid = cnpj_util.validate(cnpj_value)
            if not is_valid:
                data['status'] = False
                data['errors'].add(cnpj_line)
        return data

    def _validate_date(birthdate: list) -> dict:
        data = {'status': True, 'errors': set()}
        for date in birthdate:
            date_value = date[0]
            date_line = date[1]
            if isinstance(date_value, datetime):
                continue
            elif isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, "%d/%m/%Y")
                    continue
                except ValueError:
                    data['status'] = False
                    data['errors'].add(date_line)
            else:
                data['status'] = False
                data['errors'].add(date_line)
        return data

    def _validate_estado(estados: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_estados = ['ac', 'al', 'am', 'ap', 'ba', 'ce',
                         'df', 'es', 'go', 'ma', 'mg', 'ms', 'mt', 'pa', 'pb', 'pe', 'pi', 'pr', 'rj', 'rn', 'ro', 'rr', 'rs', 'sc', 'se', 'sp', 'to']
        for estado in estados:
            estado_value = estado[0]
            estado_line = estado[1]
            if estado_value.lower() not in valid_estados:
                data['status'] = False
                data['errors'].add(estado_line)
        return data

    def _validate_inscricao_estadual(inscricoes: list) -> dict:
        data = {'status': True, 'errors': set()}
        for inscricao in inscricoes:
            inscricao_value = inscricao[0]
            inscricao_line = inscricao[1]
            cleaned_inscricao = remove_special_characters(inscricao_value)
            if len(cleaned_inscricao) != 12:
                data['status'] = False
                data['errors'].add(inscricao_line)
        return data

    def _validate_iss_retido(list_of_iss: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_iss = ['sim', 'não']
        for iss in list_of_iss:
            iss_value = iss[0]
            iss_line = iss[1]
            if iss_value.lower() not in valid_iss:
                data['status'] = False
                data['errors'].add(iss_line)
        return data

    def _validate_month(months: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_months = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro', 'todos']
        for month in months:
            month_value = month[0]
            month_line = month[1]
            if month_value.lower() not in valid_months:
                data['status'] = False
                data['errors'].add(month_line)
        return data

    def _validate_name(names: list) -> dict:
        data = {'status': True, 'errors': set()}
        for name in names:
            name_value = name[0]
            name_line = name[1]
            is_valid = isinstance(
                name_value, str) and name_value != 'nan' and len(name_value) > 0
            if not is_valid:
                data['status'] = False
                data['errors'].add(name_line)
        return data

    def _validate_nfe(nfes: list) -> dict:
        data = {'status': True, 'errors': set()}
        for nfe in nfes:
            nfe_value = nfe[0]
            nfe_line = nfe[1]
            cleaned_nfe = remove_special_characters(nfe_value)
            cleaned_nfe = cleaned_nfe.replace(' ', '')
            if len(cleaned_nfe) != 44:
                data['status'] = False
                data['errors'].add(nfe_line)
            try:
                int(cleaned_nfe)
            except Exception as e:
                print('error', e, e.__traceback__.tb_lineno)
                data['status'] = False
                data['errors'].add(nfe_line)
        return data

    def _validate_number(numbers: list) -> dict:
        data = {'status': True, 'errors': set()}
        for number in numbers:
            number_value = number[0]
            number_line = number[1]
            if isinstance(number_value, str):
                # Removing currency sign and decimal separator
                try:
                    number_value = number_value.replace(
                        'R$', '').replace(',', '.')
                    number_value = float(number_value)
                except ValueError as e:
                    if ',' in number_value:
                        number_value = number_value.split(',')[0]
                    if '.' in number_value:
                        number_value = number_value.split('.')[0]
                    number_value = remove_special_characters(number_value)
            try:
                int(number_value)
            except Exception as e:
                print('error', e, e.__traceback__.tb_lineno)
                data['status'] = False
                data['errors'].add(number_line)
        return data

    def _validate_periodo_de_consulta(periodos: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_periodos = ['último mês', 'últimos 3 meses',
                          'últimos 6 meses', 'últimos 12 meses', 'todos']
        for periodo in periodos:
            periodo_value = periodo[0]
            periodo_line = periodo[1]
            if not periodo_value.lower() in valid_periodos:
                data['status'] = False
                data['errors'].add(periodo_line)
        return data

    def _validate_periodo_de_referencia(periodos: list) -> dict:
        data = {'status': True, 'errors': set()}
        for periodo in periodos:
            periodo_value = periodo[0]
            periodo_line = periodo[1]
            try:
                if '/' not in periodo_value:
                    periodo_value = str(periodo_value)
                    periodo_value = f"{periodo_value[:2]}/{periodo_value[2:]}"
                periodo_value = datetime.strptime(periodo_value, '%m/%Y')
            except Exception as e:
                data['status'] = False
                data['errors'].add(periodo_line)

        return data

    def _validate_placa_do_veiculo(placas: "list[str]") -> dict:
        data = {'status': True, 'errors': set()}
        for placa in placas:
            placa_value = placa[0]
            placa_line = placa[1]
            contLetra = 0
            contNum = 0
            cleaned_placa = remove_special_characters(placa_value)
            if len(cleaned_placa) != 7:
                data['status'] = False
                data['errors'].add(placa_line)
                return data

            for i, item in enumerate(cleaned_placa):
                if item.isalpha() and (i == 0 or i == 1 or i == 2 or i == 4):
                    contLetra += 1
                elif item.isdigit() and (i == 3 or i == 4 or i == 5 or i == 6):
                    contNum += 1

            if not (contLetra == 3 and contNum == 4) and not (contLetra == 4 and contNum == 3):
                data['status'] = False
                data['errors'].add(placa_line)
                return data

        return data

    def _validate_qualificacao_receita(qualificacoes: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_qualificacoes = ['normal', 'comunicações',
                               'energia elétrica', 'petróleo', 'transporte']
        for qualificacao in qualificacoes:
            qualificacao_value = qualificacao[0]
            qualificacao_line = qualificacao[1]
            if not qualificacao_value.lower() in valid_qualificacoes:
                data['status'] = False
                data['errors'].add(qualificacao_line)
        return data

    def _validate_renavam(renavans: "list[str]") -> dict:
        data = {'status': True, 'errors': set()}
        renavam_util = RENAVAM()
        for renavam in renavans:
            renavam_value = renavam[0]
            renavam_line = renavam[1]
            desired_length = 11
            renavam_value = remove_special_characters(renavam_value)
            if len(renavam_value) < desired_length:
                renavam_value = include_zeros_to_the_left(
                    string=renavam_value, desired_length=desired_length)
            is_valid = renavam_util.validate(renavam_value)
            if not is_valid:
                data['status'] = False
                data['errors'].add(renavam_line)
        return data

    def _validate_situacao_da_certidao(situacoes: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_situacoes = ['válida', 'expirada', 'todas']
        for situacao in situacoes:
            situacao_value = situacao[0]
            situacao_line = situacao[1]
            if not situacao_value.lower() in valid_situacoes:
                data['status'] = False
                data['errors'].add(situacao_line)
        return data

    def _validate_situacao_da_guia(situacoes: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_situacoes = ['pendentes', 'quitadas', 'canceladas']
        for situacao in situacoes:
            situacao_value = situacao[0]
            situacao_line = situacao[1]
            if not situacao_value.lower() in valid_situacoes:
                data['status'] = False
                data['errors'].add(situacao_line)
        return data

    def _validate_tipo_de_debito(tipos_de_debitos: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_tipos_de_debitos = [
            '(icms) apuração', '(icms) apuração - simples nacional', '(icms) operação/prestação', '(icms) operação/prestação - simples nacional', 'recolhimento antecipado', 'outros recolhimentos']
        for tipo_de_debito in tipos_de_debitos:
            tipo_de_debito_value = tipo_de_debito[0]
            tipo_de_debito_line = tipo_de_debito[1]
            if not tipo_de_debito_value.lower() in valid_tipos_de_debitos:
                data['status'] = False
                data['errors'].add(tipo_de_debito_line)
        return data

    def _validate_tipo_do_rps(list_of_rps: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_rps = ['normal', 'misto', 'cupom']
        for rps in list_of_rps:
            rps_value = rps[0]
            rps_line = rps[1]
            if not rps_value.lower() in valid_rps:
                data['status'] = False
                data['errors'].add(rps_line)
        return data

    def _validate_tributacao_dos_servicos(tributacoes_de_servico: list) -> dict:
        data = {'status': True, 'errors': set()}
        valid_tributacoes = [
            'no município', 'fora do município', 'com benefício fiscal', 'suspenso por decisão judicial', 'suspenso por processos adm.']
        for tributacao in tributacoes_de_servico:
            tributacao_value = tributacao[0]
            tributacao_line = tributacao[1]
            if not tributacao_value.lower() in valid_tributacoes:
                data['status'] = False
                data['errors'].add(tributacao_line)
        return data

    def _validate_year(years: list) -> dict:
        data = {'status': True, 'errors': set()}
        for year in years:
            year_value = year[0]
            year_line = year[1]
            cleaned_year = remove_special_characters(year_value)
            if not len(cleaned_year) == 4:
                data['status'] = False
                data['errors'].add(year_line)
        return data

    field = remove_accents(input_str=field)
    field = field.lower()

    if "ano" in field:
        field = "ano"
    elif "cpf/cnpj" in field:
        field = "cpf/cnpj"
    elif "cpf" in field:
        field = "cpf"
    elif "cnpj" in field:
        field = "cnpj"
    elif "data" in field:
        field = "data"
    elif "mes" in field:
        field = "mes"
    elif "codigo" in field or "cidade" in field or "matricula" in field or "informacoes complementares" in field or "serie" in field or "incondicionados" in field or "item" in field or "subitem" in field or "servico" in field or "discriminacao dos servicos":
        field = "nome"
    elif "atualizacao monetaria" in field or "contribuinte" in field or "fecp" in field or "icms" in field or "juros" in field or "multa" in field or "numero" in field or "rgi" in field or "valor" in field or "r$" in field:
        field = "numero"

    function_reference = {
        "ano": _validate_year,
        "cep": _validate_cep,
        "cnae": _validate_cnae,
        "cpf/cnpj": check_if_it_is_cpf_or_cnpj,
        "cnpj": _validate_cnpj,
        "cpf": _validate_cpf,
        "data": _validate_date,
        "estado": _validate_estado,
        "inscricao estadual": _validate_inscricao_estadual,
        "iss retido": _validate_iss_retido,
        "mes": _validate_month,
        "nome": _validate_name,
        "nota fiscal eletronica": _validate_nfe,
        "numero": _validate_number,
        "placa do veiculo": _validate_placa_do_veiculo,
        "periodo de consulta": _validate_periodo_de_consulta,
        "periodo de referencia": _validate_periodo_de_referencia,
        "qualificacao receita": _validate_qualificacao_receita,
        "renavam": _validate_renavam,
        "situacao da certidao": _validate_situacao_da_certidao,
        "situacao da guia": _validate_situacao_da_guia,
        "tipo de debito": _validate_tipo_de_debito,
        "tipo do rps": _validate_tipo_do_rps,
        "tributacao dos servicos": _validate_tributacao_dos_servicos
    }

    return function_reference[field]
