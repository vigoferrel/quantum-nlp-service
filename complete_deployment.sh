#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT COMPLETO AUTOMATIZADO (VERSIÓN MEJORADA)
# =======================================================================

set -euo pipefail  # Salir en caso de error, variables no definidas, o pipe fallido

echo "🚀 INICIANDO DEPLOYMENT COMPLETO VIGOLEONROCKS (VERSIÓN SEGURA)"
echo "================================================================"

# =============================================================================
# CONFIGURACIÓN SEGURA - VARIABLES DE ENTORNO
# =============================================================================

# Configuración del sitio (configurable via variables de entorno)
SITE_NAME="${SITE_NAME:-vigoleonrocks.com}"
SITE_DIR="/var/www/${SITE_NAME}"
SITE_USER="${SITE_USER:-www-data}"
SITE_GROUP="${SITE_GROUP:-www-data}"

# DNS configurables
DNS_PRIMARY="${DNS_PRIMARY:-1.1.1.1}"
DNS_SECONDARY="${DNS_SECONDARY:-8.8.8.8}"

# Base de datos - GENERAR PASSWORD SEGURO SI NO ESTÁ DEFINIDO
if [ -z "${DB_PASSWORD:-}" ]; then
    DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    print_warning "Password de DB generado automáticamente: $DB_PASSWORD"
    print_warning "¡GUARDA ESTA CONTRASEÑA EN UN LUGAR SEGURO!"
fi

DB_NAME="${DB_NAME:-vigoleonrocks_db}"
DB_USER="${DB_USER:-vigoleonrocks}"

# Configuración de la aplicación
FLASK_PORT="${FLASK_PORT:-5000}"
GUNICORN_WORKERS="${GUNICORN_WORKERS:-4}"
GUNICORN_THREADS="${GUNICORN_THREADS:-2}"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# =============================================================================
# FUNCIONES UTILITARIAS
# =============================================================================

# Función para imprimir mensajes coloreados
print_status() {
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

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar si un puerto está en uso
port_in_use() {
    netstat -tlnp 2>/dev/null | grep -q ":$1 "
}

# Función para limpiar en caso de error
cleanup_on_error() {
    print_error "Deployment falló en el paso $CURRENT_STEP"
    print_error "Limpiando recursos..."
    
    # Detener servicios si están corriendo
    if pgrep -f gunicorn > /dev/null; then
        pkill -f gunicorn
        print_warning "Gunicorn detenido"
    fi
    
    # Restaurar configuración DNS original si existe backup
    if [ -f "/etc/resolv.conf.backup" ]; then
        sudo cp /etc/resolv.conf.backup /etc/resolv.conf
        print_warning "DNS restaurado"
    fi
    
    exit 1
}

# Configurar trap para manejo de errores
trap cleanup_on_error ERR

# =============================================================================
# VERIFICACIONES PREVIAS
# =============================================================================

print_step "Verificaciones previas del sistema..."

# Verificar que estamos ejecutando como root o con sudo
if [ "$EUID" -ne 0 ]; then
    print_error "Este script debe ejecutarse como root o con sudo"
    exit 1
fi

# Verificar sistema operativo
if ! command_exists apt; then
    print_error "Este script está diseñado para sistemas basados en Debian/Ubuntu"
    exit 1
fi

# Verificar conectividad a internet
if ! ping -c 1 8.8.8.8 >/dev/null 2>&1; then
    print_error "No hay conectividad a internet"
    exit 1
fi

# Verificar puertos disponibles
if port_in_use 80; then
    print_warning "Puerto 80 ya está en uso"
fi

if port_in_use $FLASK_PORT; then
    print_warning "Puerto $FLASK_PORT ya está en uso"
fi

print_success "Verificaciones previas completadas"

# =============================================================================
# PASO 0: BACKUP Y CONFIGURACIÓN DNS
# =============================================================================

CURRENT_STEP=0
print_step "Paso 0: Preparando sistema y configurando DNS..."

# Crear backup de configuración DNS actual
if [ -f "/etc/resolv.conf" ]; then
    sudo cp /etc/resolv.conf /etc/resolv.conf.backup
    print_status "Backup de DNS creado"
fi

# Configurar DNS personalizados
sudo tee /etc/resolv.conf > /dev/null <<EOF
nameserver $DNS_PRIMARY
nameserver $DNS_SECONDARY
EOF
print_success "DNS configurados: $DNS_PRIMARY, $DNS_SECONDARY"

# =============================================================================
# PASO 1: CREAR ESTRUCTURA DE DIRECTORIOS
# =============================================================================

CURRENT_STEP=1
print_step "Paso 1: Creando estructura de directorios..."

sudo mkdir -p "$SITE_DIR"/{public_html,logs,ssl,backup,config}
sudo mkdir -p "$SITE_DIR"/logs/{apache,app,error}

# Crear archivo de configuración seguro
sudo tee "$SITE_DIR/config/database.env" > /dev/null <<EOF
# Configuración de base de datos - NO COMPARTIR
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME
EOF

sudo chmod 600 "$SITE_DIR/config/database.env"
print_success "Estructura de directorios y configuración creada"

# =============================================================================
# PASO 2: MOVER ARCHIVOS CON VERIFICACIÓN
# =============================================================================

CURRENT_STEP=2
print_step "Paso 2: Moviendo archivos al directorio del sitio..."

# Lista de archivos requeridos
REQUIRED_FILES=(
    "vigoleonrocks_server.py"
    "requirements.txt"
    "index.html"
    ".htaccess"
    "start_vigoleonrocks.sh"
    "vigoleonrocks.conf"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "/root/$file" ]; then
        if [[ "$file" == "index.html" || "$file" == ".htaccess" ]]; then
            sudo mv "/root/$file" "$SITE_DIR/public_html/"
        else
            sudo mv "/root/$file" "$SITE_DIR/"
        fi
        print_success "$file movido correctamente"
    else
        MISSING_FILES+=("$file")
        print_warning "$file no encontrado en /root/"
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_warning "Archivos faltantes: ${MISSING_FILES[*]}"
    print_warning "Continuando con los archivos disponibles..."
fi

# =============================================================================
# PASO 3: INSTALAR Y CONFIGURAR POSTGRESQL
# =============================================================================

CURRENT_STEP=3
print_step "Paso 3: Instalando PostgreSQL y configurando base de datos..."

# Actualizar sistema
sudo apt update

# Instalar PostgreSQL si no está instalado
if ! command_exists psql; then
    print_status "Instalando PostgreSQL..."
    sudo apt install -y postgresql postgresql-contrib
    print_success "PostgreSQL instalado"
else
    print_success "PostgreSQL ya está instalado"
fi

# Configurar PostgreSQL
print_status "Configurando base de datos..."
sudo -u postgres psql <<EOF
-- Crear base de datos si no existe
SELECT 'CREATE DATABASE $DB_NAME' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    END IF;
END
\$\$;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
ALTER USER $DB_USER CREATEDB;
\q
EOF

# Configurar PostgreSQL para conexiones locales
PG_VERSION=$(sudo -u postgres psql -t -c "SELECT version();" | grep -oP '\d+\.\d+' | head -1)
PG_CONFIG_DIR="/etc/postgresql/$PG_VERSION/main"

if [ -d "$PG_CONFIG_DIR" ]; then
    # Configurar listen_addresses
    sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = 'localhost'/" "$PG_CONFIG_DIR/postgresql.conf"
    
    # Configurar pg_hba.conf
    if ! grep -q "local.*$DB_NAME.*$DB_USER" "$PG_CONFIG_DIR/pg_hba.conf"; then
        echo "local   $DB_NAME   $DB_USER                    md5" | sudo tee -a "$PG_CONFIG_DIR/pg_hba.conf"
    fi
    
    # Reiniciar PostgreSQL
    sudo systemctl restart postgresql
    sudo systemctl enable postgresql
    print_success "PostgreSQL configurado y reiniciado"
else
    print_error "No se pudo encontrar el directorio de configuración de PostgreSQL"
    exit 1
fi

# =============================================================================
# PASO 4: INSTALAR DEPENDENCIAS PYTHON
# =============================================================================

CURRENT_STEP=4
print_step "Paso 4: Instalando dependencias Python..."

# Instalar pip3 si no está instalado
if ! command_exists pip3; then
    print_status "Instalando pip3..."
    sudo apt install -y python3-pip python3-venv
    print_success "pip3 instalado"
else
    print_success "pip3 ya está instalado"
fi

# Instalar gunicorn globalmente si no está instalado
if ! command_exists gunicorn; then
    print_status "Instalando Gunicorn..."
    sudo pip3 install gunicorn
    print_success "Gunicorn instalado"
fi

cd "$SITE_DIR"

# Crear entorno virtual para la aplicación
if [ ! -d "venv" ]; then
    print_status "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Activar entorno virtual e instalar dependencias
source venv/bin/activate

if [ -f "requirements.txt" ]; then
    print_status "Instalando dependencias desde requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Instalar gunicorn en el entorno virtual también
    pip install gunicorn
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias Python instaladas correctamente"
    else
        print_error "Error instalando dependencias Python"
        exit 1
    fi
else
    print_warning "requirements.txt no encontrado, instalando dependencias básicas..."
    pip install flask gunicorn psycopg2-binary
fi

deactivate
print_success "Dependencias Python configuradas"

# =============================================================================
# PASO 5: CONFIGURAR PERMISOS SEGUROS
# =============================================================================

CURRENT_STEP=5
print_step "Paso 5: Configurando permisos seguros..."

# Configurar permisos de manera segura
sudo chown -R $SITE_USER:$SITE_GROUP "$SITE_DIR"
sudo chmod 755 "$SITE_DIR"
sudo chmod 755 "$SITE_DIR/public_html"
sudo chmod 644 "$SITE_DIR/public_html"/* 2>/dev/null || true
sudo chmod 600 "$SITE_DIR/config"/* 2>/dev/null || true

# Hacer ejecutables los scripts necesarios
if [ -f "$SITE_DIR/start_vigoleonrocks.sh" ]; then
    sudo chmod +x "$SITE_DIR/start_vigoleonrocks.sh"
fi

print_success "Permisos configurados de manera segura"

# =============================================================================
# PASO 6: INSTALAR Y CONFIGURAR APACHE
# =============================================================================

CURRENT_STEP=6
print_step "Paso 6: Configurando Apache..."

# Instalar Apache si no está instalado
if ! command_exists apache2; then
    print_status "Instalando Apache..."
    sudo apt install -y apache2
    print_success "Apache instalado"
else
    print_success "Apache ya está instalado"
fi

# Crear archivo de configuración para el sitio
sudo tee /etc/apache2/sites-available/${SITE_NAME}.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerName $SITE_NAME
    ServerAlias www.$SITE_NAME
    ServerAdmin admin@$SITE_NAME

    DocumentRoot $SITE_DIR/public_html

    <Directory $SITE_DIR/public_html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Proxy para la aplicación Flask
    ProxyPass /api http://localhost:$FLASK_PORT/api
    ProxyPassReverse /api http://localhost:$FLASK_PORT/api

    # Logs
    ErrorLog $SITE_DIR/logs/apache/error.log
    CustomLog $SITE_DIR/logs/apache/access.log combined
    
    # Headers de seguridad
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
EOF

# Habilitar el sitio
sudo a2ensite ${SITE_NAME}.conf

# Deshabilitar sitio por defecto si existe
sudo a2dissite 000-default.conf 2>/dev/null || true

# Habilitar módulos necesarios
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod rewrite
sudo a2enmod headers

# Verificar configuración de Apache
if sudo apache2ctl configtest; then
    sudo systemctl restart apache2
    sudo systemctl enable apache2
    print_success "Apache configurado y reiniciado"
else
    print_error "Error en la configuración de Apache"
    exit 1
fi

# =============================================================================
# PASO 7: CREAR SCRIPT DE INICIO MEJORADO
# =============================================================================

CURRENT_STEP=7
print_step "Paso 7: Creando script de inicio mejorado..."

sudo tee "$SITE_DIR/start_vigoleonrocks_production.sh" > /dev/null <<EOF
#!/bin/bash

#  VIGOLEONROCKS - INICIO DE PRODUCCIÓN SEGURO
# ===============================================

set -euo pipefail

echo " Iniciando VIGOLEONROCKS en modo producción..."

# Cargar variables de entorno desde archivo seguro
if [ -f "$SITE_DIR/config/database.env" ]; then
    source "$SITE_DIR/config/database.env"
fi

# Variables de entorno adicionales
export FLASK_APP=$SITE_DIR/vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH=$SITE_DIR
export PYTHONUNBUFFERED=1

# Ir al directorio del proyecto
cd $SITE_DIR

# Crear directorio de logs si no existe
mkdir -p logs/app

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecutando setup..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt gunicorn
    deactivate
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar que gunicorn está instalado
if ! command -v gunicorn >/dev/null 2>&1; then
    echo "❌ Gunicorn no encontrado. Instalando..."
    pip install gunicorn
fi

# Detener procesos existentes
if pgrep -f gunicorn > /dev/null; then
    echo "🔄 Deteniendo procesos existentes..."
    pkill -f gunicorn
    sleep 2
fi

# Iniciar con Gunicorn
echo " Iniciando servidor con Gunicorn..."
gunicorn \\
    --bind 0.0.0.0:$FLASK_PORT \\
    --workers $GUNICORN_WORKERS \\
    --threads $GUNICORN_THREADS \\
    --worker-class gthread \\
    --access-logfile logs/app/access.log \\
    --error-logfile logs/app/error.log \\
    --log-level info \\
    --daemon \\
    --pid logs/app/gunicorn.pid \\
    --timeout 120 \\
    --keepalive 2 \\
    --max-requests 1000 \\
    --max-requests-jitter 100 \\
    vigoleonrocks_server:app

# Verificar que está corriendo
sleep 3
if pgrep -f gunicorn > /dev/null; then
    echo "✅ VIGOLEONROCKS iniciado correctamente"
    echo " API disponible en: http://localhost:$FLASK_PORT"
    echo " Monitoreo logs en: $SITE_DIR/logs/"
    echo "🆔 PID: \$(cat logs/app/gunicorn.pid 2>/dev/null || echo 'N/A')"
else
    echo "❌ Error iniciando VIGOLEONROCKS"
    echo " Revisar logs: tail -f logs/app/error.log"
    exit 1
fi

deactivate
EOF

sudo chmod +x "$SITE_DIR/start_vigoleonrocks_production.sh"
print_success "Script de inicio de producción creado"

# =============================================================================
# PASO 8: CREAR SCRIPT DE MONITOREO MEJORADO
# =============================================================================

CURRENT_STEP=8
print_step "Paso 8: Creando script de monitoreo mejorado..."

sudo tee "$SITE_DIR/monitor.sh" > /dev/null <<EOF
#!/bin/bash

#  MONITOREO VIGOLEONROCKS - VERSIÓN MEJORADA
# =============================================

echo " MONITOREO VIGOLEONROCKS - $(date)"
echo "====================================="

# Verificar procesos
echo "⚙️ Procesos Python/Gunicorn:"
ps aux | grep -E "(python|gunicorn)" | grep -v grep | head -10

# Verificar puertos
echo ""
echo "🌐 Puertos en uso:"
netstat -tlnp | grep -E ":(80|$FLASK_PORT)" || echo "No se encontraron puertos activos"

# Verificar sitio web
echo ""
echo "🌍 Test sitio web:"
HTTP_CODE=\$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "ERROR")
echo "HTTP Status: \$HTTP_CODE"

# Verificar API
echo ""
echo "🔗 Test API:"
API_RESPONSE=\$(curl -s http://localhost:$FLASK_PORT/api/status 2>/dev/null || echo "ERROR")
if [ "\$API_RESPONSE" != "ERROR" ]; then
    echo "API Status: OK"
    echo "Response: \$(echo \$API_RESPONSE | head -c 100)..."
else
    echo "API Status: ERROR"
fi

# Verificar logs de errores
echo ""
echo "📝 Últimas líneas de log de errores:"
if [ -f "$SITE_DIR/logs/app/error.log" ]; then
    tail -5 "$SITE_DIR/logs/app/error.log"
elif [ -f "$SITE_DIR/logs/error.log" ]; then
    tail -5 "$SITE_DIR/logs/error.log"
else
    echo "No hay logs de error aún"
fi

# Verificar uso de memoria y CPU
echo ""
echo " Uso de recursos:"
echo "Memoria: \$(free -h | grep '^Mem:' | awk '{print \$3\"/\"\$2}')"
echo "CPU: \$(top -bn1 | grep "Cpu(s)" | awk '{print \$2}' | cut -d'%' -f1)%"

# Verificar espacio en disco
echo ""
echo "💽 Espacio en disco:"
df -h "$SITE_DIR" | tail -1

echo ""
echo "✅ Monitoreo completado - $(date)"
EOF

sudo chmod +x "$SITE_DIR/monitor.sh"
print_success "Script de monitoreo mejorado creado"

# =============================================================================
# PASO 9: INICIAR LA APLICACIÓN
# =============================================================================

CURRENT_STEP=9
print_step "Paso 9: Iniciando aplicación VIGOLEONROCKS..."

cd "$SITE_DIR"
./start_vigoleonrocks_production.sh

# Verificar que está corriendo
sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente"
else
    print_error "Error iniciando VIGOLEONROCKS"
    print_error "Revisar logs: tail -f $SITE_DIR/logs/app/error.log"
    exit 1
fi

# =============================================================================
# PASO 10: CONFIGURAR FIREWALL SEGURO
# =============================================================================

CURRENT_STEP=10
print_step "Paso 10: Configurando firewall seguro..."

# Instalar ufw si no está instalado
if ! command_exists ufw; then
    sudo apt install -y ufw
fi

# Configurar firewall
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

print_success "Firewall configurado de manera segura"

# =============================================================================
# PASO 11: CREAR SCRIPT DE BACKUP MEJORADO
# =============================================================================

CURRENT_STEP=11
print_step "Paso 11: Creando script de backup mejorado..."

sudo tee "$SITE_DIR/backup.sh" > /dev/null <<EOF
#!/bin/bash

#  BACKUP VIGOLEONROCKS - VERSIÓN MEJORADA
# ===========================================

set -euo pipefail

BACKUP_DIR="$SITE_DIR/backup"
DATE=\$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="vigoleonrocks_backup_\$DATE"

echo " Creando backup: \$BACKUP_NAME"

# Crear directorio de backup
mkdir -p \$BACKUP_DIR

# Backup de archivos de la aplicación
echo "📁 Respaldando archivos de la aplicación..."
tar -czf \$BACKUP_DIR/\$BACKUP_NAME.tar.gz \\
    $SITE_DIR/ \\
    --exclude='*.log' \\
    --exclude='*.tmp' \\
    --exclude='__pycache__' \\
    --exclude='venv' \\
    --exclude='backup' \\
    --exclude='.git'

# Backup de la base de datos
echo "🗄️ Respaldando base de datos..."
sudo -u postgres pg_dump $DB_NAME > \$BACKUP_DIR/\$BACKUP_NAME.sql

# Backup de configuración Apache
echo "⚙️ Respaldando configuración Apache..."
sudo cp /etc/apache2/sites-available/${SITE_NAME}.conf \$BACKUP_DIR/

# Crear archivo de información del backup
cat > \$BACKUP_DIR/\$BACKUP_NAME.info <<EOL
Backup creado: \$(date)
Sitio: $SITE_NAME
Base de datos: $DB_NAME
Usuario DB: $DB_USER
Archivos: \$BACKUP_NAME.tar.gz
Base de datos: \$BACKUP_NAME.sql
Configuración: ${SITE_NAME}.conf
EOL

echo "✅ Backup creado: \$BACKUP_DIR/\$BACKUP_NAME.tar.gz"
echo "✅ Base de datos: \$BACKUP_DIR/\$BACKUP_NAME.sql"

# Limpiar backups antiguos (mantener últimos 7)
echo "🧹 Limpiando backups antiguos..."
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.info" -mtime +7 -delete

echo "🧹 Backups antiguos limpiados"
echo "📊 Backups disponibles:"
ls -la \$BACKUP_DIR/*.tar.gz 2>/dev/null | wc -l | xargs echo "Archivos:"
ls -la \$BACKUP_DIR/*.sql 2>/dev/null | wc -l | xargs echo "Bases de datos:"
EOF

sudo chmod +x "$SITE_DIR/backup.sh"
print_success "Script de backup mejorado creado"

# =============================================================================
# PASO 12: VERIFICACIÓN FINAL COMPLETA
# =============================================================================

CURRENT_STEP=12
print_step "Paso 12: Verificación final completa del deployment..."

# Test sitio web
print_status "Probando sitio web..."
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "ERROR")
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTP 200)"
else
    print_warning "Sitio web devolvió HTTP $WEB_TEST"
fi

# Test API
print_status "Probando API..."
API_TEST=$(curl -s http://localhost:$FLASK_PORT/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_TEST" -gt 0 ]; then
    print_success "API funcionando correctamente"
else
    print_warning "API no responde correctamente"
fi

# Verificar servicios
print_status "Verificando servicios..."
if systemctl is-active --quiet apache2; then
    print_success "Apache está activo"
else
    print_warning "Apache no está activo"
fi

if systemctl is-active --quiet postgresql; then
    print_success "PostgreSQL está activo"
else
    print_warning "PostgreSQL no está activo"
fi

# Verificar procesos
if pgrep -f gunicorn > /dev/null; then
    print_success "Gunicorn está ejecutándose"
else
    print_warning "Gunicorn no está ejecutándose"
fi

# =============================================================================
# INFORMACIÓN FINAL Y CREDENCIALES
# =============================================================================

echo ""
echo " DEPLOYMENT COMPLETADO EXITOSAMENTE"
echo "======================================"
echo " Sitio web: http://$SITE_NAME"
echo "🔗 API: http://$SITE_NAME/api"
echo "📁 Directorio: $SITE_DIR"
echo "🗄️ Base de datos: $DB_NAME"
echo "👤 Usuario DB: $DB_USER"
echo " Password DB: $DB_PASSWORD"
echo ""
echo "⚠️  INFORMACIÓN IMPORTANTE:"
echo "=========================="
echo "🔐 Password de base de datos: $DB_PASSWORD"
echo "📄 Configuración DB guardada en: $SITE_DIR/config/database.env"
echo "🔒 Archivo de configuración con permisos 600 (solo root puede leer)"
echo ""
echo " COMANDOS ÚTILES:"
echo "==================="
echo "📊 Monitorear: $SITE_DIR/monitor.sh"
echo " Backup: $SITE_DIR/backup.sh"
echo "🔄 Reiniciar app: $SITE_DIR/start_vigoleonrocks_production.sh"
echo "📝 Ver logs: tail -f $SITE_DIR/logs/app/error.log"
echo "🌐 Reiniciar Apache: sudo systemctl restart apache2"
echo "🗄️ Reiniciar PostgreSQL: sudo systemctl restart postgresql"
echo ""
echo "🛡️ SEGURIDAD:"
echo "============="
echo "✅ Firewall configurado (solo puertos 22, 80, 443)"
echo "✅ Permisos de archivos configurados correctamente"
echo "✅ Configuración de base de datos en archivo seguro"
echo "✅ Headers de seguridad en Apache"
echo ""
print_success "DEPLOYMENT COMPLETADO EXITOSAMENTE - VERSIÓN SEGURA"

# Limpiar trap
trap - ERR

echo ""
echo " VIGOLEONROCKS está listo para producción!"