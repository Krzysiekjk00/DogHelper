from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_username(value):
    if User.objects.filter(username=value):
        raise ValidationError('This username already exists in our base.')
