# VIGOLEONROCKS - Service Stop Script
# Para detener servicios ejecutándose en segundo plano

param(
    [switch]$Force
)

Write-Host "🛑 ===== DETENIENDO VIGOLEONROCKS =====" -ForegroundColor Yellow

# Verificar si hay un PID registrado
if (-not (Test-Path "run\api.pid")) {
    Write-Host "⚠️  No se encontró archivo de PID" -ForegroundColor Yellow
    Write-Host "   Buscando procesos python con vigoleonrocks..." -ForegroundColor Gray
    
    $processes = Get-Process python -ErrorAction SilentlyContinue | Where-Object { 
        $_.CommandLine -match "vigoleonrocks" 
    }
    
    if ($processes) {
        Write-Host "💡 Encontrados $($processes.Count) proceso(s) python relacionados:" -ForegroundColor Cyan
        foreach ($proc in $processes) {
            Write-Host "   - PID: $($proc.Id)" -ForegroundColor White
            if ($Force) {
                Stop-Process -Id $proc.Id -Force
                Write-Host "   ✅ Proceso $($proc.Id) detenido" -ForegroundColor Green
            }
        }
        if (-not $Force) {
            Write-Host "   Usa -Force para detenerlos" -ForegroundColor Gray
        }
    } else {
        Write-Host "✅ No hay procesos VIGOLEONROCKS ejecutándose" -ForegroundColor Green
    }
    exit 0
}

# Leer PID del archivo
$pid = Get-Content "run\api.pid" -ErrorAction SilentlyContinue

if (-not $pid) {
    Write-Host "❌ No se pudo leer el PID del archivo" -ForegroundColor Red
    exit 1
}

# Verificar si el proceso existe
$process = Get-Process -Id $pid -ErrorAction SilentlyContinue

if (-not $process) {
    Write-Host "⚠️  El proceso PID $pid ya no está ejecutándose" -ForegroundColor Yellow
    Remove-Item "run\api.pid" -ErrorAction SilentlyContinue
    Write-Host "✅ Archivo PID limpiado" -ForegroundColor Green
    exit 0
}

# Detener el proceso
Write-Host "🔄 Deteniendo proceso VIGOLEONROCKS (PID: $pid)..." -ForegroundColor Yellow

try {
    Stop-Process -Id $pid -Force:$Force
    Start-Sleep -Seconds 2
    
    # Verificar que se detuvo
    $processAfter = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($processAfter) {
        Write-Host "⚠️  El proceso aún está ejecutándose. Forzando terminación..." -ForegroundColor Yellow
        Stop-Process -Id $pid -Force
        Start-Sleep -Seconds 1
    }
    
    Write-Host "✅ Proceso detenido exitosamente" -ForegroundColor Green
    
    # Limpiar archivo PID
    Remove-Item "run\api.pid" -ErrorAction SilentlyContinue
    Write-Host "✅ Archivo PID limpiado" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎯 VIGOLEONROCKS detenido correctamente" -ForegroundColor Green
    Write-Host "   Para reiniciar: .\start-vigoleonrocks.ps1" -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Error deteniendo proceso: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
