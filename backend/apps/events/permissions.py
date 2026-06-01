from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEventOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in SAFE_METHODS and request.user.role == 'collaborator':
            return obj.invitations.filter(email=request.user.email).exists()
        return obj.organizer == request.user


class CanCreateEvent(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ('admin', 'organizer')


class CanDeleteEvent(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.organizer == request.user
