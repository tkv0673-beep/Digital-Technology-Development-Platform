"""
Courses URLs - proxy to courses service
"""
from django.urls import path
from .views import CoursesProxyView

urlpatterns = [
    path('', CoursesProxyView.as_view({'get': 'list', 'post': 'create'}), name='courses-list'),
    path('<int:pk>/', CoursesProxyView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='courses-detail'),
    path('<int:pk>/lessons/', CoursesProxyView.as_view({'get': 'lessons'}), name='courses-lessons'),
    path('<int:pk>/enroll/', CoursesProxyView.as_view({'post': 'enroll'}), name='courses-enroll'),
    path('<int:pk>/progress/', CoursesProxyView.as_view({'get': 'progress'}), name='courses-progress'),
]

