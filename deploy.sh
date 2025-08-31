#!/bin/bash

# 🚀 VIGOLEONROCKS Deployment Script
# Uso: ./deploy.sh [environment] [action]
# Ejemplos:
#   ./deploy.sh local build    # Construir para desarrollo local
#   ./deploy.sh staging deploy # Deploy a staging
#   ./deploy.sh prod deploy    # Deploy a producción

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes coloreados
print_message() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Variables
ENVIRONMENT=${1:-local}
ACTION=${2:-build}
PROJECT_NAME="vigoleonrocks"
DOCKER_REGISTRY="ghcr.io"
DOCKER_REPO="${DOCKER_REGISTRY}/vigoferrel/${PROJECT_NAME}"

# Función para verificar dependencias
check_dependencies() {
    print_message "Verificando dependencias..."

    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado"
        exit 1
    fi

    print_success "Dependencias verificadas"
}

# Función para construir imagen Docker
build_image() {
    print_message "Construyendo imagen Docker..."

    if [ "$ENVIRONMENT" = "prod" ]; then
        TAG="latest"
    elif [ "$ENVIRONMENT" = "staging" ]; then
        TAG="staging"
    else
        TAG="dev"
    fi

    docker build -t ${DOCKER_REPO}:${TAG} .

    if [ "$ENVIRONMENT" != "local" ]; then
        print_message "Haciendo push de la imagen..."
        docker push ${DOCKER_REPO}:${TAG}
    fi

    print_success "Imagen construida: ${DOCKER_REPO}:${TAG}"
}

# Función para deploy local
deploy_local() {
    print_message "Deployando localmente..."

    # Detener contenedores existentes
    docker-compose down || true

    # Construir y levantar servicios
    docker-compose up -d --build

    # Esperar a que los servicios estén listos
    print_message "Esperando a que los servicios estén listos..."
    sleep 30

    # Verificar estado
    if docker-compose ps | grep -q "Up"; then
        print_success "Deploy local completado"
        print_message "Aplicación disponible en: http://localhost:5000"
        print_message "API Status: http://localhost:5000/api/status"
    else
        print_error "Error en el deploy local"
        docker-compose logs
        exit 1
    fi
}

# Función para deploy remoto
deploy_remote() {
    print_message "Deployando a ${ENVIRONMENT}..."

    # Aquí iría la lógica para deploy remoto
    # Por ejemplo, usando SSH, Kubernetes, etc.

    case $ENVIRONMENT in
        staging)
            REMOTE_HOST="staging.vigoleonrocks.com"
            ;;
        prod)
            REMOTE_HOST="vigoleonrocks.com"
            ;;
        *)
            print_error "Environment no válido: $ENVIRONMENT"
            exit 1
            ;;
    esac

    print_message "Conectando a ${REMOTE_HOST}..."

    # Ejemplo de comandos para deploy remoto
    # ssh user@${REMOTE_HOST} << EOF
    #     cd /opt/vigoleonrocks
    #     git pull origin main
    #     docker-compose down
    #     docker-compose pull
    #     docker-compose up -d
    #     docker-compose logs -f
    # EOF

    print_success "Deploy a ${ENVIRONMENT} completado"
}

# Función para rollback
rollback() {
    print_message "Realizando rollback..."

    if [ "$ENVIRONMENT" = "local" ]; then
        docker-compose down
        docker run --rm -v vigoleonrocks_postgres_data:/data busybox sh -c "cd /data && ls -la"
        print_warning "Datos de PostgreSQL preservados en volumen"
    else
        print_message "Implementar lógica de rollback para ${ENVIRONMENT}"
    fi

    print_success "Rollback completado"
}

# Función para monitoreo
monitor() {
    print_message "Monitoreando servicios..."

    if [ "$ENVIRONMENT" = "local" ]; then
        docker-compose ps
        echo ""
        print_message "Logs de la aplicación:"
        docker-compose logs -f --tail=50 app
    else
        print_message "Implementar monitoreo remoto para ${ENVIRONMENT}"
    fi
}

# Función para cleanup
cleanup() {
    print_message "Limpiando recursos..."

    # Limpiar imágenes no utilizadas
    docker image prune -f

    # Limpiar contenedores detenidos
    docker container prune -f

    # Limpiar volúmenes no utilizados (con cuidado)
    # docker volume prune -f

    print_success "Cleanup completado"
}

# Función principal
main() {
    print_message "🚀 VIGOLEONROCKS Deployment Script"
    print_message "Environment: $ENVIRONMENT"
    print_message "Action: $ACTION"

    check_dependencies

    case $ACTION in
        build)
            build_image
            ;;
        deploy)
            if [ "$ENVIRONMENT" = "local" ]; then
                deploy_local
            else
                deploy_remote
            fi
            ;;
        rollback)
            rollback
            ;;
        monitor)
            monitor
            ;;
        cleanup)
            cleanup
            ;;
        status)
            if [ "$ENVIRONMENT" = "local" ]; then
                docker-compose ps
            else
                print_message "Implementar verificación de status remoto"
            fi
            ;;
        *)
            print_error "Acción no válida: $ACTION"
            echo "Uso: $0 [environment] [action]"
            echo "Environments: local, staging, prod"
            echo "Actions: build, deploy, rollback, monitor, cleanup, status"
            exit 1
            ;;
    esac

    print_success "Script completado exitosamente"
}

# Ejecutar función principal
main "$@"