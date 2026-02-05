# Руководство для Windows

## Установка зависимостей

### Docker Desktop
Скачайте и установите Docker Desktop для Windows:
https://www.docker.com/products/docker-desktop

### Git
Установите Git для Windows:
https://git-scm.com/download/win

## Использование PowerShell скриптов

В Windows используйте PowerShell скрипты вместо Makefile:

### Основные команды

```powershell
# Собрать все Docker образы
.\Makefile.ps1 build

# Запустить все сервисы
.\Makefile.ps1 up

# Остановить все сервисы
.\Makefile.ps1 down

# Применить миграции
.\Makefile.ps1 migrate

# Запустить тесты
.\Makefile.ps1 test

# Показать логи
.\Makefile.ps1 logs

# Очистить контейнеры и volumes
.\Makefile.ps1 clean
```

### Или используйте скрипты напрямую

```powershell
# Миграции
.\scripts\migrate.ps1

# Тесты
.\scripts\test.ps1

# Запуск сервисов
.\scripts\up.ps1

# Остановка сервисов
.\scripts\down.ps1
```

## Альтернатива: Установка Make для Windows

Если вы хотите использовать оригинальный Makefile, установите Make:

### Вариант 1: Chocolatey
```powershell
choco install make
```

### Вариант 2: Scoop
```powershell
scoop install make
```

### Вариант 3: GnuWin32
Скачайте и установите с: http://gnuwin32.sourceforge.net/packages/make.htm

После установки Make вы сможете использовать команды:
```bash
make migrate
make test
make up
```

## Docker Compose команды напрямую

Вы также можете использовать docker-compose напрямую:

```powershell
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down

# Миграции для конкретного сервиса
docker-compose exec tokens-service python manage.py migrate

# Логи
docker-compose logs -f

# Пересборка
docker-compose build
```

## Разрешения PowerShell

Если получаете ошибку о политике выполнения скриптов:

```powershell
# Проверить текущую политику
Get-ExecutionPolicy

# Установить политику для текущего пользователя (если нужно)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

