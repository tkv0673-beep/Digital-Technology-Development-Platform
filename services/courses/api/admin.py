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
    list_display = ('name', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('name', 'description')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'achievement', 'unlocked_at')
    list_filter = ('unlocked_at',)
    search_fields = ('user_id',)

