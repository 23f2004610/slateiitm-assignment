from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission class that allows access based on user roles.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Get the allowed roles from the view
        allowed_roles = getattr(view, 'allowed_roles', [])

        # Ensure the user has a valid role
        if not request.user.role:
            return False

        # Grant access if the user's role is in the allowed roles
        return request.user.role in allowed_roles
