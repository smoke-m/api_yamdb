from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current = timezone.now().year
    if value > current:
        raise ValidationError(f"Год не может быть больше текущего ({current})")
