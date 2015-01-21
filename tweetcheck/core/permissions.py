from rest_framework import permissions

class IsOrganizationAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow approvers to change
    the details of users other than themselves.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_approver and obj != request.user:
            # This request is not trying to update its own user
            # and it's not coming from an approver
            return False

        return True
