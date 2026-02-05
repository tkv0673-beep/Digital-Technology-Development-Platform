#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests

# Test direct login to tokens service
url = 'http://tokens-service:8000/api/auth/login/'
data = {'username': 'admin', 'password': 'admin123'}

print(f'Testing login to: {url}')
print(f'Data: {data}')

try:
    response = requests.post(url, json=data, timeout=10)
    print(f'Status: {response.status_code}')
    print(f'Response: {response.text}')
    print(f'Headers: {response.headers}')
except Exception as e:
    print(f'Error: {e}')

