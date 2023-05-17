import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current = timezone.now().year
    if value > current:
        raise ValidationError(f"Год не может быть больше текущего ({current})")


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя не может быть "me"')
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(f'В имени запрещенные символы: {value}')
