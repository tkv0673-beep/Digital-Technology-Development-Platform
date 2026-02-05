"""
Models for chatbot service
"""
from django.db import models


class ChatMessage(models.Model):
    """
    Chat message model
    """
    user_id = models.IntegerField()
    message = models.TextField()
    response = models.TextField()
    lesson_id = models.IntegerField(null=True, blank=True, help_text='Context lesson ID')
    context_data = models.JSONField(default=dict, help_text='Additional context data')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['lesson_id']),
        ]


class ChatContext(models.Model):
    """
    Chat context for lessons
    """
    lesson_id = models.IntegerField(unique=True)
    context_prompt = models.TextField(help_text='Context prompt for the lesson')
    common_questions = models.JSONField(default=list, help_text='Common questions and answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_contexts'
        verbose_name = 'Контекст чата'
        verbose_name_plural = 'Контексты чата'

