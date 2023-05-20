import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone


def max_min_validator():
    return [
        MaxValueValidator(10, 'Не так много, max 10!'),
        MinValueValidator(1, 'Хоть 1 поставь!')
    ]


def validate_year(value):
    if value >= timezone.now().year:
        raise ValidationError('Год указан не верно.')


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя не может быть "me"')
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(f'В имени запрещенные символы: {value}')
