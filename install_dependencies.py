#!/usr/bin/env python3
"""
📦 QBTC DEPENDENCIES INSTALLER
Instalador de dependencias para el sistema QBTC
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Instalar un paquete específico"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error instalando {package}")
        return False

def main():
    """Instalar todas las dependencias"""
    print("📦 INSTALANDO DEPENDENCIAS QBTC")
    print("="*50)
    
    # Dependencias principales
    core_dependencies = [
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "requests>=2.25.0",
        "numpy>=1.21.0",
        "psutil>=5.8.0"
    ]
    
    # Dependencias opcionales
    optional_dependencies = [
        "pika>=1.2.0",  # Para RabbitMQ
        "fastapi>=0.68.0",  # Para APIs avanzadas
        "uvicorn>=0.15.0",  # Para FastAPI
        "supabase>=0.5.0",  # Para Supabase
        "streamlit>=1.0.0",  # Para interfaces Streamlit
        "tailwindcss>=0.0.1",  # Para Tailwind CSS
        "markdown>=3.3.0",  # Para markdown
        "pygments>=2.10.0"  # Para syntax highlighting
    ]
    
    print("🔧 Instalando dependencias principales...")
    for dep in core_dependencies:
        install_package(dep)
    
    print("\n🔧 Instalando dependencias opcionales...")
    for dep in optional_dependencies:
        install_package(dep)
    
    print("\n✅ Instalación completada")
    print("🚀 Ejecuta 'python start_qbtc_system.py' para iniciar el sistema")

if __name__ == "__main__":
    main()
