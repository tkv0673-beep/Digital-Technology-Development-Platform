"""
Serializers for chatbot service
"""
from rest_framework import serializers
from .models import ChatMessage, ChatContext


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for chat message"""
    class Meta:
        model = ChatMessage
        fields = ('id', 'message', 'response', 'lesson_id', 'created_at')
        read_only_fields = ('id', 'response', 'created_at')


class ChatMessageRequestSerializer(serializers.Serializer):
    """Serializer for chat message request"""
    message = serializers.CharField()
    lesson_id = serializers.IntegerField(required=False, allow_null=True)
    context_data = serializers.JSONField(required=False, default=dict)


class ChatContextSerializer(serializers.ModelSerializer):
    """Serializer for chat context"""
    class Meta:
        model = ChatContext
        fields = ('lesson_id', 'context_prompt', 'common_questions', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

