from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверяет год выпуска произведения."""
    if value > timezone.now().year:
        raise ValidationError('Год выпуска превышает текущий.')
