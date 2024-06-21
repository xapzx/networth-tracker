from rest_framework import permissions


class isOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user


class onlyAdminCanDelete(permissions.BasePermission):
    """
    Custom permission to restrict users (except admins) from deleting objects.
    """

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return request.user.is_staff or request.user.is_superuser
        return True


class onlyOneAccountAllowed(permissions.BasePermission):
    """
    Custom permission to restrict users to a single account.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.account_set.exists()
        return True  # Allow other methods (GET, PUT, PATCH, DELETE)
