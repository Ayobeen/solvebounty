from rest_framework import permissions

class IsPoster(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['POSTER', 'BOTH', 'ADMIN']
        )

class IsSolver(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['SOLVER', 'BOTH', 'ADMIN']
        )

class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.role in ['ADMIN', 'MODERATOR'])
        )

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'poster'):
            return obj.poster == request.user
        if hasattr(obj, 'solver'):
            return obj.solver == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False
