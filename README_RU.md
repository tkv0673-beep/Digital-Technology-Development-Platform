# Платформа для освоения ИТ компетенций

Веб-платформа для обучения старшего поколения цифровым технологиям.

## Описание

Интерактивная веб-платформа с симуляциями реальных интерфейсов для безопасного обучения использованию смартфонов, компьютеров и популярных сервисов.

## Быстрый старт

```bash
# Клонировать репозиторий
git clone <repository-url>
cd Digital-Technology-Development-Platform

# Запустить все сервисы
docker-compose up -d

# Применить миграции
make migrate

# Загрузить начальные данные
docker-compose exec courses-service python manage.py loaddata initial_courses
```

Платформа доступна по адресу: http://localhost

## Документация

- [Архитектура](docs/ARCHITECTURE.md)
- [API Документация](docs/API.md)
- [Руководство по развертыванию](docs/DEPLOYMENT.md)
- [Руководство по разработке](docs/DEVELOPMENT.md)
- [Тестирование](docs/TESTING.md)

## Технологии

- Backend: Python 3.11, Django 4.2
- Frontend: React 18, MobX
- База данных: PostgreSQL
- Кеш: Redis
- Очереди: RabbitMQ
- Хранилище: MinIO (S3)
- Контейнеризация: Docker, Docker Compose

