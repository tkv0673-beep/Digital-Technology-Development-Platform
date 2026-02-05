# Руководство по развертыванию

## Требования

- Docker 20.10+
- Docker Compose 2.0+
- Git

## Быстрый старт

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd Digital-Technology-Development-Platform
```

2. **Настройка переменных окружения**

Создайте файл `.env` в корне проекта (опционально):
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
```

3. **Запуск сервисов**
```bash
docker-compose up -d
```

4. **Применение миграций**

Для каждого микросервиса:
```bash
# Proxy
docker-compose exec proxy-service python manage.py migrate

# Tokens
docker-compose exec tokens-service python manage.py migrate

# Notifications
docker-compose exec notifications-service python manage.py migrate

# Streaming
docker-compose exec streaming-service python manage.py migrate

# Courses
docker-compose exec courses-service python manage.py migrate

# ChatBot
docker-compose exec chatbot-service python manage.py migrate
```

5. **Создание суперпользователя**
```bash
docker-compose exec proxy-service python manage.py createsuperuser
```

6. **Загрузка начальных данных**
```bash
docker-compose exec courses-service python manage.py loaddata initial_courses
```

7. **Настройка MinIO**

Откройте http://localhost:9001 и создайте buckets:
- `video-storage` (для видео)
- `courses-storage` (для изображений курсов)

## Проверка работы

- Frontend: http://localhost
- API: http://localhost/api
- MinIO Console: http://localhost:9001
- RabbitMQ Management: http://localhost:15672

## Остановка сервисов

```bash
docker-compose down
```

## Очистка данных

```bash
docker-compose down -v
```

## Production развертывание

1. Обновите `SECRET_KEY` в `.env`
2. Настройте реальный SMTP сервер для уведомлений
3. Настройте реальный S3 вместо MinIO
4. Включите HTTPS через Nginx
5. Настройте мониторинг и логирование

