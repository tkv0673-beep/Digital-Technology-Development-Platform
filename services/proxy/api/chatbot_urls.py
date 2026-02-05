"""
ChatBot URLs - proxy to chatbot service
"""
from django.urls import path
from .views import ChatBotMessageProxyView, ChatBotContextProxyView

urlpatterns = [
    path('message/', ChatBotMessageProxyView.as_view(), name='chatbot-message'),
    path('context/<int:lesson_id>/', ChatBotContextProxyView.as_view(), name='chatbot-context'),
]

