"""
Business logic services for notifications
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Notification
from .tasks import send_email_task, send_sms_task


class NotificationService:
    """
    Service for sending notifications
    """
    
    @staticmethod
    def send_email(user_id, recipient, subject, message, template=None, context=None):
        """Send email notification"""
        notification = Notification.objects.create(
            user_id=user_id,
            notification_type='email',
            subject=subject,
            message=message,
            recipient=recipient,
            status='pending'
        )
        
        # Send via Celery task
        send_email_task.delay(notification.id, template, context)
        
        return notification
    
    @staticmethod
    def send_sms(user_id, recipient, message):
        """Send SMS notification"""
        notification = Notification.objects.create(
            user_id=user_id,
            notification_type='sms',
            message=message,
            recipient=recipient,
            status='pending'
        )
        
        # Send via Celery task
        send_sms_task.delay(notification.id)
        
        return notification
    
    @staticmethod
    def send_password_reset_email(email, token, user_id):
        """Send password reset email"""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        context = {
            'reset_url': reset_url,
            'token': token,
        }
        
        return NotificationService.send_email(
            user_id=user_id,
            recipient=email,
            subject='Сброс пароля',
            message=f'Для сброса пароля перейдите по ссылке: {reset_url}',
            template='password_reset.html',
            context=context
        )
    
    @staticmethod
    def send_registration_email(email, username, user_id):
        """Send registration confirmation email"""
        context = {
            'username': username,
            'login_url': f"{settings.FRONTEND_URL}/login",
        }
        
        return NotificationService.send_email(
            user_id=user_id,
            recipient=email,
            subject='Добро пожаловать на платформу!',
            message=f'Добро пожаловать, {username}! Вы успешно зарегистрированы.',
            template='registration.html',
            context=context
        )

