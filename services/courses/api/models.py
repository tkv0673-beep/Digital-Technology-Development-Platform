"""
Models for courses service
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Course(models.Model):
    """
    Course model
    """
    DIFFICULTY_CHOICES = [
        ('basic', 'Базовый'),
        ('advanced', 'Расширенный'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='basic')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    mentor_id = models.IntegerField(help_text='User ID of the mentor who created the course')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        indexes = [
            models.Index(fields=['mentor_id']),
            models.Index(fields=['is_published', 'difficulty']),
        ]


class Lesson(models.Model):
    """
    Lesson model
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    video_id = models.IntegerField(help_text='Video ID from streaming service', null=True, blank=True)
    content = models.JSONField(default=dict, help_text='Interactive simulation content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']
        indexes = [
            models.Index(fields=['course', 'order']),
        ]


class Enrollment(models.Model):
    """
    User enrollment in course
    """
    user_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        db_table = 'enrollments'
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = [['user_id', 'course']]
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['course', 'user_id']),
        ]


class LessonProgress(models.Model):
    """
    User progress in lesson
    """
    user_id = models.IntegerField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    last_accessed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lesson_progress'
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
        unique_together = [['user_id', 'lesson']]
        indexes = [
            models.Index(fields=['user_id', 'is_completed']),
        ]


class Achievement(models.Model):
    """
    Achievement model
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='achievements', null=True, blank=True)
    condition = models.JSONField(default=dict, help_text='Conditions to unlock achievement')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'achievements'
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class UserAchievement(models.Model):
    """
    User achievements
    """
    user_id = models.IntegerField()
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_achievements'
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        unique_together = [['user_id', 'achievement']]
        indexes = [
            models.Index(fields=['user_id']),
        ]

