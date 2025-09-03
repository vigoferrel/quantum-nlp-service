#!/usr/bin/env python3
"""
Script de Deployment Simplificado al VPS
VIGOLEONROCKS.COM - Sistema Python Flask Multilingüe
"""

import os
import subprocess
import time

# Configuración del VPS
VPS_CONFIG = {
    'hostname': 'srv984842.hstgr.cloud',
    'ip': '72.60.61.49',
    'username': 'root',
    'deploy_dir': '/var/www/vigoleonrocks.com'
}

def deploy_to_vps():
    """Deployment simplificado al VPS"""
    print("🚀 DEPLOYMENT SIMPLIFICADO AL VPS VIGOLEONROCKS.COM")
    print("=" * 60)
    print(f"🌍 Ubicación: Brazil - São Paulo")
    print(f"🖥️ Sistema: Ubuntu 24.04 with Dokploy")
    print(f"🏠 Hostname: {VPS_CONFIG['hostname']}")
    print(f"🌐 IP: {VPS_CONFIG['ip']}")
    print(f"👤 Usuario: {VPS_CONFIG['username']}")
    print("=" * 60)
    
    # Verificar archivos necesarios
    print("\n📦 VERIFICANDO ARCHIVOS:")
    print("-" * 40)
    
    required_files = [
        "vigoleonrocks_server.py",
        "requirements.txt",
        ".htaccess",
        "start_vigoleonrocks.sh",
        "vigoleonrocks.conf",
        "index.html"
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NO ENCONTRADO")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Archivos faltantes: {missing_files}")
        print("Ejecuta primero: python deploy_vigoleonrocks_com.py")
        return False
    
    # Subir archivos con SCP
    print("\n📤 SUBIENDO ARCHIVOS AL VPS:")
    print("-" * 40)
    
    for file in required_files:
        print(f"🔄 Subiendo {file}...")
        scp_command = f"scp {file} {VPS_CONFIG['username']}@{VPS_CONFIG['hostname']}:{VPS_CONFIG['deploy_dir']}/"
        
        try:
            result = subprocess.run(scp_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {file} subido exitosamente")
            else:
                print(f"❌ Error subiendo {file}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error en SCP: {e}")
    
    # Comandos SSH para configurar el servidor
    print("\n🔧 COMANDOS SSH PARA EJECUTAR:")
    print("-" * 40)
    
    ssh_commands = [
        f"ssh {VPS_CONFIG['username']}@{VPS_CONFIG['hostname']}",
        "",
        "# Una vez conectado al VPS, ejecuta estos comandos:",
        "",
        "# 1. Preparar el servidor",
        "apt-get update && apt-get upgrade -y",
        "apt-get install -y python3 python3-pip python3-venv apache2 supervisor curl",
        f"mkdir -p {VPS_CONFIG['deploy_dir']}",
        f"cd {VPS_CONFIG['deploy_dir']}",
        "",
        "# 2. Configurar permisos",
        "chmod +x start_vigoleonrocks.sh",
        "chown -R www-data:www-data .",
        "chmod -R 755 .",
        "",
        "# 3. Instalar dependencias Python",
        "pip3 install -r requirements.txt",
        "",
        "# 4. Configurar supervisor",
        "cp vigoleonrocks.conf /etc/supervisor/conf.d/",
        "supervisorctl reread",
        "supervisorctl update",
        "supervisorctl start vigoleonrocks",
        "",
        "# 5. Configurar Apache",
        "a2enmod proxy",
        "a2enmod proxy_http",
        "a2enmod rewrite",
        "systemctl restart apache2",
        "",
        "# 6. Verificar deployment",
        "supervisorctl status vigoleonrocks",
        "curl http://localhost:5000/api/status",
        "netstat -tlnp | grep :5000"
    ]
    
    for cmd in ssh_commands:
        print(cmd)
    
    print("\n🌐 URLs DE VERIFICACIÓN:")
    print("-" * 40)
    print("https://vigoleonrocks.com/")
    print("https://vigoleonrocks.com/api/status")
    print("https://vigoleonrocks.com/api/vigoleonrocks")
    
    return True

def create_deployment_script():
    """Crear script de deployment para ejecutar en el VPS"""
    print("\n📝 CREANDO SCRIPT DE DEPLOYMENT:")
    print("-" * 40)
    
    script_content = f"""#!/bin/bash
# VIGOLEONROCKS.COM - Script de Deployment
echo "🚀 VIGOLEONROCKS.COM - DEPLOYMENT SCRIPT"
echo "=========================================="

# 1. Preparar el servidor
echo "📦 Preparando servidor..."
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv apache2 supervisor curl

# 2. Crear directorio
echo "📁 Creando directorio..."
mkdir -p {VPS_CONFIG['deploy_dir']}
cd {VPS_CONFIG['deploy_dir']}

# 3. Configurar permisos
echo "🔧 Configurando permisos..."
chmod +x start_vigoleonrocks.sh
chown -R www-data:www-data .
chmod -R 755 .

# 4. Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
pip3 install -r requirements.txt

# 5. Configurar supervisor
echo "⚙️ Configurando supervisor..."
cp vigoleonrocks.conf /etc/supervisor/conf.d/
supervisorctl reread
supervisorctl update
supervisorctl start vigoleonrocks

# 6. Configurar Apache
echo "🌐 Configurando Apache..."
a2enmod proxy
a2enmod proxy_http
a2enmod rewrite
systemctl restart apache2

# 7. Verificar deployment
echo "🔍 Verificando deployment..."
sleep 5
supervisorctl status vigoleonrocks
curl -s http://localhost:5000/api/status
netstat -tlnp | grep :5000

echo "🎉 DEPLOYMENT COMPLETADO!"
echo "🌐 URLs:"
echo "   https://vigoleonrocks.com/"
echo "   https://vigoleonrocks.com/api/status"
"""
    
    with open("deploy_vps.sh", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ deploy_vps.sh creado")
    print("📋 Para ejecutar en el VPS:")
    print(f"   scp deploy_vps.sh {VPS_CONFIG['username']}@{VPS_CONFIG['hostname']}:/tmp/")
    print(f"   ssh {VPS_CONFIG['username']}@{VPS_CONFIG['hostname']}")
    print("   chmod +x /tmp/deploy_vps.sh")
    print("   /tmp/deploy_vps.sh")

if __name__ == "__main__":
    print("🚀 VPS DEPLOYMENT SIMPLIFICADO - VIGOLEONROCKS.COM")
    print("=" * 60)
    
    # Ejecutar deployment
    deploy_to_vps()
    
    # Crear script de deployment
    create_deployment_script()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Ejecutar los comandos SCP mostrados arriba")
    print("2. Conectar al VPS via SSH")
    print("3. Ejecutar los comandos de configuración")
    print("4. Verificar las URLs de funcionamiento")
