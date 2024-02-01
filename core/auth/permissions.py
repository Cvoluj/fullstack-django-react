from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class UserPermission(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS

        if view.basename in ['post']:
            return bool(request.user and
                        request.user.is_authenticated)

        if view.basename in ['post-comment']:
            if request.method in ['DELETE']:
                return bool(
                    request.user.is_superuser
                    or request.user in [obj.author, obj.post.author]
                )
            return bool(request.user and request.user.is_authenticated)

        if view.basename in ['user']:
            if request.method in SAFE_METHODS:
                return True
            return bool(request.user.id == obj.id)
        return False

    def has_permission(self, request: Request, view):
        if view.basename in ['post', 'post-comment', 'user', 'auth-logout']:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS

            return bool(request.user and
                        request.user.is_authenticated)

        return False
