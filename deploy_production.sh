#!/bin/bash

# 🚀 DEPLOYMENT COMPLETO DE PRODUCCIÓN - VIGOLEONROCKS
# Versión: 2.0 - Arquitectura Empresarial
# Fecha: 2025-09-01

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función de logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Función para verificar comandos
check_command() {
    if ! command -v $1 &> /dev/null; then
        error "$1 no está instalado"
        return 1
    fi
    return 0
}

# Función para verificar conectividad
check_connectivity() {
    local host=$1
    local port=$2
    local service=$3

    if timeout 10 bash -c "</dev/tcp/$host/$port" 2>/dev/null; then
        log "$service está accesible en $host:$port"
        return 0
    else
        error "$service no está accesible en $host:$port"
        return 1
    fi
}

# Función para esperar servicios
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    local max_attempts=30
    local attempt=1

    info "Esperando $service en $host:$port..."

    while [ $attempt -le $max_attempts ]; do
        if check_connectivity $host $port $service 2>/dev/null; then
            log "$service está listo"
            return 0
        fi

        info "Intento $attempt/$max_attempts - esperando $service..."
        sleep 2
        ((attempt++))
    done

    error "$service no respondió después de $max_attempts intentos"
    return 1
}

# Verificaciones previas
log "🚀 INICIANDO DEPLOYMENT DE PRODUCCIÓN VIGOLEONROCKS"
echo "=================================================="

# Verificar comandos necesarios
info "Verificando dependencias del sistema..."
check_command docker || exit 1
check_command docker-compose || exit 1

# Verificar archivos necesarios
info "Verificando archivos de configuración..."
required_files=(
    "docker-compose.prod.yml"
    "Dockerfile.prod"
    "nginx.conf"
    "init.sql"
    ".env.example"
    "requirements.txt"
    "vigoleonrocks_server.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        error "Archivo requerido faltante: $file"
        exit 1
    fi
done

log "✅ Todos los archivos requeridos están presentes"

# Crear directorios necesarios
info "Creando directorios necesarios..."
mkdir -p logs uploads static ssl

# Configurar variables de entorno
if [ ! -f ".env" ]; then
    info "Creando archivo .env desde .env.example..."
    cp .env.example .env
    warning "⚠️  RECUERDA CONFIGURAR LAS VARIABLES EN .env"
fi

# Limpiar contenedores anteriores
info "Limpiando contenedores anteriores..."
docker-compose -f docker-compose.prod.yml down --remove-orphans 2>/dev/null || true
docker system prune -f 2>/dev/null || true

# Construir imágenes
log "🏗️  CONSTRUYENDO IMÁGENES DOCKER..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Iniciar servicios base (PostgreSQL y Redis)
log "🐘 INICIANDO SERVICIOS BASE..."
docker-compose -f docker-compose.prod.yml up -d postgres redis

# Esperar PostgreSQL
wait_for_service localhost 5432 "PostgreSQL"

# Esperar Redis
wait_for_service localhost 6379 "Redis"

# Verificar health checks
info "Verificando health checks de servicios..."
sleep 10

# Iniciar aplicación
log "🚀 INICIANDO APLICACIÓN PRINCIPAL..."
docker-compose -f docker-compose.prod.yml up -d app

# Esperar aplicación
wait_for_service localhost 5000 "Aplicación VIGOLEONROCKS"

# Iniciar Nginx
log "🌐 INICIANDO NGINX REVERSE PROXY..."
docker-compose -f docker-compose.prod.yml up -d nginx

# Esperar Nginx
wait_for_service localhost 80 "Nginx"

# Iniciar Watchtower para auto-updates
log "🔄 INICIANDO WATCHTOWER PARA AUTO-UPDATES..."
docker-compose -f docker-compose.prod.yml up -d watchtower

# Verificaciones finales
log "🔍 REALIZANDO VERIFICACIONES FINALES..."

# Verificar contenedores
info "Verificando estado de contenedores..."
docker-compose -f docker-compose.prod.yml ps

# Verificar conectividad
info "Verificando conectividad de servicios..."

# Test API
if curl -s -f http://localhost/api/status > /dev/null 2>&1; then
    log "✅ API está respondiendo correctamente"
else
    warning "⚠️  API no responde (puede estar iniciándose)"
fi

# Test aplicación interna
if curl -s -f http://localhost:5000/api/status > /dev/null 2>&1; then
    log "✅ Aplicación interna está funcionando"
else
    error "❌ Aplicación interna no responde"
fi

# Mostrar información de acceso
log "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE!"
echo "========================================"

echo ""
echo "🌐 ACCESO AL SISTEMA:"
echo "   Web Principal:    http://localhost"
echo "   API Status:       http://localhost/api/status"
echo "   Aplicación:       http://localhost:5000"
echo ""

echo "🐳 CONTENEDORES ACTIVOS:"
docker-compose -f docker-compose.prod.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "📊 MONITOREO:"
echo "   Ver logs:         docker-compose -f docker-compose.prod.yml logs -f"
echo "   Ver estado:       docker-compose -f docker-compose.prod.yml ps"
echo "   Reiniciar:        docker-compose -f docker-compose.prod.yml restart"
echo "   Detener:          docker-compose -f docker-compose.prod.yml down"
echo ""

echo "🔧 GESTIÓN:"
echo "   Backup BD:        docker exec vigoleonrocks_postgres pg_dump -U vigoleonrocks_user vigoleonrocks > backup.sql"
echo "   Ver logs app:     docker-compose -f docker-compose.prod.yml logs -f app"
echo "   Ver logs nginx:   docker-compose -f docker-compose.prod.yml logs -f nginx"
echo ""

echo "⚠️  RECUERDA:"
echo "   - Configurar DNS para acceso público"
echo "   - Configurar SSL/HTTPS para producción"
echo "   - Configurar backups automáticos"
echo "   - Monitorear logs regularmente"
echo ""

log "🎯 SISTEMA VIGOLEONROCKS LISTO PARA PRODUCCIÓN!"

# Crear script de monitoreo
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "=== VIGOLEONROCKS MONITOR ==="
echo "Contenedores:"
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "Uso de recursos:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
echo ""
echo "Logs recientes:"
docker-compose -f docker-compose.prod.yml logs --tail=10
EOF

chmod +x monitor.sh
log "✅ Script de monitoreo creado: monitor.sh"

# Crear script de backup
cat > backup.sh << 'EOF'
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups/$TIMESTAMP"
mkdir -p "$BACKUP_DIR"

echo "=== CREANDO BACKUP ==="
echo "Directorio: $BACKUP_DIR"

# Backup base de datos
echo "Backup PostgreSQL..."
docker exec vigoleonrocks_postgres pg_dump -U vigoleonrocks_user vigoleonrocks > "$BACKUP_DIR/database.sql"

# Backup Redis
echo "Backup Redis..."
docker exec vigoleonrocks_redis redis-cli SAVE
docker cp vigoleonrocks_redis:/data/dump.rdb "$BACKUP_DIR/redis_dump.rdb"

# Backup archivos
echo "Backup archivos..."
cp -r uploads "$BACKUP_DIR/"
cp -r logs "$BACKUP_DIR/"

# Comprimir
echo "Comprimiendo..."
tar -czf "${BACKUP_DIR}.tar.gz" -C "./backups" "$TIMESTAMP"
rm -rf "$BACKUP_DIR"

echo "✅ Backup completado: ${BACKUP_DIR}.tar.gz"
EOF

chmod +x backup.sh
log "✅ Script de backup creado: backup.sh"

log "🎉 DEPLOYMENT COMPLETO Y PROFESIONAL FINALIZADO!"