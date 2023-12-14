import re

from django.core.exceptions import ValidationError


def username_validator(value):
    unmatched = re.sub(r'^[\w.@+-]+\Z', '', value)
    if value == 'me':
        raise ValidationError('Нельзя использовать имя "me"')
    elif value in re.sub(r'^[\w.@+-]+\Z', '', value):
        raise ValidationError(
            f'Имя не может включать слудующие знаки: {unmatched}',
        )
    return value
