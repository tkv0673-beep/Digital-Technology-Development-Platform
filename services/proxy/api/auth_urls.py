"""
Authentication URLs - proxy to tokens service
"""
from django.urls import path
from .views import RegisterProxyView, LoginProxyView, RefreshProxyView, LogoutProxyView

urlpatterns = [
    path('register/', RegisterProxyView.as_view(), name='register'),
    path('login/', LoginProxyView.as_view(), name='login'),
    path('refresh/', RefreshProxyView.as_view(), name='refresh'),
    path('logout/', LogoutProxyView.as_view(), name='logout'),
]

