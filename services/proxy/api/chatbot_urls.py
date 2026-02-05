"""
ChatBot URLs - proxy to chatbot service
"""
from django.urls import path
from .views import ChatBotProxyView

urlpatterns = [
    path('message/', ChatBotProxyView.as_view({'post': 'message'}), name='chatbot-message'),
    path('context/<int:lesson_id>/', ChatBotProxyView.as_view({'get': 'context'}), name='chatbot-context'),
]

