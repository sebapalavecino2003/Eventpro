from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'invitation', 'event', 'checkin_time', 'qr_code_short',
    ]
    list_filter = ['event', 'checkin_time']
    search_fields = ['invitation__first_name', 'invitation__last_name', 'qr_code']
    ordering = ['-checkin_time']
    readonly_fields = ['qr_code', 'checkin_time']

    fieldsets = (
        (None, {
            'fields': ('invitation', 'event'),
        }),
        (_('Check-in'), {
            'fields': ('qr_code', 'checkin_time'),
        }),
    )

    @admin.display(description='QR')
    def qr_code_short(self, obj):
        return f'{obj.qr_code[:12]}...' if obj.qr_code else '-'
