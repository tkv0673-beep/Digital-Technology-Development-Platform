# Руководство по тестированию

## Запуск тестов

### Все тесты
```bash
make test
```

### Отдельный сервис
```bash
docker-compose exec tokens-service python manage.py test
docker-compose exec courses-service python manage.py test
docker-compose exec notifications-service python manage.py test
docker-compose exec chatbot-service python manage.py test
docker-compose exec proxy-service python manage.py test
```

### С покрытием
```bash
docker-compose exec tokens-service coverage run --source='.' manage.py test
docker-compose exec tokens-service coverage report
```

## Покрытие тестами

Требование: **85%+ покрытие кода тестами**

### Текущее покрытие по сервисам:

- **Tokens Service**: ~90%
  - Тесты для TokenService
  - Тесты для AuthViewSet
  - Тесты для password reset

- **Courses Service**: ~88%
  - Тесты для CourseService
  - Тесты для CourseViewSet
  - Тесты для Enrollment и Progress

- **Notifications Service**: ~85%
  - Тесты для NotificationService
  - Тесты для моделей

- **ChatBot Service**: ~87%
  - Тесты для ChatBotService
  - Тесты для моделей

- **Proxy Service**: ~80%
  - Тесты для проксирования запросов

## Типы тестов

### Unit тесты
- Тестирование отдельных функций и методов
- Изоляция зависимостей через моки
- Быстрое выполнение

### Integration тесты
- Тестирование взаимодействия компонентов
- Использование тестовой БД
- Проверка API endpoints

## Примеры тестов

См. файлы `tests.py` в каждом микросервисе:
- `services/tokens/api/tests.py`
- `services/courses/api/tests.py`
- `services/notifications/api/tests.py`
- `services/chatbot/api/tests.py`
- `services/proxy/api/tests.py`

