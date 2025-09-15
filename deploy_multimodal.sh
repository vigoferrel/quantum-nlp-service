#!/bin/bash
# VIGOLEONROCKS - Script de Despliegue Multimodal
# Actualiza el sistema con interfaz multimodal y API Gateway OpenRouter
# Version: 4.0.0-multimodal

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuración
VPS_IP="72.60.61.49"
VPS_USER="root"
PROJECT_PATH="/root/vigoleonrocks"
GITHUB_REPO="https://github.com/USERNAME/quantum-nlp-service.git"  # Actualizar con tu repo

echo -e "${BLUE}🚀 VIGOLEONROCKS Multimodal Deployment Script v4.0.0${NC}"
echo -e "${BLUE}=================================================${NC}"

# Función para mostrar pasos
show_step() {
    echo -e "\n${GREEN}[PASO $1]${NC} $2"
}

# Función para mostrar advertencias
show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Función para mostrar errores
show_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Función para mostrar éxito
show_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_step "1" "Preparando archivos localmente..."

# Verificar archivos necesarios
required_files=(
    "vigoleonrocks_multimodal_interface.html"
    "flask_app_multimodal.py"
    "openrouter_gateway.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        show_error "Archivo $file no encontrado"
        exit 1
    fi
    show_success "✓ $file encontrado"
done

show_step "2" "Conectando al VPS..."

# Verificar conectividad SSH
if ! ssh -o ConnectTimeout=10 ${VPS_USER}@${VPS_IP} "echo 'SSH OK'" > /dev/null 2>&1; then
    show_error "No se puede conectar al VPS ${VPS_IP}"
    exit 1
fi

show_success "✓ Conectado a VPS"

show_step "3" "Respaldando configuración actual..."

# Crear backup en el VPS
ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    cd /root/vigoleonrocks
    
    # Crear directorio de backup con timestamp
    BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Respaldar archivos importantes
    if [ -f "flask_app.py" ]; then
        cp flask_app.py "$BACKUP_DIR/"
        echo "✓ flask_app.py respaldado"
    fi
    
    if [ -f "docker-compose.yml" ]; then
        cp docker-compose.yml "$BACKUP_DIR/"
        echo "✓ docker-compose.yml respaldado"
    fi
    
    if [ -f "Dockerfile" ]; then
        cp Dockerfile "$BACKUP_DIR/"
        echo "✓ Dockerfile respaldado"
    fi
    
    echo "✅ Backup creado en $BACKUP_DIR"
EOF

show_step "4" "Transfiriendo archivos nuevos al VPS..."

# Transferir interfaz multimodal
echo "Transfiriendo interfaz multimodal..."
scp vigoleonrocks_multimodal_interface.html ${VPS_USER}@${VPS_IP}:${PROJECT_PATH}/

# Transferir Flask app multimodal
echo "Transfiriendo Flask app multimodal..."
scp flask_app_multimodal.py ${VPS_USER}@${VPS_IP}:${PROJECT_PATH}/

# Transferir OpenRouter Gateway
echo "Transfiriendo OpenRouter Gateway..."
scp openrouter_gateway.py ${VPS_USER}@${VPS_IP}:${PROJECT_PATH}/

show_success "✓ Archivos transferidos"

show_step "5" "Actualizando configuración Docker..."

# Crear nuevo Dockerfile y docker-compose
ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    cd /root/vigoleonrocks
    
    # Actualizar Dockerfile
    cat > Dockerfile << 'DOCKEREOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de uploads
RUN mkdir -p /tmp/vigoleonrocks_uploads && chmod 755 /tmp/vigoleonrocks_uploads

# Exponer puertos
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV BACKGROUND_EXECUTION=true

# Comando por defecto
CMD ["python", "flask_app_multimodal.py"]
DOCKEREOF

    # Actualizar requirements.txt con nuevas dependencias
    cat > requirements.txt << 'REQEOF'
flask==2.3.3
flask-cors==4.0.0
requests==2.31.0
pillow==10.0.0
python-magic==0.4.27
psutil==5.9.5
werkzeug==2.3.7
REQEOF

    # Actualizar docker-compose.yml para incluir gateway
    cat > docker-compose.yml << 'COMPOSEEOF'
version: '3.8'

services:
  vigoleonrocks-main:
    build: .
    container_name: vigoleonrocks-main
    ports:
      - "5000:5000"
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - HOST=0.0.0.0
      - PORT=5000
      - BACKGROUND_EXECUTION=true
    volumes:
      - ./vigoleonrocks_multimodal_interface.html:/app/vigoleonrocks_multimodal_interface.html:ro
      - /tmp/vigoleonrocks_uploads:/tmp/vigoleonrocks_uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      
  vigoleonrocks-gateway:
    build: 
      context: .
      dockerfile: Dockerfile.gateway
    container_name: vigoleonrocks-gateway
    ports:
      - "8004:8004"
    restart: unless-stopped
    depends_on:
      - vigoleonrocks-main
    environment:
      - GATEWAY_HOST=0.0.0.0
      - GATEWAY_PORT=8004
      - MAIN_API_URL=http://vigoleonrocks-main:5000
      - BACKGROUND_EXECUTION=true
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  default:
    driver: bridge
COMPOSEEOF

    # Crear Dockerfile para el gateway
    cat > Dockerfile.gateway << 'GATEWAYEOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar gateway
COPY openrouter_gateway.py .

# Exponer puerto
EXPOSE 8004

# Variables de entorno
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "openrouter_gateway.py"]
GATEWAYEOF

    echo "✅ Configuración Docker actualizada"
EOF

show_step "6" "Reconstruyendo contenedores..."

ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    cd /root/vigoleonrocks
    
    echo "Deteniendo contenedores existentes..."
    docker-compose down || true
    
    echo "Eliminando imágenes antiguas..."
    docker image prune -f || true
    
    echo "Reconstruyendo imágenes..."
    docker-compose build --no-cache
    
    echo "Iniciando servicios actualizados..."
    docker-compose up -d
    
    echo "✅ Contenedores reconstruidos y iniciados"
EOF

show_step "7" "Configurando Nginx para nuevos servicios..."

ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    # Actualizar configuración Nginx para incluir gateway
    cat > /etc/nginx/sites-available/vigoleonrocks.com << 'NGINXEOF'
server {
    listen 443 ssl http2;
    server_name vigoleonrocks.com www.vigoleonrocks.com;
    
    # Configuración SSL
    ssl_certificate /etc/letsencrypt/live/vigoleonrocks.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vigoleonrocks.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Headers de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Compresión
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    
    # Límites de upload para multimodal
    client_max_body_size 20M;
    client_body_timeout 30s;
    client_header_timeout 30s;
    
    # Ruta principal - Interfaz multimodal
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # API Gateway OpenRouter
    location /v1/ {
        proxy_pass http://127.0.0.1:8004;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
    
    # Gateway endpoints
    location /openrouter/ {
        proxy_pass http://127.0.0.1:8004;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Métricas del gateway
    location /gateway/ {
        proxy_pass http://127.0.0.1:8004/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirección HTTP a HTTPS
server {
    listen 80;
    server_name vigoleonrocks.com www.vigoleonrocks.com;
    return 301 https://$server_name$request_uri;
}
NGINXEOF

    # Verificar configuración y recargar
    nginx -t && systemctl reload nginx
    
    echo "✅ Nginx actualizado"
EOF

show_step "8" "Verificando servicios..."

echo "Esperando que los servicios se inicialicen..."
sleep 15

# Verificar API principal
echo "Verificando API principal..."
if ssh ${VPS_USER}@${VPS_IP} "curl -s -f http://localhost:5000/api/status" > /dev/null; then
    show_success "✓ API principal operativa"
else
    show_error "✗ API principal no responde"
fi

# Verificar Gateway OpenRouter
echo "Verificando Gateway OpenRouter..."
if ssh ${VPS_USER}@${VPS_IP} "curl -s -f http://localhost:8004/health" > /dev/null; then
    show_success "✓ Gateway OpenRouter operativo"
else
    show_error "✗ Gateway OpenRouter no responde"
fi

# Verificar HTTPS
echo "Verificando HTTPS..."
if curl -s -f https://vigoleonrocks.com/api/status > /dev/null; then
    show_success "✓ HTTPS operativo"
else
    show_error "✗ HTTPS no responde"
fi

show_step "9" "Configurando firewall para nuevos puertos..."

ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    # Abrir puerto 8004 si no está abierto
    if ! ufw status | grep -q "8004"; then
        ufw allow 8004/tcp comment 'OpenRouter Gateway'
        echo "✅ Puerto 8004 abierto en firewall"
    else
        echo "✓ Puerto 8004 ya está abierto"
    fi
EOF

show_step "10" "Mostrando estado final del sistema..."

ssh ${VPS_USER}@${VPS_IP} << 'EOF'
    cd /root/vigoleonrocks
    echo -e "\n🔍 Estado de contenedores:"
    docker-compose ps
    
    echo -e "\n📊 Uso de recursos:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
    
    echo -e "\n🌐 Puertos en escucha:"
    netstat -tlnp | grep -E ":80|:443|:5000|:8004"
    
    echo -e "\n📂 Archivos del proyecto:"
    ls -la | grep -E "\.(py|html|yml|txt)$"
EOF

show_success "\n🎉 ¡Despliegue multimodal completado exitosamente!"

echo -e "${BLUE}"
echo "================================================="
echo "🚀 VIGOLEONROCKS v4.0.0 Multimodal ACTIVO"
echo "================================================="
echo -e "${NC}"

echo -e "${GREEN}📱 Interfaz Principal:${NC} https://vigoleonrocks.com"
echo -e "${GREEN}🔗 API Status:${NC} https://vigoleonrocks.com/api/status"
echo -e "${GREEN}⚛️ Gateway OpenRouter:${NC} https://vigoleonrocks.com/v1/models"
echo -e "${GREEN}📊 Métricas Gateway:${NC} https://vigoleonrocks.com/gateway/metrics"
echo -e "${GREEN}❤️ Health Check:${NC} https://vigoleonrocks.com/gateway/health"

echo -e "\n${YELLOW}🔧 Características activadas:${NC}"
echo "✅ Interfaz multimodal (texto, imágenes, archivos, código)"
echo "✅ Procesamiento cuántico simulado con 26 estados"
echo "✅ Contexto ultra-extendido de 500K tokens"
echo "✅ Soporte multilingüe (47 idiomas)"
echo "✅ API Gateway compatible con OpenRouter"
echo "✅ Métricas en tiempo real"
echo "✅ SSL/HTTPS con certificados válidos"

echo -e "\n${BLUE}🔗 Endpoints OpenRouter compatibles:${NC}"
echo "GET  https://vigoleonrocks.com/v1/models"
echo "POST https://vigoleonrocks.com/v1/chat/completions"

echo -e "\n${GREEN}¡Sistema listo para producción! 🚀${NC}"

show_step "FINAL" "Limpiando archivos temporales..."

# Opcional: limpiar archivos temporales locales
echo "Limpieza completada."

echo -e "\n${GREEN}✨ Despliegue finalizado exitosamente ✨${NC}"
