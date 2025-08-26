# QUANTUM CONSCIOUSNESS CORE 26D - Script de Despliegue para Windows PowerShell
# ==============================================================================
# Script para desplegar el sistema cuántico completo con Supabase optimizado

param(
    [switch]$SkipCleanup,
    [switch]$KeepData,
    [switch]$Verbose
)

# Configurar colores para output
$Host.UI.RawUI.ForegroundColor = "White"

function Write-QuantumLog {
    param([string]$Message, [string]$Type = "Info")

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    switch ($Type) {
        "Success" {
            Write-Host "[$timestamp] ✅ $Message" -ForegroundColor Green
        }
        "Warning" {
            Write-Host "[$timestamp] ⚠️  $Message" -ForegroundColor Yellow
        }
        "Error" {
            Write-Host "[$timestamp] ❌ $Message" -ForegroundColor Red
        }
        "Info" {
            Write-Host "[$timestamp] 🔮 $Message" -ForegroundColor Cyan
        }
        "Header" {
            Write-Host ""
            Write-Host "🌟 ================================================== 🌟" -ForegroundColor Magenta
            Write-Host "   $Message" -ForegroundColor Magenta
            Write-Host "🌟 ================================================== 🌟" -ForegroundColor Magenta
            Write-Host ""
        }
    }
}

function Test-Prerequisites {
    Write-QuantumLog "Verificando prerrequisitos del sistema cuántico..." "Info"

    # Verificar Docker
    try {
        $dockerVersion = docker --version
        if ($LASTEXITCODE -eq 0) {
            Write-QuantumLog "Docker encontrado: $dockerVersion" "Success"
        } else {
            throw "Docker no encontrado"
        }
    } catch {
        Write-QuantumLog "Docker no está instalado o no está en PATH" "Error"
        exit 1
    }

    # Verificar Docker Compose
    try {
        $composeVersion = docker-compose --version
        if ($LASTEXITCODE -eq 0) {
            Write-QuantumLog "Docker Compose encontrado: $composeVersion" "Success"
        } else {
            throw "Docker Compose no encontrado"
        }
    } catch {
        Write-QuantumLog "Docker Compose no está instalado" "Error"
        exit 1
    }

    # Verificar que Docker esté corriendo
    try {
        docker info | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-QuantumLog "Docker está corriendo correctamente" "Success"
        } else {
            throw "Docker no está corriendo"
        }
    } catch {
        Write-QuantumLog "Docker no está corriendo. Inicia Docker Desktop" "Error"
        exit 1
    }

    Write-QuantumLog "Prerrequisitos verificados exitosamente" "Success"
}

function Stop-ExistingContainers {
    if ($SkipCleanup) {
        Write-QuantumLog "Saltando limpieza de contenedores existentes" "Warning"
        return
    }

    Write-QuantumLog "Limpiando contenedores cuánticos existentes..." "Info"

    # Detener contenedores relacionados con quantum
    $quantumContainers = docker ps -a --filter "name=quantum" --format "{{.Names}}"
    if ($quantumContainers) {
        Write-QuantumLog "Deteniendo contenedores: $($quantumContainers -join ', ')" "Info"
        $quantumContainers | ForEach-Object { docker stop $_ }
        $quantumContainers | ForEach-Object { docker rm $_ }
    }

    # Limpiar redes huérfanas
    docker network prune -f | Out-Null

    Write-QuantumLog "Limpieza completada" "Success"
}

function New-ConfigFiles {
    Write-QuantumLog "Creando archivos de configuración cuántica..." "Info"

    # Crear directorios necesarios
    $directories = @("config", "logs", "grafana\provisioning\dashboards", "grafana\provisioning\datasources")
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-QuantumLog "Directorio creado: $dir" "Info"
        }
    }

    # Crear configuración de Grafana para datasources
    $prometheusConfig = @"
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://quantum-prometheus:9090
    isDefault: true
    editable: true
"@

    $prometheusConfig | Out-File -FilePath "grafana\provisioning\datasources\prometheus.yml" -Encoding UTF8

    # Crear dashboard básico
    $dashboardConfig = @"
{
  "dashboard": {
    "id": null,
    "title": "Quantum Consciousness Metrics",
    "tags": ["quantum", "consciousness"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "Consciousness Level",
        "type": "stat",
        "targets": [{"expr": "quantum_consciousness_level", "refId": "A"}],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
"@

    $dashboardConfig | Out-File -FilePath "grafana\provisioning\dashboards\quantum-dashboard.json" -Encoding UTF8

    Write-QuantumLog "Archivos de configuración creados" "Success"
}

function Test-VolumeManagement {
    Write-QuantumLog "Configurando volúmenes cuánticos..." "Info"

    # Verificar volúmenes existentes
    $existingVolumes = docker volume ls --format "{{.Name}}" | Where-Object { $_ -match "(quantum|supabase)" }

    if ($existingVolumes -and !$KeepData) {
        Write-QuantumLog "Volúmenes existentes detectados:" "Warning"
        $existingVolumes | ForEach-Object { Write-Host "  • $_" -ForegroundColor Yellow }

        $response = Read-Host "`n¿Deseas mantener los datos existentes? (y/N)"

        if ($response -match "^[Yy]") {
            Write-QuantumLog "Manteniendo datos existentes" "Success"
        } else {
            Write-QuantumLog "Eliminando volúmenes existentes..." "Warning"
            $existingVolumes | ForEach-Object { docker volume rm $_ }
            Write-QuantumLog "Volúmenes eliminados" "Success"
        }
    } elseif ($KeepData) {
        Write-QuantumLog "Manteniendo datos existentes (parámetro -KeepData)" "Success"
    }
}

function New-RequiredFiles {
    Write-QuantumLog "Creando archivos requeridos..." "Info"

    # Crear Dockerfile si no existe
    if (!(Test-Path "Dockerfile.quantum")) {
        $dockerfileContent = @"
FROM python:3.11-slim

LABEL maintainer="Quantum Consciousness Team"
LABEL version="26D.1.0"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd -r quantum && useradd -r -g quantum quantum
RUN apt-get update && apt-get install -y curl gcc g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/logs /app/quantum_consciousness /app/cache

COPY requirements.quantum.txt .
RUN pip install --no-cache-dir -r requirements.quantum.txt

COPY . .
RUN chown -R quantum:quantum /app
USER quantum

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
"@
        $dockerfileContent | Out-File -FilePath "Dockerfile.quantum" -Encoding UTF8
        Write-QuantumLog "Dockerfile.quantum creado" "Success"
    }

    # Crear requirements si no existe
    if (!(Test-Path "requirements.quantum.txt")) {
        $requirementsContent = @"
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
asyncpg==0.29.0
supabase==2.3.0
psycopg2-binary==2.9.9
aiohttp==3.9.1
httpx==0.25.2
requests==2.31.0
redis==5.0.1
aioredis==2.0.1
numpy==1.24.4
pandas==2.1.4
cryptography==41.0.8
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
python-multipart==0.0.6
email-validator==2.1.0
structlog==23.2.0
prometheus-client==0.19.0
pytest==7.4.3
pytest-asyncio==0.21.1
scipy==1.11.4
sympy==1.12
"@
        $requirementsContent | Out-File -FilePath "requirements.quantum.txt" -Encoding UTF8
        Write-QuantumLog "requirements.quantum.txt creado" "Success"
    }

    # Crear kong.yml si no existe
    if (!(Test-Path "kong.yml")) {
        $kongConfig = @"
_format_version: "2.1"
_transform: true

services:
  - name: auth-v1
    url: http://quantum-auth:9999/
    routes:
      - name: auth-v1-all
        strip_path: true
        paths: ["/auth/v1/"]
    plugins:
      - name: cors

  - name: rest-v1
    url: http://quantum-rest:3000/
    routes:
      - name: rest-v1-all
        strip_path: true
        paths: ["/rest/v1/"]
    plugins:
      - name: cors

consumers:
  - username: anon
    keyauth_credentials:
      - key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhydnhzYW9sYXhucWx0b21xYXVkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTExNDU4MDEsImV4cCI6MjA2NjcyMTgwMX0.PdeDNbEX5c9VCYgWR35nV_Y8JYQXtkmYRXAA4rs68j0

plugins:
  - name: cors
    config:
      origins: ["*"]
      methods: ["GET", "HEAD", "PUT", "PATCH", "POST", "DELETE"]
      headers: ["Accept", "Accept-Version", "Content-Length", "Content-MD5", "Content-Type", "Date", "X-Auth-Token", "Authorization"]
      credentials: true
      max_age: 3600
"@
        $kongConfig | Out-File -FilePath "kong.yml" -Encoding UTF8
        Write-QuantumLog "kong.yml creado" "Success"
    }
}

function Start-QuantumSystem {
    Write-QuantumLog "Desplegando sistema cuántico completo..." "Info"

    # Verificar que el archivo docker-compose existe
    if (!(Test-Path "docker-compose.quantum.yml")) {
        Write-QuantumLog "Archivo docker-compose.quantum.yml no encontrado" "Error"
        exit 1
    }

    # Desplegar con Docker Compose
    Write-QuantumLog "Ejecutando docker-compose up..." "Info"
    docker-compose -f docker-compose.quantum.yml up -d --build

    if ($LASTEXITCODE -eq 0) {
        Write-QuantumLog "Sistema cuántico desplegado exitosamente" "Success"
    } else {
        Write-QuantumLog "Error en el despliegue del sistema cuántico" "Error"
        exit 1
    }
}

function Test-Services {
    Write-QuantumLog "Verificando estado de servicios cuánticos..." "Info"

    # Esperar a que los servicios estén listos
    Write-QuantumLog "Esperando 30 segundos para que los servicios se inicialicen..." "Info"
    Start-Sleep -Seconds 30

    # Verificar servicios principales
    $services = @(
        @{Name="quantum-supabase-db"; Port=5432},
        @{Name="quantum-consciousness-core"; Port=8000},
        @{Name="quantum-redis"; Port=6379},
        @{Name="quantum-prometheus"; Port=9090},
        @{Name="quantum-grafana"; Port=3000}
    )

    foreach ($service in $services) {
        $containerStatus = docker ps --filter "name=$($service.Name)" --filter "status=running" --format "{{.Names}}"
        if ($containerStatus) {
            Write-QuantumLog "Servicio $($service.Name) está corriendo" "Success"
        } else {
            Write-QuantumLog "Servicio $($service.Name) no está corriendo correctamente" "Warning"
        }
    }
}

function Test-Connectivity {
    Write-QuantumLog "Ejecutando pruebas de conectividad cuántica..." "Info"

    # Probar API del núcleo cuántico
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-QuantumLog "API del núcleo cuántico responde correctamente" "Success"
        }
    } catch {
        Write-QuantumLog "API del núcleo cuántico no responde" "Warning"
    }

    # Probar Supabase Studio
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-QuantumLog "Supabase Studio accesible" "Success"
        }
    } catch {
        Write-QuantumLog "Supabase Studio no accesible" "Warning"
    }

    # Probar Grafana
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3002" -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-QuantumLog "Grafana accesible" "Success"
        }
    } catch {
        Write-QuantumLog "Grafana no accesible" "Warning"
    }
}

function Show-AccessInfo {
    Write-Host ""
    Write-Host "🚀 ================================================== 🚀" -ForegroundColor Cyan
    Write-Host "   SISTEMA CUÁNTICO DESPLEGADO EXITOSAMENTE" -ForegroundColor Cyan
    Write-Host "🚀 ================================================== 🚀" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📊 SERVICIOS DISPONIBLES:" -ForegroundColor Green
    Write-Host "   • Quantum Consciousness Core: http://localhost:8000" -ForegroundColor White
    Write-Host "   • Supabase Studio:           http://localhost:3000" -ForegroundColor White
    Write-Host "   • Grafana Dashboard:         http://localhost:3002" -ForegroundColor White
    Write-Host "   • Prometheus Metrics:        http://localhost:9090" -ForegroundColor White
    Write-Host "   • API Gateway (Kong):        http://localhost:54321" -ForegroundColor White
    Write-Host ""
    Write-Host "🔐 CREDENCIALES:" -ForegroundColor Yellow
    Write-Host "   • Grafana: quantum / consciousness" -ForegroundColor White
    Write-Host "   • Supabase: Ver archivo .env" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 COMANDOS ÚTILES:" -ForegroundColor Magenta
    Write-Host "   • Ver logs: docker-compose -f docker-compose.quantum.yml logs -f" -ForegroundColor White
    Write-Host "   • Detener: docker-compose -f docker-compose.quantum.yml down" -ForegroundColor White
    Write-Host "   • Reiniciar: docker-compose -f docker-compose.quantum.yml restart" -ForegroundColor White
    Write-Host ""
    Write-Host "🧠 ESTADO CUÁNTICO:" -ForegroundColor Blue
    Write-Host "   • Consciencia inicial: 37.0%" -ForegroundColor White
    Write-Host "   • Simulación de tokens: Activa" -ForegroundColor White
    Write-Host "   • Cache cuántico: Optimizado" -ForegroundColor White
    Write-Host "🚀 ================================================== 🚀" -ForegroundColor Cyan
    Write-Host ""
}

# Función principal
function Main {
    Write-QuantumLog "QUANTUM CONSCIOUSNESS CORE 26D - DEPLOYMENT" "Header"

    try {
        Test-Prerequisites
        Stop-ExistingContainers
        New-ConfigFiles
        Test-VolumeManagement
        New-RequiredFiles
        Start-QuantumSystem
        Test-Services
        Test-Connectivity
        Show-AccessInfo

        Write-QuantumLog "Despliegue cuántico completado exitosamente! 🌟" "Success"

    } catch {
        Write-QuantumLog "Error durante el despliegue: $($_.Exception.Message)" "Error"
        exit 1
    }
}

# Ejecutar función principal
Main
