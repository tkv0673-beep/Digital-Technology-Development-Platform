"""
Streaming URLs - proxy to streaming service
"""
from django.urls import path
from .views import StreamingProxyView

urlpatterns = [
    path('video/<int:video_id>/', StreamingProxyView.as_view({'get': 'stream'}), name='stream-video'),
    path('video/<int:video_id>/info/', StreamingProxyView.as_view({'get': 'info'}), name='video-info'),
]

