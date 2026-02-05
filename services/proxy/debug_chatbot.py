#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from api.views import ChatBotMessageProxyView
import json

# Create a mock request
factory = RequestFactory()
data = {'message': 'Привет'}
json_data = json.dumps(data, ensure_ascii=False)
print(f'Original data: {data}')
print(f'JSON string: {json_data}')
print(f'JSON bytes: {json_data.encode("utf-8")}')

request = factory.post(
    '/api/chatbot/message/',
    data=json_data,
    content_type='application/json'
)

print(f'Request body: {request.body}')
print(f'Request body type: {type(request.body)}')
print(f'Request body decoded: {request.body.decode("utf-8")}')

