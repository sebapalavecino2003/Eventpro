import hashlib

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def generate_qr_hash(invitation_id):
    raw = f'event-checkin-{invitation_id}'
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


class Invitation(models.Model):
    class RSVPStatus(models.TextChoices):
        PENDING = 'pending', _('Pendiente')
        CONFIRMED = 'confirmed', _('Confirmado')
        REJECTED = 'rejected', _('Rechazado')

    first_name = models.CharField(_('nombres'), max_length=150)
    last_name = models.CharField(_('apellidos'), max_length=150)
    email = models.EmailField(_('correo electrónico'), max_length=254)
    phone = models.CharField(_('teléfono'), max_length=20, blank=True, null=True)
    rsvp_status = models.CharField(
        _('estado RSVP'),
        max_length=20,
        choices=RSVPStatus.choices,
        default=RSVPStatus.PENDING,
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='invitations',
        verbose_name=_('evento'),
    )
    qr_hash = models.CharField(
        _('hash QR'),
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('fecha de actualización'), auto_now=True)

    class Meta:
        verbose_name = _('invitación')
        verbose_name_plural = _('invitaciones')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'email'],
                name='uq_event_email',
                violation_error_message='Este invitado ya fue agregado a este evento.',
            ),
        ]
        indexes = [
            models.Index(fields=['event'], name='idx_invitation_event'),
            models.Index(fields=['rsvp_status'], name='idx_invitation_rsvp'),
            models.Index(fields=['email'], name='idx_invitation_email'),
        ]

    def __str__(self):
        return f'{self.full_name} - {self.event.title}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


@receiver(post_save, sender=Invitation)
def set_invitation_qr_hash(sender, instance, created, **kwargs):
    if created and not instance.qr_hash:
        qr_hash = generate_qr_hash(instance.id)
        Invitation.objects.filter(id=instance.id).update(qr_hash=qr_hash)
