"""
Unit tests for courses service
"""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Lesson, Enrollment, LessonProgress, Achievement
from .services import CourseService


class CourseServiceTests(TestCase):
    """Tests for CourseService"""
    
    def setUp(self):
        self.user_id = 1
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            difficulty='basic',
            mentor_id=1,
            is_published=True
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Test Lesson Description',
            order=1
        )
    
    def test_enroll_user(self):
        """Test user enrollment"""
        enrollment = CourseService.enroll_user(self.user_id, self.course.id)
        self.assertIsNotNone(enrollment)
        self.assertEqual(enrollment.user_id, self.user_id)
        self.assertEqual(enrollment.course, self.course)
        self.assertEqual(enrollment.progress_percentage, 0)
    
    def test_update_progress(self):
        """Test progress update"""
        enrollment = CourseService.enroll_user(self.user_id, self.course.id)
        CourseService.complete_lesson(self.user_id, self.lesson.id)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.progress_percentage, 100)
    
    def test_complete_lesson(self):
        """Test lesson completion"""
        progress = CourseService.complete_lesson(self.user_id, self.lesson.id)
        self.assertIsNotNone(progress)
        self.assertTrue(progress.is_completed)
        self.assertIsNotNone(progress.completed_at)


class CourseViewSetTests(TestCase):
    """Tests for CourseViewSet"""
    
    def setUp(self):
        self.client = APIClient()
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            difficulty='basic',
            mentor_id=1,
            is_published=True
        )
    
    def test_list_courses(self):
        """Test course listing"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_course(self):
        """Test course retrieval"""
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Course')
    
    def test_filter_by_difficulty(self):
        """Test course filtering by difficulty"""
        response = self.client.get('/api/courses/?difficulty=basic')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EnrollmentTests(TestCase):
    """Tests for enrollment"""
    
    def setUp(self):
        self.user_id = 1
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            difficulty='basic',
            mentor_id=1,
            is_published=True
        )
    
    def test_enrollment_creation(self):
        """Test enrollment creation"""
        enrollment = Enrollment.objects.create(
            user_id=self.user_id,
            course=self.course
        )
        self.assertIsNotNone(enrollment)
        self.assertEqual(enrollment.user_id, self.user_id)
        self.assertEqual(enrollment.course, self.course)


class AchievementTests(TestCase):
    """Tests for achievements"""
    
    def setUp(self):
        self.user_id = 1
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            difficulty='basic',
            mentor_id=1,
            is_published=True
        )
        self.achievement = Achievement.objects.create(
            name='Test Achievement',
            description='Test Description',
            course=self.course,
            condition={'type': 'course_completion'}
        )
    
    def test_achievement_creation(self):
        """Test achievement creation"""
        self.assertIsNotNone(self.achievement)
        self.assertEqual(self.achievement.name, 'Test Achievement')

