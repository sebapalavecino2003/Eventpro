from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'email', 'event', 'rsvp_status', 'created_at',
    ]
    list_filter = ['rsvp_status', 'event']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('event', 'first_name', 'last_name', 'email', 'phone'),
        }),
        (_('RSVP'), {
            'fields': ('rsvp_status',),
        }),
        (_('Fechas del sistema'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )
