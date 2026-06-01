from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'organizer'


class IsCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'collaborator'


class IsAdminOrOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'organizer')


class IsAdminOrCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('admin', 'collaborator')
