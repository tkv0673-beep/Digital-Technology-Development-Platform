# PowerShell script to load initial fixtures
Write-Host "Loading initial course data..." -ForegroundColor Green
docker-compose exec -T courses-service python manage.py loaddata api/fixtures/initial_courses.json
Write-Host "Fixtures loaded!" -ForegroundColor Green

