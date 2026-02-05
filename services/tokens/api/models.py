"""
Models for tokens service
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Extended User model with roles
    """
    ROLE_CHOICES = [
        ('mentor', 'Ментор'),
        ('mentee', 'Менти'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mentee')
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    # Fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )


class RefreshToken(models.Model):
    """
    Refresh token storage
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'refresh_tokens'
        verbose_name = 'Refresh токен'
        verbose_name_plural = 'Refresh токены'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'is_revoked']),
        ]
    
    def is_valid(self):
        """Check if token is valid"""
        return not self.is_revoked and self.expires_at > timezone.now()


class PasswordResetToken(models.Model):
    """
    Password reset token storage
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Токен сброса пароля'
        verbose_name_plural = 'Токены сброса пароля'
        indexes = [
            models.Index(fields=['token']),
        ]
    
    def is_valid(self):
        """Check if token is valid"""
        return not self.is_used and self.expires_at > timezone.now()

