from django.db.models import Count, Q

from .models import Event
from .serializers import (
    EventCreateSerializer,
    EventDetailSerializer,
    EventListSerializer,
    EventStatusSerializer,
    EventUpdateSerializer,
)


class EventService:
    @staticmethod
    def _base_queryset():
        return Event.objects.select_related('organizer').annotate(
            guest_count=Count('invitations', distinct=True),
            confirmed_count=Count(
                'invitations',
                filter=Q(invitations__rsvp_status='confirmed'),
                distinct=True,
            ),
            attendance_count=Count('attendances', distinct=True),
        )

    @staticmethod
    def list_events(user, params):
        queryset = EventService._base_queryset()

        if user.role == 'admin':
            pass
        elif user.role == 'organizer':
            queryset = queryset.filter(organizer=user)
        else:
            queryset = queryset.filter(invitations__email=user.email)

        status = params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        category = params.get('category')
        if category:
            queryset = queryset.filter(category=category)

        search = params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search),
            )

        ordering = params.get('ordering', '-event_date')
        allowed_ordering = [
            'event_date', '-event_date', 'created_at', '-created_at',
            'title', '-title', 'status', '-status',
        ]
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    @staticmethod
    def get_event(event_id, user):
        queryset = EventService._base_queryset()
        if user.role == 'admin':
            pass
        elif user.role == 'organizer':
            queryset = queryset.filter(organizer=user)
        else:
            queryset = queryset.filter(invitations__email=user.email)
        return queryset.get(id=event_id)

    @staticmethod
    def create_event(user, data):
        serializer = EventCreateSerializer(
            data=data,
            context={'request': type('Req', (), {'user': user})()},
        )
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        return event

    @staticmethod
    def update_event(event, data):
        serializer = EventUpdateSerializer(event, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete_event(event):
        event.delete()
        return True

    @staticmethod
    def change_status(event, new_status):
        serializer = EventStatusSerializer(data={'status': new_status})
        serializer.is_valid(raise_exception=True)

        if not event.can_transition_to(new_status):
            from rest_framework.exceptions import ValidationError
            raise ValidationError(
                f'No es posible cambiar de "{event.get_status_display()}" '
                f'a "{dict(Event.Status.choices).get(new_status, new_status)}".',
            )

        event.status = new_status
        event.save()
        return event
