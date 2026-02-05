"""
ChatBot service URLs
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChatBotViewSet, ChatContextViewSet

router = DefaultRouter()
router.register(r'chatbot', ChatBotViewSet, basename='chatbot')
router.register(r'contexts', ChatContextViewSet, basename='contexts')

urlpatterns = router.urls

