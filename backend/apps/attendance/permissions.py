from rest_framework.permissions import BasePermission

from events.models import Event


class CanManageAttendance(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role != 'organizer':
            return False

        event_id = request.query_params.get('event')
        if event_id:
            return Event.objects.filter(id=event_id, organizer=request.user).exists()
        return True


class CanCheckin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'organizer')

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if not hasattr(obj, 'organizer'):
            return obj.event.organizer == request.user
        return obj.organizer == request.user


class IsEventOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.event.organizer == request.user
