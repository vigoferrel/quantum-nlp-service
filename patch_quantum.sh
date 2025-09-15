#!/bin/bash
# Script para añadir la ruta /quantum a simple_api.py

echo "🔧 Aplicando patch para añadir ruta /quantum..."

# Backup del archivo original
cp /app/simple_api.py /app/simple_api.py.bak

# Usar sed para añadir el handler de /quantum después de la línea que contiene '/api/status'
sed -i '/elif path == "\/api\/status":/a\
        elif path == "/quantum":\
            try:\
                with open("/app/vigoleonrocks_quantum_command_center.html", "r", encoding="utf-8") as f:\
                    html_content = f.read()\
                self.send_response(200)\
                self.send_header("Content-type", "text/html; charset=utf-8")\
                self.end_headers()\
                self.wfile.write(html_content.encode("utf-8"))\
            except FileNotFoundError:\
                fallback_html = """<!DOCTYPE html><html><head><title>VIGOLEONROCKS Quantum Command Center</title><meta charset="utf-8"><style>body { font-family: Arial, sans-serif; margin: 40px; background: #0a0a0a; color: #00ff00; } h1 { color: #00ffff; } .loading { animation: blink 1s infinite; } @keyframes blink { 50% { opacity: 0.5; } }</style></head><body><h1>🎯 VIGOLEONROCKS Quantum Command Center</h1><p class="loading">⚡ Sistema cuántico inicializando...</p><p>🔧 Frontend completo en desarrollo</p><p><a href="/" style="color: #00ff00;">← Volver al API principal</a></p></body></html>"""\
                self.send_response(200)\
                self.send_header("Content-type", "text/html; charset=utf-8")\
                self.end_headers()\
                self.wfile.write(fallback_html.encode("utf-8"))' /app/simple_api.py

# También añadir el enlace en la página principal
sed -i 's|<li><code>/api/connect?token=TOKEN|<li><code>/quantum</code> - Quantum Command Center</li>\n                    <li><code>/api/connect?token=TOKEN|' /app/simple_api.py

echo "✅ Patch aplicado exitosamente"
echo "🔄 Reiniciando servidor..."

# Encontrar y matar el proceso Python existente
pkill -f "python.*simple_api.py" || true
sleep 2

# Reiniciar el servidor en background
nohup python /app/simple_api.py --background > /dev/null 2>&1 &

echo "🚀 Servidor reiniciado con ruta /quantum disponible"
