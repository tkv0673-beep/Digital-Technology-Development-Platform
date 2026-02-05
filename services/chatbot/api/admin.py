"""
Admin configuration for chatbot service
"""
from django.contrib import admin
from .models import ChatMessage, ChatContext


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lesson_id', 'created_at')
    list_filter = ('lesson_id', 'created_at')
    search_fields = ('message', 'response')


@admin.register(ChatContext)
class ChatContextAdmin(admin.ModelAdmin):
    list_display = ('lesson_id', 'created_at', 'updated_at')
    search_fields = ('context_prompt',)

