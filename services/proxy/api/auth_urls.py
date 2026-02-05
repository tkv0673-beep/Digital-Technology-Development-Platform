"""
Authentication URLs - proxy to tokens service
"""
from django.urls import path
from .views import AuthProxyView

urlpatterns = [
    path('register/', AuthProxyView.as_view(http_method_names=['post']), name='register'),
    path('login/', AuthProxyView.as_view(http_method_names=['post']), name='login'),
    path('refresh/', AuthProxyView.as_view(http_method_names=['post']), name='refresh'),
    path('logout/', AuthProxyView.as_view(http_method_names=['post']), name='logout'),
]

