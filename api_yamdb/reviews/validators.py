from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value >= timezone.now().year:
        raise ValidationError('Год указан не верно.')


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Имя не может быть "me"')
