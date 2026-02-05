"""
Celery tasks for notifications
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification
from django.utils import timezone


@shared_task
def send_email_task(notification_id, template=None, context=None):
    """Task to send email"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        if template and context:
            message = render_to_string(f'emails/{template}', context)
        else:
            message = notification.message
        
        send_mail(
            subject=notification.subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient],
            fail_silently=False,
            html_message=message if template else None
        )
        
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
    except Exception as e:
        notification = Notification.objects.get(id=notification_id)
        notification.status = 'failed'
        notification.error_message = str(e)
        notification.save()
        raise


@shared_task
def send_sms_task(notification_id):
    """Task to send SMS (placeholder - integrate with SMS provider)"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # TODO: Integrate with SMS provider (Twilio, SMS.ru, etc.)
        # For now, just mark as sent
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
    except Exception as e:
        notification = Notification.objects.get(id=notification_id)
        notification.status = 'failed'
        notification.error_message = str(e)
        notification.save()
        raise

