"""
Admin configuration for notifications service
"""
from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'notification_type', 'subject', 'status', 'sent_at', 'created_at')
    list_filter = ('notification_type', 'status', 'created_at')
    search_fields = ('recipient', 'subject', 'message')

