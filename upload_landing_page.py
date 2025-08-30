#!/usr/bin/env python3
"""
Script para subir la landing page de Vigoleonrocks al servidor de Hostinger
"""

import os
import subprocess
import sys

def upload_to_hostinger():
    """Subir la landing page al servidor de Hostinger"""
    
    print("🚀 SUBIENDO LANDING PAGE A HOSTINGER")
    print("=" * 50)
    
    # Verificar que el archivo existe
    landing_page = "vigoleonrocks_landing_page.html"
    if not os.path.exists(landing_page):
        print(f"❌ Error: No se encontró {landing_page}")
        return False
    
    print(f"✅ Archivo encontrado: {landing_page}")
    print(f"📁 Tamaño: {os.path.getsize(landing_page)} bytes")
    
    # Información del servidor
    server_info = {
        "host": "82.112.246.20",
        "port": "65002",
        "user": "u819436651",
        "remote_path": "domains/vigoleonrocks.com/public_html/"
    }
    
    print(f"\n📡 Información del servidor:")
    print(f"   Host: {server_info['host']}")
    print(f"   Puerto: {server_info['port']}")
    print(f"   Usuario: {server_info['user']}")
    print(f"   Ruta remota: {server_info['remote_path']}")
    
    # Comando SCP para subir el archivo
    scp_command = [
        "scp",
        "-P", server_info["port"],
        landing_page,
        f"{server_info['user']}@{server_info['host']}:{server_info['remote_path']}index.html"
    ]
    
    print(f"\n📤 Comando SCP:")
    print(f"   {' '.join(scp_command)}")
    
    try:
        print(f"\n🔄 Subiendo archivo...")
        result = subprocess.run(scp_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ ¡Archivo subido exitosamente!")
            print(f"🌐 La landing page estará disponible en: https://vigoleonrocks.com")
            
            # Comandos adicionales para configurar
            print(f"\n🔧 Comandos adicionales para ejecutar en el servidor:")
            print(f"   ssh -p {server_info['port']} {server_info['user']}@{server_info['host']}")
            print(f"   cd {server_info['remote_path']}")
            print(f"   ls -la")
            print(f"   chmod 644 index.html")
            
            return True
        else:
            print(f"❌ Error al subir archivo:")
            print(f"   STDOUT: {result.stdout}")
            print(f"   STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_backup_script():
    """Crear script de backup para el servidor"""
    
    backup_script = """#!/bin/bash
# Script de backup para vigoleonrocks.com

echo "🔄 Creando backup de la configuración actual..."

# Crear directorio de backup
mkdir -p ~/backup_vigoleonrocks_$(date +%Y%m%d_%H%M%S)

# Backup de archivos actuales
cp -r domains/vigoleonrocks.com/public_html/* ~/backup_vigoleonrocks_$(date +%Y%m%d_%H%M%S)/

echo "✅ Backup creado exitosamente"
echo "📁 Ubicación: ~/backup_vigoleonrocks_$(date +%Y%m%d_%H%M%S)/"
"""
    
    with open("backup_script.sh", "w") as f:
        f.write(backup_script)
    
    print("✅ Script de backup creado: backup_script.sh")

def main():
    """Función principal"""
    
    print("🧠 VIGOLEONROCKS - UPLOAD LANDING PAGE")
    print("=" * 50)
    
    # Crear script de backup
    create_backup_script()
    
    # Subir landing page
    success = upload_to_hostinger()
    
    if success:
        print(f"\n🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print(f"📋 Próximos pasos:")
        print(f"   1. Verificar que la página funciona: https://vigoleonrocks.com")
        print(f"   2. Configurar cuentas de correo corporativas en Hostinger")
        print(f"   3. Crear subdominios para API y documentación")
        print(f"   4. Probar la interfaz web moderna: python vigoleonrocks_web_ui.py")
    else:
        print(f"\n❌ Error en el proceso. Revisar logs arriba.")
        print(f"💡 Alternativa: Subir manualmente via File Manager de Hostinger")

if __name__ == "__main__":
    main()
