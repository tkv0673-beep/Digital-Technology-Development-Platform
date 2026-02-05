# PowerShell script to test protected endpoints
Write-Host "Testing protected endpoints..." -ForegroundColor Green

# 1. Login first
Write-Host "`n1. Logging in..." -ForegroundColor Yellow
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method Post -Body $loginBody -ContentType "application/json"
    Write-Host "Login successful!" -ForegroundColor Green
    $accessToken = $loginResponse.access_token
    $headers = @{
        "Authorization" = "Bearer $accessToken"
    }
    
    # 2. Test course enrollment
    Write-Host "`n2. Testing course enrollment..." -ForegroundColor Yellow
    try {
        $enrollResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/courses/1/enroll/" -Method Post -Headers $headers -ContentType "application/json"
        Write-Host "Enrollment successful!" -ForegroundColor Green
        Write-Host "Response: $($enrollResponse | ConvertTo-Json)" -ForegroundColor Cyan
    } catch {
        Write-Host "Enrollment failed: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
        }
    }
    
    # 3. Test chatbot message
    Write-Host "`n3. Testing chatbot message..." -ForegroundColor Yellow
    $chatBody = @{
        message = "Привет, как дела?"
    } | ConvertTo-Json
    
    try {
        $chatResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/chatbot/message/" -Method Post -Body $chatBody -Headers $headers -ContentType "application/json"
        Write-Host "Chatbot response successful!" -ForegroundColor Green
        Write-Host "Response: $($chatResponse | ConvertTo-Json)" -ForegroundColor Cyan
    } catch {
        Write-Host "Chatbot failed: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
        }
    }
    
} catch {
    Write-Host "Login failed: $($_.Exception.Message)" -ForegroundColor Red
}

