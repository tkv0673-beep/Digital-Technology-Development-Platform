"""
Signals for tokens service
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
import requests
from django.conf import settings


@receiver(post_save, sender=User)
def send_registration_notification(sender, instance, created, **kwargs):
    """
    Send registration notification when user is created
    """
    if created and instance.email:
        try:
            requests.post(
                f'{settings.NOTIFICATIONS_SERVICE_URL}/api/notifications/registration/',
                json={
                    'email': instance.email,
                    'username': instance.username,
                    'user_id': instance.id
                },
                timeout=5
            )
        except requests.RequestException:
            pass  # Log error but don't fail

