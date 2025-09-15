#!/usr/bin/env pwsh
<#
🚀 VIGOLEONROCKS Simple Launcher
Lanza los servicios en segundo plano
#>

Write-Host "🚀 VIGOLEONROCKS - Iniciando Sistema Completo" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan

# Verificar directorio
if (!(Test-Path "flask_app.py")) {
    Write-Host "❌ Error: flask_app.py no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "🌟 Iniciando servicios..." -ForegroundColor Cyan

# 1. Iniciar Flask Backend
Write-Host "1️⃣ Iniciando Flask Backend (puerto 5000)..." -ForegroundColor Blue

$flaskJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    python flask_app.py
} -ArgumentList (Get-Location).Path

if ($flaskJob) {
    Write-Host "   ✅ Flask Backend iniciado (Job ID: $($flaskJob.Id))" -ForegroundColor Green
}

Start-Sleep -Seconds 4

# 2. Iniciar API Gateway
Write-Host "2️⃣ Iniciando API Gateway (puerto 8004)..." -ForegroundColor Blue

$gatewayJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    python api_gateway_8004.py
} -ArgumentList (Get-Location).Path

if ($gatewayJob) {
    Write-Host "   ✅ API Gateway iniciado (Job ID: $($gatewayJob.Id))" -ForegroundColor Green
}

Start-Sleep -Seconds 3

# 3. Verificar servicios
Write-Host "🔍 Verificando servicios..." -ForegroundColor Cyan

# Test Flask
try {
    $response = Invoke-RestMethod "http://localhost:5000/api/status" -TimeoutSec 5
    Write-Host "   ✅ Flask Backend: operacional" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Flask Backend: no responde aún" -ForegroundColor Yellow
}

# Test Gateway
try {
    $response = Invoke-RestMethod "http://localhost:8004/health" -TimeoutSec 5
    Write-Host "   ✅ API Gateway: operacional" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ API Gateway: no responde aún" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 VIGOLEONROCKS Sistema Activo" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "📍 URLs principales:" -ForegroundColor White
Write-Host "   🏠 Landing:      http://localhost:5000/" -ForegroundColor Cyan
Write-Host "   💬 Chat:         http://localhost:5000/ui" -ForegroundColor Cyan  
Write-Host "   🎯 Command:      http://localhost:5000/quantum" -ForegroundColor Cyan
Write-Host "   📊 Status:       http://localhost:5000/api/status" -ForegroundColor Cyan
Write-Host "   📊 Metrics:      http://localhost:5000/api/quantum-metrics" -ForegroundColor Cyan
Write-Host "   🚪 Gateway:      http://localhost:8004/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Endpoints API:" -ForegroundColor White
Write-Host "   POST /api/vigoleonrocks  - Conversación" -ForegroundColor Gray
Write-Host "   POST /api/openrouter-proxy - OpenRouter" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Jobs IDs:" -ForegroundColor White
Write-Host "   Flask: $($flaskJob.Id)" -ForegroundColor Gray
Write-Host "   Gateway: $($gatewayJob.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "📜 Comandos:" -ForegroundColor Yellow
Write-Host "   Get-Job         # Ver jobs activos" -ForegroundColor Gray
Write-Host "   Stop-Job -Id X  # Detener job" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 VIGOLEONROCKS corriendo en segundo plano!" -ForegroundColor Green
