from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'event_date', 'event_time', 'status',
        'category', 'organizer', 'created_at',
    ]
    list_filter = ['status', 'category', 'event_date']
    search_fields = ['title', 'description', 'location']
    ordering = ['-event_date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'event_date'

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'organizer'),
        }),
        (_('Programación'), {
            'fields': ('event_date', 'event_time', 'location'),
        }),
        (_('Clasificación'), {
            'fields': ('category', 'status', 'image'),
        }),
        (_('Fechas del sistema'), {
            'fields': ('created_at', 'updated_at'),
        }),
    )
