# VIGOLEONROCKS - Manual Deployment Steps
# Ejecutar paso a paso para evitar problemas de buffer

Write-Host "=== VIGOLEONROCKS Manual Deployment ===" -ForegroundColor Green

# Paso 1: Limpiar directorio remoto
Write-Host "Paso 1: Limpiando directorio remoto..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "rm -rf /root/quantum-nlp-service"

# Paso 2: Clonar repositorio
Write-Host "Paso 2: Clonando repositorio..." -ForegroundColor Yellow  
ssh root@srv984842.hstgr.cloud "git clone https://github.com/tu-usuario/quantum-nlp-service.git"

# Paso 3: Crear directorios necesarios
Write-Host "Paso 3: Creando directorios..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "mkdir -p /root/quantum-nlp-service/logs /root/quantum-nlp-service/metrics"

# Paso 4: Instalar Docker si no existe
Write-Host "Paso 4: Verificando Docker..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "which docker || curl -fsSL https://get.docker.com | sh"

# Paso 5: Instalar Docker Compose
Write-Host "Paso 5: Verificando Docker Compose..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "which docker-compose || pip3 install docker-compose"

# Paso 6: Navegar al directorio y construir
Write-Host "Paso 6: Construyendo servicios..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "cd /root/quantum-nlp-service && docker-compose build"

# Paso 7: Iniciar servicios
Write-Host "Paso 7: Iniciando servicios..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "cd /root/quantum-nlp-service && docker-compose up -d"

# Paso 8: Verificar estado
Write-Host "Paso 8: Verificando estado..." -ForegroundColor Yellow
ssh root@srv984842.hstgr.cloud "cd /root/quantum-nlp-service && docker-compose ps"

Write-Host "=== Deployment Manual Completado ===" -ForegroundColor Green
Write-Host "Accede a: http://srv984842.hstgr.cloud:8001" -ForegroundColor Cyan
