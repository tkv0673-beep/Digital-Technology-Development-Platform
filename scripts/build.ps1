# PowerShell script to build all Docker images
Write-Host "Building all Docker images..." -ForegroundColor Green
docker-compose build
Write-Host "Build completed!" -ForegroundColor Green

