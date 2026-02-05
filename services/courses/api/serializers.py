"""
Serializers for courses service
"""
from rest_framework import serializers
from .models import Course, Lesson, Enrollment, LessonProgress, Achievement, UserAchievement


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lesson"""
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'order', 'video_id', 'content', 'progress', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def get_progress(self, obj):
        """Get user progress for lesson"""
        request = self.context.get('request')
        if request and hasattr(request, 'user_id'):
            try:
                progress = LessonProgress.objects.get(user_id=request.user_id, lesson=obj)
                return {
                    'is_completed': progress.is_completed,
                    'score': progress.score,
                    'last_accessed_at': progress.last_accessed_at
                }
            except LessonProgress.DoesNotExist:
                return None
        return None


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for course"""
    lessons_count = serializers.SerializerMethodField()
    enrollment = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = (
            'id', 'title', 'description', 'difficulty', 'thumbnail_url',
            'mentor_id', 'is_published', 'lessons_count', 'enrollment',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_lessons_count(self, obj):
        """Get lessons count"""
        return obj.lessons.count()
    
    def get_enrollment(self, obj):
        """Get user enrollment"""
        request = self.context.get('request')
        if request and hasattr(request, 'user_id'):
            try:
                enrollment = Enrollment.objects.get(user_id=request.user_id, course=obj)
                return {
                    'enrolled_at': enrollment.enrolled_at,
                    'progress_percentage': enrollment.progress_percentage,
                    'completed_at': enrollment.completed_at
                }
            except Enrollment.DoesNotExist:
                return None
        return None
    
    def get_thumbnail_url(self, obj):
        """Get thumbnail URL"""
        if obj.thumbnail:
            return obj.thumbnail.url
        return None


class CourseDetailSerializer(CourseSerializer):
    """Detailed serializer for course with lessons"""
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ('lessons',)


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollment"""
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'enrolled_at', 'completed_at', 'progress_percentage')
        read_only_fields = ('id', 'enrolled_at')


class AchievementSerializer(serializers.ModelSerializer):
    """Serializer for achievement"""
    icon_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = ('id', 'name', 'description', 'icon_url', 'condition')
    
    def get_icon_url(self, obj):
        """Get icon URL"""
        if obj.icon:
            return obj.icon.url
        return None


class UserAchievementSerializer(serializers.ModelSerializer):
    """Serializer for user achievement"""
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ('id', 'achievement', 'unlocked_at')

