"""
Admin configuration for courses service
"""
from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonProgress, Achievement, UserAchievement


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'mentor_id', 'is_published', 'created_at')
    list_filter = ('difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    
    def save_model(self, request, obj, form, change):
        """Override save to set mentor_id for new courses"""
        if not change:  # New course
            if request.user.is_authenticated:
                # Try to get user_id from authenticated user
                user_id = getattr(request.user, 'user_id', getattr(request.user, 'id', None))
                if user_id:
                    obj.mentor_id = user_id
                elif not obj.mentor_id:
                    # Fallback: use user ID from request if available
                    obj.mentor_id = request.user.id if hasattr(request.user, 'id') else 1
            elif not obj.mentor_id:
                obj.mentor_id = 1  # Default mentor
        super().save_model(request, obj, form, change)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'course', 'progress_percentage', 'enrolled_at', 'completed_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('user_id',)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'lesson', 'is_completed', 'score', 'last_accessed_at')
    list_filter = ('is_completed', 'last_accessed_at')
    search_fields = ('user_id',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)
    search_fields = ('name', 'description')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'achievement', 'unlocked_at')
    list_filter = ('unlocked_at',)
    search_fields = ('user_id',)

