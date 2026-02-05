"""
Signals for courses service
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, LessonProgress


@receiver(post_save, sender=Enrollment)
def update_course_statistics(sender, instance, created, **kwargs):
    """
    Update course statistics when enrollment is created
    """
    if created:
        # Invalidate cache or update statistics
        pass


@receiver(post_save, sender=LessonProgress)
def check_achievements(sender, instance, created, **kwargs):
    """
    Check achievements when lesson progress is updated
    """
    if instance.is_completed:
        from .services import CourseService
        CourseService.check_achievements(instance.user_id, instance.lesson.course_id)

