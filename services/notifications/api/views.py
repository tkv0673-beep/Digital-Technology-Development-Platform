"""
Views for notifications service
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notification
from .serializers import (
    NotificationSerializer,
    PasswordResetNotificationSerializer,
    RegistrationNotificationSerializer
)
from .services import NotificationService


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Notification endpoints
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def password_reset(self, request):
        """Send password reset notification"""
        serializer = PasswordResetNotificationSerializer(data=request.data)
        if serializer.is_valid():
            NotificationService.send_password_reset_email(
                email=serializer.validated_data['email'],
                token=serializer.validated_data['token'],
                user_id=serializer.validated_data['user_id']
            )
            return Response({'message': 'Password reset email sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def registration(self, request):
        """Send registration notification"""
        serializer = RegistrationNotificationSerializer(data=request.data)
        if serializer.is_valid():
            NotificationService.send_registration_email(
                email=serializer.validated_data['email'],
                username=serializer.validated_data['username'],
                user_id=serializer.validated_data['user_id']
            )
            return Response({'message': 'Registration email sent'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

