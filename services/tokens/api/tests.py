"""
Unit tests for tokens service
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, RefreshToken, PasswordResetToken
from .services import TokenService

User = get_user_model()


class TokenServiceTests(TestCase):
    """Tests for TokenService"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_generate_access_token(self):
        """Test access token generation"""
        token = TokenService.generate_access_token(self.user)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
    
    def test_generate_refresh_token(self):
        """Test refresh token generation"""
        token = TokenService.generate_refresh_token(self.user)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertTrue(RefreshToken.objects.filter(user=self.user, token=token).exists())
    
    def test_validate_access_token(self):
        """Test access token validation"""
        token = TokenService.generate_access_token(self.user)
        payload = TokenService.validate_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload['user_id'], self.user.id)
        self.assertEqual(payload['username'], self.user.username)
    
    def test_validate_refresh_token(self):
        """Test refresh token validation"""
        token = TokenService.generate_refresh_token(self.user)
        user = TokenService.validate_refresh_token(token)
        self.assertEqual(user, self.user)
    
    def test_revoke_refresh_token(self):
        """Test refresh token revocation"""
        token = TokenService.generate_refresh_token(self.user)
        result = TokenService.revoke_refresh_token(token)
        self.assertTrue(result)
        refresh_token = RefreshToken.objects.get(token=token)
        self.assertTrue(refresh_token.is_revoked)


class AuthViewSetTests(TestCase):
    """Tests for AuthViewSet"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'role': 'mentee'
        }
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_user(self):
        """Test user login"""
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_refresh_token(self):
        """Test token refresh"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        refresh_token = TokenService.generate_refresh_token(user)
        response = self.client.post('/api/auth/refresh/', {
            'refresh_token': refresh_token
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)


class PasswordResetTests(TestCase):
    """Tests for password reset"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpass123'
        )
    
    def test_create_password_reset_token(self):
        """Test password reset token creation"""
        token = TokenService.create_password_reset_token(self.user)
        self.assertIsNotNone(token)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user, token=token).exists())
    
    def test_validate_password_reset_token(self):
        """Test password reset token validation"""
        token = TokenService.create_password_reset_token(self.user)
        user = TokenService.validate_password_reset_token(token)
        self.assertEqual(user, self.user)
    
    def test_use_password_reset_token(self):
        """Test password reset token usage"""
        token = TokenService.create_password_reset_token(self.user)
        result = TokenService.use_password_reset_token(token)
        self.assertTrue(result)
        reset_token = PasswordResetToken.objects.get(token=token)
        self.assertTrue(reset_token.is_used)

