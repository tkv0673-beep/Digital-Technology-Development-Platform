"""
JWT Authentication for chatbot service
Extracts user info from JWT token or request headers
"""
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
import jwt
from django.conf import settings
import requests


class AuthenticatedUser:
    """
    Simple user object for authenticated requests
    """
    def __init__(self, user_id, username=None, role=None):
        self.id = user_id
        self.pk = user_id
        self.user_id = user_id  # For compatibility
        self.username = username or f'user_{user_id}'
        self.role = role
        self.is_authenticated = True
        self.is_anonymous = False
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
    
    def __str__(self):
        return self.username


class JWTAuthentication(BaseAuthentication):
    """
    JWT Authentication that validates tokens via tokens service
    or extracts user info from headers set by proxy
    """
    
    def authenticate(self, request):
        # First, try to get user_id from headers (set by proxy middleware)
        if hasattr(request, 'user_id') and request.user_id:
            user = AuthenticatedUser(
                request.user_id,
                getattr(request, 'username', None),
                getattr(request, 'user_role', None)
            )
            return (user, None)
        
        # Fallback: try to validate JWT token directly
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            # Validate token with tokens service
            tokens_service_url = getattr(settings, 'TOKENS_SERVICE_URL', 'http://tokens-service:8000')
            response = requests.post(
                f'{tokens_service_url}/api/tokens/validate/',
                json={'token': token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                user_id = data.get('user_id')
                username = data.get('username')
                role = data.get('role')
                
                if user_id:
                    user = AuthenticatedUser(user_id, username, role)
                    return (user, None)
            
            return None
            
        except Exception:
            return None

