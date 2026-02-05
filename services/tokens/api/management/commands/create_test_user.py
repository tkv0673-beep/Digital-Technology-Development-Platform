"""
Management command to create test user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a test user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='testuser', help='Username')
        parser.add_argument('--email', type=str, default='test@example.com', help='Email')
        parser.add_argument('--password', type=str, default='testpass123', help='Password')
        parser.add_argument('--role', type=str, default='mentee', choices=['mentor', 'mentee'], help='User role')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        role = options['role']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created user {username} with role {role}'))

