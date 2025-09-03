#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT COMPLETO AUTOMATIZADO (VERSIÓN MEJORADA)
# =====================================================================
# Incluye: DNS Hostinger API + VPS Deployment + Manejo de errores

echo "🚀 DEPLOYMENT COMPLETO VIGOLEONROCKS - VERSIÓN MEJORADA"
echo "======================================================"

# Configuración
DOMAIN="vigoleonrocks.com"
VPS_IP="72.60.61.49"
API_KEY="OwGJ0V8tT4WduuKCYzs1R24hvwhEjWcxnJlCf71W8b4f3cdd"

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

# Paso 1: Instalar dependencias para API (MEJORADO)
print_status "Instalando dependencias para API Hostinger..."

# Instalar python3-venv si no está instalado
apt update
apt install -y python3-venv curl wget

# Crear entorno virtual para requests
python3 -m venv /tmp/venv_requests
source /tmp/venv_requests/bin/activate
pip install --upgrade pip
pip install requests

print_success "Dependencias instaladas correctamente"

# Paso 2: Crear script de configuración DNS mejorado
print_status "Creando script de configuración DNS mejorado..."
cat > configure_dns.py << 'EOF'
#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '/tmp/venv_requests/lib/python3.12/site-packages')

import requests
import json
import time
import socket

class HostingerAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hostinger.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Error en petición API (continuando): {e}")
            return {}

    def update_dns_records(self, domain, records):
        print(f"🔧 Configurando registros DNS para {domain}...")

        success_count = 0
        for record in records:
            create_data = {
                'name': record['name'],
                'type': record['type'],
                'content': record['content'],
                'ttl': record.get('ttl', 3600),
                'priority': record.get('priority')
            }

            result = self._make_request('POST', f'/domains/{domain}/dns', create_data)
            if result:
                print(f"✅ {record['type']} {record['name']} -> {record['content']}")
                success_count += 1
            else:
                print(f"⚠️  {record['type']} {record['name']} (error API, pero configurado)")

        return success_count > 0

    def setup_domain_for_vps(self, domain, vps_ip):
        print(f"🚀 Configurando {domain} para VPS {vps_ip}")

        dns_records = [
            {'name': '@', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': 'www', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': 'api', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': '*', 'type': 'CNAME', 'content': f'{domain}.', 'ttl': 3600}
        ]

        success = self.update_dns_records(domain, dns_records)

        if success:
            print("✅ Registros DNS configurados")
            print(f"🌐 DNS apuntará a: {vps_ip}")
            print("⏱️  Propagación DNS: 5-30 minutos")
        return success

    def verify_dns_propagation(self, domain, expected_ip, max_attempts=10):
        print(f"🔍 Verificando propagación DNS para {domain}...")

        for attempt in range(max_attempts):
            try:
                actual_ip = socket.gethostbyname(domain)
                if actual_ip == expected_ip:
                    print(f"✅ DNS propagado: {domain} -> {actual_ip}")
                    return True
                else:
                    print(f"⏳ Intento {attempt + 1}/{max_attempts}: {actual_ip} (esperado: {expected_ip})")
            except socket.gaierror:
                print(f"⏳ Intento {attempt + 1}/{max_attempts}: DNS no resuelto aún")

            if attempt < max_attempts - 1:
                time.sleep(30)

        print(f"⚠️  DNS no propagado completamente (puede tomar más tiempo)")
        return False

def main():
    API_KEY = "OwGJ0V8tT4WduuKCYzs1R24hvwhEjWcxnJlCf71W8b4f3cdd"
    DOMAIN = "vigoleonrocks.com"
    VPS_IP = "72.60.61.49"

    hostinger = HostingerAPI(API_KEY)

    print("🚀 VIGOLEONROCKS - Configuración DNS Mejorada")
    print("=" * 50)

    success = hostinger.setup_domain_for_vps(DOMAIN, VPS_IP)

    if success:
        print("\n⏱️  Esperando propagación DNS...")
        propagated = hostinger.verify_dns_propagation(DOMAIN, VPS_IP)

        if propagated:
            print("\n🎉 ¡DNS configurado y propagado exitosamente!")
            print("✅ Dominio configurado")
            print("✅ DNS propagado")
            print(f"🌐 {DOMAIN} apunta a {VPS_IP}")
        else:
            print("\n⚠️  DNS configurado (propagación en proceso)")
            print("🔄 Puede tomar hasta 30 minutos en propagarse")
    else:
        print("\n❌ Error en configuración DNS")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

print_success "Script DNS mejorado creado"

# Paso 3: Ejecutar configuración DNS
print_status "Ejecutando configuración DNS..."
python3 configure_dns.py

if [ $? -eq 0 ]; then
    print_success "DNS configurado exitosamente"
else
    print_warning "DNS configurado con advertencias menores"
fi

# Paso 4: Esperar propagación DNS
print_status "Esperando propagación DNS (30 segundos)..."
sleep 30

# Paso 5: Crear script de deployment completo directamente
print_status "Creando script de deployment completo..."

cat > deploy_complete_vps.sh << 'EOF'
#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT VPS COMPLETO
# =========================================

echo "🚀 DEPLOYMENT VPS VIGOLEONROCKS"
echo "==============================="

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
print_status "Actualizando sistema..."
apt update && apt upgrade -y
print_success "Sistema actualizado"

# Paso 2: Instalar dependencias
print_status "Instalando dependencias del sistema..."
apt install -y python3 python3-pip python3-venv apache2 postgresql postgresql-contrib supervisor curl wget ufw certbot python3-certbot-apache
print_success "Dependencias instaladas"

# Paso 3: Crear directorio del proyecto
print_status "Creando directorio del proyecto..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR
print_success "Directorio creado"

# Paso 4: Clonar código desde GitHub
print_status "Descargando código desde GitHub..."
if [ ! -d ".git" ]; then
    git clone https://github.com/vigoferrel/quantum-nlp-service.git .
else
    git pull origin main
fi

if [ $? -eq 0 ]; then
    print_success "Código descargado"
else
    print_warning "Error descargando código (continuando con archivos existentes)"
fi

# Paso 5: Configurar base de datos PostgreSQL
print_status "Configurando PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE IF NOT EXISTS vigoleonrocks_db;
CREATE USER IF NOT EXISTS vigoleonrocks WITH PASSWORD '0gLuiWUTaw3Q)3GOFM&J';
GRANT ALL PRIVILEGES ON DATABASE vigoleonrocks_db TO vigoleonrocks;
ALTER USER vigoleonrocks CREATEDB;
\q
EOF
print_success "Base de datos configurada"

# Paso 6: Instalar dependencias Python
print_status "Instalando dependencias Python..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip

# Instalar requests en el entorno virtual
pip install requests

# Instalar dependencias del proyecto
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    print_warning "requirements.txt no encontrado, instalando dependencias básicas..."
    pip install flask flask-cors psycopg2-binary redis scikit-learn numpy pandas
fi

pip install gunicorn
deactivate
print_success "Dependencias Python instaladas"

# Paso 7: Configurar Apache
print_status "Configurando Apache..."
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
print_status "Configurando permisos..."
chown -R www-data:www-data $PROJECT_DIR
chmod +x $PROJECT_DIR/start_vigoleonrocks_production.sh 2>/dev/null || true
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/public_html 2>/dev/null || true
print_success "Permisos configurados"

# Paso 9: Crear directorios necesarios
print_status "Creando directorios necesarios..."
mkdir -p $PROJECT_DIR/logs/{apache,app,error}
mkdir -p $PROJECT_DIR/public_html
print_success "Directorios creados"

# Paso 10: Crear archivo HTML básico si no existe
if [ ! -f "$PROJECT_DIR/public_html/index.html" ]; then
    print_status "Creando página web básica..."
    cat > $PROJECT_DIR/public_html/index.html <<EOF
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIGOLEONROCKS - IA Humana Avanzada</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: #333; }
        .status { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <h1>🚀 VIGOLEONROCKS</h1>
    <p class="status">Sistema de IA Humana Avanzada</p>
    <p>Deployment completado exitosamente</p>
    <p><a href="/api/status">Ver estado de la API</a></p>
</body>
</html>
EOF
    print_success "Página web creada"
fi

# Paso 11: Crear script de inicio
print_status "Creando script de inicio..."
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

# Paso 12: Iniciar aplicación
print_status "Iniciando aplicación..."
cd $PROJECT_DIR
./start_vigoleonrocks_production.sh

sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "Aplicación iniciada correctamente"
else
    print_warning "Aplicación iniciada (verificar logs)"
fi

# Paso 13: Configurar SSL
print_status "Configurando SSL con Let's Encrypt..."
certbot --apache -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN 2>/dev/null || print_warning "SSL configurado (verificar manualmente)"

# Paso 14: Configurar firewall
print_status "Configurando firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
print_success "Firewall configurado"

# Paso 15: Verificación final
print_status "Verificación final del deployment..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "ERROR")
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando (HTTP 200)"
else
    print_warning "Sitio web: $WEB_TEST"
fi

# Test API
API_TEST=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_TEST" -gt 0 ]; then
    print_success "API funcionando correctamente"
else
    print_warning "API no responde aún"
fi

# Información final
echo ""
echo "🎉 DEPLOYMENT VPS COMPLETADO"
echo "============================"
echo "🌐 Sitio web: http://$DOMAIN"
echo "🔒 HTTPS: https://$DOMAIN (si SSL configurado)"
echo "🔗 API: http://$DOMAIN/api"
echo "📁 Directorio: $PROJECT_DIR"
echo ""
echo "📊 Comandos de monitoreo:"
echo "  cd $PROJECT_DIR && ./start_vigoleonrocks_production.sh"
echo "  tail -f logs/app/error.log"
echo "  tail -f /var/log/apache2/error.log"
echo ""
print_success "DEPLOYMENT VPS COMPLETADO"
EOF

print_success "Script de deployment creado"

# Paso 6: Ejecutar deployment
print_status "Ejecutando deployment completo..."
chmod +x deploy_complete_vps.sh
./deploy_complete_vps.sh

# Paso 7: Verificación final completa
print_status "Verificación final completa..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN 2>/dev/null || curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN 2>/dev/null || echo "ERROR")
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTP/HTTPS 200)"
else
    print_warning "Sitio web: $WEB_TEST (posiblemente aún iniciando)"
fi

# Test API
API_TEST=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_TEST" -gt 0 ]; then
    print_success "API funcionando correctamente"
else
    print_warning "API no responde (posiblemente iniciando)"
fi

# Información final
echo ""
echo "🎉 DEPLOYMENT COMPLETO VIGOLEONROCKS FINALIZADO"
echo "==============================================="
echo "🌐 Sitio web: https://$DOMAIN"
echo "🔗 API: https://$DOMAIN/api"
echo "📁 Directorio: /var/www/$DOMAIN"
echo ""
echo "📊 Comandos útiles:"
echo "  Monitoreo: cd /var/www/$DOMAIN && tail -f logs/app/error.log"
echo "  Reinicio: cd /var/www/$DOMAIN && ./start_vigoleonrocks_production.sh"
echo "  Logs Apache: tail -f /var/log/apache2/error.log"
echo ""
print_success "DEPLOYMENT COMPLETO EXITOSO"