#!/bin/bash

# 🚀 VIGOLEONROCKS - AUTO-FIX DEPLOYMENT
# ======================================

echo "🔧 AUTO-FIX DEPLOYMENT VIGOLEONROCKS"
echo "===================================="

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

# Paso 1: Verificar estado del sistema
print_status "Paso 1: Verificando estado del sistema..."
ps aux | grep -E "(python|gunicorn|nginx|apache)" | grep -v grep

# Verificar puertos
print_status "Verificando puertos..."
netstat -tlnp | grep -E ":(80|5000|3000)"

# Paso 2: Verificar archivos del proyecto
print_status "Paso 2: Verificando archivos del proyecto..."
if [ -f "/var/www/vigoleonrocks.com/vigoleonrocks_server.py" ]; then
    print_success "vigoleonrocks_server.py encontrado"
else
    print_error "vigoleonrocks_server.py NO encontrado"
fi

if [ -f "/var/www/vigoleonrocks.com/requirements.txt" ]; then
    print_success "requirements.txt encontrado"
else
    print_error "requirements.txt NO encontrado"
fi

# Paso 3: Instalar dependencias si es necesario
print_status "Paso 3: Verificando dependencias Python..."
cd /var/www/vigoleonrocks.com

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas correctamente"
    else
        print_error "Error instalando dependencias"
    fi
else
    print_error "requirements.txt no encontrado"
fi

# Paso 4: Matar procesos existentes
print_status "Paso 4: Limpiando procesos existentes..."
pkill -f gunicorn
pkill -f python
pkill -f vigoleonrocks_server.py

sleep 2

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

# Paso 5: Verificar y configurar Nginx
print_status "Paso 5: Verificando Nginx..."

# Verificar si Nginx está instalado
if ! command -v nginx &> /dev/null; then
    print_warning "Nginx no está instalado, instalando..."
    apt update && apt install -y nginx
fi

# Crear configuración de Nginx
sudo tee /etc/nginx/sites-available/vigoleonrocks > /dev/null <<EOF
server {
    listen 80;
    server_name 72.60.61.49;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api {
        proxy_pass http://localhost:5000/api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Habilitar sitio
sudo ln -sf /etc/nginx/sites-available/vigoleonrocks /etc/nginx/sites-enabled/

# Remover configuración por defecto
sudo rm -f /etc/nginx/sites-enabled/default

# Probar configuración
sudo nginx -t
if [ $? -eq 0 ]; then
    print_success "Configuración de Nginx correcta"
    sudo systemctl restart nginx
    print_success "Nginx reiniciado"
else
    print_error "Error en configuración de Nginx"
fi

# Paso 6: Iniciar aplicación Python
print_status "Paso 6: Iniciando aplicación VIGOLEONROCKS..."

cd /var/www/vigoleonrocks.com

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
sleep 3
if pgrep -f gunicorn > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente"
else
    print_error "Error iniciando VIGOLEONROCKS"
    # Intentar inicio directo
    print_warning "Intentando inicio directo..."
    python3 vigoleonrocks_server.py &
    sleep 3
    if pgrep -f vigoleonrocks_server.py > /dev/null; then
        print_success "VIGOLEONROCKS iniciado en modo directo"
    else
        print_error "No se pudo iniciar la aplicación"
    fi
fi

# Paso 7: Verificar servicios
print_status "Paso 7: Verificando servicios..."

# Verificar Nginx
if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx está activo"
else
    print_error "Nginx no está activo"
    sudo systemctl start nginx
fi

# Verificar aplicación
if pgrep -f gunicorn > /dev/null || pgrep -f vigoleonrocks_server.py > /dev/null; then
    print_success "Aplicación Python está corriendo"
else
    print_error "Aplicación Python no está corriendo"
fi

# Paso 8: Probar conectividad
print_status "Paso 8: Probando conectividad..."

# Probar localhost
curl -s -o /dev/null -w "Localhost: %{http_code}\n" http://localhost

# Probar localhost:5000
curl -s -o /dev/null -w "Python App: %{http_code}\n" http://localhost:5000

# Probar API
curl -s http://localhost:5000/api/status | head -3

# Paso 9: Configurar firewall
print_status "Paso 9: Configurando firewall..."
sudo ufw allow 80
sudo ufw allow 5000
sudo ufw --force enable

# Paso 10: Crear script de monitoreo
print_status "Paso 10: Creando script de monitoreo..."
cat > monitor.sh << 'EOF'
#!/bin/bash
echo "📊 ESTADO DEL SISTEMA VIGOLEONROCKS"
echo "==================================="

echo "🔍 Procesos:"
ps aux | grep -E "(nginx|gunicorn|python)" | grep -v grep

echo ""
echo "🌐 Puertos:"
netstat -tlnp | grep -E ":(80|5000)"

echo ""
echo "🔗 Tests:"
echo "Nginx (80): $(curl -s -o /dev/null -w "%{http_code}" http://localhost)"
echo "App (5000): $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)"
echo "API Status: $(curl -s http://localhost:5000/api/status | grep -c "status") respuestas"

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x monitor.sh

# Paso 11: Verificación final
print_status "Paso 11: Verificación final..."

# Test completo
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost)
APP_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000)
API_TEST=$(curl -s http://localhost:5000/api/status | grep -c "status")

if [ "$WEB_TEST" = "200" ] && [ "$APP_TEST" = "200" ] && [ "$API_TEST" -gt 0 ]; then
    print_success "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE!"
    echo ""
    echo "🌐 URLs disponibles:"
    echo "   Web: http://72.60.61.49"
    echo "   API: http://72.60.61.49/api/status"
    echo "   Monitor: ./monitor.sh"
else
    print_error "❌ Algunos servicios no funcionan correctamente"
    echo "Web: $WEB_TEST | App: $APP_TEST | API: $API_TEST"
fi

echo ""
echo "🔧 Comandos útiles:"
echo "  Ver logs: tail -f logs/error.log"
echo "  Reiniciar Nginx: sudo systemctl restart nginx"
echo "  Reiniciar app: ./start_production.sh"
echo "  Monitorear: ./monitor.sh"

print_success "AUTO-FIX COMPLETADO"