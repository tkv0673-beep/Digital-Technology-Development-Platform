#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User
from django.contrib.auth import authenticate

# Check admin user
admin = User.objects.filter(username='admin').first()
if admin:
    print(f'Admin exists: True')
    print(f'Password check: {admin.check_password("admin123")}')
    print(f'Is superuser: {admin.is_superuser}')
    print(f'Is staff: {admin.is_staff}')
    
    # Test authenticate
    auth_user = authenticate(username='admin', password='admin123')
    print(f'Authenticate result: {auth_user}')
    if auth_user:
        print(f'Authenticated user: {auth_user.username}')
    else:
        print('Authentication failed!')
else:
    print('Admin user not found!')

