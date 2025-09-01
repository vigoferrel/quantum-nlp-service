#!/usr/bin/env python3
"""
Script de Deployment Directo al VPS
VIGOLEONROCKS.COM - Sistema Python Flask Multilingüe
"""

import os
import subprocess
import paramiko
import time
from datetime import datetime

# Configuración del VPS
VPS_CONFIG = {
    'hostname': 'srv984842.hstgr.cloud',
    'ip': '72.60.61.49',
    'username': 'root',
    'port': 22,
    'deploy_dir': '/var/www/vigoleonrocks.com'
}

def deploy_to_vps():
    """Deployment directo al VPS"""
    print("🚀 DEPLOYMENT DIRECTO AL VPS VIGOLEONROCKS.COM")
    print("=" * 60)
    print(f"🌍 Ubicación: Brazil - São Paulo")
    print(f"🖥️ Sistema: Ubuntu 24.04 with Dokploy")
    print(f"🏠 Hostname: {VPS_CONFIG['hostname']}")
    print(f"🌐 IP: {VPS_CONFIG['ip']}")
    print(f"👤 Usuario: {VPS_CONFIG['username']}")
    print("=" * 60)
    
    # Solicitar contraseña SSH
    print("\n🔐 CONFIGURACIÓN SSH:")
    print("-" * 40)
    password = input("Ingresa la contraseña SSH del VPS: ")
    
    try:
        # Conectar al VPS
        print("\n🔗 CONECTANDO AL VPS...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            VPS_CONFIG['hostname'],
            port=VPS_CONFIG['port'],
            username=VPS_CONFIG['username'],
            password=password,
            timeout=30
        )
        
        print("✅ Conexión SSH establecida")
        
        # Crear directorio de deployment
        print("\n📁 PREPARANDO DIRECTORIO...")
        commands = [
            f"mkdir -p {VPS_CONFIG['deploy_dir']}",
            f"cd {VPS_CONFIG['deploy_dir']}",
            "pwd"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode().strip()
            if cmd.startswith("pwd"):
                print(f"✅ Directorio: {result}")
        
        # Subir archivos
        print("\n📤 SUBIENDO ARCHIVOS...")
        sftp = ssh.open_sftp()
        
        files_to_upload = [
            "vigoleonrocks_server.py",
            "requirements.txt",
            ".htaccess",
            "start_vigoleonrocks.sh",
            "vigoleonrocks.conf",
            "index.html"
        ]
        
        for file in files_to_upload:
            if os.path.exists(file):
                remote_path = f"{VPS_CONFIG['deploy_dir']}/{file}"
                sftp.put(file, remote_path)
                print(f"✅ {file} -> {remote_path}")
            else:
                print(f"❌ {file} - NO ENCONTRADO")
        
        sftp.close()
        
        # Configurar permisos
        print("\n🔧 CONFIGURANDO PERMISOS...")
        commands = [
            f"chmod +x {VPS_CONFIG['deploy_dir']}/start_vigoleonrocks.sh",
            f"chown -R www-data:www-data {VPS_CONFIG['deploy_dir']}",
            f"chmod -R 755 {VPS_CONFIG['deploy_dir']}"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(f"✅ {cmd}")
        
        # Instalar dependencias Python
        print("\n🐍 INSTALANDO DEPENDENCIAS PYTHON...")
        commands = [
            "apt-get update",
            "apt-get install -y python3 python3-pip python3-venv",
            f"cd {VPS_CONFIG['deploy_dir']}",
            "pip3 install -r requirements.txt"
        ]
        
        for cmd in commands:
            print(f"🔄 Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(f"✅ {cmd}")
            else:
                error = stderr.read().decode()
                print(f"❌ Error en {cmd}: {error}")
        
        # Configurar supervisor
        print("\n⚙️ CONFIGURANDO SUPERVISOR...")
        commands = [
            "apt-get install -y supervisor",
            f"cp {VPS_CONFIG['deploy_dir']}/vigoleonrocks.conf /etc/supervisor/conf.d/",
            "supervisorctl reread",
            "supervisorctl update",
            "supervisorctl start vigoleonrocks"
        ]
        
        for cmd in commands:
            print(f"🔄 Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(f"✅ {cmd}")
            else:
                error = stderr.read().decode()
                print(f"⚠️ {cmd}: {error}")
        
        # Verificar estado del servidor
        print("\n🔍 VERIFICANDO ESTADO DEL SERVIDOR...")
        time.sleep(5)  # Esperar a que el servidor inicie
        
        commands = [
            "supervisorctl status vigoleonrocks",
            "curl -s http://localhost:5000/api/status",
            "netstat -tlnp | grep :5000"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.read().decode().strip()
            print(f"📊 {cmd}:")
            print(f"   {result}")
        
        # Configurar Apache/Nginx (si es necesario)
        print("\n🌐 CONFIGURANDO SERVIDOR WEB...")
        commands = [
            "apt-get install -y apache2",
            "a2enmod proxy",
            "a2enmod proxy_http",
            "a2enmod rewrite",
            "systemctl restart apache2"
        ]
        
        for cmd in commands:
            print(f"🔄 Ejecutando: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print(f"✅ {cmd}")
            else:
                error = stderr.read().decode()
                print(f"⚠️ {cmd}: {error}")
        
        ssh.close()
        
        print("\n🎉 DEPLOYMENT COMPLETADO!")
        print("=" * 60)
        print("🌐 URLs de Verificación:")
        print(f"   https://vigoleonrocks.com/")
        print(f"   https://vigoleonrocks.com/api/status")
        print(f"   https://vigoleonrocks.com/api/vigoleonrocks")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error en deployment: {e}")
        return False
    
    return True

def create_ssh_key_deployment():
    """Crear deployment con clave SSH"""
    print("\n🔑 DEPLOYMENT CON CLAVE SSH:")
    print("-" * 40)
    print("Para deployment automático, crea una clave SSH:")
    print("1. ssh-keygen -t rsa -b 4096")
    print("2. ssh-copy-id root@srv984842.hstgr.cloud")
    print("3. Ejecuta el script de deployment")

if __name__ == "__main__":
    print("🚀 VPS DEPLOYMENT SCRIPT - VIGOLEONROCKS.COM")
    print("=" * 60)
    
    # Verificar archivos necesarios
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
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nEjecuta primero: python deploy_vigoleonrocks_com.py")
        exit(1)
    
    # Ejecutar deployment
    deploy_to_vps()
    
    # Información adicional
    create_ssh_key_deployment()
