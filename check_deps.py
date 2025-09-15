#!/usr/bin/env python3
"""
Script para verificar dependencias disponibles en el sistema
"""

def check_dependency(module_name, import_name=None):
    """Verifica si una dependencia está disponible"""
    import_name = import_name or module_name
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {module_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: No disponible ({e})")
        return False

if __name__ == "__main__":
    print("🔍 Verificando dependencias del sistema...")
    print("=" * 50)
    
    # Core Python
    import sys
    print(f"🐍 Python: {sys.version}")
    print()
    
    # Dependencias básicas disponibles
    print("📦 Dependencias básicas:")
    check_dependency("Pillow", "PIL")
    check_dependency("NumPy", "numpy")
    check_dependency("PSUtil", "psutil")
    print()
    
    # Dependencias de visión
    print("👁️ Dependencias de visión:")
    check_dependency("OpenCV", "cv2")
    check_dependency("PIL ImageFilter", "PIL.ImageFilter")
    check_dependency("PIL ImageEnhance", "PIL.ImageEnhance")
    print()
    
    # Dependencias ML (si están disponibles)
    print("🧠 Dependencias de ML:")
    check_dependency("PyTorch", "torch")
    check_dependency("Transformers", "transformers")
    check_dependency("CLIP", "clip")
    print()
    
    # Dependencias de audio
    print("🎵 Dependencias de audio:")
    check_dependency("PyDub", "pydub")
    check_dependency("Mutagen", "mutagen")
    check_dependency("LibROSA", "librosa")
    print()
    
    print("✅ Verificación completada.")
