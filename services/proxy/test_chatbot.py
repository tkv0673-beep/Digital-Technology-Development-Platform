#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import requests
import json

# Test login first
login_response = requests.post(
    'http://tokens-service:8000/api/auth/login/',
    json={'username': 'admin', 'password': 'admin123'}
)
print(f'Login status: {login_response.status_code}')
if login_response.status_code == 200:
    token_data = login_response.json()
    access_token = token_data['access_token']
    print(f'Got token: {access_token[:50]}...')
    
    # Test chatbot with token
    headers = {'Authorization': f'Bearer {access_token}'}
    chatbot_data = {'message': 'Привет'}
    print(f'Sending data: {chatbot_data}')
    print(f'Data as JSON: {json.dumps(chatbot_data, ensure_ascii=False)}')
    
    chatbot_response = requests.post(
        'http://chatbot-service:8000/api/chatbot/message/',
        json=chatbot_data,
        headers=headers
    )
    print(f'Chatbot status: {chatbot_response.status_code}')
    print(f'Chatbot response: {chatbot_response.text[:500]}')

