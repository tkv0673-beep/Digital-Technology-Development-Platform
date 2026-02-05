# PowerShell script to run migrations for all services
Write-Host "Running migrations for all services..." -ForegroundColor Green

docker-compose exec -T proxy-service python manage.py migrate
docker-compose exec -T tokens-service python manage.py migrate
docker-compose exec -T notifications-service python manage.py migrate
docker-compose exec -T streaming-service python manage.py migrate
docker-compose exec -T courses-service python manage.py migrate
docker-compose exec -T chatbot-service python manage.py migrate

Write-Host "Migrations completed!" -ForegroundColor Green

