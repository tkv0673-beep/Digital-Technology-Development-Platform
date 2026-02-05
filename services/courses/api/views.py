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
        if self.request.user.is_authenticated:
            user_role = getattr(self.request.user, 'role', None)
            if user_role != 'mentor':
                queryset = queryset.filter(is_published=True)
        else:
            queryset = queryset.filter(is_published=True)
        
        return queryset.prefetch_related('lessons')
    
    def perform_create(self, serializer):
        """Create course - only mentors can create"""
        if not self.request.user.is_authenticated:
            raise PermissionError('Authentication required')
        user_role = getattr(self.request.user, 'role', None)
        if user_role == 'mentor':
            user_id = getattr(self.request.user, 'user_id', self.request.user.id)
            serializer.save(mentor_id=user_id)
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
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        course = self.get_object()
        user_id = getattr(request.user, 'user_id', request.user.id)
        enrollment = CourseService.enroll_user(user_id, course.id)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get course progress"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        course = self.get_object()
        user_id = getattr(request.user, 'user_id', request.user.id)
        try:
            enrollment = Enrollment.objects.get(user_id=user_id, course=course)
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
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        lesson = self.get_object()
        score = request.data.get('score')
        user_id = getattr(request.user, 'user_id', request.user.id)
        progress = CourseService.complete_lesson(user_id, lesson.id, score)
        return Response({'message': 'Lesson completed', 'progress': progress.progress_percentage})


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Enrollment endpoints
    """
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Enrollment.objects.none()
        user_id = getattr(self.request.user, 'user_id', self.request.user.id)
        return Enrollment.objects.filter(user_id=user_id).select_related('course')


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
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user_id = getattr(request.user, 'user_id', request.user.id)
        achievements = UserAchievement.objects.filter(user_id=user_id)
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)


class UserStatisticsViewSet(viewsets.ViewSet):
    """
    User statistics endpoints
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get user statistics for profile"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user_id = getattr(request.user, 'user_id', request.user.id)
        
        # Get enrollments
        enrollments = Enrollment.objects.filter(user_id=user_id).select_related('course')
        total_courses = enrollments.count()
        completed_courses = enrollments.filter(completed_at__isnull=False).count()
        
        # Get progress
        total_lessons = 0
        completed_lessons = 0
        for enrollment in enrollments:
            course_lessons = enrollment.course.lessons.count()
            total_lessons += course_lessons
            completed_lessons += LessonProgress.objects.filter(
                user_id=user_id,
                lesson__course=enrollment.course,
                completed_at__isnull=False
            ).count()
        
        # Get achievements
        achievements_count = UserAchievement.objects.filter(user_id=user_id).count()
        
        # Calculate average progress
        avg_progress = 0
        if enrollments.exists():
            total_progress = sum(e.progress_percentage for e in enrollments)
            avg_progress = total_progress / enrollments.count()
        
        return Response({
            'total_courses': total_courses,
            'completed_courses': completed_courses,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'achievements_count': achievements_count,
            'average_progress': round(avg_progress, 2),
            'enrollments': [
                {
                    'course_id': e.course.id,
                    'course_title': e.course.title,
                    'progress_percentage': e.progress_percentage,
                    'enrolled_at': e.enrolled_at,
                    'completed_at': e.completed_at
                }
                for e in enrollments[:10]  # Last 10 enrollments
            ]
        })

