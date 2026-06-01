from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrador')
        ORGANIZER = 'organizer', _('Organizador')
        COLLABORATOR = 'collaborator', _('Colaborador')

    email = models.EmailField(
        _('correo electrónico'),
        max_length=254,
        unique=True,
        error_messages={'unique': 'Ya existe un usuario con este correo electrónico.'},
    )
    username = models.CharField(
        _('nombre de usuario'),
        max_length=150,
        unique=True,
        error_messages={'unique': 'Ya existe un usuario con este nombre de usuario.'},
    )
    first_name = models.CharField(_('nombres'), max_length=150)
    last_name = models.CharField(_('apellidos'), max_length=150)
    phone = models.CharField(_('teléfono'), max_length=20, blank=True, null=True)
    profile_image = models.ImageField(
        _('imagen de perfil'),
        upload_to='profiles/',
        blank=True,
        null=True,
    )
    role = models.CharField(
        _('rol'),
        max_length=20,
        choices=Role.choices,
        default=Role.ORGANIZER,
    )
    is_active = models.BooleanField(_('activo'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    email_verified = models.BooleanField(_('email verificado'), default=False)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email'], name='idx_user_email'),
            models.Index(fields=['username'], name='idx_user_username'),
            models.Index(fields=['role'], name='idx_user_role'),
        ]

    def __str__(self):
        return f'{self.get_full_name()} ({self.email})'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='email_verification_token',
    )
    token = models.CharField(_('token'), max_length=255, unique=True)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)

    class Meta:
        verbose_name = _('token de verificación')
        verbose_name_plural = _('tokens de verificación')

    def __str__(self):
        return f'Token para {self.user.email}'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='password_reset_tokens',
    )
    token = models.CharField(_('token'), max_length=255, unique=True)
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    used = models.BooleanField(_('usado'), default=False)

    class Meta:
        verbose_name = _('token de restablecimiento')
        verbose_name_plural = _('tokens de restablecimiento')

    def __str__(self):
        return f'Reset token para {self.user.email}'
