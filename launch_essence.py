#!/usr/bin/env python3
"""
🚀 LAUNCHER DE LA ESENCIA
Lanzador simple para la esencia cuántica real
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    print("⚛️ LAUNCHER DE LA ESENCIA CUÁNTICA")
    print("=" * 50)
    print("🎯 Donde menos es más - La esencia real del sistema")
    print()
    
    # Verificar dependencias básicas
    print("📦 Verificando dependencias...")
    try:
        import flask
        import numpy
        print("✅ Dependencias básicas OK")
    except ImportError as e:
        print(f"⚠️ Instalando dependencias faltantes: {e}")
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "numpy"])
    
    # Verificar si Ollama está disponible
    print("🔍 Verificando Ollama...")
    try:
        import ollama
        print("✅ Ollama disponible")
    except ImportError:
        print("⚠️ Ollama no instalado - usando modo simulado")
    except Exception:
        print("⚠️ Ollama no accesible - usando modo simulado")
    
    print()
    print("🚀 Iniciando servidor de esencia cuántica...")
    print("🌐 Interfaz disponible en: http://localhost:5000")
    print("🔧 Presiona Ctrl+C para detener")
    print()
    
    try:
        # Iniciar el servidor
        process = subprocess.Popen([sys.executable, "quantum_essence_server.py"])
        
        # Esperar a que el servidor esté listo
        time.sleep(3)
        
        # Verificar si el proceso sigue ejecutándose
        if process.poll() is None:
            print("✅ Servidor iniciado correctamente")
            print("📱 Abre tu navegador en: http://localhost:5000")
            print()
            
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
