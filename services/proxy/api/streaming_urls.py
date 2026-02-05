"""
Streaming URLs - proxy to streaming service
"""
from django.urls import path
from .views import StreamingVideoProxyView, StreamingVideoInfoProxyView

urlpatterns = [
    path('video/<int:video_id>/', StreamingVideoProxyView.as_view(), name='stream-video'),
    path('video/<int:video_id>/info/', StreamingVideoInfoProxyView.as_view(), name='video-info'),
]

