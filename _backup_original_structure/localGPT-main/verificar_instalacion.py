#!/usr/bin/env python3
"""
Script de verificación post-instalación para LocalGPT
Verifica que todo esté funcionando después de la reparación
"""

import sys
import os
import subprocess

def check_python_packages():
    """Verifica que los paquetes críticos estén instalados"""
    print("🔍 Verificando paquetes Python...")
    
    critical_packages = [
        ("torch", "PyTorch"),
        ("transformers", "Transformers"),
        ("langchain", "LangChain"),
        ("chromadb", "ChromaDB"),
        ("streamlit", "Streamlit"),
        ("sentence_transformers", "Sentence Transformers")
    ]
    
    optional_packages = [
        ("InstructorEmbedding", "Instructor Embeddings"),
        ("llama_cpp", "Llama CPP"),
        ("accelerate", "Accelerate")
    ]
    
    print("\n📦 Paquetes Críticos:")
    all_critical_ok = True
    for package, name in critical_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - FALTA")
            all_critical_ok = False
    
    print("\n📦 Paquetes Opcionales:")
    for package, name in optional_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"⚠️  {name} - No disponible (no crítico)")
    
    return all_critical_ok

def check_directories():
    """Verifica que las carpetas necesarias existan"""
    print("\n📁 Verificando directorios...")
    
    required_dirs = [
        "SOURCE_DOCUMENTS",
        "DB",
        "models",
        "local_chat_history"
    ]
    
    all_dirs_ok = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ - FALTA")
            all_dirs_ok = False
            # Crear directorio faltante
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"  ➡️  Creado automáticamente")
            except:
                print(f"  ❌ No se pudo crear")
    
    return all_dirs_ok

def check_key_files():
    """Verifica que los archivos clave estén presentes"""
    print("\n📄 Verificando archivos clave...")
    
    key_files = [
        ("constants.py", "Configuración principal"),
        ("ingest.py", "Script de procesamiento"),
        ("run_localGPT.py", "Script principal"),
        ("requirements.txt", "Dependencias")
    ]
    
    optional_files = [
        ("constants_windows.py", "Configuración Windows"),
        ("iniciar_seguro.py", "Script de inicio seguro"),
        ("reparar_definitivo.py", "Script de reparación")
    ]
    
    print("\n📋 Archivos Críticos:")
    all_files_ok = True
    for filename, description in key_files:
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - FALTA - {description}")
            all_files_ok = False
    
    print("\n📋 Archivos Opcionales:")
    for filename, description in optional_files:
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"⚠️  {filename} - No disponible - {description}")
    
    return all_files_ok

def test_torch_functionality():
    """Prueba funcionalidad específica de PyTorch"""
    print("\n🧪 Probando PyTorch...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} importado")
        
        # Probar creación de tensor
        x = torch.randn(2, 3)
        print("✅ Creación de tensores funciona")
        
        # Verificar CUDA
        if torch.cuda.is_available():
            print(f"✅ CUDA disponible - {torch.cuda.get_device_name(0)}")
            print(f"   Devices: {torch.cuda.device_count()}")
        else:
            print("ℹ️  CUDA no disponible - usando CPU (normal)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en PyTorch: {e}")
        return False

def test_langchain_functionality():
    """Prueba funcionalidad específica de LangChain"""
    print("\n🧪 Probando LangChain...")
    
    try:
        from langchain.document_loaders import TextLoader
        print("✅ Document loaders disponibles")
        
        from langchain.text_splitter import CharacterTextSplitter
        print("✅ Text splitters disponibles")
        
        from langchain.embeddings import HuggingFaceInstructEmbeddings
        print("✅ Embeddings disponibles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en LangChain: {e}")
        return False

def test_sample_document():
    """Verifica que haya documentos de muestra"""
    print("\n📄 Verificando documentos de muestra...")
    
    source_dir = "SOURCE_DOCUMENTS"
    if not os.path.exists(source_dir):
        print(f"❌ Directorio {source_dir} no existe")
        return False
    
    files = os.listdir(source_dir)
    if not files:
        print("⚠️  No hay documentos en SOURCE_DOCUMENTS/")
        print("   Copia algunos archivos PDF, TXT, DOCX allí para probar")
        return False
    
    print(f"✅ {len(files)} archivos encontrados:")
    for file in files:
        print(f"   📄 {file}")
    
    return True

def show_next_steps(all_ok):
    """Muestra los siguientes pasos"""
    print("\n" + "="*60)
    
    if all_ok:
        print("🎉 ¡VERIFICACIÓN COMPLETADA - TODO FUNCIONA!")
        print("="*60)
        print()
        print("🚀 SIGUIENTES PASOS:")
        print()
        print("1. 📄 Añadir documentos:")
        print("   - Copia archivos a SOURCE_DOCUMENTS/")
        print("   - Formatos: PDF, TXT, DOCX, CSV, MD")
        print()
        print("2. 🔄 Procesar documentos:")
        print("   python ingest.py --device_type cpu")
        print()
        print("3. 💬 Hacer preguntas:")
        print("   python run_localGPT.py --device_type cpu")
        print()
        print("🌐 INTERFAZ WEB (Opcional):")
        print("   Terminal 1: python run_localGPT_API.py")
        print("   Terminal 2: python localGPTUI/localGPTUI.py")
        print("   Navegador: http://localhost:5111/")
        
    else:
        print("⚠️  VERIFICACIÓN INCOMPLETA - ALGUNOS PROBLEMAS")
        print("="*60)
        print()
        print("🔧 ACCIONES RECOMENDADAS:")
        print()
        print("1. Ejecuta la reparación:")
        print("   python reparar_definitivo.py")
        print()
        print("2. O reinstala paquetes críticos:")
        print("   pip install torch transformers langchain chromadb")
        print()
        print("3. Verifica de nuevo:")
        print("   python verificar_instalacion.py")
    
    print()
    print("📚 RECURSOS:")
    print("   - SOLUCION_AUTO_GPTQ.md  # Guía completa")
    print("   - iniciar_seguro.py      # Configuración de entorno")
    print("   - iniciar.bat           # Menú interactivo")
    print()
    print("="*60)

def main():
    """Función principal de verificación"""
    print("🔍 LocalGPT - Verificación de Instalación")
    print("="*50)
    
    # Verificaciones individuales
    packages_ok = check_python_packages()
    dirs_ok = check_directories()
    files_ok = check_key_files()
    torch_ok = test_torch_functionality()
    langchain_ok = test_langchain_functionality()
    docs_present = test_sample_document()
    
    # Resultado general
    all_critical_ok = packages_ok and files_ok and torch_ok and langchain_ok
    
    print(f"\n📊 RESUMEN DE VERIFICACIÓN:")
    print(f"   Paquetes críticos: {'✅' if packages_ok else '❌'}")
    print(f"   Directorios: {'✅' if dirs_ok else '❌'}")
    print(f"   Archivos clave: {'✅' if files_ok else '❌'}")
    print(f"   PyTorch: {'✅' if torch_ok else '❌'}")
    print(f"   LangChain: {'✅' if langchain_ok else '❌'}")
    print(f"   Documentos: {'✅' if docs_present else '⚠️ '}")
    
    show_next_steps(all_critical_ok)
    
    return 0 if all_critical_ok else 1

if __name__ == "__main__":
    sys.exit(main())
