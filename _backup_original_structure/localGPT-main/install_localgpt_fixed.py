#!/usr/bin/env python3
"""
Script de instalación mejorado para localGPT
Maneja errores comunes de instalación en Windows
"""

import subprocess
import sys
import os
import platform

def run_command(command, check=True, capture_output=True):
    """Ejecuta un comando y muestra la salida"""
    print(f"\n>>> Ejecutando: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=capture_output, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print("STDERR:", result.stderr)
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

def create_requirements_safe():
    """Crea un requirements.txt sin paquetes problemáticos para Windows"""
    safe_requirements = """# Natural Language Processing - Version segura para Windows
langchain==0.0.267
chromadb==0.4.6
pdfminer.six==20221105
InstructorEmbedding
sentence-transformers==2.2.2
faiss-cpu
huggingface_hub==0.25.0
transformers
protobuf==3.20.2
docx2txt
unstructured
# unstructured[pdf]  # Comentado para evitar errores

# Utilities
urllib3==1.26.6
accelerate
click
flask
requests

# Streamlit related
streamlit
Streamlit-extras

# Excel File Manipulation
openpyxl

# Windows specific
bitsandbytes-windows
"""
    
    with open("requirements_safe.txt", "w") as f:
        f.write(safe_requirements)
    print("✅ Archivo requirements_safe.txt creado")

def install_core_packages():
    """Instala paquetes básicos uno por uno"""
    print("\n🔧 Instalando paquetes básicos...")
    
    # Actualizar pip primero
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("❌ Error actualizando pip")
        return False
    
    # Paquetes esenciales en orden específico
    core_packages = [
        "wheel",
        "setuptools",
        "numpy",
        "torch",
        "langchain==0.0.267",
        "transformers",
        "sentence-transformers==2.2.2",
        "chromadb==0.4.6",
        "faiss-cpu",
        "streamlit",
        "flask",
        "requests",
        "InstructorEmbedding",
        "accelerate",
        "huggingface_hub==0.25.0",
        "pdfminer.six==20221105",
        "docx2txt",
        "unstructured",
        "openpyxl",
        "protobuf==3.20.2",
        "urllib3==1.26.6",
        "click",
        "Streamlit-extras"
    ]
    
    failed_packages = []
    
    for package in core_packages:
        print(f"\n📦 Instalando {package}...")
        if not run_command(f"{sys.executable} -m pip install {package}", check=False):
            print(f"⚠️  Error instalando {package}, continuando...")
            failed_packages.append(package)
        else:
            print(f"✅ {package} instalado correctamente")
    
    # Intentar instalar bitsandbytes para Windows
    if platform.system() == "Windows":
        print(f"\n📦 Instalando bitsandbytes para Windows...")
        if not run_command(f"{sys.executable} -m pip install bitsandbytes-windows", check=False):
            print("⚠️  bitsandbytes-windows falló, continuando sin él...")
    
    if failed_packages:
        print(f"\n⚠️  Paquetes que fallaron: {', '.join(failed_packages)}")
        print("   El sistema puede funcionar sin algunos de estos paquetes")
    
    return len(failed_packages) < len(core_packages) // 2  # Si fallan menos de la mitad, continuamos

def install_optional_packages():
    """Instala paquetes opcionales que pueden fallar"""
    print("\n🔧 Instalando paquetes opcionales...")
    
    optional_packages = [
        ("auto-gptq==0.6.0", "Cuantización GPTQ (solo para GPU avanzadas)"),
        ("unstructured[pdf]", "Soporte extendido para PDF"),
        ("bitsandbytes", "Optimización de memoria (alternativo)")
    ]
    
    for package, description in optional_packages:
        print(f"\n📦 Intentando instalar {package} - {description}")
        if run_command(f"{sys.executable} -m pip install {package}", check=False):
            print(f"✅ {package} instalado")
        else:
            print(f"⚠️  {package} falló - no es crítico, continuando...")

def install_llama_cpp(gpu_support=False):
    """Instala llama-cpp-python con soporte GPU si es necesario"""
    print("\n🦙 Instalando llama-cpp-python...")
    
    if gpu_support and platform.system() == "Windows":
        # Para Windows con GPU NVIDIA - versión más compatible
        print("Instalando versión con soporte CUDA...")
        success = run_command(f"{sys.executable} -m pip install llama-cpp-python[cublas]", check=False)
        if not success:
            print("Intentando instalación manual con CMAKE...")
            # Fallback manual
            os.environ["CMAKE_ARGS"] = "-DLLAMA_CUBLAS=on"
            os.environ["FORCE_CMAKE"] = "1"
            success = run_command(f"{sys.executable} -m pip install llama-cpp-python --no-cache-dir", check=False)
    elif platform.system() == "Darwin":  # macOS
        # Para Mac con Metal
        print("Instalando versión con soporte Metal...")
        os.environ["CMAKE_ARGS"] = "-DLLAMA_METAL=on"
        os.environ["FORCE_CMAKE"] = "1"
        success = run_command(f"{sys.executable} -m pip install llama-cpp-python --no-cache-dir", check=False)
    else:
        # CPU solamente
        print("Instalando versión CPU...")
        success = run_command(f"{sys.executable} -m pip install llama-cpp-python", check=False)
    
    if not success:
        print("⚠️  llama-cpp-python falló, intentando versión básica...")
        success = run_command(f"{sys.executable} -m pip install llama-cpp-python", check=False)
    
    return success

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

def create_windows_config():
    """Crea configuración específica para Windows"""
    print("\n⚙️  Creando configuración para Windows...")
    
    # Archivo de configuración que evita errores comunes
    config_content = """# Configuración localGPT para Windows
import os
import sys

# Evitar errores de CUDA en Windows
os.environ.setdefault('CUDA_VERSION', '11.8')
os.environ.setdefault('CUDA_HOME', '')

# Configurar encoding para Windows
if sys.platform == 'win32':
    import locale
    locale.setlocale(locale.LC_ALL, 'C')
"""
    
    with open("windows_config.py", "w") as f:
        f.write(config_content)
    
    print("✅ Configuración de Windows creada")

def test_installation():
    """Prueba que los paquetes críticos funcionen"""
    print("\n🧪 Probando instalación...")
    
    critical_imports = [
        ("langchain", "LangChain"),
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
        ("chromadb", "ChromaDB"),
        ("streamlit", "Streamlit")
    ]
    
    failed_imports = []
    
    for module, name in critical_imports:
        try:
            __import__(module)
            print(f"✅ {name} funciona correctamente")
        except ImportError as e:
            print(f"❌ {name} falló: {e}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\n⚠️  Módulos que fallaron: {', '.join(failed_imports)}")
        print("   Algunos features pueden no funcionar correctamente")
        return False
    else:
        print("\n✅ Todas las importaciones críticas funcionan!")
        return True

def download_sample_document():
    """Descarga documento de muestra para testing"""
    print("\n📄 Creando documento de muestra...")
    
    sample_file = "SOURCE_DOCUMENTS/manual_localgpt.txt"
    sample_content = """
MANUAL DE USO DE LOCALGPT

LocalGPT es una herramienta de inteligencia artificial que te permite hacer preguntas sobre tus documentos de forma completamente privada y local.

CARACTERÍSTICAS PRINCIPALES:
- Procesamiento 100% local en tu computadora
- Sin envío de datos a servidores externos
- Soporte para múltiples formatos: PDF, TXT, DOCX, CSV, MD, HTML
- Interfaz de línea de comandos y web
- Memoria conversacional opcional

COMANDOS BÁSICOS:

1. PROCESAR DOCUMENTOS:
   python ingest.py
   - Analiza todos los documentos en SOURCE_DOCUMENTS/
   - Crea una base de datos vectorial local
   - Solo necesitas hacerlo una vez por cada conjunto nuevo de documentos

2. HACER PREGUNTAS:
   python run_localGPT.py
   - Inicia el modo conversacional
   - Escribe tus preguntas en lenguaje natural
   - Escribe 'exit' para salir

3. INTERFAZ WEB:
   python run_localGPT_API.py (en una terminal)
   python localGPTUI/localGPTUI.py (en otra terminal)
   Luego abre: http://localhost:5111/

OPCIONES AVANZADAS:
- --show_sources: Muestra las fuentes de las respuestas
- --use_history: Habilita memoria conversacional
- --save_qa: Guarda preguntas y respuestas
- --device_type cpu: Fuerza uso de CPU

FORMATOS SOPORTADOS:
- PDF: Documentos, libros, manuales
- TXT: Texto plano
- DOCX: Documentos de Word
- CSV: Hojas de cálculo
- MD: Archivos Markdown
- HTML: Páginas web

CONSEJOS DE USO:
- Organiza tus documentos por temas en subcarpetas
- Usa nombres descriptivos para tus archivos
- Para mejores resultados, usa documentos en inglés
- Los documentos más largos proporcionan más contexto

RESOLUCIÓN DE PROBLEMAS:
- Si hay errores de memoria, cierra otras aplicaciones
- Para problemas de GPU, usa --device_type cpu
- Si las respuestas son lentas, considera usar un modelo más pequeño

¡Disfruta usando LocalGPT de forma privada y segura!
"""
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_content)
    print(f"✅ Manual creado: {sample_file}")

def show_next_steps():
    """Muestra los siguientes pasos después de la instalación"""
    print("\n" + "="*60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("="*60)
    print()
    print("📋 SIGUIENTES PASOS:")
    print()
    print("1. 📄 Añadir documentos:")
    print("   - Copia tus archivos a SOURCE_DOCUMENTS/")
    print("   - Formatos: PDF, TXT, DOCX, CSV, MD, HTML")
    print()
    print("2. 🔄 Procesar documentos:")
    print("   python ingest.py")
    print()
    print("3. 💬 Hacer preguntas:")
    print("   python run_localGPT.py")
    print()
    print("4. 🌐 Interfaz web:")
    print("   Terminal 1: python run_localGPT_API.py")
    print("   Terminal 2: python localGPTUI/localGPTUI.py")
    print("   Navegador: http://localhost:5111/")
    print()
    print("🚀 INICIO RÁPIDO:")
    print("   - Ejecuta: iniciar.bat")
    print("   - Selecciona opción del menú")
    print()
    print("⚠️  PRIMERA EJECUCIÓN:")
    print("   - Descargará modelos (~4-7GB)")
    print("   - Requiere conexión a internet inicialmente")
    print("   - Después funciona sin internet")
    print()
    print("🆘 SI HAY PROBLEMAS:")
    print("   - Revisa INSTALACION_ES.md")
    print("   - Usa: python run_localGPT.py --device_type cpu")
    print("   - GitHub: github.com/PromtEngineer/localGPT/issues")
    print()
    print("="*60)

def main():
    """Función principal de instalación mejorada"""
    print("🚀 LocalGPT - Instalador Mejorado para Windows")
    print("="*55)
    
    # Verificar Python
    if not check_python_version():
        input("Presiona Enter para salir...")
        return 1
    
    # Detectar GPU
    has_gpu = check_gpu()
    
    # Crear configuración para Windows
    create_windows_config()
    
    # Crear requirements seguros
    create_requirements_safe()
    
    # Instalar paquetes básicos
    if not install_core_packages():
        print("\n❌ Error crítico en la instalación")
        print("Revisa los errores arriba y verifica:")
        print("- Conexión a internet")
        print("- Espacio en disco")
        print("- Permisos de administrador")
        input("Presiona Enter para salir...")
        return 1
    
    # Instalar paquetes opcionales
    install_optional_packages()
    
    # Instalar llama-cpp-python
    if not install_llama_cpp(has_gpu):
        print("\n⚠️  llama-cpp-python falló")
        print("   Puedes intentar instalarlo manualmente más tarde")
        print("   El sistema funcionará con CPU solamente")
    
    # Crear directorios
    create_directories()
    
    # Crear documento de muestra
    download_sample_document()
    
    # Probar instalación
    test_installation()
    
    # Mostrar siguientes pasos
    show_next_steps()
    
    input("\nPresiona Enter para continuar...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
