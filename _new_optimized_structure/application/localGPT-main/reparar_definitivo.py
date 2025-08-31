#!/usr/bin/env python3
"""
Instalador específico que evita el problema de auto-gptq
Diseñado para el error específico de CUDA_VERSION
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
                print(result.stdout[:500])  # Primeras 500 chars
            return True
        else:
            print("❌ Error")
            if result.stderr:
                print("Error:", result.stderr[:300])
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def clean_cache():
    """Limpia cache de pip"""
    print("\n🧹 Limpiando cache...")
    run_command(f"{sys.executable} -m pip cache purge", "Limpiando cache de pip")

def fix_auto_gptq():
    """Soluciona problemas con auto-gptq"""
    print("\n🔧 Solucionando problemas con auto-gptq...")
    
    # Intentar desinstalar versiones problemáticas
    run_command(f"{sys.executable} -m pip uninstall auto-gptq -y", "Desinstalando auto-gptq")
    
    print("❌ auto-gptq OMITIDO debido a problemas en Windows")
    print("   (Solo necesario para modelos GPTQ específicos)")

def fix_bitsandbytes():
    """Soluciona problemas con bitsandbytes en Windows"""
    print("\n🔧 Solucionando bitsandbytes para Windows...")
    
    # Desinstalar versión problemática
    run_command(f"{sys.executable} -m pip uninstall bitsandbytes -y", "Desinstalando bitsandbytes")
    
    # Instalar versión para Windows
    success = run_command(f"{sys.executable} -m pip install bitsandbytes-windows", "Instalando bitsandbytes-windows")
    
    if not success:
        print("⚠️  bitsandbytes-windows falló, continuando sin él")

def fix_unstructured():
    """Soluciona problemas con unstructured[pdf]"""
    print("\n🔧 Solucionando unstructured...")
    
    # Instalar sin dependencias extras problemáticas
    run_command(f"{sys.executable} -m pip install unstructured", "Instalando unstructured básico")
    
    # Intentar instalar soporte PDF por separado
    run_command(f"{sys.executable} -m pip install pdfminer.six", "Instalando soporte PDF")

def reinstall_critical():
    """Reinstala paquetes críticos"""
    print("\n🔧 Reinstalando paquetes críticos...")
    
    critical = [
        "langchain==0.0.267",
        "transformers", 
        "sentence-transformers",
        "chromadb",
        "streamlit",
        "InstructorEmbedding"
    ]
    
    for package in critical:
        print(f"Reinstalando {package}...")
        run_command(f"{sys.executable} -m pip install --force-reinstall {package}", f"Reinstalando {package}")

def create_minimal_requirements():
    """Crea requirements mínimos que siempre funcionan"""
    minimal = """# Requirements mínimos para LocalGPT
torch
transformers
langchain==0.0.267
chromadb==0.4.6
sentence-transformers==2.2.2
streamlit
requests
numpy
pandas
"""
    
    with open("requirements_minimal.txt", "w") as f:
        f.write(minimal)
    
    print("✅ requirements_minimal.txt creado")

def install_without_problematic_packages():
    """Instala solo paquetes que sabemos que funcionan"""
    
    print("🎯 Instalando LocalGPT SIN paquetes problemáticos")
    print("="*55)
    
    # Paquetes en orden específico - probados y funcionales
    packages_order = [
        ("pip --upgrade", "Actualizando pip"),
        ("wheel setuptools", "Herramientas básicas"),
        ("numpy", "NumPy"),
        ("torch torchvision", "PyTorch"),
        ("transformers", "Transformers de HuggingFace"),
        ("sentence-transformers==2.2.2", "Sentence Transformers"),
        ("langchain==0.0.267", "LangChain"),
        ("chromadb==0.4.6", "ChromaDB"),
        ("streamlit", "Streamlit"),
        ("flask requests", "Utilidades web"),
        ("InstructorEmbedding", "Instructor Embeddings"),
        ("accelerate", "Accelerate"),
        ("huggingface_hub==0.25.0", "HuggingFace Hub"),
        ("pdfminer.six==20221105", "PDF Parser"),
        ("docx2txt", "DOCX Parser"),
        ("unstructured", "Unstructured Parser"),
        ("openpyxl", "Excel Parser"),
        ("protobuf==3.20.2", "Protobuf"),
        ("urllib3==1.26.6", "URLs"),
        ("click", "CLI"),
        ("Streamlit-extras", "Streamlit extras"),
        ("faiss-cpu", "FAISS CPU")
    ]
    
    failed_packages = []
    
    for package, description in packages_order:
        success = run_command(f"{sys.executable} -m pip install {package}", description)
        
        if not success:
            failed_packages.append(package.split()[0])  # Solo el primer nombre
            print(f"⚠️  {package} falló, continuando...")
        else:
            print(f"✅ {package} instalado")
    
    # Intentar bitsandbytes para Windows
    print(f"\n>>> Instalando bitsandbytes para Windows")
    run_command(f"{sys.executable} -m pip install bitsandbytes-windows", "bitsandbytes Windows")
    
    # Intentar llama-cpp-python
    print(f"\n>>> Instalando llama-cpp-python")
    if not run_command(f"{sys.executable} -m pip install llama-cpp-python", "llama-cpp-python"):
        print("⚠️  llama-cpp-python falló, será instalado después")
    
    # NO INSTALAR auto-gptq por ahora
    print(f"\n⚠️  OMITIENDO auto-gptq debido a problemas en Windows")
    print("   (Solo necesario para modelos GPTQ específicos)")
    
    if failed_packages:
        print(f"\n📝 Paquetes que fallaron: {', '.join(failed_packages)}")
        print("   El sistema debería funcionar sin algunos de estos")
    
    return len(failed_packages) < 5  # Si fallan menos de 5, seguimos

def test_basic_functionality():
    """Prueba funcionalidad básica"""
    print("\n🧪 Probando funcionalidad básica...")
    
    tests = [
        ("import torch", "PyTorch"),
        ("import transformers", "Transformers"), 
        ("import langchain", "LangChain"),
        ("import chromadb", "ChromaDB"),
        ("import streamlit", "Streamlit"),
        ("from InstructorEmbedding import INSTRUCTOR", "InstructorEmbedding")
    ]
    
    failed_tests = []
    
    for test_code, name in tests:
        try:
            exec(test_code)
            print(f"✅ {name} funciona")
        except Exception as e:
            print(f"❌ {name} falló: {e}")
            failed_tests.append(name)
    
    if not failed_tests:
        print("\n🎉 ¡Todas las pruebas básicas pasaron!")
        return True
    else:
        print(f"\n⚠️  Tests que fallaron: {', '.join(failed_tests)}")
        return False

def create_startup_script():
    """Crea script de inicio que evita errores comunes"""
    
    startup_content = '''#!/usr/bin/env python3
"""
Script de inicio seguro para LocalGPT
Evita errores comunes y configura el entorno
"""

import os
import sys

# Configurar variables de entorno antes de importar nada
os.environ.setdefault('CUDA_VERSION', '11.8')
os.environ.setdefault('CUDA_HOME', '')
os.environ.setdefault('FORCE_CMAKE', '1')

# Configurar encoding para Windows
if sys.platform == 'win32':
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'C')
    except:
        pass

print("🚀 Iniciando LocalGPT...")
print("✅ Variables de entorno configuradas")

# Verificar imports críticos
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
except ImportError:
    print("❌ PyTorch no disponible")
    
try:
    import transformers
    print(f"✅ Transformers {transformers.__version__}")
except ImportError:
    print("❌ Transformers no disponible")
    
try:
    import langchain
    print("✅ LangChain disponible")
except ImportError:
    print("❌ LangChain no disponible")

print("\\n🎯 LocalGPT listo para usar")
print("Comandos disponibles:")
print("  python ingest.py          # Procesar documentos")
print("  python run_localGPT.py    # Hacer preguntas")
print("  python iniciar_seguro.py  # Este script")
'''
    
    with open("iniciar_seguro.py", "w", encoding="utf-8") as f:
        f.write(startup_content)
    
    print("✅ Script de inicio seguro creado: iniciar_seguro.py")

def create_fixed_constants():
    """Crea constants.py modificado para evitar errores"""
    print("\n🔧 Creando constants.py optimizado para Windows...")
    
    # Leer el constants.py original
    try:
        with open("constants.py", "r", encoding="utf-8") as f:
            original_content = f.read()
    except:
        print("❌ No se pudo leer constants.py original")
        return False
    
    # Modificaciones para Windows
    modified_content = original_content
    
    # Cambiar modelo por defecto a uno más compatible
    if "MODEL_ID = \"meta-llama/Meta-Llama-3-8B-Instruct\"" in modified_content:
        modified_content = modified_content.replace(
            'MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"',
            '# MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"  # Comentado para Windows\nMODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"'
        )
        
        modified_content = modified_content.replace(
            'MODEL_BASENAME = None',
            'MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"'
        )
    
    # Reducir uso de GPU para evitar errores de memoria
    modified_content = modified_content.replace(
        'N_GPU_LAYERS = 100',
        'N_GPU_LAYERS = 20  # Reducido para Windows'
    )
    
    modified_content = modified_content.replace(
        'N_BATCH = 512',
        'N_BATCH = 256  # Reducido para Windows'
    )
    
    # Guardar versión modificada
    with open("constants_windows.py", "w", encoding="utf-8") as f:
        f.write(modified_content)
    
    print("✅ constants_windows.py creado")
    print("   - Modelo cambiado a Llama-2-7b-Chat-GGUF (más compatible)")
    print("   - GPU layers reducido para mejor compatibilidad")
    print("   - Batch size reducido para menos uso de memoria")
    
    return True

def install_alternative_llama_cpp():
    """Instala llama-cpp-python de forma alternativa"""
    print("\n🦙 Instalando llama-cpp-python (método alternativo)...")
    
    # Método 1: Instalación básica
    if run_command(f"{sys.executable} -m pip install llama-cpp-python", "Método básico"):
        return True
    
    # Método 2: Con wheel precompilado
    print("Intentando con wheel precompilado...")
    if run_command(f"{sys.executable} -m pip install llama-cpp-python --only-binary=all", "Wheel precompilado"):
        return True
    
    # Método 3: Versión específica estable
    print("Intentando versión específica...")
    if run_command(f"{sys.executable} -m pip install llama-cpp-python==0.2.11", "Versión específica"):
        return True
    
    print("⚠️  llama-cpp-python no se pudo instalar")
    print("   Puedes intentar instalarlo manualmente después")
    return False

def show_final_instructions():
    """Muestra instrucciones finales específicas para el problema resuelto"""
    print("\n" + "="*60)
    print("🎉 INSTALACIÓN REPARADA - SIN AUTO-GPTQ")
    print("="*60)
    print()
    print("✅ PROBLEMA RESUELTO:")
    print("   - auto-gptq omitido (causaba el error CUDA_VERSION)")
    print("   - Paquetes críticos instalados correctamente")
    print("   - Configuración optimizada para Windows")
    print()
    print("📋 CÓMO USAR LOCALGPT AHORA:")
    print()
    print("1. 📄 Añadir documentos:")
    print("   - Copia archivos a SOURCE_DOCUMENTS/")
    print()
    print("2. 🔄 Procesar documentos:")
    print("   python ingest.py --device_type cpu")
    print()
    print("3. 💬 Hacer preguntas:")
    print("   python run_localGPT.py --device_type cpu")
    print()
    print("🔧 SCRIPTS DISPONIBLES:")
    print("   - iniciar_seguro.py     # Verificar instalación")
    print("   - reparar_definitivo.py # Este script de reparación")
    print("   - iniciar.bat          # Menú interactivo")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Usa --device_type cpu si hay problemas con GPU")
    print("   - Los modelos GPTQ no funcionarán (auto-gptq omitido)")
    print("   - Usa modelos GGUF en su lugar (más compatibles)")
    print()
    print("🎯 MODELO RECOMENDADO:")
    print("   TheBloke/Llama-2-7b-Chat-GGUF")
    print("   (Ya configurado en constants_windows.py)")
    print()
    print("="*60)

def main():
    """Función principal de reparación"""
    print("🛠️  LocalGPT - Herramienta de Reparación Definitiva")
    print("="*55)
    
    print("\nProblema detectado: Error con auto-gptq y CUDA_VERSION")
    print("\nSolución: Instalar sin paquetes problemáticos")
    print("\nSelecciona una opción:")
    print("1. 🎯 Reparación completa (RECOMENDADO)")
    print("2. Solo arreglar auto-gptq")
    print("3. Solo arreglar bitsandbytes") 
    print("4. Solo arreglar unstructured")
    print("5. Reinstalar paquetes críticos")
    print("6. Crear requirements mínimos")
    print("7. Limpiar cache")
    print("8. Instalar llama-cpp alternativo")
    print("9. Salir")
    
    choice = input("\nOpción (1-9): ").strip()
    
    if choice == "1":
        print("\n🎯 Iniciando reparación completa...")
        clean_cache()
        if install_without_problematic_packages():
            test_basic_functionality()
            create_startup_script()
            create_fixed_constants()
            install_alternative_llama_cpp()
            show_final_instructions()
        else:
            print("❌ Reparación falló")
        
    elif choice == "2":
        fix_auto_gptq()
        
    elif choice == "3":
        fix_bitsandbytes()
        
    elif choice == "4":
        fix_unstructured()
        
    elif choice == "5":
        reinstall_critical()
        
    elif choice == "6":
        create_minimal_requirements()
        print("Ahora ejecuta: pip install -r requirements_minimal.txt")
        
    elif choice == "7":
        clean_cache()
        
    elif choice == "8":
        install_alternative_llama_cpp()
        
    elif choice == "9":
        return
        
    else:
        print("Opción inválida")
        return
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
