#!/bin/bash

# 🚀 COMPLETAR DEPLOYMENT VPS VIGOLEONROCKS
# =========================================

echo "🚀 COMPLETANDO DEPLOYMENT VPS VIGOLEONROCKS"
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

# Paso 1: Instalar pip3
print_status "Paso 1: Instalando pip3..."
apt update
apt install -y python3-pip
print_success "pip3 instalado"

# Paso 2: Instalar dependencias Python
print_status "Paso 2: Instalando dependencias Python..."
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

# Paso 3: Configurar permisos
print_status "Paso 3: Configurando permisos..."
chown -R www-data:www-data /var/www/vigoleonrocks.com
chmod +x /var/www/vigoleonrocks.com/start_vigoleonrocks.sh
chmod 755 /var/www/vigoleonrocks.com
chmod 755 /var/www/vigoleonrocks.com/public_html
print_success "Permisos configurados"

# Paso 4: Instalar y configurar Apache
print_status "Paso 4: Configurando Apache..."

# Instalar Apache si no está instalado
if ! command -v apache2 &> /dev/null; then
    print_status "Instalando Apache..."
    apt update
    apt install -y apache2
    print_success "Apache instalado"
else
    print_success "Apache ya está instalado"
fi

# Crear archivo de configuración para el sitio
tee /etc/apache2/sites-available/vigoleonrocks.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerName vigoleonrocks.com
    ServerAlias www.vigoleonrocks.com
    ServerAdmin admin@vigoleonrocks.com

    DocumentRoot /var/www/vigoleonrocks.com/public_html

    <Directory /var/www/vigoleonrocks.com/public_html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    # Proxy para la aplicación Flask
    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api

    # Logs
    ErrorLog /var/www/vigoleonrocks.com/logs/error.log
    CustomLog /var/www/vigoleonrocks.com/logs/access.log combined
</VirtualHost>
EOF

# Habilitar el sitio
a2ensite vigoleonrocks.conf

# Habilitar módulos necesarios
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite

# Reiniciar Apache
systemctl restart apache2
print_success "Apache configurado y reiniciado"

# Paso 5: Crear script de inicio mejorado
print_status "Paso 5: Creando script de inicio mejorado..."
tee /var/www/vigoleonrocks.com/start_vigoleonrocks_production.sh > /dev/null <<'EOF'
#!/bin/bash

# 🚀 VIGOLEONROCKS - INICIO DE PRODUCCIÓN
# =======================================

echo "🚀 Iniciando VIGOLEONROCKS en modo producción..."

# Variables de entorno
export FLASK_APP=/var/www/vigoleonrocks.com/vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH=/var/www/vigoleonrocks.com
export DB_PASSWORD="0gLuiWUTaw3Q)3GOFM&J"
export DATABASE_URL="postgresql://vigoleonrocks:0gLuiWUTaw3Q)3GOFM&J@localhost:5432/vigoleonrocks_db"

# Ir al directorio del proyecto
cd /var/www/vigoleonrocks.com

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
    echo "📊 Monitoreo logs en: /var/www/vigoleonrocks.com/logs/"
else
    echo "❌ Error iniciando VIGOLEONROCKS"
    exit 1
fi
EOF

chmod +x /var/www/vigoleonrocks.com/start_vigoleonrocks_production.sh
print_success "Script de inicio de producción creado"

# Paso 6: Crear script de monitoreo
print_status "Paso 6: Creando script de monitoreo..."
tee /var/www/vigoleonrocks.com/monitor.sh > /dev/null <<'EOF'
#!/bin/bash

echo "📊 MONITOREO VIGOLEONROCKS"
echo "=========================="

# Verificar procesos
echo "⚙️ Procesos Python/Gunicorn:"
ps aux | grep -E "(python|gunicorn)" | grep -v grep

# Verificar puertos
echo ""
echo "🌐 Puertos:"
netstat -tlnp | grep -E ":(80|5000)"

# Verificar sitio web
echo ""
echo "🌍 Test sitio web:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost

# Verificar API
echo ""
echo "🔗 Test API:"
curl -s http://localhost:5000/api/status | head -3

# Verificar logs
echo ""
echo "📝 Últimas líneas de log de errores:"
if [ -f "/var/www/vigoleonrocks.com/logs/error.log" ]; then
    tail -5 /var/www/vigoleonrocks.com/logs/error.log
else
    echo "No hay logs de error aún"
fi

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x /var/www/vigoleonrocks.com/monitor.sh
print_success "Script de monitoreo creado"

# Paso 7: Iniciar la aplicación
print_status "Paso 7: Iniciando aplicación VIGOLEONROCKS..."
cd /var/www/vigoleonrocks.com
./start_vigoleonrocks_production.sh

# Verificar que está corriendo
sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente"
else
    print_error "Error iniciando VIGOLEONROCKS"
fi

# Paso 8: Configurar firewall
print_status "Paso 8: Configurando firewall..."
ufw allow 80
ufw allow 443
ufw --force enable
print_success "Firewall configurado"

# Paso 9: Verificación final
print_status "Paso 9: Verificación final del deployment..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTP 200)"
else
    print_warning "Sitio web devolvió HTTP $WEB_TEST"
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
echo "🎉 DEPLOYMENT COMPLETADO"
echo "========================"
echo "🌐 Sitio web: http://vigoleonrocks.com"
echo "🔗 API: http://vigoleonrocks.com/api"
echo "📁 Directorio: /var/www/vigoleonrocks.com"
echo "📊 Monitoreo: ./monitor.sh"
echo ""
echo "🔧 Comandos útiles:"
echo "  - Ver logs: tail -f logs/error.log"
echo "  - Reiniciar: systemctl restart apache2"
echo "  - Monitorear: ./monitor.sh"
echo "  - Backup: ./backup.sh"
echo ""
print_success "DEPLOYMENT COMPLETADO EXITOSAMENTE"
