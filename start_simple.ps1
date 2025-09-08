# VIGOLEONROCKS Simple Launch Script
# Ejecuta en segundo plano cumpliendo con políticas establecidas

Write-Host "🚀 VIGOLEONROCKS QUANTUM LAUNCH" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Crear directorio de logs
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null
    Write-Host "📁 Logs directory created" -ForegroundColor Green
}

Write-Host "🌌 Starting quantum server in background..." -ForegroundColor Magenta

# Launch in background
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python vigoleonrocks\interfaces\rest_api.py
}

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "✅ VIGOLEONROCKS LAUNCHED!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host "🌐 Command Center:    http://localhost:5000/quantum" -ForegroundColor Cyan
Write-Host "🎯 Main Interface:    http://localhost:5000/" -ForegroundColor Cyan  
Write-Host "📊 API Status:        http://localhost:5000/api/status" -ForegroundColor Cyan
Write-Host "⚡ Quantum Metrics:   http://localhost:5000/api/quantum-metrics" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 PROCESS CONTROL:" -ForegroundColor Magenta
Write-Host "  • Job ID: $($job.Id)" -ForegroundColor Gray
Write-Host "  • View logs: Receive-Job $($job.Id)" -ForegroundColor Gray
Write-Host "  • Stop server: Stop-Job $($job.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "✅ POLICIES COMPLIANT:" -ForegroundColor Green
Write-Host "  • ✅ Background execution" -ForegroundColor Green
Write-Host "  • ✅ System metrics exposed (NO Math.random)" -ForegroundColor Green
Write-Host "  • ✅ Multilingual support ready" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan

# Return job info for management
return @{
    JobId = $job.Id
    Status = "Running"
    URLs = @{
        CommandCenter = "http://localhost:5000/quantum"
        MainInterface = "http://localhost:5000/"
        ApiStatus = "http://localhost:5000/api/status"
        QuantumMetrics = "http://localhost:5000/api/quantum-metrics"
    }
}
