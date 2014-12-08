from rest_framework import permissions

from .models import Tweet

class IsApprover(permissions.BasePermission):
    """
    Object-level permission to only allow approvers to change
    the status of a tweet.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if 'status' in request.data:
            if not request.user.is_approver and request.data['status'] != Tweet.PENDING:
                # The user is not an approver but they are trying to set the status
                # to an approved or reject
                return False

        return True
