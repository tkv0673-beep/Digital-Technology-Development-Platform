"""
Models for notifications service
"""
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    """
    Notification record
    """
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает отправки'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]
    
    user_id = models.IntegerField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    recipient = models.CharField(max_length=255)  # email or phone
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        indexes = [
            models.Index(fields=['user_id', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]

