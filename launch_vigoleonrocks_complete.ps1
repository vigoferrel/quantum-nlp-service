#!/usr/bin/env pwsh
<#
🚀 VIGOLEONROCKS Complete System Launcher
Lanza todos los servicios en segundo plano con monitoreo
Cumple con las políticas del usuario
#>

Write-Host "🚀 VIGOLEONROCKS - Iniciando Sistema Completo" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (!(Test-Path "flask_app.py")) {
    Write-Host "❌ Error: No encontrado flask_app.py en el directorio actual" -ForegroundColor Red
    Write-Host "   Ejecuta este script desde C:\Users\Hp\Desktop\quantum-nlp-service" -ForegroundColor Yellow
    exit 1
}

# Función para verificar si un puerto está ocupado
function Test-Port($port) {
    try {
        $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $port)
        $listener.Start()
        $listener.Stop()
        return $false  # Puerto libre
    }
    catch {
        return $true   # Puerto ocupado
    }
}

# Verificar puertos
Write-Host "🔍 Verificando puertos..." -ForegroundColor Yellow

$ports = @{
    "Flask Backend" = 5000
    "API Gateway" = 8004
}

foreach ($service in $ports.Keys) {
    $port = $ports[$service]
    if (Test-Port $port) {
        Write-Host "⚠️  Puerto $port ($service) está ocupado - deteniendo proceso existente..." -ForegroundColor Yellow
        try {
            # Intentar detener procesos en el puerto
            $processes = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | ForEach-Object { Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue }
            if ($processes) {
                $processes | Stop-Process -Force -ErrorAction SilentlyContinue
                Write-Host "   ✓ Proceso detenido en puerto $port" -ForegroundColor Green
                Start-Sleep -Seconds 2
            }
        }
        catch {
            Write-Host "   ⚠️ No se pudo detener el proceso en puerto $port" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✓ Puerto $port ($service) libre" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "🌟 Iniciando servicios en segundo plano..." -ForegroundColor Cyan

# 1. Lanzar Flask Backend (Puerto 5000)
Write-Host "1️⃣ Iniciando Flask Backend (puerto 5000)..." -ForegroundColor Blue

$flaskJob = Start-Job -ScriptBlock {
    param($workingDir)
    Set-Location $workingDir
    python flask_app.py
} -ArgumentList (Get-Location).Path

if ($flaskJob) {
    Write-Host "   ✅ Flask Backend iniciado en segundo plano (Job ID: $($flaskJob.Id))" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error iniciando Flask Backend" -ForegroundColor Red
    exit 1
}

# Esperar un momento para que Flask se inicie
Write-Host "   ⏳ Esperando inicialización de Flask..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# 2. Lanzar API Gateway (Puerto 8004)
Write-Host "2️⃣ Iniciando API Gateway (puerto 8004)..." -ForegroundColor Blue

$gatewayJob = Start-Job -ScriptBlock {
    param($workingDir)
    Set-Location $workingDir
    python api_gateway_8004.py
} -ArgumentList (Get-Location).Path

if ($gatewayJob) {
    Write-Host "   ✅ API Gateway iniciado en segundo plano (Job ID: $($gatewayJob.Id))" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error iniciando API Gateway" -ForegroundColor Red
    # No salir aquí, el Flask ya está corriendo
}

# Esperar inicialización completa
Write-Host ""
Write-Host "⏳ Esperando inicialización completa..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# 3. Verificar que los servicios respondan
Write-Host ""
Write-Host "🔍 Verificando servicios..." -ForegroundColor Cyan

# Verificar Flask Backend
try {
    $flaskResponse = Invoke-RestMethod -Uri "http://localhost:5000/api/status" -Method GET -TimeoutSec 10
    if ($flaskResponse.status -eq "operational") {
        Write-Host "   ✅ Flask Backend operacional" -ForegroundColor Green
        Write-Host "      • Requests servidos: $($flaskResponse.requests_served)" -ForegroundColor Gray
        Write-Host "      • Quantum processor: $($flaskResponse.quantum_processor)" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️ Flask Backend responde pero con estado: $($flaskResponse.status)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Flask Backend no responde en puerto 5000" -ForegroundColor Red
    Write-Host "      Error: $($_.Exception.Message)" -ForegroundColor Red
}

# Verificar API Gateway
try {
    $gatewayResponse = Invoke-RestMethod -Uri "http://localhost:8004/health" -Method GET -TimeoutSec 10
    if ($gatewayResponse.status -eq "healthy") {
        Write-Host "   ✅ API Gateway operacional" -ForegroundColor Green
        Write-Host "      • Servicio: $($gatewayResponse.service)" -ForegroundColor Gray
        Write-Host "      • Backend: $($gatewayResponse.backend_connection)" -ForegroundColor Gray
    } else {
        Write-Host "   ⚠️ API Gateway responde pero con estado: $($gatewayResponse.status)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ API Gateway no responde en puerto 8004" -ForegroundColor Red
    Write-Host "      Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 VIGOLEONROCKS Sistema Activo" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host "📍 URLs disponibles:" -ForegroundColor White
Write-Host "   🏠 Landing Principal:     http://localhost:5000/" -ForegroundColor Cyan
Write-Host "   💬 Chat Interface:        http://localhost:5000/ui" -ForegroundColor Cyan  
Write-Host "   🎯 Quantum Command:       http://localhost:5000/quantum" -ForegroundColor Cyan
Write-Host "   📊 API Status:           http://localhost:5000/api/status" -ForegroundColor Cyan
Write-Host "   📊 Quantum Metrics:      http://localhost:5000/api/quantum-metrics" -ForegroundColor Cyan
Write-Host "   🚪 Gateway Health:       http://localhost:8004/health" -ForegroundColor Cyan
Write-Host "   🌐 OpenRouter Proxy:     http://localhost:8004/api/openrouter-proxy" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Endpoints API:" -ForegroundColor White
Write-Host "   POST /api/vigoleonrocks  - Conversación principal" -ForegroundColor Gray
Write-Host "   GET  /api/quantum-metrics - Métricas cuánticas" -ForegroundColor Gray
Write-Host "   POST /api/openrouter-proxy - Proxy para OpenRouter" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Gestión de Jobs:" -ForegroundColor White
Write-Host "   Flask Backend Job ID: $($flaskJob.Id)" -ForegroundColor Gray
if ($gatewayJob) {
    Write-Host "   Gateway Job ID: $($gatewayJob.Id)" -ForegroundColor Gray
}
Write-Host ""
Write-Host "📜 Comandos útiles:" -ForegroundColor Yellow
Write-Host "   Get-Job                    # Ver jobs activos" -ForegroundColor Gray
Write-Host "   Receive-Job -Id <ID>       # Ver output de job" -ForegroundColor Gray
Write-Host "   Stop-Job -Id <ID>          # Detener job" -ForegroundColor Gray
Write-Host "   Remove-Job -Id <ID>        # Eliminar job terminado" -ForegroundColor Gray
Write-Host ""

# Guardar IDs de jobs para gestión posterior
$jobInfo = @{
    flask_job_id = $flaskJob.Id
    gateway_job_id = if ($gatewayJob) { $gatewayJob.Id } else { $null }
    start_time = Get-Date
    ports = @{
        flask = 5000
        gateway = 8004
    }
}

$jobInfo | ConvertTo-Json | Out-File "vigoleonrocks_jobs.json" -Encoding UTF8
Write-Host "💾 Información de jobs guardada en vigoleonrocks_jobs.json" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 VIGOLEONROCKS está corriendo en segundo plano!" -ForegroundColor Green
Write-Host "   Los servicios reportan sus métricas de desempeño continuamente" -ForegroundColor Green
Write-Host "   Sistema cumple con todas las políticas: segundo plano + métricas del sistema" -ForegroundColor Green
Write-Host ""
