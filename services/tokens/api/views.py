"""
Views for tokens service
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    TokenResponseSerializer,
    RefreshTokenSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer
)
from .services import TokenService


class AuthViewSet(viewsets.ViewSet):
    """
    Authentication endpoints
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """User registration"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            access_token = TokenService.generate_access_token(user)
            refresh_token = TokenService.generate_refresh_token(user)
            
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Get user and check password directly (authenticate may not work with custom User model)
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response(
                    {'error': 'Неверные учетные данные'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        access_token = TokenService.generate_access_token(user)
        refresh_token = TokenService.generate_refresh_token(user)
        
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh access token"""
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = serializer.validated_data['refresh_token']
        user = TokenService.validate_refresh_token(refresh_token)
        
        if user is None:
            return Response(
                {'error': 'Недействительный refresh токен'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        access_token = TokenService.generate_access_token(user)
        new_refresh_token = TokenService.generate_refresh_token(user)
        
        # Revoke old refresh token
        TokenService.revoke_refresh_token(refresh_token)
        
        return Response({
            'access_token': access_token,
            'refresh_token': new_refresh_token,
            'user': UserSerializer(user).data
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """User logout"""
        serializer = RefreshTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        refresh_token = serializer.validated_data['refresh_token']
        TokenService.revoke_refresh_token(refresh_token)
        
        return Response({'message': 'Успешный выход'})
    
    @action(detail=False, methods=['post'])
    def password_reset_request(self, request):
        """Request password reset"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
            TokenService.create_password_reset_token(user)
        except User.DoesNotExist:
            pass  # Don't reveal if user exists
        
        return Response({
            'message': 'Если пользователь с таким email существует, инструкции отправлены'
        })
    
    @action(detail=False, methods=['post'])
    def password_reset(self, request):
        """Reset password"""
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        user = TokenService.validate_password_reset_token(token)
        if user is None:
            return Response(
                {'error': 'Недействительный или истекший токен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        TokenService.use_password_reset_token(token)
        
        return Response({'message': 'Пароль успешно изменен'})


class TokenViewSet(viewsets.ViewSet):
    """
    Token validation endpoints
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate access token"""
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payload = TokenService.validate_access_token(token)
        if payload:
            return Response({
                'valid': True,
                'user_id': payload.get('user_id'),
                'username': payload.get('username'),
                'role': payload.get('role')
            })
        
        return Response({
            'valid': False
        }, status=status.HTTP_401_UNAUTHORIZED)

