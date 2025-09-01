#!/usr/bin/env python3
"""
Script de Deployment para vigoleonrocks.com
Sistema VIGOLEONROCKS Multilingüe Global - SOLO PYTHON
"""

import os
import subprocess
import requests
import json
from datetime import datetime

def deploy_to_vigoleonrocks_com():
    """Deployment completo a vigoleonrocks.com - SOLO PYTHON"""
    print("🚀 DEPLOYMENT A VIGOLEONROCKS.COM - SOLO PYTHON")
    print("=" * 60)
    
    # 1. Verificar configuración actual
    print("\n📊 VERIFICANDO SITIO ACTUAL:")
    print("-" * 40)
    
    try:
        # Verificar el sitio actual
        response = requests.get("https://vigoleonrocks.com/", timeout=10)
        print(f"✅ Sitio accesible: {response.status_code}")
        print("🔄 Reemplazando sistema PHP con Python Flask")
                
    except Exception as e:
        print(f"❌ Error verificando sitio: {e}")
    
    # 2. Preparar archivos para deployment
    print("\n📦 PREPARANDO ARCHIVOS PYTHON:")
    print("-" * 40)
    
    files_to_deploy = [
        "vigoleonrocks_server.py",
        "requirements.txt", 
        "Dockerfile",
        ".dockerignore",
        "README.md"
    ]
    
    for file in files_to_deploy:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NO ENCONTRADO")
    
    # 3. Crear configuración de servidor web para Python
    print("\n🌐 CONFIGURACIÓN DE SERVIDOR WEB - PYTHON:")
    print("-" * 40)
    
    # Crear archivo .htaccess para redirección completa a Python
    htaccess_content = """
# VIGOLEONROCKS - Configuración de Servidor Web - SOLO PYTHON
RewriteEngine On

# Redirigir TODO a Python Flask
RewriteRule ^(.*)$ http://localhost:5000/$1 [P,L]

# Headers para Python
ProxyPreserveHost On
ProxyPass / http://localhost:5000/
ProxyPassReverse / http://localhost:5000/
"""
    
    with open(".htaccess", "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    print("✅ .htaccess creado (solo Python)")
    
    # 4. Crear script de inicio del servidor Python
    startup_script = """#!/bin/bash
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
"""
    
    with open("start_vigoleonrocks.sh", "w", encoding="utf-8") as f:
        f.write(startup_script)
    print("✅ start_vigoleonrocks.sh creado")
    
    # 5. Crear archivo de configuración de supervisor
    supervisor_config = """[program:vigoleonrocks]
command=python3 /var/www/vigoleonrocks.com/vigoleonrocks_server.py
directory=/var/www/vigoleonrocks.com
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/vigoleonrocks.log
environment=FLASK_ENV="production"
"""
    
    with open("vigoleonrocks.conf", "w", encoding="utf-8") as f:
        f.write(supervisor_config)
    print("✅ vigoleonrocks.conf creado")
    
    # 6. Instrucciones de deployment
    print("\n📋 INSTRUCCIONES DE DEPLOYMENT - SOLO PYTHON:")
    print("-" * 40)
    print("1. Subir archivos al servidor:")
    print("   - vigoleonrocks_server.py")
    print("   - requirements.txt")
    print("   - .htaccess")
    print("   - start_vigoleonrocks.sh")
    print("   - vigoleonrocks.conf")
    print("")
    print("2. En el servidor web:")
    print("   chmod +x start_vigoleonrocks.sh")
    print("   pip3 install -r requirements.txt")
    print("   ./start_vigoleonrocks.sh")
    print("")
    print("3. Configurar supervisor:")
    print("   sudo cp vigoleonrocks.conf /etc/supervisor/conf.d/")
    print("   sudo supervisorctl reread")
    print("   sudo supervisorctl update")
    print("   sudo supervisorctl start vigoleonrocks")
    print("")
    print("4. Verificar APIs Python:")
    print("   https://vigoleonrocks.com/api/status")
    print("   https://vigoleonrocks.com/api/vigoleonrocks")
    print("   https://vigoleonrocks.com/")
    
    return True

def create_deployment_package():
    """Crear paquete de deployment"""
    print("\n📦 CREANDO PAQUETE DE DEPLOYMENT:")
    print("-" * 40)
    
    # Crear directorio de deployment
    deploy_dir = "deployment_vigoleonrocks_com"
    if not os.path.exists(deploy_dir):
        os.makedirs(deploy_dir)
    
    # Archivos a incluir
    files = [
        "vigoleonrocks_server.py",
        "requirements.txt",
        ".htaccess", 
        "start_vigoleonrocks.sh",
        "vigoleonrocks.conf",
        "README.md"
    ]
    
    for file in files:
        if os.path.exists(file):
            import shutil
            shutil.copy2(file, deploy_dir)
            print(f"✅ {file} -> {deploy_dir}/")
    
    print(f"\n📦 Paquete creado en: {deploy_dir}/")
    print("📋 Lista de archivos:")
    for file in os.listdir(deploy_dir):
        print(f"   📄 {file}")
    
    return deploy_dir

def create_index_html():
    """Crear página principal HTML para Python"""
    print("\n🌐 CREANDO PÁGINA PRINCIPAL HTML:")
    print("-" * 40)
    
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 VIGOLEONROCKS - Sistema de IA Multilingüe</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status {
            background: rgba(0,255,0,0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .api-test {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #45a049;
        }
        .result {
            background: rgba(0,0,0,0.5);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 VIGOLEONROCKS</h1>
        <div class="status">
            <h2>✅ Sistema de IA Multilingüe Operativo</h2>
            <p>Python Flask Server - 12 Idiomas Soportados</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h3>🌍 Multilingüe</h3>
                <p>12 idiomas: ES, EN, PT, FR, DE, IT, ZH, JA, KO, RU, AR, HI, NL</p>
            </div>
            <div class="feature">
                <h3>🧠 IA Humana</h3>
                <p>Respuestas naturales y empáticas en todos los idiomas</p>
            </div>
            <div class="feature">
                <h3>⚡ Quantum</h3>
                <p>26 estados cuánticos simultáneos - Supremacy Score: 0.998</p>
            </div>
        </div>
        
        <div class="api-test">
            <h3>🧪 Probar APIs</h3>
            <button onclick="testStatus()">Test Status API</button>
            <button onclick="testLanguage()">Test Language Detection</button>
            <button onclick="testResponse()">Test Human Response</button>
            <div id="result" class="result"></div>
        </div>
    </div>

    <script>
        async function testStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<strong>Status API:</strong><br>' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
            }
        }
        
        async function testLanguage() {
            try {
                const response = await fetch('/api/detect-language', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: 'Hola mundo'})
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<strong>Language Detection:</strong><br>' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
            }
        }
        
        async function testResponse() {
            try {
                const response = await fetch('/api/vigoleonrocks', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: 'Hola', language: 'es'})
                });
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    '<strong>Human Response:</strong><br>' + JSON.stringify(data, null, 2);
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html creado")
    
    return "index.html"

if __name__ == "__main__":
    print("🚀 VIGOLEONROCKS.COM DEPLOYMENT SCRIPT - SOLO PYTHON")
    print("=" * 60)
    
    # Ejecutar deployment
    deploy_to_vigoleonrocks_com()
    
    # Crear página principal
    create_index_html()
    
    # Crear paquete
    package_dir = create_deployment_package()
    
    print(f"\n🎉 DEPLOYMENT PREPARADO - SOLO PYTHON!")
    print(f"📦 Paquete listo en: {package_dir}/")
    print("🌐 Sube estos archivos a tu servidor web")
    print("🔗 Dominio: https://vigoleonrocks.com/")
    print("🐍 Sistema: 100% Python Flask Multilingüe")
