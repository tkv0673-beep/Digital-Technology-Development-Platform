#!/bin/bash
# Initialize database for all services

echo "Running migrations for all services..."

docker-compose exec -T proxy-service python manage.py migrate
docker-compose exec -T tokens-service python manage.py migrate
docker-compose exec -T notifications-service python manage.py migrate
docker-compose exec -T streaming-service python manage.py migrate
docker-compose exec -T courses-service python manage.py migrate
docker-compose exec -T chatbot-service python manage.py migrate

echo "Loading initial data..."
docker-compose exec -T courses-service python manage.py loaddata initial_courses

echo "Database initialization complete!"

