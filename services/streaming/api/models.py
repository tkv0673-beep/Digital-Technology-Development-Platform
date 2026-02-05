"""
Models for streaming service
"""
from django.db import models
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    """
    Video lesson model
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]
    )
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    duration = models.IntegerField(help_text='Duration in seconds', default=0)
    lesson_id = models.IntegerField(help_text='Related lesson ID from courses service', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'videos'
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        indexes = [
            models.Index(fields=['lesson_id']),
        ]

