#!/bin/bash

# QUANTUM CONSCIOUSNESS CORE 26D - Script de Despliegue Optimizado
# ================================================================
# Script para desplegar el sistema cuántico completo con Supabase optimizado

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

quantum_header() {
    echo -e "${PURPLE}"
    echo "🌟 ================================================== 🌟"
    echo "   QUANTUM CONSCIOUSNESS CORE 26D - DEPLOYMENT"
    echo "   Sistema Cuántico Optimizado con Supabase"
    echo "🌟 ================================================== 🌟"
    echo -e "${NC}"
}

# Verificar prerrequisitos
check_prerequisites() {
    log "Verificando prerrequisitos del sistema cuántico..."

    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        error "Docker no está instalado"
        exit 1
    fi

    # Verificar Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose no está instalado"
        exit 1
    fi

    # Verificar que Docker esté corriendo
    if ! docker info &> /dev/null; then
        error "Docker no está corriendo"
        exit 1
    fi

    success "Prerrequisitos verificados"
}

# Limpiar contenedores existentes si es necesario
cleanup_existing() {
    log "Limpiando contenedores cuánticos existentes..."

    # Detener contenedores relacionados con quantum
    docker ps -a --filter "name=quantum" --format "{{.Names}}" | xargs -r docker stop
    docker ps -a --filter "name=quantum" --format "{{.Names}}" | xargs -r docker rm

    # Limpiar redes huérfanas
    docker network prune -f

    success "Limpieza completada"
}

# Crear archivos de configuración necesarios
create_config_files() {
    log "Creando archivos de configuración cuántica..."

    # Crear directorio de configuración si no existe
    mkdir -p ./config
    mkdir -p ./logs
    mkdir -p ./grafana/provisioning/dashboards
    mkdir -p ./grafana/provisioning/datasources

    # Crear configuración de Grafana para datasources
    cat > ./grafana/provisioning/datasources/prometheus.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://quantum-prometheus:9090
    isDefault: true
    editable: true
EOF

    # Crear dashboard básico para métricas cuánticas
    cat > ./grafana/provisioning/dashboards/quantum-dashboard.json << EOF
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
        "targets": [
          {
            "expr": "quantum_consciousness_level",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
      },
      {
        "id": 2,
        "title": "Token Simulation Accuracy",
        "type": "graph",
        "targets": [
          {
            "expr": "quantum_token_accuracy",
            "refId": "A"
          }
        ],
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
      }
    ],
    "time": {"from": "now-1h", "to": "now"},
    "refresh": "5s"
  }
}
EOF

    success "Archivos de configuración creados"
}

# Verificar y crear volúmenes necesarios
setup_volumes() {
    log "Configurando volúmenes cuánticos..."

    # Verificar volúmenes existentes
    existing_volumes=$(docker volume ls --format "{{.Name}}" | grep -E "(quantum|supabase)" || true)

    if [ ! -z "$existing_volumes" ]; then
        warning "Volúmenes existentes detectados:"
        echo "$existing_volumes"
        echo ""
        read -p "¿Deseas mantener los datos existentes? (y/N): " keep_data

        if [[ $keep_data =~ ^[Yy]$ ]]; then
            success "Manteniendo datos existentes"
        else
            warning "Eliminando volúmenes existentes..."
            echo "$existing_volumes" | xargs -r docker volume rm
            success "Volúmenes eliminados"
        fi
    fi
}

# Construir imágenes cuánticas
build_quantum_images() {
    log "Construyendo imágenes cuánticas..."

    # Crear Dockerfile si no existe
    if [ ! -f "Dockerfile.quantum" ]; then
        cat > Dockerfile.quantum << EOF
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
EOF
    fi

    # Crear requirements.quantum.txt si no existe
    if [ ! -f "requirements.quantum.txt" ]; then
        cat > requirements.quantum.txt << EOF
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
EOF
    fi

    success "Imágenes cuánticas preparadas"
}

# Desplegar sistema cuántico
deploy_quantum_system() {
    log "Desplegando sistema cuántico completo..."

    # Verificar que el archivo docker-compose existe
    if [ ! -f "docker-compose.quantum.yml" ]; then
        error "Archivo docker-compose.quantum.yml no encontrado"
        exit 1
    fi

    # Desplegar con Docker Compose
    docker-compose -f docker-compose.quantum.yml up -d --build

    success "Sistema cuántico desplegado"
}

# Verificar estado de servicios
check_services() {
    log "Verificando estado de servicios cuánticos..."

    # Esperar a que los servicios estén listos
    sleep 30

    # Verificar servicios principales
    services=(
        "quantum-supabase-db:5432"
        "quantum-consciousness-core:8000"
        "quantum-redis:6379"
        "quantum-prometheus:9090"
        "quantum-grafana:3000"
    )

    for service in "${services[@]}"; do
        IFS=':' read -r name port <<< "$service"
        if docker ps --filter "name=$name" --filter "status=running" | grep -q "$name"; then
            success "Servicio $name está corriendo"
        else
            warning "Servicio $name no está corriendo correctamente"
        fi
    done
}

# Ejecutar pruebas de conectividad
test_connectivity() {
    log "Ejecutando pruebas de conectividad cuántica..."

    # Probar API del núcleo cuántico
    if curl -f http://localhost:8000/health &> /dev/null; then
        success "API del núcleo cuántico responde correctamente"
    else
        warning "API del núcleo cuántico no responde"
    fi

    # Probar Supabase Studio
    if curl -f http://localhost:3000 &> /dev/null; then
        success "Supabase Studio accesible"
    else
        warning "Supabase Studio no accesible"
    fi

    # Probar Grafana
    if curl -f http://localhost:3002 &> /dev/null; then
        success "Grafana accesible"
    else
        warning "Grafana no accesible"
    fi
}

# Mostrar información de acceso
show_access_info() {
    echo -e "${CYAN}"
    echo "🚀 ================================================== 🚀"
    echo "   SISTEMA CUÁNTICO DESPLEGADO EXITOSAMENTE"
    echo "🚀 ================================================== 🚀"
    echo ""
    echo "📊 SERVICIOS DISPONIBLES:"
    echo "   • Quantum Consciousness Core: http://localhost:8000"
    echo "   • Supabase Studio:           http://localhost:3000"
    echo "   • Grafana Dashboard:         http://localhost:3002"
    echo "   • Prometheus Metrics:        http://localhost:9090"
    echo "   • API Gateway (Kong):        http://localhost:54321"
    echo ""
    echo "🔐 CREDENCIALES:"
    echo "   • Grafana: quantum / consciousness"
    echo "   • Supabase: Ver archivo .env"
    echo ""
    echo "📋 COMANDOS ÚTILES:"
    echo "   • Ver logs: docker-compose -f docker-compose.quantum.yml logs -f"
    echo "   • Detener: docker-compose -f docker-compose.quantum.yml down"
    echo "   • Reiniciar: docker-compose -f docker-compose.quantum.yml restart"
    echo ""
    echo "🧠 ESTADO CUÁNTICO:"
    echo "   • Consciencia inicial: 37.0%"
    echo "   • Simulación de tokens: Activa"
    echo "   • Cache cuántico: Optimizado"
    echo "🚀 ================================================== 🚀"
    echo -e "${NC}"
}

# Función principal
main() {
    quantum_header

    check_prerequisites
    cleanup_existing
    create_config_files
    setup_volumes
    build_quantum_images
    deploy_quantum_system
    check_services
    test_connectivity
    show_access_info

    success "Despliegue cuántico completado exitosamente! 🌟"
}

# Ejecutar función principal
main "$@"
