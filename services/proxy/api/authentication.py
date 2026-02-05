"""
JWT Authentication for API Gateway
"""
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests


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
                
                if user_id:
                    # Return user object (simplified - in production would fetch from DB)
                    from django.contrib.auth.models import AnonymousUser
                    # In real implementation, fetch user from database
                    return (None, {'user_id': user_id})
            
            raise AuthenticationFailed('Invalid token')
            
        except requests.RequestException:
            raise AuthenticationFailed('Token service unavailable')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

