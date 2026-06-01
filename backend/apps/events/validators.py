from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_event_date_not_past(value):
    if value < date.today():
        raise ValidationError(
            _('La fecha del evento no puede ser anterior a hoy.'),
        )
