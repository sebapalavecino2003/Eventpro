import hashlib

from django.db import migrations


def _qr_hash(invitation_id):
    raw = f'event-checkin-{invitation_id}'
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def populate_qr_hash(apps, schema_editor):
    Invitation = apps.get_model('invitations', 'Invitation')
    for inv in Invitation.objects.iterator():
        if not inv.qr_hash:
            Invitation.objects.filter(id=inv.id).update(
                qr_hash=_qr_hash(inv.id),
            )


class Migration(migrations.Migration):

    dependencies = [
        ('invitations', '0002_add_qr_hash'),
    ]

    operations = [
        migrations.RunPython(populate_qr_hash, reverse_code=migrations.RunPython.noop),
    ]
