"""
Middleware to extract user info from JWT token
"""
import jwt
from django.conf import settings
from django.utils.functional import SimpleLazyObject


def get_user_from_token(request):
    """Extract user info from JWT token"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get('type') == 'access':
            return {
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'role': payload.get('role')
            }
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        pass
    
    return None


class JWTAuthMiddleware:
    """
    Middleware to add user info to request from JWT token
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user_info = get_user_from_token(request)
        if user_info:
            request.user_id = user_info['user_id']
            request.user_role = user_info['role']
            request.username = user_info['username']
        else:
            request.user_id = None
            request.user_role = None
            request.username = None
        
        response = self.get_response(request)
        return response

