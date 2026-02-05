# Быстрый старт

## Запуск платформы

### 1. Запустите все сервисы:
```powershell
docker-compose up -d
```

### 2. Примените миграции:
```powershell
.\scripts\migrate.ps1
```

### 3. Создайте суперпользователя (если еще не создан):
```powershell
docker-compose exec -T tokens-service python manage.py shell -c "from api.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
```

### 4. Загрузите начальные курсы:
```powershell
docker-compose exec -T courses-service python manage.py loaddata api/fixtures/initial_courses.json
```

## Доступ к платформе

### Веб-интерфейс:
- **Фронтенд**: http://localhost:3000
- **Через Nginx**: http://localhost

### API:
- **Proxy (единая точка входа)**: http://localhost:8000
- **Tokens Service**: http://localhost:8001
- **Notifications Service**: http://localhost:8002
- **Streaming Service**: http://localhost:8003
- **Courses Service**: http://localhost:8004
- **ChatBot Service**: http://localhost:8005

### Админ-панели и утилиты:
- **Django Admin (Tokens)**: http://localhost:8001/admin
  - Логин: `admin`
  - Пароль: `admin123`
- **Django Admin (Courses)**: http://localhost:8004/admin
- **RabbitMQ Management**: http://localhost:15672
  - Логин: `guest`
  - Пароль: `guest`
- **MinIO Console**: http://localhost:9001
  - Логин: `dt_admin`
  - Пароль: `dt_password123`

## Тестовые учетные данные

### Суперпользователь:
- **Username**: `admin`
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: Ментор (может создавать курсы)

### Создание нового пользователя через API:

```powershell
# Регистрация нового пользователя
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "test123456"
    role = "mentee"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register/" -Method Post -Body $body -ContentType "application/json"
```

## Проверка работоспособности

### Проверьте статус всех сервисов:
```powershell
docker-compose ps
```

Все сервисы должны быть в статусе `Up` и `healthy` (где применимо).

### Проверьте логи:
```powershell
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f proxy-service
docker-compose logs -f courses-service
```

## Следующие шаги

1. Откройте http://localhost в браузере
2. Зарегистрируйтесь или войдите с учетными данными `admin` / `admin123`
3. Просмотрите доступные курсы
4. Запишитесь на курс
5. Начните обучение!

## Устранение неполадок

Если что-то не работает:

1. **Проверьте логи**: `docker-compose logs -f [service-name]`
2. **Перезапустите сервисы**: `docker-compose restart`
3. **Пересоберите образы**: `.\scripts\rebuild.ps1`
4. **Проверьте базу данных**: `docker-compose exec postgres psql -U dt_user -d dt_platform -c "\dt"`

Подробнее см. `docs/TROUBLESHOOTING.md`

