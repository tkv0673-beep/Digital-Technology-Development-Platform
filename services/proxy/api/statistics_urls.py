"""
Statistics URLs - proxy to courses service
"""
from django.urls import path
from .views import UserStatisticsProxyView

urlpatterns = [
    path('profile/', UserStatisticsProxyView.as_view(), name='statistics-profile'),
]

