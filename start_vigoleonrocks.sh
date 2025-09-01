#!/bin/bash
# VIGOLEONROCKS Startup Script - SOLO PYTHON
cd /var/www/vigoleonrocks.com

# Detener procesos PHP existentes (opcional)
pkill -f php || true

# Instalar dependencias Python
pip3 install -r requirements.txt

# Iniciar servidor Python Flask
python3 vigoleonrocks_server.py &
echo "VIGOLEONROCKS Python Server iniciado en puerto 5000"

# Verificar que el servidor esté funcionando
sleep 3
curl -s http://localhost:5000/api/status > /dev/null && echo "✅ Servidor Python funcionando" || echo "❌ Error iniciando servidor"
