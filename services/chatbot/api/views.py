"""
Views for chatbot service
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage, ChatContext
from .serializers import (
    ChatMessageSerializer,
    ChatMessageRequestSerializer,
    ChatContextSerializer
)
from .services import ChatBotService


class ChatBotViewSet(viewsets.ViewSet):
    """
    ChatBot endpoints
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def message(self, request):
        """Send message to chatbot"""
        serializer = ChatMessageRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_message = serializer.validated_data['message']
        lesson_id = serializer.validated_data.get('lesson_id')
        context_data = serializer.validated_data.get('context_data', {})
        
        # Generate response
        response_text = ChatBotService.generate_response(
            user_message=user_message,
            lesson_id=lesson_id,
            context_data=context_data
        )
        
        # Save message
        user_id = getattr(request.user, 'user_id', request.user.id)
        chat_message = ChatBotService.save_message(
            user_id=user_id,
            message=user_message,
            response=response_text,
            lesson_id=lesson_id,
            context_data=context_data
        )
        
        return Response({
            'response': response_text,
            'message_id': chat_message.id
        })
    
    @action(detail=False, methods=['get'], url_path='context/(?P<lesson_id>[0-9]+)')
    def context(self, request, lesson_id=None):
        """Get context for lesson"""
        try:
            context_obj = ChatContext.objects.get(lesson_id=lesson_id)
            serializer = ChatContextSerializer(context_obj)
            return Response(serializer.data)
        except ChatContext.DoesNotExist:
            # Try to get from courses service and create context
            context = ChatBotService.get_lesson_context(lesson_id)
            return Response({
                'lesson_id': lesson_id,
                'context_prompt': context.get('prompt', ''),
                'common_questions': context.get('common_questions', [])
            })
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get chat history"""
        user_id = getattr(request.user, 'user_id', request.user.id)
        messages = ChatMessage.objects.filter(user_id=user_id).order_by('-created_at')[:50]
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class ChatContextViewSet(viewsets.ModelViewSet):
    """
    Chat context management (for admins/mentors)
    """
    queryset = ChatContext.objects.all()
    serializer_class = ChatContextSerializer
    permission_classes = [IsAuthenticated]

