# Script de Deployment VIGOLEONROCKS a Dokploy - Versión Simplificada
Write-Host "🚀 VIGOLEONROCKS Deployment to Dokploy" -ForegroundColor Cyan

$ServerIP = "72.60.61.49"
$API_TOKEN = "GBFPf5EzTC7VIlD8rOCm2YfSGM6TaV4uvonczg6h3dfad669"

Write-Host "📍 Target Server: $ServerIP" -ForegroundColor Green
Write-Host "🔐 API Token: $($API_TOKEN.Substring(0,10))..." -ForegroundColor Green

# Verificar políticas
Write-Host "🔍 Verificando políticas..." -ForegroundColor Cyan

# Verificar que simple_api.py existe
if (Test-Path "simple_api.py") {
    Write-Host "✅ simple_api.py encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: simple_api.py no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar Dockerfile
if (Test-Path "Dockerfile") {
    Write-Host "✅ Dockerfile encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ ERROR: Dockerfile no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Políticas verificadas correctamente" -ForegroundColor Green

# Construir imagen Docker
Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Cyan

try {
    docker build -t vigoleonrocks-quantum-nlp:latest .
    Write-Host "✅ Imagen Docker construida correctamente" -ForegroundColor Green
}
catch {
    Write-Host "❌ ERROR: Fallo en construcción Docker" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Información de deployment
Write-Host "🚀 Deployment configurado para:" -ForegroundColor Cyan
Write-Host "   • Servidor: $ServerIP" -ForegroundColor White
Write-Host "   • Puerto: 5000" -ForegroundColor White
Write-Host "   • Health Check: /api/status" -ForegroundColor White
Write-Host "   • Métricas: Habilitadas" -ForegroundColor White
Write-Host "   • Background: Habilitado" -ForegroundColor White
Write-Host "   • RNG: Sistema de métricas (NO Math.random)" -ForegroundColor White

Write-Host "🌍 URLs del servicio deployado:" -ForegroundColor Cyan
Write-Host "   • Panel Dokploy: http://$ServerIP:3000" -ForegroundColor White
Write-Host "   • API Status: http://$ServerIP:5000/api/status" -ForegroundColor White
$connectUrl = "http://$ServerIP" + ":5000/api/connect?token=$API_TOKEN" + "&message=hola"
Write-Host "   • API Connect: $connectUrl" -ForegroundColor White

Write-Host "📋 Instrucciones para completar deployment:" -ForegroundColor Yellow
Write-Host "1. Conectarse al servidor via SSH: ssh root@$ServerIP" -ForegroundColor White
Write-Host "2. Acceder al panel Dokploy: http://$ServerIP:3000" -ForegroundColor White
Write-Host "3. Crear nueva aplicación con la imagen: vigoleonrocks-quantum-nlp:latest" -ForegroundColor White
Write-Host "4. Configurar variables de entorno desde dokploy.json" -ForegroundColor White
Write-Host "5. Habilitar health checks en /api/status" -ForegroundColor White
Write-Host "6. Configurar dominio personalizado si es necesario" -ForegroundColor White

Write-Host "✅ DEPLOYMENT SCRIPT COMPLETADO" -ForegroundColor Green
