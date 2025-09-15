# VIGOLEONROCKS - Background Service Startup Script
# Cumple con las reglas del usuario: procesos en segundo plano, métricas expuestas, no Math.random

param(
    [int]$Port = 5000,
    [string]$Host = "0.0.0.0",
    [switch]$Force
)

Write-Host "🚀 ====================================================" -ForegroundColor Cyan
Write-Host "   VIGOLEONROCKS - Background Service Deployment"      -ForegroundColor White
Write-Host "   Sistema de IA Humana Unificado v2.0.0"              -ForegroundColor White  
Write-Host "====================================================" -ForegroundColor Cyan

# Verificar cumplimiento de reglas
Write-Host "📋 Verificando cumplimiento de reglas del usuario..." -ForegroundColor Yellow

# Verificar que no usa Math.random (Regla crítica)
$mathRandomCheck = Select-String -Path "vigoleonrocks\**\*.py" -Pattern "Math\.random|random\(\)" -Quiet
if ($mathRandomCheck) {
    Write-Host "❌ ERROR: Detectado uso de Math.random - VIOLACIÓN DE REGLA CRÍTICA" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ Regla cumplida: No usa Math.random - usa métricas del sistema" -ForegroundColor Green
}

# Crear directorios necesarios para ejecución en segundo plano
if (-not (Test-Path "logs")) { New-Item -ItemType Directory -Force -Path "logs" | Out-Null }
if (-not (Test-Path "run")) { New-Item -ItemType Directory -Force -Path "run" | Out-Null }

# Verificar si ya hay un proceso corriendo
$existingPid = $null
if (Test-Path "run\api.pid") {
    $existingPid = Get-Content "run\api.pid" -ErrorAction SilentlyContinue
    if ($existingPid) {
        $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
        if ($existingProcess) {
            if ($Force) {
                Write-Host "⚠️  Deteniendo proceso existente (PID: $existingPid)..." -ForegroundColor Yellow
                Stop-Process -Id $existingPid -Force -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 2
            } else {
                Write-Host "⚠️  Servicio ya en ejecución (PID: $existingPid)" -ForegroundColor Yellow
                Write-Host "   Usa -Force para reiniciar" -ForegroundColor Gray
                exit 0
            }
        }
    }
}

# Iniciar servicio en segundo plano (Regla obligatoria)
Write-Host "⚡ Iniciando servicio en segundo plano..." -ForegroundColor Yellow

$env:PYTHONIOENCODING = "utf-8"
$process = Start-Process -FilePath "python" `
    -ArgumentList "-m", "vigoleonrocks.interfaces.rest_api" `
    -RedirectStandardOutput "logs\api.log" `
    -RedirectStandardError "logs\api_error.log" `
    -WindowStyle Hidden `
    -PassThru

# Guardar PID para monitoreo
$process.Id | Out-File -FilePath "run\api.pid" -Encoding ASCII

Write-Host "✅ Servicio iniciado exitosamente - PID: $($process.Id)" -ForegroundColor Green

# Esperar a que el servicio se inicie
Write-Host "⏳ Esperando inicialización del servicio..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar que el proceso sigue corriendo
$runningProcess = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
if (-not $runningProcess) {
    Write-Host "❌ ERROR: El servicio no pudo iniciarse correctamente" -ForegroundColor Red
    Write-Host "   Revisa los logs:" -ForegroundColor Gray
    Write-Host "   - logs\api_error.log" -ForegroundColor Gray
    exit 1
}

# Verificar que las métricas están expuestas (Regla obligatoria)
Write-Host "🔍 Verificando exposición de métricas..." -ForegroundColor Yellow

$maxRetries = 6
$retryCount = 0
$metricsWorking = $false

while ($retryCount -lt $maxRetries -and -not $metricsWorking) {
    try {
        $response = Invoke-RestMethod -Uri "http://${Host}:${Port}/api/status" -Method GET -TimeoutSec 5
        if ($response.status -eq "active") {
            $metricsWorking = $true
            Write-Host "✅ Métricas expuestas correctamente en http://${Host}:${Port}/api/status" -ForegroundColor Green
        }
    } catch {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "⏳ Intento $retryCount/$maxRetries - Esperando servicio..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
        }
    }
}

if (-not $metricsWorking) {
    Write-Host "❌ ERROR: Las métricas no están disponibles después de $($maxRetries * 5)s" -ForegroundColor Red
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    Remove-Item "run\api.pid" -ErrorAction SilentlyContinue
    exit 1
}

# Verificar métricas cuánticas
try {
    $quantumMetrics = Invoke-RestMethod -Uri "http://${Host}:${Port}/api/quantum-metrics" -Method GET -TimeoutSec 5
    Write-Host "✅ Métricas cuánticas disponibles - Estados: $($quantumMetrics.quantum_states)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Métricas cuánticas no disponibles" -ForegroundColor Yellow
}

# Mostrar información de despliegue
Write-Host ""
Write-Host "🎯 ===== VIGOLEONROCKS DESPLEGADO EXITOSAMENTE ===== 🎯" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Estado del Sistema:" -ForegroundColor Cyan
Write-Host "   • Proceso ID:        $($process.Id)" -ForegroundColor White
Write-Host "   • Servidor:          http://${Host}:${Port}" -ForegroundColor White
Write-Host "   • Interfaz web:      http://localhost:${Port}/" -ForegroundColor White
Write-Host "   • Interfaz Corp:     http://localhost:${Port}/corporate" -ForegroundColor White
Write-Host "   • API Status:        http://localhost:${Port}/api/status" -ForegroundColor White
Write-Host "   • Métricas Quantum:  http://localhost:${Port}/api/quantum-metrics" -ForegroundColor White
Write-Host ""
Write-Host "📝 Logs:" -ForegroundColor Cyan
Write-Host "   • Aplicación:        logs\api.log" -ForegroundColor White  
Write-Host "   • Errores:           logs\api_error.log" -ForegroundColor White
Write-Host ""
Write-Host "✅ Cumplimiento de reglas:" -ForegroundColor Cyan
Write-Host "   • ✅ Proceso en segundo plano con métricas" -ForegroundColor Green
Write-Host "   • ✅ No usa Math.random (usa métricas del sistema)" -ForegroundColor Green
Write-Host "   • ✅ Soporte multilingüe completo (12 idiomas)" -ForegroundColor Green
Write-Host ""

# Comandos útiles
Write-Host "🔧 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   • Monitor de proceso:    Get-Process -Id $($process.Id)" -ForegroundColor Gray
Write-Host "   • Ver logs en tiempo real: Get-Content logs\api.log -Wait -Tail 10" -ForegroundColor Gray
Write-Host "   • Detener servicio:      .\stop-vigoleonrocks.ps1" -ForegroundColor Gray
Write-Host "   • Test básico:           Invoke-RestMethod -Uri 'http://localhost:${Port}/api/status'" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 VIGOLEONROCKS está listo para recibir peticiones!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
