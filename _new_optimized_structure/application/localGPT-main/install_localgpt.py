#!/usr/bin/env python3
"""
Script de instalación para localGPT
Automatiza el proceso de instalación de dependencias y configuración inicial
"""

import subprocess
import sys
import os
import platform

def run_command(command, check=True):
    """Ejecuta un comando y muestra la salida"""
    print(f"\n>>> Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Verifica que Python sea 3.10 o superior"""
    version = sys.version_info
    print(f"Versión de Python detectada: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ ERROR: Se requiere Python 3.10 o superior")
        print("Por favor instala Python 3.10+ desde https://python.org")
        return False
    
    print("✅ Versión de Python compatible")
    return True

def check_gpu():
    """Detecta si hay GPU NVIDIA disponible"""
    try:
        result = subprocess.run("nvidia-smi", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU NVIDIA detectada")
            print(result.stdout.split('\n')[0])  # Primera línea con info de la GPU
            return True
    except:
        pass
    
    print("⚠️  No se detectó GPU NVIDIA, se usará CPU")
    return False

def install_requirements():
    """Instala los requerimientos del proyecto"""
    print("\n🔧 Instalando dependencias...")
    
    # Actualizar pip
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("❌ Error actualizando pip")
        return False
    
    # Instalar requirements.txt
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Error instalando requirements.txt")
        return False
    
    return True

def install_llama_cpp(gpu_support=False):
    """Instala llama-cpp-python con soporte GPU si es necesario"""
    print("\n🦙 Instalando llama-cpp-python...")
    
    if gpu_support and platform.system() == "Windows":
        # Para Windows con GPU NVIDIA
        env_vars = "CMAKE_ARGS=\"-DLLAMA_CUBLAS=on\" FORCE_CMAKE=1"
        command = f"{env_vars} {sys.executable} -m pip install llama-cpp-python --no-cache-dir"
    elif platform.system() == "Darwin":  # macOS
        # Para Mac con Metal
        env_vars = "CMAKE_ARGS=\"-DLLAMA_METAL=on\" FORCE_CMAKE=1"
        command = f"{env_vars} {sys.executable} -m pip install llama-cpp-python --no-cache-dir"
    else:
        # CPU solamente
        command = f"{sys.executable} -m pip install llama-cpp-python"
    
    return run_command(command, check=False)  # No fallar si hay error

def create_directories():
    """Crea los directorios necesarios"""
    print("\n📁 Creando directorios necesarios...")
    
    directories = [
        "SOURCE_DOCUMENTS",
        "DB", 
        "models",
        "local_chat_history"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")

def download_sample_document():
    """Descarga documento de muestra para testing"""
    print("\n📄 Verificando documento de muestra...")
    
    sample_file = "SOURCE_DOCUMENTS/constitucion_muestra.txt"
    if not os.path.exists(sample_file):
        # Crear un documento de muestra simple
        sample_content = """
DOCUMENTO DE MUESTRA PARA LOCALGPT

Este es un documento de prueba para verificar que localGPT funciona correctamente.

LocalGPT es una herramienta que permite hacer preguntas sobre documentos de forma privada y local.

Características principales:
- Procesamiento completamente local
- Sin envío de datos a servidores externos  
- Soporte para múltiples formatos de archivo
- Interfaz de línea de comandos y web

Para usar localGPT:
1. Coloca tus documentos en la carpeta SOURCE_DOCUMENTS
2. Ejecuta python ingest.py para procesar los documentos
3. Ejecuta python run_localGPT.py para hacer preguntas

¡Disfruta usando localGPT de forma privada y segura!
"""
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"✅ Documento de muestra creado: {sample_file}")
    else:
        print(f"✅ Documento de muestra ya existe: {sample_file}")

def show_next_steps():
    """Muestra los siguientes pasos después de la instalación"""
    print("\n" + "="*60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("="*60)
    print()
    print("📋 SIGUIENTES PASOS:")
    print()
    print("1. 📄 Añadir documentos:")
    print("   - Copia tus archivos PDF, TXT, DOCX, etc. a la carpeta SOURCE_DOCUMENTS/")
    print()
    print("2. 🔄 Procesar documentos:")
    print("   python ingest.py")
    print()
    print("3. 💬 Hacer preguntas:")
    print("   python run_localGPT.py")
    print()
    print("4. 🌐 Interfaz web (opcional):")
    print("   python run_localGPT_API.py")
    print("   (En otra terminal): python localGPTUI/localGPTUI.py")
    print("   (Abrir navegador): http://localhost:5111/")
    print()
    print("📚 COMANDOS ÚTILES:")
    print("   - python run_localGPT.py --help          # Ver opciones")
    print("   - python run_localGPT.py --show_sources  # Mostrar fuentes")
    print("   - python run_localGPT.py --use_history   # Habilitar historial")
    print("   - python ingest.py --device_type cpu     # Forzar uso de CPU")
    print()
    print("⚠️  NOTAS IMPORTANTES:")
    print("   - La primera ejecución descargará modelos (requiere internet)")
    print("   - Los modelos pueden ocupar varios GB de espacio")
    print("   - Una vez descargados, funciona sin internet")
    print()
    print("="*60)

def main():
    """Función principal de instalación"""
    print("🚀 Iniciando instalación de localGPT")
    print("="*50)
    
    # Verificar Python
    if not check_python_version():
        return 1
    
    # Detectar GPU
    has_gpu = check_gpu()
    
    # Instalar dependencias principales
    if not install_requirements():
        print("\n❌ Error en la instalación de dependencias")
        return 1
    
    # Instalar llama-cpp-python
    if not install_llama_cpp(has_gpu):
        print("\n⚠️  Advertencia: Error instalando llama-cpp-python")
        print("   Puedes intentar instalarlo manualmente más tarde")
    
    # Crear directorios
    create_directories()
    
    # Crear documento de muestra
    download_sample_document()
    
    # Mostrar siguientes pasos
    show_next_steps()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
