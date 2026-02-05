# PowerShell Makefile alternative for Windows
# Usage: .\Makefile.ps1 <command>

param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsPath = Join-Path $ScriptPath "scripts"

switch ($Command.ToLower()) {
    "build" {
        & "$ScriptsPath\build.ps1"
    }
    "up" {
        & "$ScriptsPath\up.ps1"
    }
    "down" {
        & "$ScriptsPath\down.ps1"
    }
    "restart" {
        docker-compose restart
    }
    "logs" {
        & "$ScriptsPath\logs.ps1"
    }
    "migrate" {
        & "$ScriptsPath\migrate.ps1"
    }
    "test" {
        & "$ScriptsPath\test.ps1"
    }
    "clean" {
        & "$ScriptsPath\clean.ps1"
    }
    default {
        Write-Host "Available commands:" -ForegroundColor Yellow
        Write-Host "  .\Makefile.ps1 build      - Build all Docker images"
        Write-Host "  .\Makefile.ps1 up         - Start all services"
        Write-Host "  .\Makefile.ps1 down       - Stop all services"
        Write-Host "  .\Makefile.ps1 restart    - Restart all services"
        Write-Host "  .\Makefile.ps1 logs       - Show logs from all services"
        Write-Host "  .\Makefile.ps1 migrate    - Run migrations for all services"
        Write-Host "  .\Makefile.ps1 test       - Run tests for all services"
        Write-Host "  .\Makefile.ps1 clean      - Remove all containers and volumes"
    }
}

