"""
Management command to create sample course
"""
from django.core.management.base import BaseCommand
from api.models import Course, Lesson


class Command(BaseCommand):
    help = 'Create a sample course with lessons'

    def handle(self, *args, **options):
        course, created = Course.objects.get_or_create(
            title='Пример курса',
            defaults={
                'description': 'Это пример курса для тестирования',
                'difficulty': 'basic',
                'mentor_id': 1,
                'is_published': True
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course.title}'))

        # Create sample lessons
        lesson1, _ = Lesson.objects.get_or_create(
            course=course,
            order=1,
            defaults={
                'title': 'Урок 1: Введение',
                'description': 'Вводный урок',
                'content': {'type': 'simulation', 'steps': []}
            }
        )

        lesson2, _ = Lesson.objects.get_or_create(
            course=course,
            order=2,
            defaults={
                'title': 'Урок 2: Практика',
                'description': 'Практический урок',
                'content': {'type': 'simulation', 'steps': []}
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Created {course.lessons.count()} lessons'))

