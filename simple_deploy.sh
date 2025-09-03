#!/bin/bash

echo "🚀 DEPLOYMENT SENCILLO VIGOLEONROCKS"
echo "==================================="

# Verificar archivos
echo "📁 Verificando archivos..."
ls -la

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt --quiet

# Matar procesos existentes
echo "🛑 Limpiando procesos..."
pkill -f gunicorn
pkill -f python
pkill -f vigoleonrocks_server.py

sleep 2

# Iniciar aplicación
echo "🚀 Iniciando VIGOLEONROCKS..."
python3 vigoleonrocks_server.py &
echo $! > server.pid

# Verificar que inició
sleep 3
if pgrep -f vigoleonrocks_server.py > /dev/null; then
    echo "✅ VIGOLEONROCKS iniciado correctamente"
else
    echo "❌ Error iniciando VIGOLEONROCKS"
fi

# Test de conectividad
echo "🔗 Probando conectividad..."
curl -s http://localhost:5000/api/status

echo ""
echo "🌐 URLs disponibles:"
echo "   API: http://localhost:5000/api/status"
echo "   Web: http://localhost:5000"
echo ""
echo "✅ DEPLOYMENT COMPLETADO"