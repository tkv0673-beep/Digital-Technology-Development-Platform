"""
Tokens service URLs
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, TokenViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'tokens', TokenViewSet, basename='tokens')

urlpatterns = router.urls

