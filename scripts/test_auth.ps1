# PowerShell script to test authentication
Write-Host "Testing authentication..." -ForegroundColor Green

# Test login
Write-Host "`n1. Testing login..." -ForegroundColor Yellow
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method Post -Body $loginBody -ContentType "application/json"
    Write-Host "Login successful!" -ForegroundColor Green
    Write-Host "Access token: $($loginResponse.access_token.Substring(0, 50))..." -ForegroundColor Cyan
    
    # Test courses with token
    Write-Host "`n2. Testing courses access with token..." -ForegroundColor Yellow
    $headers = @{
        "Authorization" = "Bearer $($loginResponse.access_token)"
    }
    
    $coursesResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/courses/" -Method Get -Headers $headers
    Write-Host "Courses access successful! Found $($coursesResponse.count) courses" -ForegroundColor Green
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host "Response: $($_.Exception.Response)" -ForegroundColor Red
}

# Test courses without token (should work now)
Write-Host "`n3. Testing courses access without token..." -ForegroundColor Yellow
try {
    $coursesResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/courses/" -Method Get
    Write-Host "Courses access successful! Found $($coursesResponse.count) courses" -ForegroundColor Green
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

