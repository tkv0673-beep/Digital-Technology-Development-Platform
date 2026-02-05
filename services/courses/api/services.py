"""
Business logic services for courses
"""
from django.db.models import Count, Avg
from django.utils import timezone
from .models import Course, Lesson, Enrollment, LessonProgress, Achievement, UserAchievement


class CourseService:
    """
    Service for course management
    """
    
    @staticmethod
    def enroll_user(user_id, course_id):
        """Enroll user in course"""
        course = Course.objects.get(id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(
            user_id=user_id,
            course=course,
            defaults={'progress_percentage': 0}
        )
        return enrollment
    
    @staticmethod
    def update_progress(user_id, course_id):
        """Update course progress"""
        enrollment = Enrollment.objects.get(user_id=user_id, course_id=course_id)
        course = enrollment.course
        
        total_lessons = course.lessons.count()
        if total_lessons == 0:
            return enrollment
        
        completed_lessons = LessonProgress.objects.filter(
            user_id=user_id,
            lesson__course=course,
            is_completed=True
        ).count()
        
        progress_percentage = int((completed_lessons / total_lessons) * 100)
        enrollment.progress_percentage = progress_percentage
        
        if progress_percentage == 100:
            enrollment.completed_at = timezone.now()
        
        enrollment.save()
        return enrollment
    
    @staticmethod
    def complete_lesson(user_id, lesson_id, score=None):
        """Mark lesson as completed"""
        lesson = Lesson.objects.get(id=lesson_id)
        progress, created = LessonProgress.objects.get_or_create(
            user_id=user_id,
            lesson=lesson
        )
        
        progress.is_completed = True
        if score is not None:
            progress.score = score
        progress.completed_at = timezone.now()
        progress.save()
        
        # Update course progress
        CourseService.update_progress(user_id, lesson.course_id)
        
        # Check achievements
        CourseService.check_achievements(user_id, lesson.course_id)
        
        return progress
    
    @staticmethod
    def check_achievements(user_id, course_id):
        """Check and unlock achievements"""
        course = Course.objects.get(id=course_id)
        achievements = Achievement.objects.filter(course=course)
        
        enrollment = Enrollment.objects.get(user_id=user_id, course=course)
        
        for achievement in achievements:
            # Check if already unlocked
            if UserAchievement.objects.filter(user_id=user_id, achievement=achievement).exists():
                continue
            
            # Check conditions
            condition = achievement.condition
            condition_type = condition.get('type')
            
            if condition_type == 'course_completion' and enrollment.progress_percentage == 100:
                UserAchievement.objects.create(user_id=user_id, achievement=achievement)
            elif condition_type == 'lesson_completion':
                lesson_count = condition.get('lesson_count', 1)
                completed = LessonProgress.objects.filter(
                    user_id=user_id,
                    lesson__course=course,
                    is_completed=True
                ).count()
                if completed >= lesson_count:
                    UserAchievement.objects.create(user_id=user_id, achievement=achievement)

