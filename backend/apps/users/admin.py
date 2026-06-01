from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import EmailVerificationToken, PasswordResetToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'role', 'is_active', 'email_verified', 'is_staff', 'created_at',
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'email_verified']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {
            'fields': ('username', 'first_name', 'last_name', 'phone', 'profile_image'),
        }),
        (_('Rol y permisos'), {
            'fields': ('role', 'is_active', 'email_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at']
    search_fields = ['user__email', 'token']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'used', 'created_at']
    list_filter = ['used']
    search_fields = ['user__email', 'token']
