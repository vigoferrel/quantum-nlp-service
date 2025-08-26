#!/usr/bin/env python3
"""
Reparación específica para Python 3.13
Muchos paquetes aún no son compatibles con Python 3.13
"""

import subprocess
import sys
import os

def run_command(command, description=""):
    """Ejecuta comando con manejo de errores"""
    print(f"\n>>> {description}")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Éxito")
            if result.stdout:
                print(result.stdout[:300])  # Primeras 300 chars
            return True
        else:
            print("❌ Error")
            if result.stderr:
                print("Error:", result.stderr[:200])
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def check_python_version():
    """Verifica versión de Python y advierte sobre 3.13"""
    version = sys.version_info
    print(f"🐍 Python detectado: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 13:
        print("⚠️  ADVERTENCIA: Python 3.13 detectado")
        print("   Muchos paquetes ML aún no soportan Python 3.13")
        print("   Se recomienda Python 3.10 o 3.11 para ML")
        return "too_new"
    elif version.major == 3 and version.minor >= 10:
        print("✅ Versión compatible")
        return "compatible"
    else:
        print("❌ Versión muy antigua")
        return "too_old"

def install_compatible_versions():
    """Instala versiones específicamente compatibles con Python 3.13"""
    print("\n🔧 Instalando versiones compatibles con Python 3.13...")
    
    # Actualizar herramientas base primero
    base_tools = [
        "pip --upgrade",
        "setuptools --upgrade", 
        "wheel --upgrade",
        "build",
        "packaging"
    ]
    
    for tool in base_tools:
        run_command(f"{sys.executable} -m pip install {tool}", f"Actualizando {tool}")
    
    # Paquetes en orden específico con versiones más nuevas/compatibles
    compatible_packages = [
        ("numpy>=1.24.0", "NumPy actualizado"),
        ("torch>=2.0.0", "PyTorch reciente"),
        ("transformers>=4.30.0", "Transformers actualizado"),
        ("sentence-transformers>=2.3.0", "Sentence Transformers nuevo"),  # Versión más nueva
        ("langchain>=0.1.0", "LangChain actualizado"),  # Versión más nueva
        ("chromadb>=0.4.15", "ChromaDB actualizado"),
        ("streamlit>=1.28.0", "Streamlit actualizado"),
        ("flask>=2.3.0", "Flask actualizado"),
        ("requests>=2.31.0", "Requests actualizado"),
        ("accelerate>=0.21.0", "Accelerate actualizado"),
        ("huggingface_hub>=0.16.0", "HuggingFace Hub actualizado"),
        ("pdfminer.six", "PDF Parser"),
        ("docx2txt", "DOCX Parser"),
        ("unstructured", "Unstructured Parser"),
        ("openpyxl", "Excel Parser"),
        ("protobuf>=4.0.0", "Protobuf actualizado"),
        ("click>=8.0.0", "Click actualizado"),
        ("faiss-cpu", "FAISS CPU")
    ]
    
    failed_packages = []
    
    for package, description in compatible_packages:
        success = run_command(f"{sys.executable} -m pip install {package}", description)
        
        if not success:
            failed_packages.append(package.split(">=")[0].split("==")[0])
            print(f"⚠️  {package} falló, continuando...")
            
            # Intentar sin versión específica
            base_name = package.split(">=")[0].split("==")[0]
            print(f"Intentando {base_name} sin versión específica...")
            if run_command(f"{sys.executable} -m pip install {base_name}", f"Instalando {base_name} básico"):
                print(f"✅ {base_name} instalado en versión básica")
        else:
            print(f"✅ {package} instalado")
    
    return failed_packages

def install_from_git():
    """Instala versiones de desarrollo que soportan Python 3.13"""
    print("\n🚀 Intentando versiones de desarrollo...")
    
    dev_packages = [
        ("git+https://github.com/UKPLab/sentence-transformers.git", "Sentence Transformers DEV"),
        ("git+https://github.com/langchain-ai/langchain.git", "LangChain DEV")
    ]
    
    for package, description in dev_packages:
        print(f"\nIntentando {description}...")
        success = run_command(f"{sys.executable} -m pip install {package}", f"Instalando {description}")
        
        if success:
            print(f"✅ {description} instalado desde repositorio")
        else:
            print(f"⚠️  {description} falló desde repositorio")

def install_precompiled_wheels():
    """Intenta instalar wheels precompiladas"""
    print("\n🎯 Intentando wheels precompiladas...")
    
    wheel_packages = [
        "sentence-transformers --only-binary=all",
        "langchain --only-binary=all",
        "chromadb --only-binary=all"
    ]
    
    for package in wheel_packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Wheel precompilada: {package}")

def create_python313_constants():
    """Crea configuración específica para Python 3.13"""
    print("\n⚙️  Creando configuración para Python 3.13...")
    
    config_content = '''# Configuración LocalGPT para Python 3.13
import os
import sys

# Configurar variables de entorno
os.environ.setdefault('CUDA_VERSION', '12.1')
os.environ.setdefault('FORCE_CMAKE', '1')

# Configuración específica para Python 3.13
if sys.version_info >= (3, 13):
    # Deshabilitar warnings de compatibilidad
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

# Modelo más compatible para Python 3.13
MODEL_ID = "microsoft/DialoGPT-medium"  # Modelo más simple y compatible
MODEL_BASENAME = None

# Configuración conservadora
N_GPU_LAYERS = 0  # Usar solo CPU por compatibilidad
N_BATCH = 128     # Batch pequeño
CONTEXT_WINDOW_SIZE = 2048
MAX_NEW_TOKENS = 512

# Embedding más simple
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Modelo pequeño y compatible

print("✅ Configuración Python 3.13 cargada")
'''
    
    with open("constants_python313.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✅ constants_python313.py creado")

def create_minimal_test():
    """Crea un test mínimo para verificar funcionalidad básica"""
    test_content = '''#!/usr/bin/env python3
"""
Test mínimo para Python 3.13
"""

def test_basic_imports():
    """Prueba imports básicos"""
    success = []
    failed = []
    
    tests = [
        ("numpy", "NumPy"),
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("sentence_transformers", "Sentence Transformers"),
        ("langchain", "LangChain"),
        ("streamlit", "Streamlit")
    ]
    
    for module, name in tests:
        try:
            __import__(module)
            print(f"✅ {name}")
            success.append(name)
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed.append(name)
    
    print(f"\\n📊 Resultado: {len(success)}/{len(tests)} paquetes funcionan")
    
    if len(success) >= 3:  # Al menos 3 paquetes básicos
        print("✅ Instalación mínima funcional")
        return True
    else:
        print("❌ Instalación insuficiente")
        return False

if __name__ == "__main__":
    test_basic_imports()
'''
    
    with open("test_python313.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ test_python313.py creado")

def show_python313_instructions():
    """Muestra instrucciones específicas para Python 3.13"""
    print("\n" + "="*60)
    print("🐍 INSTALACIÓN PARA PYTHON 3.13")
    print("="*60)
    print()
    print("⚠️  SITUACIÓN:")
    print("   Python 3.13 es muy nuevo para muchos paquetes ML")
    print("   Algunos paquetes pueden no estar disponibles")
    print()
    print("✅ SOLUCION IMPLEMENTADA:")
    print("   - Versiones más nuevas de paquetes")
    print("   - Configuración conservadora (solo CPU)")
    print("   - Modelo más simple y compatible")
    print("   - Tests de verificación")
    print()
    print("🔧 ARCHIVOS CREADOS:")
    print("   - constants_python313.py  # Configuración optimizada")
    print("   - test_python313.py       # Test de verificación")
    print()
    print("🚀 SIGUIENTES PASOS:")
    print()
    print("1. Probar instalación:")
    print("   python test_python313.py")
    print()
    print("2. Si funciona, usar configuración específica:")
    print("   cp constants_python313.py constants.py")
    print()
    print("3. Procesar documentos (solo CPU):")
    print("   python ingest.py --device_type cpu")
    print()
    print("4. Ejecutar LocalGPT:")
    print("   python run_localGPT.py --device_type cpu")
    print()
    print("💡 RECOMENDACIÓN ALTERNATIVA:")
    print("   Considera instalar Python 3.11 para mejor compatibilidad")
    print("   https://python.org/downloads/")
    print()
    print("="*60)

def main():
    """Función principal para Python 3.13"""
    print("🐍 LocalGPT - Reparación para Python 3.13")
    print("="*50)
    
    version_status = check_python_version()
    
    if version_status == "too_new":
        print("\n🔧 Aplicando soluciones para Python 3.13...")
        
        # Limpiar cache
        run_command(f"{sys.executable} -m pip cache purge", "Limpiando cache")
        
        # Instalar versiones compatibles
        failed = install_compatible_versions()
        
        # Si hay muchos fallos, intentar alternativas
        if len(failed) > 3:
            print(f"\n⚠️  {len(failed)} paquetes fallaron, intentando alternativas...")
            install_precompiled_wheels()
            install_from_git()
        
        # Crear configuración específica
        create_python313_constants()
        create_minimal_test()
        
        # Probar instalación
        print("\n🧪 Probando instalación...")
        run_command(f"{sys.executable} test_python313.py", "Test de verificación")
        
        show_python313_instructions()
        
    elif version_status == "compatible":
        print("\n✅ Tu versión de Python es compatible")
        print("   Usa el script reparar_definitivo.py normal")
        
    else:
        print("\n❌ Python muy antiguo, actualiza a 3.10+")
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
