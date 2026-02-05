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
    
    # Test chatbot with token - simulate what proxy does
    headers = {'Authorization': f'Bearer {access_token}'}
    headers['Content-Type'] = 'application/json; charset=utf-8'
    
    # Test with different data formats
    test_cases = [
        {'message': 'Привет'},
        {'message': 'Hello'},
    ]
    
    for i, chatbot_data in enumerate(test_cases):
        print(f'\nTest case {i+1}: {chatbot_data}')
        
        # Method 1: Using json parameter
        try:
            response1 = requests.post(
                'http://chatbot-service:8000/api/chatbot/message/',
                json=chatbot_data,
                headers=headers
            )
            print(f'Method 1 (json=): Status {response1.status_code}, Response: {response1.text[:200]}')
        except Exception as e:
            print(f'Method 1 failed: {e}')
        
        # Method 2: Using data with explicit encoding
        try:
            json_str = json.dumps(chatbot_data, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')
            response2 = requests.post(
                'http://chatbot-service:8000/api/chatbot/message/',
                data=json_bytes,
                headers=headers
            )
            print(f'Method 2 (data=bytes): Status {response2.status_code}, Response: {response2.text[:200]}')
        except Exception as e:
            print(f'Method 2 failed: {e}')

