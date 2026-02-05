"""
Unit tests for chatbot service
"""
from django.test import TestCase
from .models import ChatMessage, ChatContext
from .services import ChatBotService


class ChatBotServiceTests(TestCase):
    """Tests for ChatBotService"""
    
    def setUp(self):
        self.lesson_id = 1
        ChatContext.objects.create(
            lesson_id=self.lesson_id,
            context_prompt='Test context',
            common_questions=[{'question': 'test', 'answer': 'test answer'}]
        )
    
    def test_get_lesson_context(self):
        """Test getting lesson context"""
        context = ChatBotService.get_lesson_context(self.lesson_id)
        self.assertIsNotNone(context)
        self.assertIn('prompt', context)
        self.assertIn('common_questions', context)
    
    def test_generate_response(self):
        """Test response generation"""
        response = ChatBotService.generate_response('test message', self.lesson_id)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
    
    def test_save_message(self):
        """Test message saving"""
        message = ChatBotService.save_message(
            user_id=1,
            message='test message',
            response='test response',
            lesson_id=self.lesson_id
        )
        self.assertIsNotNone(message)
        self.assertEqual(message.user_id, 1)
        self.assertEqual(message.message, 'test message')


class ChatMessageModelTests(TestCase):
    """Tests for ChatMessage model"""
    
    def test_chat_message_creation(self):
        """Test chat message creation"""
        message = ChatMessage.objects.create(
            user_id=1,
            message='test message',
            response='test response',
            lesson_id=1
        )
        self.assertIsNotNone(message)
        self.assertEqual(message.user_id, 1)

