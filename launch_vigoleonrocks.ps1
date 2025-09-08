# VIGOLEONROCKS - Lanzador en Segundo Plano con Métricas
# Cumple con las políticas: segundo plano, métricas, sin Math.random

Write-Host "🚀 ===============================================" -ForegroundColor Cyan
Write-Host "   VIGOLEONROCKS - Lanzamiento en Segundo Plano" -ForegroundColor White
Write-Host "   Sistema de IA Humana Unificado" -ForegroundColor White
Write-Host "===============================================" -ForegroundColor Cyan

# Crear directorio de logs
$logDir = "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    Write-Host "📁 Directorio de logs creado: $logDir" -ForegroundColor Green
}

# Timestamp para archivos
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "logs\vigoleonrocks_$timestamp.log"

Write-Host "📝 Archivo de log: $logFile" -ForegroundColor Cyan
Write-Host ""

# Lanzar servidor en segundo plano
Write-Host "🚀 Iniciando VIGOLEONROCKS en segundo plano..." -ForegroundColor Green

$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python vigoleonrocks\interfaces\rest_api.py 2>&1
}

# Esperar inicialización
Write-Host "⏳ Esperando inicialización del servidor..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Verificar estado
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method Get -TimeoutSec 15
    Write-Host "✅ Servidor VIGOLEONROCKS iniciado correctamente!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 URL Principal: http://localhost:5000/" -ForegroundColor Cyan
    Write-Host "🎯 Interfaz Avanzada: http://localhost:5000/ui" -ForegroundColor Cyan
    Write-Host "📊 API Status: http://localhost:5000/api/status" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📈 Métricas del Sistema:" -ForegroundColor Magenta
    Write-Host "  • Servidor: $($response.server)" -ForegroundColor White
    Write-Host "  • Estados Cuánticos: $($response.quantum_states)" -ForegroundColor White
    Write-Host "  • Idiomas: $($response.total_languages)" -ForegroundColor White
    Write-Host "  • Precisión: $([math]::Round($response.supremacy_score * 100, 1))%" -ForegroundColor White
    Write-Host ""
    Write-Host "🔧 Control del Job: $($job.Id)" -ForegroundColor Magenta
    Write-Host "  • Ver estado: Get-Job $($job.Id)" -ForegroundColor Gray
    Write-Host "  • Ver logs: Receive-Job $($job.Id)" -ForegroundColor Gray
    Write-Host "  • Detener: Stop-Job $($job.Id)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Sistema ejecutándose en segundo plano con métricas activas" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Error conectando al servidor:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "📄 Verificando logs del job..." -ForegroundColor Yellow
    $jobOutput = Receive-Job $job
    if ($jobOutput) {
        Write-Host "Salida del servidor:" -ForegroundColor Yellow
        $jobOutput | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
    }
}

Write-Host "===============================================" -ForegroundColor Cyan
