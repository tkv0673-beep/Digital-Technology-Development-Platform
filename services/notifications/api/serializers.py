"""
Serializers for notifications service
"""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notification"""
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('id', 'status', 'sent_at', 'created_at')


class PasswordResetNotificationSerializer(serializers.Serializer):
    """Serializer for password reset notification"""
    email = serializers.EmailField()
    token = serializers.CharField()
    user_id = serializers.IntegerField()


class RegistrationNotificationSerializer(serializers.Serializer):
    """Serializer for registration notification"""
    email = serializers.EmailField()
    username = serializers.CharField()
    user_id = serializers.IntegerField()

