from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSelfOrIsAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy', 'partial_update'] and request.user != obj:
            return False
        return IsAuthenticated().has_permission(request, view)
