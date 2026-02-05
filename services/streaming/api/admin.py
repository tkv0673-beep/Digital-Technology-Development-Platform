"""
Admin configuration for streaming service
"""
from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_id', 'duration', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')

