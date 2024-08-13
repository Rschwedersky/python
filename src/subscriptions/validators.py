from django.core.exceptions import ValidationError
from validate_docbr import CNPJ


def validate_cnpj_when_created(cnpj):
    cnpj_util = CNPJ()

    if not cnpj_util.validate(cnpj):
        raise ValidationError('O CNPJ informado não é válido')
