"""
Authentication URLs - proxy to tokens service
"""
from django.urls import path
from .views import AuthProxyView

urlpatterns = [
    path('register/', AuthProxyView.as_view({'post': 'register'}), name='register'),
    path('login/', AuthProxyView.as_view({'post': 'login'}), name='login'),
    path('refresh/', AuthProxyView.as_view({'post': 'refresh'}), name='refresh'),
    path('logout/', AuthProxyView.as_view({'post': 'logout'}), name='logout'),
]

