from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Класс доступа с правами админа или чтения"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class OwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Класс доступа с правами админа или автора или чтения"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_moderator
            or request.user.is_admin
            or obj.author == request.user
        )


class UserIsAdmin(permissions.BasePermission):
    """Класс доступа с правами админа"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)
