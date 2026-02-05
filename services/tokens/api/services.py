"""
Business logic services for tokens
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import User, RefreshToken, PasswordResetToken
import secrets
import requests


class TokenService:
    """
    Service for JWT token management
    """
    
    @staticmethod
    def generate_access_token(user):
        """Generate JWT access token"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_ACCESS_TOKEN_LIFETIME),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @staticmethod
    def generate_refresh_token(user):
        """Generate and store refresh token"""
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(seconds=settings.JWT_REFRESH_TOKEN_LIFETIME)
        
        RefreshToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        return token
    
    @staticmethod
    def validate_access_token(token):
        """Validate access token"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            if payload.get('type') != 'access':
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def validate_refresh_token(token):
        """Validate refresh token"""
        try:
            refresh_token = RefreshToken.objects.get(token=token, is_revoked=False)
            if refresh_token.is_valid():
                return refresh_token.user
            return None
        except RefreshToken.DoesNotExist:
            return None
    
    @staticmethod
    def revoke_refresh_token(token):
        """Revoke refresh token"""
        try:
            refresh_token = RefreshToken.objects.get(token=token)
            refresh_token.is_revoked = True
            refresh_token.save()
            return True
        except RefreshToken.DoesNotExist:
            return False
    
    @staticmethod
    def create_password_reset_token(user):
        """Create password reset token"""
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=1)
        
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Send notification via notifications service
        try:
            requests.post(
                f'{settings.NOTIFICATIONS_SERVICE_URL}/api/notifications/password-reset/',
                json={
                    'email': user.email,
                    'token': token,
                    'user_id': user.id
                },
                timeout=5
            )
        except requests.RequestException:
            pass  # Log error but don't fail
        
        return token
    
    @staticmethod
    def validate_password_reset_token(token):
        """Validate password reset token"""
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_valid():
                return reset_token.user
            return None
        except PasswordResetToken.DoesNotExist:
            return None
    
    @staticmethod
    def use_password_reset_token(token):
        """Mark password reset token as used"""
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            reset_token.is_used = True
            reset_token.save()
            return True
        except PasswordResetToken.DoesNotExist:
            return False

