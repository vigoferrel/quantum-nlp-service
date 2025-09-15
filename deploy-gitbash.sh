#!/bin/bash
# VIGOLEONROCKS - Deployment Script for Git Bash
# Optimizado para evitar problemas de buffer y conexión SSH

set -e  # Exit on any error

VPS_HOST="srv984842.hstgr.cloud"
VPS_USER="root"
PROJECT_DIR="/root/quantum-nlp-service"
GITHUB_REPO="https://github.com/vigoferrel/quantum-nlp-service.git"

echo "=== VIGOLEONROCKS Deployment via Git Bash ==="
echo "Target: $VPS_USER@$VPS_HOST"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Función para ejecutar comandos SSH con manejo de errores
ssh_exec() {
    local cmd="$1"
    echo "Executing: $cmd"
    ssh -o ConnectTimeout=30 -o ServerAliveInterval=60 "$VPS_USER@$VPS_HOST" "$cmd"
}

# Paso 1: Limpiar y preparar directorio
echo "Step 1: Cleaning remote directory..."
ssh_exec "rm -rf $PROJECT_DIR"
ssh_exec "mkdir -p $PROJECT_DIR"

# Paso 2: Clonar repositorio
echo "Step 2: Cloning repository..."
ssh_exec "cd /root && git clone $GITHUB_REPO"

# Paso 3: Crear directorios necesarios
echo "Step 3: Creating required directories..."
ssh_exec "mkdir -p $PROJECT_DIR/logs $PROJECT_DIR/metrics $PROJECT_DIR/data"

# Paso 4: Verificar Docker
echo "Step 4: Checking Docker installation..."
ssh_exec "which docker > /dev/null 2>&1 || (curl -fsSL https://get.docker.com | sh && systemctl start docker && systemctl enable docker)"

# Paso 5: Verificar Docker Compose
echo "Step 5: Checking Docker Compose..."
ssh_exec "which docker-compose > /dev/null 2>&1 || pip3 install docker-compose"

# Paso 6: Construir servicios
echo "Step 6: Building Docker services..."
ssh_exec "cd $PROJECT_DIR && docker-compose build --no-cache"

# Paso 7: Iniciar servicios en background
echo "Step 7: Starting services in background..."
ssh_exec "cd $PROJECT_DIR && docker-compose up -d"

# Paso 8: Verificar estado de servicios
echo "Step 8: Checking service status..."
ssh_exec "cd $PROJECT_DIR && docker-compose ps"

# Paso 9: Verificar conectividad
echo "Step 9: Testing connectivity..."
sleep 5
ssh_exec "curl -f http://localhost:8001/health || echo 'Health check pending...'"

echo ""
echo "=== Deployment Completed Successfully ==="
echo "Access your application at: http://$VPS_HOST:8001"
echo "Quantum Command Center: http://$VPS_HOST:8001/quantum"
echo ""
echo "To check logs: ssh $VPS_USER@$VPS_HOST 'cd $PROJECT_DIR && docker-compose logs -f'"
echo "To restart: ssh $VPS_USER@$VPS_HOST 'cd $PROJECT_DIR && docker-compose restart'"
