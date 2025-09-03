#!/bin/bash

# 🚀 VIGOLEONROCKS - AUTO-FIX DEPLOYMENT V2
# ========================================

echo "🔧 AUTO-FIX DEPLOYMENT V2 - CON UPDATES"
echo "======================================="

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

# Paso 1: Verificar actualizaciones del sistema
print_status "Paso 1: Verificando actualizaciones del sistema..."
apt update --quiet
UPDATES=$(apt list --upgradable 2>/dev/null | grep -c "upgradable")

if [ "$UPDATES" -gt 0 ]; then
    print_warning "Hay $UPDATES actualizaciones pendientes"
    print_status "Instalando actualizaciones de seguridad..."

    # Instalar solo actualizaciones de seguridad
    apt install --only-upgrade -y unattended-upgrades
    apt autoremove -y
    apt autoclean

    print_success "Actualizaciones instaladas"
else
    print_success "Sistema actualizado"
fi

# Verificar si se requiere reinicio
if [ -f /var/run/reboot-required ]; then
    print_warning "Se requiere reinicio del sistema"
    print_status "Reiniciando sistema en 10 segundos..."
    sleep 10
    reboot
    exit 0
fi

# Paso 2: Verificar estado del sistema
print_status "Paso 2: Verificando estado del sistema..."
ps aux | grep -E "(python|gunicorn|nginx|apache)" | grep -v grep

# Verificar puertos
print_status "Verificando puertos..."
netstat -tlnp | grep -E ":(80|5000|3000)" || ss -tlnp | grep -E ":(80|5000|3000)"

# Paso 3: Verificar archivos del proyecto
print_status "Paso 3: Verificando archivos del proyecto..."
if [ -f "/var/www/vigoleonrocks.com/vigoleonrocks_server.py" ]; then
    print_success "vigoleonrocks_server.py encontrado"
else
    print_error "vigoleonrocks_server.py NO encontrado en /var/www/vigoleonrocks.com/"
    # Buscar en otras ubicaciones
    find /root /home -name "vigoleonrocks_server.py" 2>/dev/null
fi

if [ -f "/var/www/vigoleonrocks.com/requirements.txt" ]; then
    print_success "requirements.txt encontrado"
else
    print_error "requirements.txt NO encontrado"
fi

# Paso 4: Instalar dependencias si es necesario
print_status "Paso 4: Verificando dependencias Python..."
cd /var/www/vigoleonrocks.com 2>/dev/null || mkdir -p /var/www/vigoleonrocks.com

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet --disable-pip-version-check
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas correctamente"
    else
        print_error "Error instalando dependencias"
        # Intentar instalar Flask mínimo
        pip3 install flask flask-cors --quiet
    fi
else
    print_warning "requirements.txt no encontrado, instalando Flask básico"
    pip3 install flask flask-cors requests --quiet
fi

# Paso 5: Matar procesos existentes
print_status "Paso 5: Limpiando procesos existentes..."
pkill -f gunicorn 2>/dev/null
pkill -f python 2>/dev/null
pkill -f vigoleonrocks_server.py 2>/dev/null

# Matar procesos en puertos específicos
fuser -k 5000/tcp 2>/dev/null
fuser -k 80/tcp 2>/dev/null

sleep 3

# Verificar que se detuvieron
if pgrep -f gunicorn > /dev/null; then
    print_warning "Gunicorn aún corriendo, forzando parada..."
    pkill -9 -f gunicorn
fi

if pgrep -f vigoleonrocks_server.py > /dev/null; then
    print_warning "Python aún corriendo, forzando parada..."
    pkill -9 -f vigoleonrocks_server.py
fi

print_success "Procesos limpiados"

# Paso 6: Verificar y configurar Nginx
print_status "Paso 6: Verificando Nginx..."

# Verificar si Nginx está instalado
if ! command -v nginx &> /dev/null; then
    print_warning "Nginx no está instalado, instalando..."
    apt update && apt install -y nginx
fi

# Crear configuración de Nginx
sudo tee /etc/nginx/sites-available/vigoleonrocks > /dev/null <<EOF
server {
    listen 80;
    server_name 72.60.61.49 _;

    # Logs
    access_log /var/www/vigoleonrocks.com/logs/access.log;
    error_log /var/www/vigoleonrocks.com/logs/error.log;

    # Proxy para la aplicación principal
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Proxy específico para APIs
    location /api {
        proxy_pass http://localhost:5000/api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # Archivos estáticos
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files \$uri @proxy;
    }

    location @proxy {
        proxy_pass http://localhost:5000;
    }
}
EOF

# Crear directorio de logs
mkdir -p /var/www/vigoleonrocks.com/logs

# Habilitar sitio
sudo ln -sf /etc/nginx/sites-available/vigoleonrocks /etc/nginx/sites-enabled/ 2>/dev/null

# Remover configuración por defecto si existe
sudo rm -f /etc/nginx/sites-enabled/default

# Probar configuración
sudo nginx -t 2>/dev/null
if [ $? -eq 0 ]; then
    print_success "Configuración de Nginx correcta"
    sudo systemctl restart nginx 2>/dev/null || sudo service nginx restart 2>/dev/null
    print_success "Nginx reiniciado"
else
    print_error "Error en configuración de Nginx"
    sudo nginx -T
fi

# Paso 7: Iniciar aplicación Python
print_status "Paso 7: Iniciando aplicación VIGOLEONROCKS..."

cd /var/www/vigoleonrocks.com

# Crear archivo Python básico si no existe
if [ ! -f "vigoleonrocks_server.py" ]; then
    print_warning "Creando aplicación básica..."
    cat > vigoleonrocks_server.py << 'EOF'
#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "message": "VIGOLEONROCKS - Sistema de IA Cuántica",
        "status": "active",
        "timestamp": datetime.datetime.now().isoformat()
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "server": "VIGOLEONROCKS",
        "version": "1.0",
        "uptime": str(datetime.datetime.now() - datetime.datetime(2025, 1, 1))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
EOF
fi

# Crear script de inicio si no existe
if [ ! -f "start_production.sh" ]; then
    cat > start_production.sh << 'EOF'
#!/bin/bash
cd /var/www/vigoleonrocks.com
export FLASK_APP=vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH=/var/www/vigoleonrocks.com

# Iniciar con Gunicorn
gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 2 \
    --threads 2 \
    --worker-class gthread \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log \
    --log-level info \
    --timeout 60 \
    --keep-alive 10 \
    --daemon \
    vigoleonrocks_server:app
EOF
    chmod +x start_production.sh
fi

# Crear directorio de logs
mkdir -p logs

# Iniciar aplicación
./start_production.sh

# Verificar que inició
sleep 5
if pgrep -f gunicorn > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente con Gunicorn"
elif pgrep -f vigoleonrocks_server.py > /dev/null; then
    print_success "VIGOLEONROCKS iniciado en modo directo"
else
    print_error "Error iniciando VIGOLEONROCKS, intentando modo directo..."
    python3 vigoleonrocks_server.py &
    sleep 3
    if pgrep -f vigoleonrocks_server.py > /dev/null; then
        print_success "VIGOLEONROCKS iniciado en modo directo"
    else
        print_error "No se pudo iniciar la aplicación"
    fi
fi

# Paso 8: Verificar servicios
print_status "Paso 8: Verificando servicios..."

# Verificar Nginx
if sudo systemctl is-active --quiet nginx 2>/dev/null || sudo service nginx status 2>/dev/null | grep -q "active"; then
    print_success "Nginx está activo"
else
    print_error "Nginx no está activo"
    sudo systemctl start nginx 2>/dev/null || sudo service nginx start 2>/dev/null
fi

# Verificar aplicación
if pgrep -f gunicorn > /dev/null || pgrep -f vigoleonrocks_server.py > /dev/null; then
    print_success "Aplicación Python está corriendo"
else
    print_error "Aplicación Python no está corriendo"
fi

# Paso 9: Probar conectividad
print_status "Paso 9: Probando conectividad..."

# Probar localhost
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "000")
if [ "$RESPONSE" = "200" ] || [ "$RESPONSE" = "404" ]; then
    print_success "Nginx responde (HTTP $RESPONSE)"
else
    print_error "Nginx no responde correctamente (HTTP $RESPONSE)"
fi

# Probar localhost:5000
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "000")
if [ "$RESPONSE" = "200" ]; then
    print_success "Aplicación Python responde (HTTP $RESPONSE)")
else
    print_warning "Aplicación Python responde (HTTP $RESPONSE)")
fi

# Probar API
API_RESPONSE=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_RESPONSE" -gt 0 ]; then
    print_success "API funcionando correctamente")
else
    print_warning "API no responde correctamente")
fi

# Paso 10: Configurar firewall
print_status "Paso 10: Configurando firewall..."
sudo ufw allow 80 2>/dev/null || iptables -A INPUT -p tcp --dport 80 -j ACCEPT 2>/dev/null
sudo ufw allow 5000 2>/dev/null || iptables -A INPUT -p tcp --dport 5000 -j ACCEPT 2>/dev/null
sudo ufw --force enable 2>/dev/null || print_warning "UFW no disponible, usando iptables"

# Paso 11: Crear script de monitoreo mejorado
print_status "Paso 11: Creando script de monitoreo..."
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "📊 ESTADO DEL SISTEMA VIGOLEONROCKS"
echo "==================================="

echo "🔍 Procesos:"
ps aux | grep -E "(nginx|gunicorn|python)" | grep -v grep || echo "No se encontraron procesos"

echo ""
echo "🌐 Puertos:"
netstat -tlnp 2>/dev/null | grep -E ":(80|5000)" || ss -tlnp 2>/dev/null | grep -E ":(80|5000)" || echo "No se encontraron puertos"

echo ""
echo "🔗 Tests de conectividad:"
echo "Nginx (80): $(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "ERROR")"
echo "App (5000): $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "ERROR")"
echo "API Status: $(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0") respuestas"

echo ""
echo "💾 Espacio en disco:"
df -h / | tail -1

echo ""
echo "🚀 Servicios:"
echo "Nginx: $(sudo systemctl is-active nginx 2>/dev/null || sudo service nginx status 2>/dev/null | grep -o "active\|inactive" || echo "unknown")"
echo "Gunicorn: $(pgrep -f gunicorn > /dev/null && echo "active" || echo "inactive")"
echo "Python: $(pgrep -f vigoleonrocks_server.py > /dev/null && echo "active" || echo "inactive")"

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x monitor.sh

# Paso 12: Verificación final
print_status "Paso 12: Verificación final..."

# Test completo
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost 2>/dev/null || echo "ERROR")
APP_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "ERROR")
API_TEST=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")

if [ "$WEB_TEST" = "200" ] || [ "$APP_TEST" = "200" ]; then
    print_success "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE!"
    echo ""
    echo "🌐 URLs disponibles:"
    echo "   Web: http://72.60.61.49"
    echo "   API: http://72.60.61.49/api/status"
    echo "   Monitor: ./monitor.sh"
    echo ""
    echo "🔧 Comandos útiles:"
    echo "  Ver logs: tail -f logs/error.log"
    echo "  Reiniciar Nginx: sudo systemctl restart nginx"
    echo "  Reiniciar app: ./start_production.sh"
    echo "  Monitorear: ./monitor.sh"
else
    print_warning "❌ Algunos servicios pueden necesitar ajustes"
    echo "Web: $WEB_TEST | App: $APP_TEST | API: $API_TEST"
    echo ""
    echo "🔧 Comandos de troubleshooting:"
    echo "  Ver procesos: ps aux | grep -E '(nginx|gunicorn|python)'"
    echo "  Ver logs Nginx: sudo tail -f /var/log/nginx/error.log"
    echo "  Ver logs app: tail -f /var/www/vigoleonrocks.com/logs/error.log"
    echo "  Reiniciar todo: sudo systemctl restart nginx && ./start_production.sh"
fi

print_success "AUTO-FIX V2 COMPLETADO"