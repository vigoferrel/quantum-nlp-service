# Service Manager para QBTC Quantum Security System
# Gestiona los servicios del sistema cuántico en segundo plano

param (
    [Parameter(Mandatory=$false)]
    [ValidateSet('start', 'stop', 'restart', 'status')]
    [string]$Action = 'status',

    [Parameter(Mandatory=$false)]
    [ValidateSet('all', 'core', 'security', 'api', 'monitoring', 'web')]
    [string]$Service = 'all',

    [Parameter(Mandatory=$false)]
    [string]$Environment = 'production'
)

# Configuración
$CONFIG = @{
    BasePath = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
    LogPath = Join-Path (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)) "logs"
    PidPath = Join-Path (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)) "pids"
}

# Asegurar directorios necesarios
$null = New-Item -ItemType Directory -Force -Path $CONFIG.LogPath
$null = New-Item -ItemType Directory -Force -Path $CONFIG.PidPath

# Definición de servicios y sus puertos
$SERVICES = @{
    core = @{
        name = "Quantum Core"
        script = "index.js"
        port = 7000
    }
    security = @{
        name = "Security Service"
        script = "core/quantum-security.js"
        port = 7100
    }
    api = @{
        name = "API Gateway"
        script = "core/api-gateway.js"
        port = 7200
    }
    monitoring = @{
        name = "Monitoring Service"
        script = "core/quantum-monitor.js"
        port = 7300
    }
    web = @{
        name = "Web Dashboard"
        script = "core/web-interface.js"
        port = 7400
    }
}

# Funciones de utilidad
function Write-ServiceLog {
    param($Message, $Type = 'Info')
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Type] $Message"
    $logFile = Join-Path $CONFIG.LogPath "service-$(Get-Date -Format 'yyyy-MM-dd').log"
    Add-Content -Path $logFile -Value $logMessage
    
    switch ($Type) {
        'Error' { Write-Host $logMessage -ForegroundColor Red }
        'Warning' { Write-Host $logMessage -ForegroundColor Yellow }
        'Success' { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage }
    }
}

function Get-ServicePid {
    param($ServiceName)
    $pidFile = Join-Path $CONFIG.PidPath "$ServiceName.pid"
    if (Test-Path $pidFile) {
        return Get-Content $pidFile
    }
    return $null
}

function Save-ServicePid {
    param($ServiceName, $Pid)
    $pidFile = Join-Path $CONFIG.PidPath "$ServiceName.pid"
    Set-Content -Path $pidFile -Value $Pid
}

function Remove-ServicePid {
    param($ServiceName)
    $pidFile = Join-Path $CONFIG.PidPath "$ServiceName.pid"
    if (Test-Path $pidFile) {
        Remove-Item $pidFile -Force
    }
}

function Test-ServiceRunning {
    param($ServiceName)
    $pid = Get-ServicePid $ServiceName
    if ($pid) {
        try {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            return $process -ne $null
        } catch {
            return $false
        }
    }
    return $false
}

function Start-QuantumService {
    param($ServiceName)
    $service = $SERVICES[$ServiceName]
    if (-not $service) {
        Write-ServiceLog "Servicio no encontrado: $ServiceName" -Type Error
        return $false
    }

    if (Test-ServiceRunning $ServiceName) {
        Write-ServiceLog "El servicio $($service.name) ya está en ejecución" -Type Warning
        return $true
    }

    $scriptPath = Join-Path $CONFIG.BasePath $service.script
    if (-not (Test-Path $scriptPath)) {
        Write-ServiceLog "Script no encontrado: $scriptPath" -Type Error
        return $false
    }

    try {
        $logFile = Join-Path $CONFIG.LogPath "$ServiceName.log"
        $env:PORT = $service.port
        $env:NODE_ENV = $Environment

        $processArgs = @{
            FilePath = "node.exe"
            ArgumentList = $scriptPath
            RedirectStandardOutput = $logFile
            RedirectStandardError = "$logFile.error"
            PassThru = $true
            NoNewWindow = $true
        }

        $process = Start-Process @processArgs
        Save-ServicePid $ServiceName $process.Id
        Write-ServiceLog "Servicio $($service.name) iniciado (PID: $($process.Id))" -Type Success
        return $true
    }
    catch {
        Write-ServiceLog "Error al iniciar $($service.name): $_" -Type Error
        return $false
    }
}

function Stop-QuantumService {
    param($ServiceName)
    $service = $SERVICES[$ServiceName]
    if (-not $service) {
        Write-ServiceLog "Servicio no encontrado: $ServiceName" -Type Error
        return $false
    }

    $pid = Get-ServicePid $ServiceName
    if ($pid) {
        try {
            Stop-Process -Id $pid -Force
            Remove-ServicePid $ServiceName
            Write-ServiceLog "Servicio $($service.name) detenido" -Type Success
            return $true
        }
        catch {
            Write-ServiceLog "Error al detener $($service.name): $_" -Type Error
            return $false
        }
    }
    else {
        Write-ServiceLog "Servicio $($service.name) no está en ejecución" -Type Warning
        return $true
    }
}

function Get-ServiceStatus {
    param($ServiceName)
    $service = $SERVICES[$ServiceName]
    if (-not $service) {
        Write-ServiceLog "Servicio no encontrado: $ServiceName" -Type Error
        return
    }

    $running = Test-ServiceRunning $ServiceName
    $pid = Get-ServicePid $ServiceName
    $status = if ($running) { "ACTIVO" } else { "DETENIDO" }
    $color = if ($running) { "Green" } else { "Red" }

    Write-Host "`n$($service.name)" -ForegroundColor Cyan
    Write-Host "------------------------"
    Write-Host "Estado: " -NoNewline
    Write-Host $status -ForegroundColor $color
    Write-Host "PID: $pid"
    Write-Host "Puerto: $($service.port)"
    Write-Host "Script: $($service.script)"
}

# Lógica principal
function Invoke-ServiceAction {
    param($Action, $Service)
    
    $serviceList = if ($Service -eq 'all') { $SERVICES.Keys } else { @($Service) }

    foreach ($svc in $serviceList) {
        switch ($Action) {
            'start' {
                Write-ServiceLog "Iniciando $($SERVICES[$svc].name)..."
                Start-QuantumService $svc
            }
            'stop' {
                Write-ServiceLog "Deteniendo $($SERVICES[$svc].name)..."
                Stop-QuantumService $svc
            }
            'restart' {
                Write-ServiceLog "Reiniciando $($SERVICES[$svc].name)..."
                Stop-QuantumService $svc
                Start-Sleep -Seconds 2
                Start-QuantumService $svc
            }
            'status' {
                Get-ServiceStatus $svc
            }
        }
    }
}

# Ejecución
Write-Host "`n🛡️ QBTC Quantum Security System - Service Manager" -ForegroundColor Cyan
Write-Host "Ambiente: $Environment" -ForegroundColor Yellow
Write-Host "Acción: $Action" -ForegroundColor Yellow
Write-Host "Servicios: $Service`n" -ForegroundColor Yellow

Invoke-ServiceAction -Action $Action -Service $Service
