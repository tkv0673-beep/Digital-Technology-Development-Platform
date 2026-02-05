.PHONY: help build up down restart logs migrate test clean

help:
	@echo "Available commands:"
	@echo "  make build      - Build all Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - Show logs from all services"
	@echo "  make migrate    - Run migrations for all services"
	@echo "  make test       - Run tests for all services"
	@echo "  make clean      - Remove all containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

migrate:
	docker-compose exec proxy-service python manage.py migrate
	docker-compose exec tokens-service python manage.py migrate
	docker-compose exec notifications-service python manage.py migrate
	docker-compose exec streaming-service python manage.py migrate
	docker-compose exec courses-service python manage.py migrate
	docker-compose exec chatbot-service python manage.py migrate

test:
	docker-compose exec proxy-service python manage.py test
	docker-compose exec tokens-service python manage.py test
	docker-compose exec notifications-service python manage.py test
	docker-compose exec streaming-service python manage.py test
	docker-compose exec courses-service python manage.py test
	docker-compose exec chatbot-service python manage.py test

clean:
	docker-compose down -v
	docker system prune -f

