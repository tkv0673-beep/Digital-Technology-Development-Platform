# Руководство по решению проблем

## Проблемы с установкой зависимостей

### Таймаут при установке пакетов

Если возникают таймауты при сборке Docker образов:

1. **Увеличьте таймаут** (уже добавлено в Dockerfile):
   - Таймаут установлен на 300 секунд
   - Добавлено 5 попыток повтора

2. **Используйте pip cache**:
   ```powershell
   # Создайте volume для pip cache
   docker volume create pip-cache
   ```

3. **Соберите образы по одному**:
   ```powershell
   docker-compose build tokens-service
   docker-compose build courses-service
   # и т.д.
   ```

4. **Используйте локальный pip cache**:
   Добавьте в Dockerfile перед `RUN pip install`:
   ```dockerfile
   RUN mkdir -p /root/.cache/pip
   ```

5. **Используйте альтернативное зеркало PyPI**:
   Создайте файл `pip.conf` в каждом сервисе:
   ```ini
   [global]
   index-url = https://pypi.tuna.tsinghua.edu.cn/simple
   timeout = 300
   retries = 5
   ```

### Проблемы с миграциями

Если миграции не применяются:

1. **Проверьте подключение к БД**:
   ```powershell
   docker-compose exec postgres psql -U dt_user -d dt_platform
   ```

2. **Создайте миграции вручную**:
   ```powershell
   docker-compose exec tokens-service python manage.py makemigrations
   docker-compose exec courses-service python manage.py makemigrations
   ```

3. **Примените миграции по одному**:
   ```powershell
   docker-compose exec tokens-service python manage.py migrate
   ```

### Проблемы с запуском сервисов

1. **Проверьте логи**:
   ```powershell
   docker-compose logs -f proxy-service
   ```

2. **Перезапустите сервисы**:
   ```powershell
   docker-compose restart
   ```

3. **Проверьте порты**:
   Убедитесь, что порты 8000-8005, 5432, 6379, 5672, 9000 не заняты

### Проблемы с MinIO

1. **Создайте buckets вручную**:
   - Откройте http://localhost:9001
   - Войдите (dt_admin / dt_password123)
   - Создайте buckets: `video-storage` и `courses-storage`

2. **Проверьте подключение**:
   ```powershell
   docker-compose exec streaming-service python -c "import boto3; print('OK')"
   ```

## Медленный интернет

Если у вас медленное интернет-соединение:

1. **Соберите образы в фоне**:
   ```powershell
   docker-compose build --parallel
   ```

2. **Используйте готовые образы** (если доступны):
   ```powershell
   docker pull python:3.11-slim
   ```

3. **Соберите только необходимые сервисы**:
   ```powershell
   docker-compose build proxy-service tokens-service
   ```

