from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return IsAuthenticated().has_permission(request, view)

        # Write permissions are only allowed to the owner of the snippet.
        return request.user in [getattr(obj, 'owner', None),
                                getattr(obj, 'user', None),
                                getattr(obj, 'selected_by', None),
                                getattr(obj, 'profile', None)]
