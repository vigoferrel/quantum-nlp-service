# deploy-vps-windows.ps1 - VIGOLEONROCKS Deployment para Windows
# Optimizado para evitar errores de buffer de PowerShell

Write-Host "🚀 VIGOLEONROCKS - Deployment desde Windows" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "Target: srv984842.hstgr.cloud" -ForegroundColor Yellow
Write-Host "Timestamp: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# Variables
$VPS_HOST = "srv984842.hstgr.cloud"
$VPS_USER = "root"
$PROJECT_DIR = "/opt/vigoleonrocks"

function Execute-SSHCommand {
    param(
        [string]$Command,
        [string]$Description,
        [bool]$SuppressOutput = $false
    )
    
    Write-Host "🔄 $Description..." -ForegroundColor Blue
    
    try {
        if ($SuppressOutput) {
            $result = ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "$Command" 2>$null
        } else {
            $result = ssh -o ConnectTimeout=30 -o StrictHostKeyChecking=no "$VPS_USER@$VPS_HOST" "$Command"
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $Description completado" -ForegroundColor Green
            return $true
        } else {
            Write-Host "❌ Error en: $Description" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Excepción en: $Description - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Paso 1: Verificar conexión SSH
Write-Host "📋 Paso 1: Verificando conexión SSH..." -ForegroundColor Cyan
if (-not (Execute-SSHCommand "echo 'Conexión SSH exitosa'" "Verificar SSH" $true)) {
    Write-Host "❌ No se puede conectar al VPS. Verifica tu configuración SSH." -ForegroundColor Red
    Write-Host "Ejecuta: ssh-copy-id -p 22 $VPS_USER@$VPS_HOST" -ForegroundColor Yellow
    exit 1
}

# Paso 2: Preparar directorio (comando simple)
Write-Host "`n📋 Paso 2: Preparando directorio del proyecto..." -ForegroundColor Cyan
Execute-SSHCommand "rm -rf $PROJECT_DIR" "Limpiar directorio anterior" $true
Execute-SSHCommand "mkdir -p $PROJECT_DIR" "Crear directorio proyecto" $true

# Paso 3: Clonar repositorio
Write-Host "`n📋 Paso 3: Clonando repositorio..." -ForegroundColor Cyan
Execute-SSHCommand "cd /opt && git clone https://github.com/vigoferrel/quantum-nlp-service.git vigoleonrocks" "Clonar repositorio"

# Paso 4: Crear directorios de logs (comando dividido)
Write-Host "`n📋 Paso 4: Configurando directorios del sistema..." -ForegroundColor Cyan
Execute-SSHCommand "mkdir -p /var/log/vigoleonrocks/quantum" "Crear logs quantum" $true
Execute-SSHCommand "mkdir -p /var/log/vigoleonrocks/gateway" "Crear logs gateway" $true  
Execute-SSHCommand "mkdir -p /var/metrics/vigoleonrocks" "Crear directorio métricas" $true
Execute-SSHCommand "chmod -R 755 /var/log/vigoleonrocks /var/metrics/vigoleonrocks" "Configurar permisos" $true

# Paso 5: Verificar Docker (comando simple)
Write-Host "`n📋 Paso 5: Verificando Docker..." -ForegroundColor Cyan
Execute-SSHCommand "docker --version" "Verificar Docker"

# Paso 6: Crear docker-compose sin salida larga
Write-Host "`n📋 Paso 6: Creando configuración Docker..." -ForegroundColor Cyan
$dockerComposeContent = @"
cd $PROJECT_DIR && cat > docker-compose.prod.yml << 'DOCKER_EOF'
version: '3.8'
services:
  quantum-processor:
    build:
      context: .
      dockerfile: Dockerfile.quantum
    container_name: vigoleonrocks-quantum
    environment:
      - FLASK_ENV=production
      - PORT=5000
      - HOST=0.0.0.0
      - BACKGROUND_EXECUTION=true
      - METRICS_RNG_ENABLED=true
    ports:
      - "5000:5000"
    volumes:
      - /var/log/vigoleonrocks/quantum:/app/logs
      - /var/metrics/vigoleonrocks:/app/metrics
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - vigoleonrocks-network

  api-gateway:
    build:
      context: .
      dockerfile: Dockerfile.gateway
    container_name: vigoleonrocks-gateway
    environment:
      - NODE_ENV=production
      - GATEWAY_PORT=8004
      - VIGOLEONROCKS_BACKEND=http://quantum-processor:5000
    ports:
      - "8004:8004"
    volumes:
      - /var/log/vigoleonrocks/gateway:/app/logs
    depends_on:
      quantum-processor:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    restart: unless-stopped
    networks:
      - vigoleonrocks-network

networks:
  vigoleonrocks-network:
    driver: bridge
DOCKER_EOF
"@

Execute-SSHCommand $dockerComposeContent "Crear docker-compose.prod.yml" $true

# Paso 7: Limpiar Docker de forma segura (sin verbose output)
Write-Host "`n📋 Paso 7: Limpiando Docker..." -ForegroundColor Cyan
Execute-SSHCommand "cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml down" "Detener servicios previos" $true
Execute-SSHCommand "docker container prune -f" "Limpiar contenedores" $true
Execute-SSHCommand "docker image prune -f" "Limpiar imágenes" $true

# Paso 8: Build y deployment (en pasos separados)
Write-Host "`n📋 Paso 8: Ejecutando deployment..." -ForegroundColor Cyan
Write-Host "⚠️  Este paso puede tomar varios minutos..." -ForegroundColor Yellow

# Build en background
Execute-SSHCommand "cd $PROJECT_DIR && nohup docker-compose -f docker-compose.prod.yml build > /tmp/docker-build.log 2>&1 &" "Iniciando build" $true

# Esperar un poco para el build
Write-Host "⏳ Esperando build de imágenes..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Verificar que el build terminó y luego iniciar
Execute-SSHCommand "cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml up -d" "Iniciar servicios" $true

# Paso 9: Esperar y verificar servicios
Write-Host "`n📋 Paso 9: Verificando deployment..." -ForegroundColor Cyan
Write-Host "⏳ Esperando que los servicios inicien..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar servicios individualmente
$quantumStatus = Execute-SSHCommand "curl -f -s http://localhost:5000/api/status" "Test Quantum Processor" $true
if ($quantumStatus) {
    Write-Host "✅ Quantum Processor: ONLINE (http://$VPS_HOST:5000)" -ForegroundColor Green
} else {
    Write-Host "❌ Quantum Processor: OFFLINE" -ForegroundColor Red
}

$gatewayStatus = Execute-SSHCommand "curl -f -s http://localhost:8004/health" "Test API Gateway" $true
if ($gatewayStatus) {
    Write-Host "✅ API Gateway: ONLINE (http://$VPS_HOST:8004)" -ForegroundColor Green
} else {
    Write-Host "❌ API Gateway: OFFLINE" -ForegroundColor Red
}

# Mostrar estado de contenedores
Write-Host "`n📊 Estado de contenedores:" -ForegroundColor Cyan
Execute-SSHCommand "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" "Estado contenedores"

Write-Host "`n🎉 DEPLOYMENT COMPLETADO!" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green
Write-Host "📋 URLS DE ACCESO:" -ForegroundColor Yellow
Write-Host "✅ Quantum Processor: http://$VPS_HOST:5000/api/status" -ForegroundColor White
Write-Host "✅ API Gateway: http://$VPS_HOST:8004/health" -ForegroundColor White
Write-Host ""
Write-Host "📊 MONITOREO:" -ForegroundColor Yellow  
Write-Host "• Logs: /var/log/vigoleonrocks/" -ForegroundColor White
Write-Host "• Métricas: /var/metrics/vigoleonrocks/" -ForegroundColor White
Write-Host ""
Write-Host "🔧 COMANDOS DE MANTENIMIENTO:" -ForegroundColor Yellow
Write-Host "• Ver logs: ssh $VPS_USER@$VPS_HOST 'tail -f /var/log/vigoleonrocks/monitor.log'" -ForegroundColor White
Write-Host "• Estado: ssh $VPS_USER@$VPS_HOST 'docker ps'" -ForegroundColor White
Write-Host "• Reiniciar: ssh $VPS_USER@$VPS_HOST 'cd $PROJECT_DIR && docker-compose -f docker-compose.prod.yml restart'" -ForegroundColor White

Write-Host "`n✅ Sistema listo para integración OpenRouter!" -ForegroundColor Green
