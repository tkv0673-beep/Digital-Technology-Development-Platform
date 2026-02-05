"""
Lessons URLs - proxy to courses service
"""
from django.urls import path
from .views import LessonDetailProxyView, LessonCompleteProxyView

urlpatterns = [
    path('<int:pk>/', LessonDetailProxyView.as_view(), name='lesson-detail'),
    path('<int:pk>/complete/', LessonCompleteProxyView.as_view(), name='lesson-complete'),
]

