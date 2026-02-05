"""
Utility functions for courses service
"""
from django.db.models import Avg, Count


def calculate_course_statistics(course):
    """
    Calculate statistics for a course
    """
    enrollments = course.enrollments.all()
    
    return {
        'total_enrollments': enrollments.count(),
        'completed_enrollments': enrollments.filter(completed_at__isnull=False).count(),
        'average_progress': enrollments.aggregate(Avg('progress_percentage'))['progress_percentage__avg'] or 0,
        'average_score': LessonProgress.objects.filter(
            lesson__course=course,
            score__isnull=False
        ).aggregate(Avg('score'))['score__avg'] or 0,
    }

