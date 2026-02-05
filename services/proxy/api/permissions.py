"""
Custom permissions for proxy service
"""
from rest_framework import permissions


class IsMentor(permissions.BasePermission):
    """
    Permission check for mentor role
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            hasattr(request, 'user_role') and
            request.user_role == 'mentor'
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission check for object ownership
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            hasattr(request, 'user_id') and
            hasattr(obj, 'mentor_id') and
            obj.mentor_id == request.user_id
        )

