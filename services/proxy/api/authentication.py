"""
JWT Authentication for API Gateway
"""
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
import requests


class AuthenticatedUser:
    """
    Simple user object for authenticated requests
    """
    def __init__(self, user_id, username=None, role=None):
        self.id = user_id
        self.pk = user_id
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
    JWT Authentication class that validates tokens via tokens service
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            # Validate token with tokens service
            response = requests.post(
                f'{settings.TOKENS_SERVICE_URL}/api/tokens/validate/',
                json={'token': token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                user_id = data.get('user_id')
                username = data.get('username')
                role = data.get('role')
                
                if user_id:
                    # Return authenticated user object
                    user = AuthenticatedUser(user_id, username, role)
                    return (user, None)
            
            raise AuthenticationFailed('Invalid token')
            
        except requests.RequestException as e:
            raise AuthenticationFailed(f'Token service unavailable: {str(e)}')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')

