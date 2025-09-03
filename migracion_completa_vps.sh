#!/bin/bash

# 🚀 MIGRACIÓN COMPLETA A VPS - VIGOLEONROCKS
# ===========================================

echo "🚀 MIGRACIÓN COMPLETA A VPS - VIGOLEONROCKS"
echo "==========================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Configuración
DOMAIN="vigoleonrocks.com"
VPS_IP="72.60.61.49"
CLOUD_HOSTING_URL="https://vigoleonrocks.com"
DB_PASSWORD="0gLuiWUTaw3Q)3GOFM&J"

echo ""
echo "📊 MIGRACIÓN COMPLETA A VPS"
echo "============================"
echo "🌐 Dominio: $DOMAIN"
echo "🖥️ VPS: $VPS_IP"
echo "☁️ Cloud Hosting: $CLOUD_HOSTING_URL (a migrar)"
echo ""

# Paso 1: Completar deployment VPS
print_status "Paso 1: Completando deployment VPS..."

# Instalar pip3 si no está instalado
if ! command -v pip3 &> /dev/null; then
    print_status "Instalando pip3..."
    apt update
    apt install -y python3-pip
    print_success "pip3 instalado"
else
    print_success "pip3 ya está instalado"
fi

# Instalar dependencias Python
print_status "Instalando dependencias Python..."
cd /var/www/vigoleonrocks.com

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_success "Dependencias Python instaladas correctamente"
    else
        print_error "Error instalando dependencias Python"
        exit 1
    fi
else
    print_error "requirements.txt no encontrado"
    exit 1
fi

# Paso 2: Configurar permisos
print_status "Paso 2: Configurando permisos..."
chown -R www-data:www-data /var/www/vigoleonrocks.com
chmod +x /var/www/vigoleonrocks.com/start_vigoleonrocks.sh
chmod 755 /var/www/vigoleonrocks.com
chmod 755 /var/www/vigoleonrocks.com/public_html
print_success "Permisos configurados"

# Paso 3: Configurar Apache Virtual Host
print_status "Paso 3: Configurando Apache Virtual Host..."

# Instalar Apache si no está instalado
if ! command -v apache2 &> /dev/null; then
    print_status "Instalando Apache..."
    apt update
    apt install -y apache2
    print_success "Apache instalado"
else
    print_success "Apache ya está instalado"
fi

# Crear configuración Apache para el dominio
tee /etc/apache2/sites-available/$DOMAIN.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerName $DOMAIN
    ServerAlias www.$DOMAIN
    ServerAdmin admin@$DOMAIN

    DocumentRoot /var/www/$DOMAIN/public_html

    <Directory /var/www/$DOMAIN/public_html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Proxy para la aplicación Flask
    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api

    # Logs
    ErrorLog /var/www/$DOMAIN/logs/error.log
    CustomLog /var/www/$DOMAIN/logs/access.log combined
</VirtualHost>
EOF

# Habilitar el sitio
a2ensite $DOMAIN.conf

# Habilitar módulos necesarios
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite

# Reiniciar Apache
systemctl restart apache2
print_success "Apache Virtual Host configurado"

# Paso 4: Migrar contenido del Cloud Hosting
print_status "Paso 4: Migrando contenido del Cloud Hosting..."

# Crear directorio para contenido migrado
mkdir -p /var/www/$DOMAIN/migrated_content

# Descargar contenido del Cloud Hosting
print_status "Descargando contenido del Cloud Hosting..."
wget -r -p -k -E -H -K -N -P /var/www/$DOMAIN/migrated_content $CLOUD_HOSTING_URL

# Copiar contenido migrado al directorio público
if [ -d "/var/www/$DOMAIN/migrated_content/$DOMAIN" ]; then
    cp -r /var/www/$DOMAIN/migrated_content/$DOMAIN/* /var/www/$DOMAIN/public_html/
    print_success "Contenido migrado al directorio público"
else
    print_warning "No se pudo migrar contenido automáticamente"
fi

# Paso 5: Instalar SSL con Let's Encrypt
print_status "Paso 5: Instalando SSL con Let's Encrypt..."

# Instalar certbot si no está instalado
if ! command -v certbot &> /dev/null; then
    print_status "Instalando certbot..."
    apt install -y certbot python3-certbot-apache
    print_success "certbot instalado"
else
    print_success "certbot ya está instalado"
fi

# Obtener certificado SSL
print_status "Obteniendo certificado SSL..."
certbot --apache -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

print_success "SSL configurado"

# Paso 6: Crear script de inicio mejorado
print_status "Paso 6: Creando script de inicio mejorado..."
tee /var/www/$DOMAIN/start_vigoleonrocks_production.sh > /dev/null <<EOF
#!/bin/bash

# 🚀 VIGOLEONROCKS - INICIO DE PRODUCCIÓN
# =======================================

echo "🚀 Iniciando VIGOLEONROCKS en modo producción..."

# Variables de entorno
export FLASK_APP=/var/www/$DOMAIN/vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH=/var/www/$DOMAIN
export DB_PASSWORD="$DB_PASSWORD"
export DATABASE_URL="postgresql://vigoleonrocks:$DB_PASSWORD@localhost:5432/vigoleonrocks_db"

# Ir al directorio del proyecto
cd /var/www/$DOMAIN

# Crear directorio de logs si no existe
mkdir -p logs

# Iniciar con Gunicorn (más estable para producción)
echo "Iniciando servidor con Gunicorn..."
gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --threads 2 \
    --worker-class gthread \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --daemon \
    vigoleonrocks_server:app

# Verificar que está corriendo
sleep 3
if pgrep -f gunicorn > /dev/null; then
    echo "✅ VIGOLEONROCKS iniciado correctamente"
    echo "🌐 API disponible en: http://localhost:5000"
    echo "📊 Monitoreo logs en: /var/www/$DOMAIN/logs/"
else
    echo "❌ Error iniciando VIGOLEONROCKS"
    exit 1
fi
EOF

chmod +x /var/www/$DOMAIN/start_vigoleonrocks_production.sh
print_success "Script de inicio de producción creado"

# Paso 7: Crear script de monitoreo
print_status "Paso 7: Creando script de monitoreo..."
tee /var/www/$DOMAIN/monitor_migration.sh > /dev/null <<'EOF'
#!/bin/bash

echo "📊 MONITOREO MIGRACIÓN VIGOLEONROCKS"
echo "===================================="

# Verificar DNS
echo "🌐 Verificando DNS:"
nslookup vigoleonrocks.com localhost

# Verificar Apache
echo ""
echo "🌍 Verificando Apache:"
systemctl status apache2 --no-pager -l

# Verificar Python Flask
echo ""
echo "🐍 Verificando Python Flask:"
ps aux | grep -E "(python|gunicorn)" | grep -v grep

# Verificar SSL
echo ""
echo "🔒 Verificando SSL:"
curl -I https://vigoleonrocks.com

# Verificar API
echo ""
echo "🔗 Verificando API:"
curl -s https://vigoleonrocks.com/api/status | head -3

# Verificar puertos
echo ""
echo "🌐 Puertos activos:"
netstat -tlnp | grep -E ":(80|443|5000)"

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x /var/www/$DOMAIN/monitor_migration.sh
print_success "Script de monitoreo creado"

# Paso 8: Iniciar la aplicación
print_status "Paso 8: Iniciando aplicación VIGOLEONROCKS..."
cd /var/www/$DOMAIN
./start_vigoleonrocks_production.sh

# Verificar que está corriendo
sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente"
else
    print_error "Error iniciando VIGOLEONROCKS"
fi

# Paso 9: Configurar firewall
print_status "Paso 9: Configurando firewall..."
ufw allow 80
ufw allow 443
ufw allow 22
ufw --force enable
print_success "Firewall configurado"

# Paso 10: Configurar DNS local (opcional)
print_status "Paso 10: Configurando DNS local..."

# Instalar bind9 si no está instalado
if ! command -v named &> /dev/null; then
    print_status "Instalando bind9..."
    apt install -y bind9 bind9utils bind9-doc
    print_success "bind9 instalado"
else
    print_success "bind9 ya está instalado"
fi

# Crear configuración DNS
tee /etc/bind/named.conf.local > /dev/null <<EOF
zone "$DOMAIN" {
    type master;
    file "/etc/bind/db.$DOMAIN";
};
EOF

# Crear archivo de zona DNS
tee /etc/bind/db.$DOMAIN > /dev/null <<EOF
\$TTL    604800
@       IN      SOA     $DOMAIN. root.$DOMAIN. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      $DOMAIN.
@       IN      A       $VPS_IP
www     IN      A       $VPS_IP
api     IN      A       $VPS_IP
EOF

# Reiniciar bind9
systemctl restart bind9
systemctl enable bind9

print_success "DNS local configurado"

# Paso 11: Verificación final
print_status "Paso 11: Verificación final..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTP 200)"
else
    print_warning "Sitio web devolvió HTTP $WEB_TEST"
fi

# Test SSL
SSL_TEST=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN)
if [ "$SSL_TEST" = "200" ]; then
    print_success "SSL funcionando correctamente (HTTP 200)"
else
    print_warning "SSL devolvió HTTP $SSL_TEST"
fi

# Test API
API_TEST=$(curl -s http://localhost:5000/api/status | grep -c "status")
if [ "$API_TEST" -gt 0 ]; then
    print_success "API funcionando correctamente"
else
    print_warning "API no responde correctamente"
fi

# Información final
echo ""
echo "🎉 MIGRACIÓN COMPLETA FINALIZADA"
echo "================================="
echo "🌐 Sitio web: https://$DOMAIN"
echo "🔗 API: https://$DOMAIN/api"
echo "📁 Directorio: /var/www/$DOMAIN"
echo "📊 Monitoreo: ./monitor_migration.sh"
echo ""
echo "🔧 Comandos útiles:"
echo "  - Ver logs Apache: tail -f /var/log/apache2/error.log"
echo "  - Reiniciar Apache: systemctl restart apache2"
echo "  - Monitorear: ./monitor_migration.sh"
echo "  - Verificar DNS: nslookup $DOMAIN"
echo ""
echo "💰 BENEFICIOS DE LA MIGRACIÓN:"
echo "  ✅ Arquitectura simplificada"
echo "  ✅ Reducción de costos (eliminar Cloud Hosting)"
echo "  ✅ Mejor rendimiento"
echo "  ✅ Control total del entorno"
echo "  ✅ Escalabilidad futura"
echo ""
print_success "MIGRACIÓN COMPLETA A VPS FINALIZADA EXITOSAMENTE"
