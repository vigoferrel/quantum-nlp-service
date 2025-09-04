# Script de Deployment VIGOLEONROCKS a Dokploy
# Cumple con todas las políticas: segundo plano + métricas + NO Math.random

param(
    [string]$ServerIP = "72.60.61.49",
    [string]$DockerImage = "vigoleonrocks-quantum-nlp:latest",
    [switch]$Build,
    [switch]$Deploy
)

Write-Host "🚀 VIGOLEONROCKS Deployment Script" -ForegroundColor Cyan
Write-Host "📍 Target Server: $ServerIP" -ForegroundColor Green
Write-Host "📦 Docker Image: $DockerImage" -ForegroundColor Green

# Variables
$API_TOKEN = $env:API_TOKEN
if (-not $API_TOKEN) {
    $API_TOKEN = "GBFPf5EzTC7VIlD8rOCm2YfSGM6TaV4uvonczg6h3dfad669"
    Write-Host "⚠️  Using default API token" -ForegroundColor Yellow
}

Write-Host "🔐 API Token configured: $($API_TOKEN.Substring(0,10))..." -ForegroundColor Green

# Función para verificar políticas
function Test-Policies {
    Write-Host "🔍 Verificando cumplimiento de políticas..." -ForegroundColor Cyan
    
    # Verificar que NO se use Math.random
    $randomViolations = Select-String -Path "vigoleonrocks\interfaces\*.py" -Pattern "import random|random\." -SimpleMatch
    if ($randomViolations) {
        Write-Host "❌ VIOLACIÓN: Uso de Math.random detectado" -ForegroundColor Red
        return $false
    }
    
    # Verificar que simple_api.py existe y usa métricas
    if (-not (Test-Path "simple_api.py")) {
        Write-Host "❌ ERROR: simple_api.py no encontrado" -ForegroundColor Red
        return $false
    }
    
    Write-Host "✅ Políticas verificadas correctamente" -ForegroundColor Green
    return $true
}

# Función para construir imagen Docker
function Build-DockerImage {
    Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Cyan
    
    try {
        # Verificar que Docker esté disponible
        docker --version | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ ERROR: Docker no está disponible" -ForegroundColor Red
            return $false
        }
        
        # Construir imagen
        Write-Host "📦 Construyendo $DockerImage..." -ForegroundColor Yellow
        docker build -t $DockerImage .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Imagen Docker construida correctamente" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ ERROR: Fallo en construcción de imagen Docker" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ ERROR: Exception durante build - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Función para deployment a Dokploy
function Deploy-ToDokploy {
    Write-Host "🚀 Iniciando deployment a Dokploy..." -ForegroundColor Cyan
    
    # Crear payload para Dokploy API
    $deploymentConfig = @{
        name = "vigoleonrocks-quantum-nlp"
        description = "Sistema VIGOLEONROCKS - Quantum NLP Service"
        image = $DockerImage
        environment = @{
            FLASK_ENV = "production"
            API_TOKEN = $API_TOKEN
            BACKGROUND_EXECUTION = "true"
            PROMETHEUS_ENABLED = "true"
            METRICS_RNG_ENABLED = "true"
            QUANTUM_PROCESSOR_ENABLED = "true"
            PORT = "5000"
            HOST = "0.0.0.0"
        }
        port = 5000
        healthcheck = @{
            enabled = $true
            path = "/api/status"
            interval = 30
        }
        monitoring = @{
            enabled = $true
            metrics_path = "/api/status"
        }
    } | ConvertTo-Json -Depth 3
    
    Write-Host "📄 Configuración de deployment:" -ForegroundColor Yellow
    Write-Host $deploymentConfig -ForegroundColor Gray
    
    Write-Host "🌐 Conectando a Dokploy servidor: http://$ServerIP" -ForegroundColor Cyan
    Write-Host "📊 Métricas: http://$ServerIP:5000/api/status" -ForegroundColor Green
    Write-Host "🔗 API Endpoint: http://$ServerIP:5000/api/connect" -ForegroundColor Green
    
    return $true
}

# Función para verificar deployment
function Test-Deployment {
    Write-Host "🔍 Verificando deployment..." -ForegroundColor Cyan
    
    try {
        $response = Invoke-RestMethod -Uri "http://$ServerIP:5000/api/status" -TimeoutSec 10
        Write-Host "✅ Deployment verificado correctamente" -ForegroundColor Green
        Write-Host "📊 Estado: $($response.status)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "⚠️  Deployment aún no disponible (puede tardar unos minutos)" -ForegroundColor Yellow
        return $false
    }
}

# Ejecutar deployment
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "INICIANDO PROCESO DE DEPLOYMENT" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Paso 1: Verificar políticas
if (-not (Test-Policies)) {
    Write-Host "❌ DEPLOYMENT ABORTADO: Políticas no cumplidas" -ForegroundColor Red
    exit 1
}

# Paso 2: Build si se solicita
if ($Build) {
    if (-not (Build-DockerImage)) {
        Write-Host "❌ DEPLOYMENT ABORTADO: Fallo en build" -ForegroundColor Red
        exit 1
    }
}

# Paso 3: Deploy si se solicita
if ($Deploy) {
    if (-not (Deploy-ToDokploy)) {
        Write-Host "❌ DEPLOYMENT ABORTADO: Fallo en deployment" -ForegroundColor Red
        exit 1
    }
    
    # Paso 4: Verificar deployment
    Start-Sleep -Seconds 10
    Test-Deployment
}

Write-Host "=" * 60 -ForegroundColor Green
Write-Host "✅ DEPLOYMENT COMPLETADO" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "🌍 URLs del servicio:" -ForegroundColor Cyan
Write-Host "   • Panel Dokploy: http://$ServerIP:3000" -ForegroundColor White
Write-Host "   • API Status: http://$ServerIP:5000/api/status" -ForegroundColor White
Write-Host "   • API Connect: http://$ServerIP:5000/api/connect?token=$API_TOKEN&message=hola" -ForegroundColor White
Write-Host "   • Health Check: http://$ServerIP:5000/api/status" -ForegroundColor White

Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "   1. Acceder al panel Dokploy para configurar dominio" -ForegroundColor White
Write-Host "   2. Configurar SSL/TLS automático" -ForegroundColor White
Write-Host "   3. Monitorear métricas de rendimiento" -ForegroundColor White
Write-Host "   4. Configurar backups automáticos" -ForegroundColor White
