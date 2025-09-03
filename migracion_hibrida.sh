#!/bin/bash

# 🏗️ MIGRACIÓN ARQUITECTURA HÍBRIDA VIGOLEONROCKS
# ================================================

echo "🏗️ MIGRACIÓN ARQUITECTURA HÍBRIDA VIGOLEONROCKS"
echo "================================================"

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

echo ""
echo "📊 ANÁLISIS DE ARQUITECTURA ACTUAL:"
echo "===================================="
echo "🌐 Dominio: $DOMAIN"
echo "🖥️ VPS: $VPS_IP"
echo "☁️ Cloud Hosting: $CLOUD_HOSTING_URL"
echo ""

# Paso 1: Verificar estado actual
print_status "Paso 1: Verificando estado actual..."

# Verificar VPS
if ping -c 1 $VPS_IP > /dev/null 2>&1; then
    print_success "VPS ($VPS_IP) está accesible"
else
    print_error "VPS ($VPS_IP) no está accesible"
    exit 1
fi

# Verificar Cloud Hosting
if curl -s --head $CLOUD_HOSTING_URL | head -n 1 | grep -q "200 OK"; then
    print_success "Cloud Hosting está funcionando"
else
    print_warning "Cloud Hosting no responde correctamente"
fi

# Paso 2: Configurar DNS local
print_status "Paso 2: Configurando DNS local..."

# Instalar bind9 si no está instalado
if ! command -v named &> /dev/null; then
    print_status "Instalando bind9..."
    apt update
    apt install -y bind9 bind9utils bind9-doc
    print_success "bind9 instalado"
else
    print_success "bind9 ya está instalado"
fi

# Crear configuración DNS
sudo tee /etc/bind/named.conf.local > /dev/null <<EOF
zone "$DOMAIN" {
    type master;
    file "/etc/bind/db.$DOMAIN";
};

zone "www.$DOMAIN" {
    type master;
    file "/etc/bind/db.www.$DOMAIN";
};
EOF

# Crear archivo de zona DNS
sudo tee /etc/bind/db.$DOMAIN > /dev/null <<EOF
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

# Crear archivo de zona para www
sudo tee /etc/bind/db.www.$DOMAIN > /dev/null <<EOF
\$TTL    604800
@       IN      SOA     www.$DOMAIN. root.$DOMAIN. (
                              2         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
;
@       IN      NS      www.$DOMAIN.
@       IN      A       $VPS_IP
EOF

# Reiniciar bind9
systemctl restart bind9
systemctl enable bind9

print_success "DNS local configurado"

# Paso 3: Configurar Apache Virtual Host
print_status "Paso 3: Configurando Apache Virtual Host..."

# Crear configuración Apache para el dominio
sudo tee /etc/apache2/sites-available/$DOMAIN.conf > /dev/null <<EOF
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

# Reiniciar Apache
systemctl restart apache2

print_success "Apache Virtual Host configurado"

# Paso 4: Instalar SSL con Let's Encrypt
print_status "Paso 4: Instalando SSL con Let's Encrypt..."

# Instalar certbot si no está instalado
if ! command -v certbot &> /dev/null; then
    print_status "Instalando certbot..."
    apt install -y certbot python3-certbot-apache
    print_success "certbot instalado"
else
    print_success "certbot ya está instalado"
fi

# Obtener certificado SSL
certbot --apache -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

print_success "SSL configurado"

# Paso 5: Migrar contenido del Cloud Hosting
print_status "Paso 5: Migrando contenido del Cloud Hosting..."

# Crear directorio para contenido migrado
mkdir -p /var/www/$DOMAIN/migrated_content

# Descargar contenido del Cloud Hosting
print_status "Descargando contenido del Cloud Hosting..."
wget -r -p -k -E -H -K -N -P /var/www/$DOMAIN/migrated_content $CLOUD_HOSTING_URL

print_success "Contenido migrado"

# Paso 6: Configurar monitoreo
print_status "Paso 6: Configurando monitoreo..."

# Crear script de monitoreo
sudo tee /var/www/$DOMAIN/monitor_migration.sh > /dev/null <<'EOF'
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
systemctl status vigoleonrocks --no-pager -l

# Verificar SSL
echo ""
echo "🔒 Verificando SSL:"
curl -I https://vigoleonrocks.com

# Verificar API
echo ""
echo "🔗 Verificando API:"
curl -s https://vigoleonrocks.com/api/status | head -3

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x /var/www/$DOMAIN/monitor_migration.sh

print_success "Monitoreo configurado"

# Paso 7: Verificación final
print_status "Paso 7: Verificación final..."

# Test DNS
if nslookup $DOMAIN localhost > /dev/null 2>&1; then
    print_success "DNS funcionando correctamente"
else
    print_warning "DNS no responde correctamente"
fi

# Test Apache
if systemctl is-active --quiet apache2; then
    print_success "Apache funcionando correctamente"
else
    print_error "Apache no está funcionando"
fi

# Test SSL
if curl -s --head https://$DOMAIN | head -n 1 | grep -q "200 OK"; then
    print_success "SSL funcionando correctamente"
else
    print_warning "SSL no responde correctamente"
fi

# Información final
echo ""
echo "🎉 MIGRACIÓN COMPLETADA"
echo "======================="
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
print_success "MIGRACIÓN COMPLETADA EXITOSAMENTE"
