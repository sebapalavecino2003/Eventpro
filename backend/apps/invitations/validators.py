from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Invitation


def validate_unique_guest(event_id, email, exclude_id=None):
    queryset = Invitation.objects.filter(event_id=event_id, email__iexact=email)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    if queryset.exists():
        raise ValidationError(
            _('Este invitado ya fue agregado a este evento.'),
        )
