"""
Views for courses service
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Course, Lesson, Enrollment, LessonProgress, Achievement, UserAchievement
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    LessonSerializer,
    EnrollmentSerializer,
    AchievementSerializer,
    UserAchievementSerializer
)
from .services import CourseService


class CourseViewSet(viewsets.ModelViewSet):
    """
    Course endpoints
    """
    queryset = Course.objects.filter(is_published=True).prefetch_related('lessons')
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    def get_queryset(self):
        queryset = Course.objects.all()
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by mentor
        mentor_id = self.request.query_params.get('mentor_id')
        if mentor_id:
            queryset = queryset.filter(mentor_id=mentor_id)
        
        # For non-mentors, only show published courses
        if not hasattr(self.request, 'user_role') or self.request.user_role != 'mentor':
            queryset = queryset.filter(is_published=True)
        
        return queryset.prefetch_related('lessons')
    
    def perform_create(self, serializer):
        """Create course - only mentors can create"""
        if hasattr(self.request, 'user_role') and self.request.user_role == 'mentor':
            serializer.save(mentor_id=self.request.user_id)
        else:
            raise PermissionError('Only mentors can create courses')
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """Get course lessons"""
        course = self.get_object()
        lessons = course.lessons.all().order_by('order')
        serializer = LessonSerializer(lessons, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll in course"""
        course = self.get_object()
        enrollment = CourseService.enroll_user(request.user_id, course.id)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get course progress"""
        course = self.get_object()
        try:
            enrollment = Enrollment.objects.get(user_id=request.user_id, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response(
                {'error': 'Not enrolled in this course'},
                status=status.HTTP_404_NOT_FOUND
            )


class LessonViewSet(viewsets.ModelViewSet):
    """
    Lesson endpoints
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark lesson as completed"""
        lesson = self.get_object()
        score = request.data.get('score')
        progress = CourseService.complete_lesson(request.user_id, lesson.id, score)
        return Response({'message': 'Lesson completed', 'progress': progress.progress_percentage})


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Enrollment endpoints
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Enrollment.objects.filter(user_id=self.request.user_id).select_related('course')


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Achievement endpoints
    """
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """Get user achievements"""
        achievements = UserAchievement.objects.filter(user_id=request.user_id)
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

