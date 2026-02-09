# Digital Technology Development Platform

Веб-платформа для освоения ИТ компетенций старшим поколением.

## Описание проекта

Интерактивная веб-платформа с изменением состояния в ответ на действия пользователей, которая обеспечивает безопасную среду для практического обучения через симуляции реальных интерфейсов. Платформа содержит полноценный симулятор, позволяющий снизить страх перед ошибками и повысить уверенность пользователей в использовании цифровых инструментов.

## Ссылка на видеоролик
https://rutube.ru/video/2ea4ae5631f543a9c358d93885c671b8/

По данной ссылке вы можете ознакомиться с видеороликом,в котором демонстрируется функционирование
разработанного программного продукта в соответствии с
регламентом испытаний.

## Технологический стек

### Backend
- **Python 3.11+**
- **Django 4.2+** - микросервисная архитектура
- **PostgreSQL** - основная база данных
- **Redis** - кеширование
- **RabbitMQ** - очереди сообщений
- **AWS S3** - хранилище файлов

### Frontend
- **React 18+** - MVVM архитектура
- **TypeScript**
- **Material-UI** - компоненты интерфейса

### Инфраструктура
- **Docker** & **Docker Compose** - контейнеризация
- **Nginx** - reverse proxy и статика
- **JWT** - аутентификация (access + refresh токены)

## Архитектура микросервисов

1. **Proxy** - единая точка входа для всех запросов
2. **Tokens** - управление JWT токенами
3. **Notifications** - отправка уведомлений (email/SMS)
4. **Streaming** - обработка и стриминг видео уроков
5. **Courses** - управление курсами и контентом
6. **ChatBot** - контекстный виртуальный помощник

## Установка и запуск

### Требования
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Быстрый старт

```bash
# Клонировать репозиторий
git clone <repository-url>
cd Digital-Technology-Development-Platform

# Запустить все сервисы
docker-compose up -d

# Применить миграции
docker-compose exec proxy python manage.py migrate

# Создать суперпользователя
docker-compose exec proxy python manage.py createsuperuser

# Загрузить начальные данные курсов
docker-compose exec proxy python manage.py loaddata initial_courses
```

Платформа будет доступна по адресу: http://localhost

## Структура проекта

```
.
├── services/          # Микросервисы
│   ├── proxy/        # Единая точка входа
│   ├── tokens/       # Управление токенами
│   ├── notifications/# Уведомления
│   ├── streaming/    # Видео стриминг
│   ├── courses/      # Управление курсами
│   └── chatbot/      # Чат-бот
├── frontend/         # React приложение
├── nginx/            # Nginx конфигурация
├── docker-compose.yml
└── README.md
```

## Роли пользователей

- **Ментор** - может создавать и управлять курсами
- **Менти** - проходит курсы и отслеживает прогресс

## Функциональность

- ✅ Адаптивный интерфейс с крупными элементами управления
- ✅ Голосовое сопровождение инструкций
- ✅ Визуальные подсказки и анимации
- ✅ Интерактивные симуляции интерфейсов
- ✅ Система курсов с базовым и расширенным уровнями
- ✅ Личный кабинет с отслеживанием прогресса
- ✅ Виртуальный помощник (чат-бот) с контекстными подсказками
- ✅ Админ панель для управления курсами
- ✅ Deep links для контекстного чат-бота

## Тестирование

```bash
# Запустить все тесты
make test

# Или для конкретного сервиса
docker-compose exec tokens-service python manage.py test

# С покрытием
docker-compose exec tokens-service coverage run --source='.' manage.py test
docker-compose exec tokens-service coverage report
```

Покрытие тестами: 85%+

## Управление проектом

### Linux/Mac - Make команды
```bash
make build      # Собрать все Docker образы
make up         # Запустить все сервисы
make down       # Остановить все сервисы
make migrate    # Применить миграции
make test       # Запустить тесты
make clean      # Очистить контейнеры и volumes
```

### Windows - PowerShell скрипты
```powershell
.\Makefile.ps1 build      # Собрать все Docker образы
.\Makefile.ps1 up         # Запустить все сервисы
.\Makefile.ps1 down       # Остановить все сервисы
.\Makefile.ps1 migrate    # Применить миграции
.\Makefile.ps1 test       # Запустить тесты
.\Makefile.ps1 clean      # Очистить контейнеры и volumes
```

Или используйте скрипты напрямую:
```powershell
.\scripts\migrate.ps1
.\scripts\test.ps1
.\scripts\up.ps1
```

См. [README_WINDOWS.md](README_WINDOWS.md) для подробной информации о работе в Windows.

### Скрипты
- `scripts/init_db.sh` - Инициализация базы данных
- `scripts/create_superuser.sh` - Создание суперпользователя
- `scripts/setup_minio.sh` - Настройка MinIO buckets

## Документация

Подробная техническая документация находится в директории `docs/`.

## Лицензия

MIT

