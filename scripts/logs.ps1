# PowerShell script to show logs
param(
    [string]$Service = ""
)

if ($Service -eq "") {
    Write-Host "Showing logs for all services..." -ForegroundColor Green
    docker-compose logs -f
} else {
    Write-Host "Showing logs for $Service..." -ForegroundColor Green
    docker-compose logs -f $Service
}

