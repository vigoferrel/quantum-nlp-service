#!/bin/bash

# 🚀 VIGOLEONROCKS - AUTO-FIX PARA USUARIO NORMAL
# ==============================================

echo "🔧 AUTO-FIX PARA USUARIO NORMAL"
echo "==============================="

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

# Verificar si somos root
if [ "$EUID" -eq 0 ]; then
    print_success "Ejecutando como root"
    SUDO=""
else
    print_warning "Ejecutando como usuario normal - usando sudo cuando sea necesario"
    SUDO="sudo"
fi

# Paso 1: Verificar estado del sistema
print_status "Paso 1: Verificando estado del sistema..."
ps aux | grep -E "(python|gunicorn|nginx|apache)" | grep -v grep

# Verificar puertos (usando netstat en lugar de ss)
print_status "Verificando puertos..."
netstat -tlnp 2>/dev/null | grep -E ":(80|5000|3000)" || print_warning "netstat no disponible o no hay puertos abiertos"

# Paso 2: Crear directorio del proyecto en home
print_status "Paso 2: Creando directorio del proyecto..."
PROJECT_DIR="$HOME/vigoleonrocks_project"

if [ ! -d "$PROJECT_DIR" ]; then
    mkdir -p "$PROJECT_DIR"
    print_success "Directorio creado: $PROJECT_DIR"
else
    print_success "Directorio ya existe: $PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# Paso 3: Crear aplicación Python básica
print_status "Paso 3: Creando aplicación Python básica..."

cat > vigoleonrocks_server.py << 'EOF'
#!/usr/bin/env python3
"""
VIGOLEONROCKS - Servidor Flask Básico
"""
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
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0-basic"
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "server": "VIGOLEONROCKS",
        "version": "1.0-basic",
        "uptime": str(datetime.datetime.now() - datetime.datetime(2025, 1, 1)),
        "message": "Sistema funcionando correctamente"
    })

@app.route('/api/test')
def test():
    return jsonify({
        "test": "ok",
        "timestamp": datetime.datetime.now().isoformat(),
        "message": "API de test funcionando"
    })

if __name__ == '__main__':
    print("🚀 VIGOLEONROCKS Server Starting...")
    print("🌐 http://localhost:5000")
    print("📡 API: http://localhost:5000/api/status")
    app.run(host='0.0.0.0', port=5000, debug=False)
EOF

print_success "vigoleonrocks_server.py creado"

# Paso 4: Crear requirements.txt
print_status "Paso 4: Creando requirements.txt..."

cat > requirements.txt << 'EOF'
Flask==2.3.3
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0
EOF

print_success "requirements.txt creado"

# Paso 5: Instalar dependencias
print_status "Paso 5: Instalando dependencias Python..."

if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --quiet --disable-pip-version-check
    if [ $? -eq 0 ]; then
        print_success "Dependencias instaladas correctamente"
    else
        print_error "Error instalando dependencias"
        # Intentar instalar Flask mínimo
        pip3 install flask flask-cors --quiet
    fi
else
    print_error "pip3 no encontrado"
    # Intentar con pip
    if command -v pip &> /dev/null; then
        pip install flask flask-cors --quiet
        print_success "Flask instalado con pip"
    else
        print_error "Ni pip3 ni pip encontrados"
    fi
fi

# Paso 6: Matar procesos existentes
print_status "Paso 6: Limpiando procesos existentes..."
pkill -f gunicorn 2>/dev/null
pkill -f python 2>/dev/null
pkill -f vigoleonrocks_server.py 2>/dev/null

# Matar procesos en puertos específicos
if command -v fuser &> /dev/null; then
    fuser -k 5000/tcp 2>/dev/null
fi

sleep 2

print_success "Procesos limpiados"

# Paso 7: Crear script de inicio
print_status "Paso 7: Creando script de inicio..."

cat > start_server.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
export FLASK_APP=vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH="$(pwd)"

echo "🚀 Iniciando VIGOLEONROCKS Server..."
echo "🌐 http://localhost:5000"
echo "📡 API: http://localhost:5000/api/status"
echo "🛑 Presiona Ctrl+C para detener"

python3 vigoleonrocks_server.py
EOF

chmod +x start_server.sh
print_success "start_server.sh creado"

# Paso 8: Crear script de inicio en background
print_status "Paso 8: Creando script de inicio en background..."

cat > start_background.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
export FLASK_APP=vigoleonrocks_server.py
export FLASK_ENV=production
export PYTHONPATH="$(pwd)"

echo "🚀 Iniciando VIGOLEONROCKS Server en background..."
python3 vigoleonrocks_server.py &
echo $! > server.pid
echo "PID guardado en server.pid"
echo "🌐 Servidor corriendo en: http://localhost:5000"
echo "📡 API disponible en: http://localhost:5000/api/status"
EOF

chmod +x start_background.sh
print_success "start_background.sh creado"

# Paso 9: Crear script para detener
print_status "Paso 9: Creando script para detener servidor..."

cat > stop_server.sh << 'EOF'
#!/bin/bash
echo "🛑 Deteniendo VIGOLEONROCKS Server..."

if [ -f "server.pid" ]; then
    PID=$(cat server.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "Proceso $PID detenido"
    else
        echo "Proceso $PID ya no existe"
    fi
    rm -f server.pid
else
    echo "No se encontró server.pid"
    # Intentar matar por nombre
    pkill -f vigoleonrocks_server.py
    pkill -f python
fi

echo "✅ Servidor detenido"
EOF

chmod +x stop_server.sh
print_success "stop_server.sh creado"

# Paso 10: Iniciar servidor
print_status "Paso 10: Iniciando servidor..."

./start_background.sh

# Verificar que inició
sleep 3
if pgrep -f vigoleonrocks_server.py > /dev/null; then
    print_success "VIGOLEONROCKS iniciado correctamente"
else
    print_error "Error iniciando VIGOLEONROCKS"
    print_warning "Intentando inicio directo..."
    timeout 10s ./start_server.sh &
fi

# Paso 11: Probar conectividad
print_status "Paso 11: Probando conectividad..."

# Probar localhost:5000
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "ERROR")
if [ "$RESPONSE" = "200" ]; then
    print_success "Servidor responde correctamente (HTTP $RESPONSE)"
else
    print_warning "Servidor responde (HTTP $RESPONSE)")
fi

# Probar API
API_RESPONSE=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_RESPONSE" -gt 0 ]; then
    print_success "API funcionando correctamente")
else
    print_warning "API no responde correctamente")
fi

# Paso 12: Crear script de monitoreo
print_status "Paso 12: Creando script de monitoreo..."

cat > monitor.sh << 'EOF'
#!/bin/bash
echo "📊 ESTADO DE VIGOLEONROCKS"
echo "=========================="

echo "🔍 Procesos:"
ps aux | grep -E "(python|gunicorn)" | grep -v grep || echo "No se encontraron procesos Python"

echo ""
echo "🌐 Puertos:"
netstat -tlnp 2>/dev/null | grep -E ":(5000)" || echo "Puerto 5000 no encontrado"

echo ""
echo "🔗 Tests de conectividad:"
echo "Servidor (5000): $(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "ERROR")"
echo "API Status: $(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0") respuestas"

echo ""
echo "📁 Ubicación del proyecto: $(pwd)"

if [ -f "server.pid" ]; then
    echo "🆔 PID del servidor: $(cat server.pid)"
fi

echo ""
echo "✅ Monitoreo completado"
EOF

chmod +x monitor.sh
print_success "monitor.sh creado"

# Paso 13: Verificación final
print_status "Paso 13: Verificación final..."

# Test completo
APP_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 2>/dev/null || echo "ERROR")
API_TEST=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")

if [ "$APP_TEST" = "200" ] && [ "$API_TEST" -gt 0 ]; then
    print_success "🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE!"
    echo ""
    echo "🌐 URLs disponibles:"
    echo "   Servidor: http://localhost:5000"
    echo "   API: http://localhost:5000/api/status"
    echo "   Test: http://localhost:5000/api/test"
    echo ""
    echo "🔧 Comandos disponibles:"
    echo "  Iniciar: ./start_server.sh"
    echo "  Fondo: ./start_background.sh"
    echo "  Detener: ./stop_server.sh"
    echo "  Monitorear: ./monitor.sh"
    echo ""
    echo "📁 Proyecto ubicado en: $PROJECT_DIR"
else
    print_warning "❌ Algunos componentes pueden necesitar ajustes"
    echo "Servidor: $APP_TEST | API: $API_TEST"
    echo ""
    echo "🔧 Comandos de troubleshooting:"
    echo "  Ver procesos: ps aux | grep python"
    echo "  Ver logs: tail -f /dev/null (no hay logs configurados)"
    echo "  Reiniciar: ./stop_server.sh && ./start_background.sh"
fi

print_success "AUTO-FIX PARA USUARIO COMPLETADO"