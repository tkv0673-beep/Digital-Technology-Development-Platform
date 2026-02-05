"""
Unit tests for notifications service
"""
from django.test import TestCase
from .models import Notification
from .services import NotificationService


class NotificationServiceTests(TestCase):
    """Tests for NotificationService"""
    
    def test_send_email(self):
        """Test email notification creation"""
        notification = NotificationService.send_email(
            user_id=1,
            recipient='test@example.com',
            subject='Test Subject',
            message='Test Message'
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.notification_type, 'email')
        self.assertEqual(notification.recipient, 'test@example.com')
        self.assertEqual(notification.status, 'pending')
    
    def test_send_password_reset_email(self):
        """Test password reset email"""
        notification = NotificationService.send_password_reset_email(
            email='test@example.com',
            token='test_token',
            user_id=1
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.notification_type, 'email')
        self.assertEqual(notification.subject, 'Сброс пароля')
    
    def test_send_registration_email(self):
        """Test registration email"""
        notification = NotificationService.send_registration_email(
            email='test@example.com',
            username='testuser',
            user_id=1
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.notification_type, 'email')
        self.assertEqual(notification.subject, 'Добро пожаловать на платформу!')


class NotificationModelTests(TestCase):
    """Tests for Notification model"""
    
    def test_notification_creation(self):
        """Test notification creation"""
        notification = Notification.objects.create(
            user_id=1,
            notification_type='email',
            subject='Test Subject',
            message='Test Message',
            recipient='test@example.com'
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.status, 'pending')

