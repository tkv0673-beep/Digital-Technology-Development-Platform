"""
Utility functions for tokens service
"""
import secrets
from datetime import timedelta
from django.utils import timezone


def generate_secure_token(length=32):
    """
    Generate a secure random token
    """
    return secrets.token_urlsafe(length)


def get_token_expiry(lifetime_seconds):
    """
    Get expiry datetime for token
    """
    return timezone.now() + timedelta(seconds=lifetime_seconds)

