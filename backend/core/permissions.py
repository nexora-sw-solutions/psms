from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'SUPER_ADMIN'

class IsFirmAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # Super Admin implies Firm Admin rights usually, or check strict role
        return request.user.role in ['FIRM_ADMIN', 'SUPER_ADMIN']

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['MANAGER', 'FIRM_ADMIN', 'SUPER_ADMIN']

class IsConsultant(permissions.BasePermission):
    def has_permission(self, request, view):
        # Consultants can generally read/write their own stuff, handled in views
        return request.user.role == 'CONSULTANT' or request.user.is_staff