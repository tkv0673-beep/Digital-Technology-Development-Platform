"""
Business logic services for chatbot
"""
import requests
from django.conf import settings
from django.core.cache import cache
from .models import ChatMessage, ChatContext


class ChatBotService:
    """
    Service for chatbot interactions
    """
    
    @staticmethod
    def get_lesson_context(lesson_id):
        """Get context for lesson"""
        cache_key = f'lesson_context_{lesson_id}'
        context = cache.get(cache_key)
        
        if context is None:
            try:
                context_obj = ChatContext.objects.get(lesson_id=lesson_id)
                context = {
                    'prompt': context_obj.context_prompt,
                    'common_questions': context_obj.common_questions
                }
                cache.set(cache_key, context, 3600)  # Cache for 1 hour
            except ChatContext.DoesNotExist:
                # Fetch lesson data from courses service
                try:
                    response = requests.get(
                        f'{settings.COURSES_SERVICE_URL}/api/courses/lessons/{lesson_id}/',
                        timeout=5
                    )
                    if response.status_code == 200:
                        lesson_data = response.json()
                        context = {
                            'prompt': f"Пользователь изучает урок: {lesson_data.get('title', '')}. {lesson_data.get('description', '')}",
                            'common_questions': []
                        }
                except requests.RequestException:
                    context = {'prompt': '', 'common_questions': []}
        
        return context
    
    @staticmethod
    def generate_response(user_message, lesson_id=None, context_data=None):
        """Generate chatbot response"""
        # Get context if lesson_id provided
        context = {}
        if lesson_id:
            context = ChatBotService.get_lesson_context(lesson_id)
        
        # Build prompt
        system_prompt = """Ты - дружелюбный виртуальный помощник для платформы обучения цифровым технологиям старшего поколения.
        Твоя задача - помогать пользователям в освоении курсов, отвечать на вопросы простым и понятным языком.
        Будь терпеливым, используй простые объяснения и пошаговые инструкции."""
        
        if context.get('prompt'):
            system_prompt += f"\n\nКонтекст текущего урока: {context['prompt']}"
        
        # Check common questions first
        if context.get('common_questions'):
            for qa in context['common_questions']:
                if qa.get('question', '').lower() in user_message.lower():
                    return qa.get('answer', '')
        
        # Generate response (simplified - in production would use OpenAI or local LLM)
        # For now, return a simple response
        responses = [
            "Я помогу вам разобраться с этим вопросом. Давайте пошагово рассмотрим...",
            "Отличный вопрос! Вот как это работает...",
            "Понимаю вашу задачу. Вот пошаговая инструкция...",
        ]
        
        # Simple keyword matching for demo
        if 'помощь' in user_message.lower() or 'help' in user_message.lower():
            return "Я здесь, чтобы помочь! Расскажите, с чем у вас возникли трудности, и я дам подробные инструкции."
        elif 'следующий' in user_message.lower() or 'далее' in user_message.lower():
            return "Отлично! Вы можете перейти к следующему шагу. Следуйте инструкциям на экране."
        elif 'ошибка' in user_message.lower() or 'не работает' in user_message.lower():
            return "Не переживайте! Ошибки - это нормальная часть обучения. Попробуйте выполнить действие еще раз, следуя инструкциям."
        else:
            return responses[0]  # Default response
    
    @staticmethod
    def save_message(user_id, message, response, lesson_id=None, context_data=None):
        """Save chat message"""
        return ChatMessage.objects.create(
            user_id=user_id,
            message=message,
            response=response,
            lesson_id=lesson_id,
            context_data=context_data or {}
        )

