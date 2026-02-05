"""
Courses service URLs
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, EnrollmentViewSet, AchievementViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollments')
router.register(r'achievements', AchievementViewSet, basename='achievements')

urlpatterns = router.urls

