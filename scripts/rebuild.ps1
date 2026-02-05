# PowerShell script to rebuild Docker images
Write-Host "Rebuilding Docker images..." -ForegroundColor Green
docker-compose build
Write-Host "Rebuild completed!" -ForegroundColor Green

