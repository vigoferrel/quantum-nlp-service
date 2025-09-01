#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT COMPLETO AUTOMATIZADO
# ===================================================

echo "🚀 INICIANDO DEPLOYMENT COMPLETO VIGOLEONROCKS"
echo "==============================================="

# Configuración
DOMAIN="vigoleonrocks.com"
VPS_IP="72.60.61.49"
PROJECT_DIR="/var/www/$DOMAIN"

# Función para imprimir mensajes coloreados
print_status() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# Paso 1: Actualizar sistema
print_status "Paso 1: Actualizando sistema..."
apt update && apt upgrade -y
print_success "Sistema actualizado"

# Paso 2: Instalar dependencias
print_status "Paso 2: Instalando dependencias..."
apt install -y python3 python3-pip python3-venv apache2 postgresql postgresql-contrib supervisor curl ufw certbot python3-certbot-apache
print_success "Dependencias instaladas"

# Paso 3: Crear directorio del proyecto
print_status "Paso 3: Creando directorio del proyecto..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
print_success "Directorio creado"

# Paso 4: Clonar código actualizado
print_status "Paso 4: Descargando código actualizado..."
if [ ! -d ".git" ]; then
    git clone https://github.com/vigoferrel/quantum-nlp-service.git .
else
    git pull origin main
fi
print_success "Código descargado"

# Paso 5: Configurar base de datos
print_status "Paso 5: Configurando PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE IF NOT EXISTS vigoleonrocks_db;
CREATE USER IF NOT EXISTS vigoleonrocks WITH PASSWORD '0gLuiWUTaw3Q)3GOFM&J';
GRANT ALL PRIVILEGES ON DATABASE vigoleonrocks_db TO vigoleonrocks;
ALTER USER vigoleonrocks CREATEDB;
\q
EOF
print_success "Base de datos configurada"

# Paso 6: Instalar dependencias Python
print_status "Paso 6: Instalando dependencias Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
deactivate
print_success "Dependencias Python instaladas"

# Paso 7: Configurar Apache
print_status "Paso 7: Configurando Apache..."
cat > /etc/apache2/sites-available/$DOMAIN.conf <<EOF
<VirtualHost *:80>
    ServerName $DOMAIN
    ServerAlias www.$DOMAIN
    ServerAdmin admin@$DOMAIN

    DocumentRoot $PROJECT_DIR/public_html

    <Directory $PROJECT_DIR/public_html>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ProxyPass /api http://localhost:5000/api
    ProxyPassReverse /api http://localhost:5000/api

    ErrorLog $PROJECT_DIR/logs/apache/error.log
    CustomLog $PROJECT_DIR/logs/apache/access.log combined
</VirtualHost>
EOF

a2ensite $DOMAIN.conf
a2enmod proxy proxy_http rewrite headers
systemctl restart apache2
print_success "Apache configurado"

# Paso 8: Configurar permisos
print_status "Paso 8: Configurando permisos..."
chown -R www-data:www-data $PROJECT_DIR
chmod +x $PROJECT_DIR/start_vigoleonrocks_production.sh
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/public_html
print_success "Permisos configurados"

# Paso 9: Crear script de inicio
print_status "Paso 9: Creando script de inicio..."
cat > $PROJECT_DIR/start_vigoleonrocks_production.sh <<EOF
#!/bin/bash

echo "🚀 Iniciando VIGOLEONROCKS en producción..."

export FLASK_APP=$PROJECT_DIR/vigoleonrocks/interfaces/rest_api.py
export FLASK_ENV=production
export PYTHONPATH=$PROJECT_DIR
export DB_PASSWORD="0gLuiWUTaw3Q)3GOFM&J"
export DATABASE_URL="postgresql://vigoleonrocks:\$DB_PASSWORD@localhost:5432/vigoleonrocks_db"

cd $PROJECT_DIR
source venv/bin/activate

gunicorn \\
    --bind 0.0.0.0:5000 \\
    --workers 4 \\
    --threads 2 \\
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
    vigoleonrocks.interfaces.rest_api:app

echo "✅ VIGOLEONROCKS iniciado correctamente"
EOF

chmod +x $PROJECT_DIR/start_vigoleonrocks_production.sh
print_success "Script de inicio creado"

# Paso 10: Crear directorios de logs
print_status "Paso 10: Creando directorios de logs..."
mkdir -p $PROJECT_DIR/logs/{apache,app,error}
print_success "Directorios de logs creados"

# Paso 11: Iniciar aplicación
print_status "Paso 11: Iniciando aplicación..."
cd $PROJECT_DIR
./start_vigoleonrocks_production.sh

sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "Aplicación iniciada correctamente"
else
    print_error "Error iniciando aplicación"
fi

# Paso 12: Configurar SSL
print_status "Paso 12: Configurando SSL..."
certbot --apache -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
print_success "SSL configurado"

# Paso 13: Configurar firewall
print_status "Paso 13: Configurando firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_success "Firewall configurado"

# Paso 14: Verificación final
print_status "Paso 14: Verificación final..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN)
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTPS 200)"
else
    print_warning "Sitio web devolvió HTTPS $WEB_TEST"
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
echo "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE"
echo "===================================="
echo "🌐 Sitio web: https://$DOMAIN"
echo "🔗 API: https://$DOMAIN/api"
echo "📁 Directorio: $PROJECT_DIR"
echo ""
echo "📊 Comandos útiles:"
echo "  Monitoreo: $PROJECT_DIR/monitor_migration.sh"
echo "  Reinicio: $PROJECT_DIR/start_vigoleonrocks_production.sh"
echo "  Logs app: tail -f $PROJECT_DIR/logs/app/error.log"
echo "  Logs Apache: tail -f /var/log/apache2/error.log"
echo ""
print_success "DEPLOYMENT COMPLETO FINALIZADO"