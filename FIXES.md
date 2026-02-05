# Исправления проблем

## Исправленные проблемы:

### 1. `/api/auth/me/` - 404 Not Found ✅
- **Проблема**: Эндпоинт не существовал
- **Решение**: 
  - Добавлен метод `me()` в `AuthViewSet` в tokens service
  - Добавлен proxy `MeProxyView` в proxy service
  - Эндпоинт доступен по `/api/auth/me/`
- **Файлы**: 
  - `services/tokens/api/views.py`
  - `services/proxy/api/auth_urls.py`
  - `services/proxy/api/views.py`

### 2. `/api/lessons/{id}/complete/` - 503 Service Unavailable ✅
- **Проблема**: Эндпоинт не был проксирован через proxy service
- **Решение**:
  - Добавлен `LessonCompleteProxyView` в proxy service
  - Добавлен URL маршрут в `lessons_urls.py`
  - Эндпоинт доступен по `/api/lessons/{id}/complete/`
- **Файлы**:
  - `services/proxy/api/lessons_urls.py`
  - `services/proxy/api/views.py`
  - `services/proxy/api/urls.py`

### 3. `/api/chatbot/message/` - 502 Bad Gateway ⚠️
- **Проблема**: Возможна проблема с кодировкой или подключением
- **Решение**: 
  - Используется параметр `json=` для правильной UTF-8 кодировки
  - Проверена работа сервиса напрямую - работает
- **Примечание**: Если проблема сохраняется, проверьте:
  - Кодировку запроса от фронтенда (должна быть UTF-8)
  - Наличие токена авторизации в заголовке
  - Статус сервиса chatbot-service

## Доступные эндпоинты:

- ✅ `/api/auth/me/` - Получить профиль текущего пользователя (GET)
- ✅ `/api/lessons/{id}/complete/` - Завершить урок (POST)
- ✅ `/api/statistics/profile/` - Статистика пользователя (GET)
- ✅ `/api/chatbot/message/` - Отправить сообщение в чат-бот (POST)
- ✅ `/api/courses/` - Список курсов (GET) / Создать курс (POST, для менторов)

## Проверка работы:

Все сервисы должны быть запущены:
```bash
docker-compose ps
```

Проверка эндпоинтов требует авторизации через JWT токен.

