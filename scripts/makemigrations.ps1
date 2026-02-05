# PowerShell script to create migrations for all services
Write-Host "Creating migrations for all services..." -ForegroundColor Green

docker-compose exec -T proxy-service python manage.py makemigrations
docker-compose exec -T tokens-service python manage.py makemigrations
docker-compose exec -T notifications-service python manage.py makemigrations
docker-compose exec -T streaming-service python manage.py makemigrations
docker-compose exec -T courses-service python manage.py makemigrations
docker-compose exec -T chatbot-service python manage.py makemigrations

Write-Host "Migrations created!" -ForegroundColor Green

