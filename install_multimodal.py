#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Instalador Automático de Dependencias Multimodales
Script para instalar todos los modelos de AI avanzados de 2025
"""

import os
import sys
import subprocess
import platform
import importlib
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultimodalInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.errors = []
        self.installed_packages = []
        
    def check_python_version(self):
        """Verificar versión de Python"""
        logger.info(f"🐍 Verificando versión de Python: {sys.version}")
        
        if self.python_version < (3, 8):
            logger.error("❌ Python 3.8+ requerido para modelos multimodales avanzados")
            return False
        
        logger.info("✅ Versión de Python compatible")
        return True
    
    def check_gpu_support(self):
        """Verificar soporte GPU"""
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory // (1024**3)
                logger.info(f"🎮 GPU detectada: {gpu_name} ({gpu_memory}GB VRAM)")
                return True, "cuda"
            else:
                logger.info("💻 GPU CUDA no detectada, usando CPU")
                return True, "cpu"
        except ImportError:
            logger.warning("⚠️ PyTorch no instalado aún")
            return False, "unknown"
    
    def install_requirements(self):
        """Instalar dependencias desde requirements_multimodal.txt"""
        logger.info("📦 Instalando dependencias multimodales...")
        
        requirements_file = Path("requirements_multimodal.txt")
        if not requirements_file.exists():
            logger.error("❌ Archivo requirements_multimodal.txt no encontrado")
            return False
        
        try:
            # Actualizar pip primero
            logger.info("⬆️ Actualizando pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            
            # Instalar PyTorch primero (importante para compatibilidad)
            logger.info("🔥 Instalando PyTorch...")
            if self.system == "windows":
                torch_cmd = [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cu118"]
            else:
                torch_cmd = [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio"]
            
            subprocess.check_call(torch_cmd)
            
            # Instalar el resto de dependencias
            logger.info("📚 Instalando dependencias adicionales...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_multimodal.txt"])
            
            logger.info("✅ Dependencias instaladas correctamente")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Error instalando dependencias: {e}")
            self.errors.append(f"Instalación fallida: {e}")
            return False
    
    def verify_installation(self):
        """Verificar que las librerías críticas se instalaron correctamente"""
        logger.info("🔍 Verificando instalación...")
        
        critical_packages = [
            "torch",
            "torchvision", 
            "torchaudio",
            "transformers",
            "PIL",
            "cv2",
            "numpy",
            "whisper",
            "clip",
        ]
        
        optional_packages = [
            "librosa",
            "av",
            "soundfile"
        ]
        
        failed_critical = []
        failed_optional = []
        
        # Verificar paquetes críticos
        for package in critical_packages:
            try:
                if package == "PIL":
                    import PIL
                elif package == "cv2":
                    import cv2
                else:
                    importlib.import_module(package)
                
                logger.info(f"✅ {package} disponible")
                self.installed_packages.append(package)
                
            except ImportError:
                logger.warning(f"❌ {package} no disponible")
                failed_critical.append(package)
        
        # Verificar paquetes opcionales
        for package in optional_packages:
            try:
                importlib.import_module(package)
                logger.info(f"✅ {package} (opcional) disponible")
                self.installed_packages.append(package)
            except ImportError:
                logger.warning(f"⚠️ {package} (opcional) no disponible")
                failed_optional.append(package)
        
        # Resumen
        if failed_critical:
            logger.error(f"❌ Paquetes críticos faltantes: {', '.join(failed_critical)}")
            return False
        else:
            logger.info(f"✅ Todos los paquetes críticos instalados ({len(critical_packages - len(failed_critical))}/{len(critical_packages)})")
            
        if failed_optional:
            logger.warning(f"⚠️ Funcionalidad limitada por paquetes opcionales faltantes: {', '.join(failed_optional)}")
        
        return True
    
    def test_multimodal_manager(self):
        """Probar el sistema multimodal"""
        logger.info("🧪 Probando sistema multimodal...")
        
        try:
            from multimodal_ai_manager import MultimodalAIManager
            
            # Crear instancia de prueba
            manager = MultimodalAIManager(device="cpu")  # Usar CPU para prueba
            
            logger.info("✅ MultimodalAIManager inicializado correctamente")
            
            # Verificar configuración de modelos
            available_models = len(manager.model_configs)
            enabled_models = sum(1 for config in manager.model_configs.values() if config.enabled)
            
            logger.info(f"📊 Modelos configurados: {available_models} total, {enabled_models} habilitados")
            
            # Información de dispositivo
            logger.info(f"🔧 Dispositivo detectado: {manager.device}")
            
            # Memoria disponible
            memory_info = manager.get_memory_usage()
            logger.info(f"💾 Estado inicial: {memory_info}")
            
            return True
            
        except ImportError as e:
            logger.error(f"❌ No se puede importar MultimodalAIManager: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error probando sistema multimodal: {e}")
            return False
    
    def setup_model_cache(self):
        """Configurar directorio de cache para modelos"""
        cache_dir = Path("./model_cache")
        cache_dir.mkdir(exist_ok=True)
        
        logger.info(f"📁 Directorio de cache configurado: {cache_dir.absolute()}")
        
        # Configurar variables de entorno para Hugging Face
        os.environ["TRANSFORMERS_CACHE"] = str(cache_dir)
        os.environ["HF_HOME"] = str(cache_dir)
        
        return str(cache_dir)
    
    def generate_config_file(self):
        """Generar archivo de configuración"""
        config = {
            "multimodal_enabled": True,
            "device": "auto",
            "cache_dir": "./model_cache",
            "models": {
                "vision": ["moondream2", "florence2"],
                "audio": ["whisper_medium"],
                "multimodal": ["clip_vit"]
            },
            "optimization": {
                "use_quantization": True,
                "max_memory_per_model": "2GB",
                "parallel_processing": True
            }
        }
        
        config_file = Path("multimodal_config.json")
        with open(config_file, 'w') as f:
            import json
            json.dump(config, f, indent=2)
        
        logger.info(f"⚙️ Archivo de configuración creado: {config_file}")
    
    def print_summary(self):
        """Imprimir resumen de la instalación"""
        logger.info("\n" + "="*60)
        logger.info("📋 RESUMEN DE INSTALACIÓN MULTIMODAL")
        logger.info("="*60)
        
        logger.info(f"🐍 Python: {sys.version}")
        logger.info(f"💻 Sistema: {platform.system()} {platform.machine()}")
        
        gpu_available, device_type = self.check_gpu_support()
        if gpu_available and device_type == "cuda":
            logger.info("🎮 GPU: Disponible (CUDA)")
        else:
            logger.info("💻 GPU: No disponible (usando CPU)")
        
        logger.info(f"✅ Paquetes instalados: {len(self.installed_packages)}")
        
        if self.errors:
            logger.error(f"❌ Errores encontrados: {len(self.errors)}")
            for error in self.errors:
                logger.error(f"   - {error}")
        else:
            logger.info("🎉 ¡Instalación completada sin errores!")
        
        logger.info("\n📝 PRÓXIMOS PASOS:")
        logger.info("1. Ejecutar: python flask_app.py")
        logger.info("2. Acceder a: http://localhost:5000/multimodal")
        logger.info("3. Probar subida de imágenes/audio/video")
        logger.info("4. Los modelos se descargarán automáticamente al primer uso")
        
        logger.info("\n🔧 CONFIGURACIÓN:")
        logger.info("- Cache de modelos: ./model_cache/")
        logger.info("- Configuración: multimodal_config.json")
        logger.info("- Logs: Ver consola del servidor Flask")
        
        logger.info("="*60)
    
    def run(self):
        """Ejecutar instalación completa"""
        logger.info("🚀 VIGOLEONROCKS - Instalador Multimodal 2025")
        logger.info("Iniciando instalación de modelos de AI avanzados...\n")
        
        # Verificaciones previas
        if not self.check_python_version():
            return False
        
        # Configurar cache
        self.setup_model_cache()
        
        # Instalar dependencias
        if not self.install_requirements():
            return False
        
        # Verificar instalación
        if not self.verify_installation():
            return False
        
        # Probar sistema
        if not self.test_multimodal_manager():
            logger.warning("⚠️ Prueba del sistema multimodal falló, pero instalación básica completa")
        
        # Generar configuración
        self.generate_config_file()
        
        # Resumen final
        self.print_summary()
        
        return len(self.errors) == 0

def main():
    """Función principal"""
    installer = MultimodalInstaller()
    
    try:
        success = installer.run()
        
        if success:
            logger.info("🎉 ¡Instalación multimodal completada exitosamente!")
            sys.exit(0)
        else:
            logger.error("❌ Instalación completada con errores")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⚠️ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
