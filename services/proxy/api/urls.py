"""
API Gateway URLs - routes requests to appropriate microservices
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProxyViewSet

router = DefaultRouter()
router.register(r'proxy', ProxyViewSet, basename='proxy')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('api.auth_urls')),
    path('courses/', include('api.courses_urls')),
    path('lessons/', include('api.lessons_urls')),
    path('streaming/', include('api.streaming_urls')),
    path('chatbot/', include('api.chatbot_urls')),
]

