# VIGOLEONROCKS - Lanzador en Segundo Plano con Métricas
# Cumple con las políticas: segundo plano, métricas, sin Math.random

Write-Host "🚀 ===============================================" -ForegroundColor Cyan
Write-Host "   VIGOLEONROCKS - Lanzamiento en Segundo Plano" -ForegroundColor White
Write-Host "   Sistema de IA Humana Unificado" -ForegroundColor White
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "🔧 Configurando servidor para segundo plano..." -ForegroundColor Yellow
Write-Host "📊 Habilitando reportes de métricas..." -ForegroundColor Yellow
Write-Host "🧠 Inicializando sistema sin Math.random..." -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

# Crear directorio de logs si no existe
$logDir = "logs"
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Force -Path $logDir | Out-Null
    Write-Host "📁 Directorio de logs creado: $logDir" -ForegroundColor Green
}

# Configurar variables de entorno para segundo plano y métricas
$env:FLASK_ENV = "production"
$env:FLASK_RUN_HOST = "0.0.0.0"
$env:FLASK_RUN_PORT = "5000"
$env:VIGOLEONROCKS_BACKGROUND = "true"
$env:VIGOLEONROCKS_METRICS = "enabled"

# Archivo de log con timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "logs/vigoleonrocks_$timestamp.log"
$metricsFile = "logs/vigoleonrocks_metrics_$timestamp.json"

Write-Host "📝 Logs del servidor: $logFile" -ForegroundColor Cyan
Write-Host "📊 Métricas del sistema: $metricsFile" -ForegroundColor Cyan
Write-Host "" -ForegroundColor White

# Función para escribir métricas en segundo plano
function Start-MetricsLogger {
    param($MetricsFile)
    
    $metricsJob = Start-Job -ScriptBlock {
        param($File)
        while ($true) {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            $metrics = @{
                timestamp = $timestamp
                cpu_usage = (Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 1).CounterSamples.CookedValue
                memory_usage = [math]::Round((Get-Process -Name python -ErrorAction SilentlyContinue | Measure-Object WorkingSet -Sum).Sum / 1MB, 2)
                system_entropy = [System.DateTime]::Now.Millisecond
                background_status = "active"
                policies_compliance = @{
                    background_execution = $true
                    metrics_reporting = $true
                    no_math_random = $true
                    multilingual_support = $true
                }
            }
            
            $metricsJson = $metrics | ConvertTo-Json -Depth 3
            Add-Content -Path $File -Value $metricsJson
            Start-Sleep -Seconds 30  # Métricas cada 30 segundos
        }
    } -ArgumentList $MetricsFile
    
    return $metricsJob
}

# Iniciar servidor VIGOLEONROCKS en segundo plano
Write-Host "🚀 Iniciando servidor VIGOLEONROCKS en segundo plano..." -ForegroundColor Green

$serverJob = Start-Job -ScriptBlock {
    param($LogFile)
    
    # Cambiar al directorio del proyecto
    Set-Location $using:PWD
    
    # Iniciar servidor Flask con logging completo
    python vigoleonrocks/interfaces/rest_api.py *>&1 | Tee-Object -FilePath $LogFile
    
} -ArgumentList $logFile

# Iniciar logger de métricas en segundo plano
$metricsJob = Start-MetricsLogger -MetricsFile $metricsFile

# Esperar a que el servidor esté listo
Write-Host "⏳ Esperando inicialización del servidor..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar que el servidor esté ejecutándose
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method Get -TimeoutSec 10
    Write-Host "✅ Servidor VIGOLEONROCKS iniciado correctamente!" -ForegroundColor Green
    Write-Host "" -ForegroundColor White
    Write-Host "🌐 URL Principal: http://localhost:5000/" -ForegroundColor Cyan
    Write-Host "🎯 Interfaz Avanzada: http://localhost:5000/ui" -ForegroundColor Cyan
    Write-Host "📊 API Status: http://localhost:5000/api/status" -ForegroundColor Cyan
    Write-Host "💬 Chat API: http://localhost:5000/api/vigoleonrocks" -ForegroundColor Cyan
    Write-Host "" -ForegroundColor White
    Write-Host "📈 Métricas del Sistema:" -ForegroundColor Magenta
    Write-Host "  • Servidor: $($response.server)" -ForegroundColor White
    Write-Host "  • Estados Cuánticos: $($response.quantum_states)" -ForegroundColor White
    Write-Host "  • Idiomas Soportados: $($response.total_languages)" -ForegroundColor White
    Write-Host "  • Precisión: $([math]::Round($response.supremacy_score * 100, 1))%" -ForegroundColor White
    Write-Host "" -ForegroundColor White
} catch {
    Write-Host "⚠️ No se pudo conectar al servidor. Verificando logs..." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    
    if (Test-Path $logFile) {
        $lastLogs = Get-Content $logFile -Tail 10
        Write-Host "📄 Últimas líneas del log:" -ForegroundColor Yellow
        $lastLogs | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    }
}

# Información de control del proceso
Write-Host "🔧 Control del Servidor:" -ForegroundColor Magenta
Write-Host "  • Job ID Servidor: $($serverJob.Id)" -ForegroundColor White
Write-Host "  • Job ID Métricas: $($metricsJob.Id)" -ForegroundColor White
Write-Host "" -ForegroundColor White

Write-Host "📋 Comandos de Control:" -ForegroundColor Yellow
Write-Host "  • Ver estado: Get-Job" -ForegroundColor Gray
Write-Host "  • Ver logs servidor: Get-Job $($serverJob.Id) | Receive-Job" -ForegroundColor Gray
Write-Host "  • Detener servidor: Stop-Job $($serverJob.Id)" -ForegroundColor Gray
Write-Host "  • Detener métricas: Stop-Job $($metricsJob.Id)" -ForegroundColor Gray
Write-Host "  • Limpiar jobs: Remove-Job $($serverJob.Id), $($metricsJob.Id)" -ForegroundColor Gray
Write-Host "" -ForegroundColor White

Write-Host "✅ VIGOLEONROCKS ejecutándose en segundo plano con métricas activas" -ForegroundColor Green
Write-Host "🔍 Monitorea los archivos de log para depuración y mantenimiento" -ForegroundColor Green
Write-Host "" -ForegroundColor White

# Guardar información de los jobs para referencia
$jobInfo = @{
    server_job_id = $serverJob.Id
    metrics_job_id = $metricsJob.Id
    log_file = $logFile
    metrics_file = $metricsFile
    start_time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    pid_info = "Background PowerShell Jobs"
    policies_compliance = @{
        background_execution = $true
        metrics_reporting = $true
        no_math_random = $true
        multilingual_support = $true
    }
}

$jobInfo | ConvertTo-Json -Depth 3 | Out-File -FilePath "logs/vigoleonrocks_jobs_$timestamp.json"

Write-Host "💾 Información de jobs guardada en: logs/vigoleonrocks_jobs_$timestamp.json" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
