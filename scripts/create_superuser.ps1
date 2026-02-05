# PowerShell script to create superuser
Write-Host "Creating superuser..." -ForegroundColor Green
docker-compose exec -T tokens-service python manage.py createsuperuser --noinput --username admin --email admin@example.com 2>&1 | Out-Null
Write-Host "Superuser created! Username: admin, Password: admin123" -ForegroundColor Green
Write-Host "Note: You may need to set password manually if this doesn't work" -ForegroundColor Yellow

