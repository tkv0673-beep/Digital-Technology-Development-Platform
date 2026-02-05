"""
Custom permissions for courses service
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


class IsEnrolled(permissions.BasePermission):
    """
    Permission check for course enrollment
    """
    
    def has_object_permission(self, request, view, obj):
        if not hasattr(request, 'user_id'):
            return False
        
        from .models import Enrollment
        return Enrollment.objects.filter(
            user_id=request.user_id,
            course=obj
        ).exists()

