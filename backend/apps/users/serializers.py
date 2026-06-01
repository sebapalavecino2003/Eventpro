from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import User
from .validators import validate_password_strength


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password_strength],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone',
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                'Ya existe un usuario con este correo electrónico.',
            )
        return value.lower()

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'Ya existe un usuario con este nombre de usuario.',
            )
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Las contraseñas no coinciden.'},
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email', '').lower()
        password = data.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                'Credenciales inválidas.',
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'Esta cuenta está desactivada.',
            )

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'profile_image', 'role', 'is_active', 'email_verified',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'email', 'username', 'role', 'is_active', 'email_verified', 'created_at', 'updated_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'profile_image',
        ]

    def validate_phone(self, value):
        from .validators import validate_chilean_phone
        validate_chilean_phone(value)
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(
        validators=[validate_password_strength],
        style={'input_type': 'password'},
    )
    new_password_confirm = serializers.CharField(style={'input_type': 'password'})

    def validate_old_password(self, value):
        user = self.context.get('user')
        if not user or not user.check_password(value):
            raise serializers.ValidationError('La contraseña actual es incorrecta.')
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': 'Las contraseñas no coinciden.'},
            )
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError(
                {'new_password': 'La nueva contraseña debe ser diferente a la actual.'},
            )
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password_strength],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Las contraseñas no coinciden.'},
            )
        return data


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'profile_image', 'role', 'is_active', 'email_verified',
            'is_staff', 'is_superuser', 'created_at', 'updated_at',
        ]


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'role', 'is_active', 'email_verified', 'is_staff',
        ]
