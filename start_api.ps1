# Start VIGOLEONROCKS API Server with proper environment variables
$env:API_TOKEN = "GBFPf5EzTC7VIlD8rOCm2YfSGM6TaV4uvonczg6h3dfad669"
$env:HOST = "0.0.0.0"
$env:PORT = "5000"

Write-Host "🚀 Iniciando VIGOLEONROCKS API Server..." -ForegroundColor Cyan
Write-Host "📊 Token configurado: $($env:API_TOKEN.Substring(0,10))..." -ForegroundColor Green
Write-Host "🌐 Host: $env:HOST" -ForegroundColor Green
Write-Host "🔌 Puerto: $env:PORT" -ForegroundColor Green

# Crear directorios si no existen
New-Item -ItemType Directory -Force -Path "logs", "run" | Out-Null

# Iniciar el proceso con variables de entorno
$process = Start-Process python -ArgumentList "simple_api.py" -RedirectStandardOutput "logs\api.log" -RedirectStandardError "logs\api_error.log" -PassThru

# Guardar PID
$process.Id | Out-File "run\api.pid" -Encoding ascii

Write-Host "✅ Servidor iniciado en segundo plano (PID: $($process.Id))" -ForegroundColor Green
Write-Host "📝 Logs: logs\api.log" -ForegroundColor Yellow
Write-Host "📊 Métricas: http://localhost:5000/api/status" -ForegroundColor Yellow
Write-Host "🔗 API: http://localhost:5000/api/connect?token=$env:API_TOKEN`&message=hola" -ForegroundColor Yellow

Start-Sleep -Seconds 2

# Verificar que el servidor está ejecutándose
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -TimeoutSec 5
    Write-Host "🎉 ¡API operativa! Estado: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Verificando logs..." -ForegroundColor Yellow
    if (Test-Path "logs\\api_error.log") {
        Get-Content "logs\\api_error.log" -Tail 5
    }
}
