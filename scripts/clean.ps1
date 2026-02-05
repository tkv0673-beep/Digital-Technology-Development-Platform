# PowerShell script to clean containers and volumes
Write-Host "Cleaning containers and volumes..." -ForegroundColor Yellow
docker-compose down -v
docker system prune -f
Write-Host "Cleanup completed!" -ForegroundColor Green

