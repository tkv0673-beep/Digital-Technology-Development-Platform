"""
Streaming service URLs
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

router = DefaultRouter()
router.register(r'streaming', VideoViewSet, basename='streaming')

urlpatterns = router.urls

