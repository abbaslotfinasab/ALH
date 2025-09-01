# posts/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return True if request.method in SAFE_METHODS else bool(request.user and request.user.is_staff)
