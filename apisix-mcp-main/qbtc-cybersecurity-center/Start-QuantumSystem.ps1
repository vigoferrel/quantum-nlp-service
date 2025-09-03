# Start-QuantumSystem.ps1
# Script para lanzar el sistema cuántico unificado en segundo plano

$ErrorActionPreference = 'Stop'
$VerbosePreference = 'Continue'

# Configuración de rutas
$SYSTEM_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$FRONTEND_PATH = Join-Path $SYSTEM_ROOT "frontend-simplificado"
$SECURITY_SERVICE_PATH = Join-Path $SYSTEM_ROOT "security-service"
$LOG_PATH = Join-Path $SYSTEM_ROOT "logs"

# Crear directorio de logs si no existe
if (-not (Test-Path $LOG_PATH)) {
    New-Item -ItemType Directory -Path $LOG_PATH | Out-Null
    Write-Verbose "Directorio de logs creado: $LOG_PATH"
}

# Función para escribir logs
function Write-SystemLog {
    param(
        [string]$Message,
        [string]$Type = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Type] $Message"
    $logFile = Join-Path $LOG_PATH "quantum-system.log"
    
    Add-Content -Path $logFile -Value $logMessage
    Write-Verbose $logMessage
}

# Función para verificar puertos
function Test-PortAvailable {
    param(
        [int]$Port
    )
    
    try {
        $null = New-Object System.Net.Sockets.TcpClient('localhost', $Port)
        return $false
    }
    catch {
        return $true
    }
}

# Verificar puertos necesarios
$ports = @(3000, 3001, 3002, 3003)
foreach ($port in $ports) {
    if (-not (Test-PortAvailable $port)) {
        Write-SystemLog "Puerto $port en uso. Deteniendo el script." "ERROR"
        exit 1
    }
}

# Instalar http-server si no está instalado
try {
    $null = Get-Command http-server -ErrorAction Stop
}
catch {
    Write-SystemLog "Instalando http-server..." "INFO"
    Start-Process npm -ArgumentList "install -g http-server" -Wait -NoNewWindow
}

# Función para iniciar proceso en segundo plano
function Start-BackgroundProcess {
    param(
        [string]$Name,
        [string]$WorkingDirectory,
        [string]$Command,
        [string[]]$Arguments
    )
    
    try {
        $processInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processInfo.FileName = $Command
        $processInfo.Arguments = $Arguments -join " "
        $processInfo.WorkingDirectory = $WorkingDirectory
        $processInfo.RedirectStandardOutput = $true
        $processInfo.RedirectStandardError = $true
        $processInfo.UseShellExecute = $false
        $processInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
        
        $process = New-Object System.Diagnostics.Process
        $process.StartInfo = $processInfo
        $process.Start() | Out-Null
        
        Write-SystemLog "$Name iniciado con PID: $($process.Id)" "SUCCESS"
        return $process
    }
    catch {
        Write-SystemLog "Error al iniciar $Name`: $_" "ERROR"
        throw $_
    }
}

# Iniciar servicios principales
try {
    # Iniciar servicio de seguridad
    $securityProcess = Start-BackgroundProcess -Name "Security Service" `
        -WorkingDirectory $SECURITY_SERVICE_PATH `
        -Command "node" `
        -Arguments @("src/index.js")
    
    # Esperar a que el servicio esté listo
    Start-Sleep -Seconds 5
    
    # Iniciar frontend
    $frontendProcess = Start-BackgroundProcess -Name "Frontend Server" `
        -WorkingDirectory $FRONTEND_PATH `
        -Command "http-server" `
        -Arguments @("--port", "3000", "-c-1", "--cors")
        
    Write-SystemLog "Sistema Cuántico Unificado iniciado correctamente" "SUCCESS"
    Write-Host "`nSistema iniciado y accesible en:"
    Write-Host "- Frontend: http://localhost:3000"
    Write-Host "- API Security: http://localhost:3001"
    Write-Host "- API Events: http://localhost:3002"
    Write-Host "`nPresiona Ctrl+C para detener todos los servicios..."
    
    # Mantener el script corriendo y manejar la señal de interrupción
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Verificar si algún proceso terminó inesperadamente
        if ($securityProcess.HasExited) {
            Write-SystemLog "Security Service terminó inesperadamente" "ERROR"
            break
        }
        if ($frontendProcess.HasExited) {
            Write-SystemLog "Frontend Server terminó inesperadamente" "ERROR"
            break
        }
    }
}
catch {
    Write-SystemLog "Error crítico: $_" "ERROR"
}
finally {
    # Función para detener proceso de manera segura
    function Stop-ProcessSafely {
        param($Process, $Name)
        
        if ($Process -and -not $Process.HasExited) {
            Write-SystemLog "Deteniendo $Name..." "INFO"
            $Process.Kill()
            $Process.WaitForExit()
            Write-SystemLog "$Name detenido" "SUCCESS"
        }
    }
    
    # Detener todos los procesos
    Stop-ProcessSafely -Process $frontendProcess -Name "Frontend Server"
    Stop-ProcessSafely -Process $securityProcess -Name "Security Service"
    
    Write-SystemLog "Sistema Cuántico Unificado detenido" "INFO"
}
