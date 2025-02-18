from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method == permissions.SAFE_METHODS or (request.user or request.user.is_staff))