from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    message = 'Нельзя менять не совё.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator')


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
            or request.user.is_superuser
        )
    # def has_permission(self, request, view):
    #     if request.user.is_authenticated:
    #         return bool(request.user.is_staff
    #                     or request.user.role == 'admin')
