import re

from rest_framework import serializers


def validate_password_strength(value):
    if len(value) < 8:
        raise serializers.ValidationError(
            'La contraseña debe tener al menos 8 caracteres.',
        )
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError(
            'La contraseña debe contener al menos una mayúscula.',
        )
    if not re.search(r'[a-z]', value):
        raise serializers.ValidationError(
            'La contraseña debe contener al menos una minúscula.',
        )
    if not re.search(r'\d', value):
        raise serializers.ValidationError(
            'La contraseña debe contener al menos un número.',
        )


def validate_chilean_phone(value):
    if value and not re.match(r'^\+?56\d{9}$', value):
        raise serializers.ValidationError(
            'El teléfono debe tener formato chileno (+569XXXXXXXX).',
        )


def validate_email_not_taken(value):
    from .models import User
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError(
            'Ya existe un usuario con este correo electrónico.',
        )
