#!/usr/bin/env python3
"""
Script de reparación para problemas comunes en LocalGPT
Soluciona errores típicos de instalación en Windows
"""

import subprocess
import sys
import os

def run_command(command, check=False):
    """Ejecuta un comando sin fallar"""
    print(f"\n>>> {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def fix_auto_gptq():
    """Soluciona problemas con auto-gptq"""
    print("\n🔧 Solucionando problemas con auto-gptq...")
    
    # Intentar desinstalar versiones problemáticas
    run_command(f"{sys.executable} -m pip uninstall auto-gptq -y")
    
    # Instalar versión compatible o saltar
    print("Intentando instalar auto-gptq compatible...")
    success = run_command(f"{sys.executable} -m pip install auto-gptq --no-deps")
    
    if not success:
        print("⚠️  auto-gptq no es compatible, continuando sin él")
        print("   (Solo afecta modelos GPTQ avanzados)")

def fix_bitsandbytes():
    """Soluciona problemas con bitsandbytes en Windows"""
    print("\n🔧 Solucionando bitsandbytes para Windows...")
    
    # Desinstalar versión problemática
    run_command(f"{sys.executable} -m pip uninstall bitsandbytes -y")
    
    # Instalar versión para Windows
    success = run_command(f"{sys.executable} -m pip install bitsandbytes-windows")
    
    if not success:
        print("⚠️  bitsandbytes-windows falló, continuando sin él")

def fix_unstructured():
    """Soluciona problemas con unstructured[pdf]"""
    print("\n🔧 Solucionando unstructured...")
    
    # Instalar sin dependencias extras problemáticas
    run_command(f"{sys.executable} -m pip install unstructured")
    
    # Intentar instalar soporte PDF por separado
    print("Instalando soporte PDF básico...")
    run_command(f"{sys.executable} -m pip install pdfminer.six")

def fix_torch():
    """Verifica y repara PyTorch"""
    print("\n🔧 Verificando PyTorch...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} funciona")
        
        # Verificar CUDA
        if torch.cuda.is_available():
            print(f"✅ CUDA disponible: {torch.cuda.get_device_name(0)}")
        else:
            print("⚠️  CUDA no disponible, usando CPU")
            
    except ImportError:
        print("❌ PyTorch no instalado, instalando...")
        run_command(f"{sys.executable} -m pip install torch")

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
        run_command(f"{sys.executable} -m pip install --force-reinstall {package}")

def clean_cache():
    """Limpia cache de pip"""
    print("\n🧹 Limpiando cache...")
    run_command(f"{sys.executable} -m pip cache purge")

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

def main():
    """Función principal de reparación"""
    print("🛠️  LocalGPT - Herramienta de Reparación")
    print("="*50)
    
    print("\nSelecciona una opción:")
    print("1. Reparación automática completa")
    print("2. Solo arreglar auto-gptq")
    print("3. Solo arreglar bitsandbytes") 
    print("4. Solo arreglar unstructured")
    print("5. Reinstalar paquetes críticos")
    print("6. Crear requirements mínimos")
    print("7. Limpiar cache")
    print("8. Salir")
    
    choice = input("\nOpción (1-8): ").strip()
    
    if choice == "1":
        clean_cache()
        fix_auto_gptq()
        fix_bitsandbytes()
        fix_unstructured()
        fix_torch()
        print("\n✅ Reparación completa terminada")
        
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
        return
        
    else:
        print("Opción inválida")
        return
    
    input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
