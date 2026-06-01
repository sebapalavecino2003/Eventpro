from datetime import date, timedelta

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from invitations.models import Invitation
from users.models import User

from .models import Event
from .permissions import IsEventOrganizer
from .serializers import EventCreateSerializer, EventStatusSerializer
from .services import EventService


def _make_organizer(email='org@test.com'):
    return User.objects.create_user(
        email=email,
        username=email,
        password='Pass1234',
        role='organizer',
        first_name='Org',
        last_name='Test',
    )


class EventCreateSerializerTest(TestCase):
    def setUp(self):
        self.user = _make_organizer()
        self.valid_data = {
            'title': 'Test Event',
            'description': 'Description',
            'event_date': date.today() + timedelta(days=10),
            'event_time': '15:00',
            'location': 'Sala A',
            'category': 'conference',
        }

    def _build_serializer(self, data):
        factory = APIRequestFactory()
        request = factory.post('/')
        request.user = self.user
        return EventCreateSerializer(data=data, context={'request': request})

    def test_create_serializer_excludes_status_from_validated_data(self):
        data = {**self.valid_data, 'status': 'active'}
        serializer = self._build_serializer(data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('status', serializer.validated_data)

    def test_create_serializer_accepts_without_status(self):
        serializer = self._build_serializer(self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_create_serializer_rejects_future_status_field(self):
        serializer = self._build_serializer(
            {**self.valid_data, 'status': 'non-existent'}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('status', serializer.validated_data)


class EventCreateServiceTest(TestCase):
    def setUp(self):
        self.user = _make_organizer()

    def test_created_event_is_always_draft(self):
        event = EventService.create_event(self.user, {
            'title': 'New Event',
            'event_date': date.today() + timedelta(days=5),
            'category': 'workshop',
        })
        self.assertEqual(event.status, Event.Status.DRAFT)

    def test_created_event_with_status_in_data_is_still_draft(self):
        event = EventService.create_event(self.user, {
            'title': 'New Event',
            'event_date': date.today() + timedelta(days=5),
            'category': 'workshop',
            'status': 'active',
        })
        self.assertEqual(event.status, Event.Status.DRAFT)

    def test_create_event_sets_organizer(self):
        event = EventService.create_event(self.user, {
            'title': 'New Event',
            'event_date': date.today() + timedelta(days=5),
            'category': 'workshop',
        })
        self.assertEqual(event.organizer, self.user)

    def test_create_event_rejects_past_date(self):
        with self.assertRaises(Exception):
            EventService.create_event(self.user, {
                'title': 'Past Event',
                'event_date': date.today() - timedelta(days=1),
                'category': 'workshop',
            })


class EventStatusTransitionTest(TestCase):
    def setUp(self):
        self.user = _make_organizer()
        self.event = EventService.create_event(self.user, {
            'title': 'Transition Event',
            'event_date': date.today() + timedelta(days=10),
            'category': 'conference',
        })

    def test_draft_to_active_valid(self):
        result = EventService.change_status(self.event, 'active')
        self.assertEqual(result.status, Event.Status.ACTIVE)

    def test_active_to_finished_valid(self):
        self.event.status = Event.Status.ACTIVE
        self.event.save()
        result = EventService.change_status(self.event, 'finished')
        self.assertEqual(result.status, Event.Status.FINISHED)

    def test_draft_to_finished_invalid(self):
        from rest_framework.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            EventService.change_status(self.event, 'finished')

    def test_finished_to_active_invalid(self):
        from rest_framework.exceptions import ValidationError
        self.event.status = Event.Status.FINISHED
        self.event.save()
        with self.assertRaises(ValidationError):
            EventService.change_status(self.event, 'active')

    def test_finished_to_draft_invalid(self):
        from rest_framework.exceptions import ValidationError
        self.event.status = Event.Status.FINISHED
        self.event.save()
        with self.assertRaises(ValidationError):
            EventService.change_status(self.event, 'draft')

    def test_invalid_status_value_raises_error(self):
        from rest_framework.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            EventService.change_status(self.event, 'invalid-status')

    def test_same_status_is_rejected(self):
        from rest_framework.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            EventService.change_status(self.event, 'draft')


class EventStatusSerializerTest(TestCase):
    def test_valid_status_accepted(self):
        serializer = EventStatusSerializer(data={'status': 'active'})
        self.assertTrue(serializer.is_valid())

    def test_invalid_status_rejected(self):
        serializer = EventStatusSerializer(data={'status': 'bogus'})
        self.assertFalse(serializer.is_valid())

    def test_empty_status_rejected(self):
        serializer = EventStatusSerializer(data={})
        self.assertFalse(serializer.is_valid())

    def test_none_status_rejected(self):
        serializer = EventStatusSerializer(data={'status': None})
        self.assertFalse(serializer.is_valid())


class CollaboratorEventServiceTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email='org@test.com',
            username='org',
            password='Pass1234',
            role='organizer',
        )
        self.collaborator = User.objects.create_user(
            email='col@test.com',
            username='col',
            password='Pass1234',
            role='collaborator',
        )
        self.other_collaborator = User.objects.create_user(
            email='other@test.com',
            username='other',
            password='Pass1234',
            role='collaborator',
        )
        self.event = EventService.create_event(self.organizer, {
            'title': 'Collaborator Event',
            'event_date': date.today() + timedelta(days=5),
            'category': 'workshop',
        })
        Invitation.objects.create(
            event=self.event,
            email=self.collaborator.email,
            first_name='Col',
            last_name='Test',
        )
        Invitation.objects.create(
            event=self.event,
            email='unrelated@test.com',
            first_name='Other',
            last_name='Guest',
        )

    def test_collaborator_lists_invited_event(self):
        events = EventService.list_events(self.collaborator, {})
        self.assertIn(self.event, events)

    def test_collaborator_list_excludes_uninvited_event(self):
        other_event = EventService.create_event(self.organizer, {
            'title': 'Other Event',
            'event_date': date.today() + timedelta(days=10),
            'category': 'conference',
        })
        events = EventService.list_events(self.collaborator, {})
        self.assertNotIn(other_event, events)

    def test_other_collaborator_not_invited_sees_no_events(self):
        events = EventService.list_events(self.other_collaborator, {})
        self.assertNotIn(self.event, events)

    def test_collaborator_gets_invited_event_by_id(self):
        event = EventService.get_event(self.event.id, self.collaborator)
        self.assertEqual(event, self.event)

    def test_collaborator_cannot_get_uninvited_event(self):
        other_event = EventService.create_event(self.organizer, {
            'title': 'Other Event',
            'event_date': date.today() + timedelta(days=10),
            'category': 'conference',
        })
        with self.assertRaises(Event.DoesNotExist):
            EventService.get_event(other_event.id, self.collaborator)

    def test_invited_collaborator_can_view_event_list(self):
        events = EventService.list_events(self.collaborator, {})
        self.assertEqual(len(events), 1)

    def test_collaborator_list_sees_no_events_when_not_invited(self):
        new_user = User.objects.create_user(
            email='new@test.com',
            username='new',
            password='Pass1234',
            role='collaborator',
        )
        events = EventService.list_events(new_user, {})
        self.assertEqual(len(events), 0)


class CollaboratorPermissionTest(TestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(
            email='org@test.com',
            username='org',
            password='Pass1234',
            role='organizer',
        )
        self.collaborator = User.objects.create_user(
            email='col@test.com',
            username='col',
            password='Pass1234',
            role='collaborator',
        )
        self.event = EventService.create_event(self.organizer, {
            'title': 'Permission Event',
            'event_date': date.today() + timedelta(days=5),
            'category': 'workshop',
        })

    def _make_request(self, method='GET', user=None):
        factory = APIRequestFactory()
        request = factory.generic(method, '/')
        request.user = user or self.collaborator
        return request

    def test_collaborator_invited_can_view(self):
        Invitation.objects.create(
            event=self.event,
            email=self.collaborator.email,
            first_name='Col',
            last_name='Test',
        )
        request = self._make_request('GET')
        self.assertTrue(
            IsEventOrganizer().has_object_permission(request, None, self.event)
        )

    def test_collaborator_not_invited_cannot_view(self):
        request = self._make_request('GET')
        self.assertFalse(
            IsEventOrganizer().has_object_permission(request, None, self.event)
        )

    def test_collaborator_cannot_modify_even_if_invited(self):
        Invitation.objects.create(
            event=self.event,
            email=self.collaborator.email,
            first_name='Col',
            last_name='Test',
        )
        for method in ('PUT', 'PATCH', 'DELETE'):
            request = self._make_request(method)
            self.assertFalse(
                IsEventOrganizer().has_object_permission(request, None, self.event),
                f'collaborator should not {method}',
            )

    def test_organizer_can_modify(self):
        request = self._make_request('PUT', user=self.organizer)
        self.assertTrue(
            IsEventOrganizer().has_object_permission(request, None, self.event)
        )
