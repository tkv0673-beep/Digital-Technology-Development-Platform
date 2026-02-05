# Руководство по разработке

## Локальная разработка

### Требования
- Python 3.11+
- Node.js 18+
- Docker и Docker Compose
- PostgreSQL (опционально, можно использовать из Docker)

### Настройка окружения

1. **Клонирование репозитория**
```bash
git clone <repository-url>
cd Digital-Technology-Development-Platform
```

2. **Создание виртуального окружения для каждого сервиса**
```bash
cd services/tokens
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Настройка переменных окружения**
Создайте `.env` файлы в каждом сервисе или используйте общий `.env` в корне.

4. **Запуск через Docker Compose**
```bash
docker-compose up -d
```

### Разработка без Docker

Для разработки отдельных сервисов без Docker:

1. Запустите зависимости (PostgreSQL, Redis, RabbitMQ) через Docker:
```bash
docker-compose up -d postgres redis rabbitmq minio
```

2. Запустите сервис локально:
```bash
cd services/tokens
python manage.py runserver
```

## Структура проекта

```
.
├── services/          # Микросервисы
│   ├── proxy/        # API Gateway
│   ├── tokens/       # Аутентификация
│   ├── notifications/# Уведомления
│   ├── streaming/    # Видео стриминг
│   ├── courses/      # Курсы
│   └── chatbot/      # Чат-бот
├── frontend/         # React приложение
├── nginx/            # Nginx конфигурация
├── docs/             # Документация
└── scripts/          # Вспомогательные скрипты
```

## Работа с Git

### Ветвление
- `master` - основная ветка (production-ready код)
- `develop` - ветка разработки
- `feature/*` - ветки для новых функций
- `fix/*` - ветки для исправлений

### Коммиты
Используйте конвенцию:
- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - документация
- `test:` - тесты
- `refactor:` - рефакторинг

## Отладка

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f proxy-service
```

### Django Debug Toolbar
Добавьте в `INSTALLED_APPS` для локальной разработки:
```python
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
```

### React DevTools
Установите расширение для браузера для отладки React компонентов.

## Тестирование

### Запуск тестов
```bash
# Все тесты
make test

# Конкретный сервис
docker-compose exec tokens-service python manage.py test
```

### Покрытие
```bash
docker-compose exec tokens-service coverage run --source='.' manage.py test
docker-compose exec tokens-service coverage report
```

## Производительность

### Профилирование Django
Используйте `django-debug-toolbar` для анализа запросов к БД.

### Профилирование React
Используйте React DevTools Profiler для анализа производительности компонентов.

## Best Practices

1. **SOLID принципы** - следуйте принципам SOLID
2. **DRY** - избегайте дублирования кода
3. **Тестирование** - пишите тесты для нового функционала
4. **Документация** - обновляйте документацию при изменениях
5. **Code Review** - все изменения проходят через review

