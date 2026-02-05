"""
Courses URLs - proxy to courses service
"""
from django.urls import path
from .views import (
    CoursesListProxyView, CoursesDetailProxyView, CoursesLessonsProxyView,
    CoursesEnrollProxyView, CoursesProgressProxyView
)

urlpatterns = [
    path('', CoursesListProxyView.as_view(), name='courses-list'),
    path('<int:pk>/', CoursesDetailProxyView.as_view(), name='courses-detail'),
    path('<int:pk>/lessons/', CoursesLessonsProxyView.as_view(), name='courses-lessons'),
    path('<int:pk>/enroll/', CoursesEnrollProxyView.as_view(), name='courses-enroll'),
    path('<int:pk>/progress/', CoursesProgressProxyView.as_view(), name='courses-progress'),
]

