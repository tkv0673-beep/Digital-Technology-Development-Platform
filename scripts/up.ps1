# PowerShell script to start all services
Write-Host "Starting all services..." -ForegroundColor Green
docker-compose up -d
Write-Host "Services started!" -ForegroundColor Green

