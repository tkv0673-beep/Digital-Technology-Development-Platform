#!/bin/bash
# Create superuser for proxy service

docker-compose exec proxy-service python manage.py createsuperuser

