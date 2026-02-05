# API Документация

## Базовый URL

```
http://localhost:8000/api
```

## Аутентификация

Все защищенные endpoints требуют JWT токен в заголовке:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Аутентификация

#### Регистрация
```
POST /api/auth/register/
Body: {
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "first_name": "string",
  "last_name": "string",
  "phone": "string",
  "role": "mentee" | "mentor"
}
```

#### Вход
```
POST /api/auth/login/
Body: {
  "username": "string",
  "password": "string"
}
Response: {
  "access_token": "string",
  "refresh_token": "string",
  "user": {...}
}
```

#### Обновление токена
```
POST /api/auth/refresh/
Body: {
  "refresh_token": "string"
}
```

#### Выход
```
POST /api/auth/logout/
Body: {
  "refresh_token": "string"
}
```

### Курсы

#### Список курсов
```
GET /api/courses/
Query params: ?difficulty=basic|advanced
```

#### Детали курса
```
GET /api/courses/{id}/
```

#### Запись на курс
```
POST /api/courses/{id}/enroll/
```

#### Прогресс курса
```
GET /api/courses/{id}/progress/
```

#### Уроки курса
```
GET /api/courses/{id}/lessons/
```

### Уроки

#### Завершение урока
```
POST /api/lessons/{id}/complete/
Body: {
  "score": number (optional)
}
```

### Стриминг

#### Получить URL для стриминга
```
GET /api/streaming/video/{video_id}/
```

#### Информация о видео
```
GET /api/streaming/video/{video_id}/info/
```

### Чат-бот

#### Отправить сообщение
```
POST /api/chatbot/message/
Body: {
  "message": "string",
  "lesson_id": number (optional),
  "context_data": object (optional)
}
```

#### Получить контекст урока
```
GET /api/chatbot/context/{lesson_id}/
```

#### История сообщений
```
GET /api/chatbot/history/
```

## Коды ответов

- `200` - Успешно
- `201` - Создано
- `400` - Неверный запрос
- `401` - Не авторизован
- `403` - Доступ запрещен
- `404` - Не найдено
- `500` - Внутренняя ошибка сервера
- `503` - Сервис недоступен

