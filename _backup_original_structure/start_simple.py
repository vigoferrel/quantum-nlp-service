#!/usr/bin/env python3
"""
🚀 QBTC SIMPLE STARTER
Iniciador simple del sistema QBTC
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("🚀 INICIANDO SISTEMA QBTC")
    print("="*50)
    
    # Obtener rutas
    project_root = Path(__file__).parent.absolute()
    llm_system_path = project_root / "localGPT-main" / "integrated_llm_system"
    
    print(f"📁 Directorio del proyecto: {project_root}")
    print(f"📁 Sistema LLM: {llm_system_path}")
    
    # Verificar que existe el directorio
    if not llm_system_path.exists():
        print(f"❌ No se encuentra el directorio: {llm_system_path}")
        return False
    
    # Verificar que existe optimal_ui.py
    optimal_ui_path = llm_system_path / "optimal_ui.py"
    if not optimal_ui_path.exists():
        print(f"❌ No se encuentra: {optimal_ui_path}")
        return False
    
    print("✅ Archivos encontrados")
    
    # Cambiar al directorio correcto
    print("🔧 Cambiando al directorio del sistema...")
    os.chdir(llm_system_path)
    
    # Verificar dependencias básicas
    print("📦 Verificando dependencias...")
    try:
        import flask
        import requests
        print("✅ Dependencias básicas OK")
    except ImportError as e:
        print(f"⚠️ Instalando dependencias faltantes: {e}")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors", "requests"])
    
    # Iniciar el servidor
    print("🚀 Iniciando servidor...")
    try:
        process = subprocess.Popen([sys.executable, "optimal_ui.py"])
        
        print("⏳ Esperando que el servidor se inicie...")
        time.sleep(3)
        
        # Verificar si el proceso sigue ejecutándose
        if process.poll() is None:
            print("✅ Servidor iniciado correctamente")
            print("📱 Abre tu navegador en: http://127.0.0.1:5000")
            print("🔧 Presiona Ctrl+C para detener")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servidor...")
                process.terminate()
                process.wait()
                print("✅ Servidor detenido")
        else:
            print("❌ El servidor se detuvo inesperadamente")
            return False
            
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
