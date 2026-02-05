# PowerShell script to run tests for all services
Write-Host "Running tests for all services..." -ForegroundColor Green

docker-compose exec -T proxy-service python manage.py test
docker-compose exec -T tokens-service python manage.py test
docker-compose exec -T notifications-service python manage.py test
docker-compose exec -T streaming-service python manage.py test
docker-compose exec -T courses-service python manage.py test
docker-compose exec -T chatbot-service python manage.py test

Write-Host "Tests completed!" -ForegroundColor Green

