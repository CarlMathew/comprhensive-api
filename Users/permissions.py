from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
        Permission for Admin users only
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == "admin"

class isManager(BasePermission):
    """Permission for Manager Only"""

    def has_permission(self, request, view):
        return request.user and request.user.role in ["admin", "manager"]

class isUser(BasePermission):
    """Permission for regular users"""

    def has_permission(self, request, view):
        return request.user and request.user.role in ["admin", "manager", "user"]
