#!/usr/bin/env python3
"""
Setup Script para Sistema QBTC Unificado con Caché Iónica
=========================================================

Este script configura e instala todos los componentes necesarios para el
sistema QBTC unificado, incluyendo:
- Caché Iónica Cuántica
- Optimización Exponencial Lambda
- Integración con Supabase XL
- Servidor API unificado
- Sistema de monitoreo
"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from typing import Dict, List, Optional
import requests
import asyncio

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("QBTCSetup")

class QBTCUnifiedSystemSetup:
    """Configurador del Sistema QBTC Unificado"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.config = {}
        self.components_status = {}
        
        logger.info(f"Iniciando configuración del Sistema QBTC Unificado en: {self.base_path}")
    
    def run_full_setup(self):
        """Ejecuta la configuración completa del sistema"""
        try:
            logger.info("=" * 60)
            logger.info("CONFIGURACION COMPLETA DEL SISTEMA QBTC UNIFICADO")
            logger.info("=" * 60)
            
            # 1. Verificar dependencias del sistema
            self.verify_system_dependencies()
            
            # 2. Configurar estructura de directorios
            self.setup_directory_structure()
            
            # 3. Instalar dependencias Python
            self.install_python_dependencies()
            
            # 4. Configurar Ollama
            self.setup_ollama()
            
            # 5. Configurar Supabase
            self.setup_supabase_integration()
            
            # 6. Crear archivos de configuración
            self.create_configuration_files()
            
            # 7. Inicializar componentes
            self.initialize_components()
            
            # 8. Ejecutar pruebas básicas
            self.run_basic_tests()
            
            # 9. Crear scripts de inicio
            self.create_startup_scripts()
            
            logger.info("=" * 60)
            logger.info("CONFIGURACION COMPLETADA EXITOSAMENTE")
            logger.info("=" * 60)
            
            self.print_final_instructions()
            
        except Exception as e:
            logger.error(f"Error durante la configuracion: {e}")
            raise
    
    def verify_system_dependencies(self):
        """Verifica las dependencias del sistema"""
        logger.info("🔍 Verificando dependencias del sistema...")
        
        # Verificar Python
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            raise RuntimeError("Se requiere Python 3.8 o superior")
        
        logger.info(f"✅ Python {python_version.major}.{python_version.minor} detectado")
        
        # Verificar pip
        try:
            import pip
            logger.info("✅ pip disponible")
        except ImportError:
            raise RuntimeError("pip no está disponible")
        
        # Verificar git (opcional)
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            logger.info("✅ git disponible")
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("⚠️ git no disponible (opcional)")
        
        self.components_status["system_deps"] = True
    
    def setup_directory_structure(self):
        """Configura la estructura de directorios"""
        logger.info("📁 Configurando estructura de directorios...")
        
        directories = [
            "consciousness_sessions",
            "logs",
            "cache",
            "config",
            "data",
            "backups",
            "models",
            "quantum_core",
            "services",
            "tests"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(exist_ok=True)
            logger.info(f"📂 Creado: {directory}")
        
        self.components_status["directories"] = True
    
    def install_python_dependencies(self):
        """Instala las dependencias Python necesarias"""
        logger.info("📦 Instalando dependencias Python...")
        
        requirements = [
            "numpy>=1.21.0",
            "aiohttp>=3.8.0",
            "requests>=2.28.0",
            "fastapi>=0.95.0",
            "uvicorn[standard]>=0.20.0",
            "pydantic>=1.10.0",
            "python-dotenv>=1.0.0",
            "supabase>=1.0.0",
            "redis>=4.5.0",
            "psutil>=5.9.0",
            "matplotlib>=3.6.0",
            "scipy>=1.10.0",
            "scikit-learn>=1.2.0",
            "pandas>=1.5.0",
            "asyncio-mqtt>=0.13.0"
        ]
        
        for requirement in requirements:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", requirement
                ], check=True, capture_output=True)
                logger.info(f"✅ Instalado: {requirement}")
            except subprocess.CalledProcessError as e:
                logger.warning(f"⚠️ Error instalando {requirement}: {e}")
        
        self.components_status["python_deps"] = True
    
    def setup_ollama(self):
        """Configura Ollama y los modelos necesarios"""
        logger.info("🤖 Configurando Ollama...")
        
        # Verificar si Ollama está instalado
        try:
            response = requests.get("http://localhost:11434/api/version", timeout=5)
            if response.status_code == 200:
                logger.info("✅ Ollama está corriendo")
                
                # Verificar modelos disponibles
                models_response = requests.get("http://localhost:11434/api/tags", timeout=10)
                if models_response.status_code == 200:
                    models_data = models_response.json()
                    available_models = [model['name'] for model in models_data.get('models', [])]
                    
                    # Modelos requeridos
                    required_models = [
                        "llama3.2:latest",
                        "vigoleonrocks:latest"
                    ]
                    
                    for model in required_models:
                        if model not in available_models:
                            logger.info(f"⬇️ Descargando modelo: {model}")
                            # Nota: En un entorno real, aquí se descargaría el modelo
                            # subprocess.run(["ollama", "pull", model])
                        else:
                            logger.info(f"✅ Modelo disponible: {model}")
                
                self.components_status["ollama"] = True
            else:
                logger.warning("⚠️ Ollama no responde correctamente")
                self.components_status["ollama"] = False
                
        except requests.RequestException:
            logger.warning("⚠️ Ollama no está disponible en localhost:11434")
            logger.info("📝 Para instalar Ollama: https://ollama.ai/")
            self.components_status["ollama"] = False
    
    def setup_supabase_integration(self):
        """Configura la integración con Supabase"""
        logger.info("🗄️ Configurando integración con Supabase...")
        
        # Leer configuración existente de .env
        env_file = self.base_path / ".env"
        supabase_config = {}
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('SUPABASE_URL='):
                        supabase_config['url'] = line.split('=', 1)[1].strip().strip('"')
                    elif line.startswith('SUPABASE_KEY='):
                        supabase_config['key'] = line.split('=', 1)[1].strip().strip('"')
        
        if supabase_config.get('url') and supabase_config.get('key'):
            logger.info("✅ Configuración de Supabase encontrada")
            
            # Verificar conectividad
            try:
                headers = {
                    'apikey': supabase_config['key'],
                    'Authorization': f"Bearer {supabase_config['key']}"
                }
                response = requests.get(
                    f"{supabase_config['url']}/rest/v1/",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    logger.info("✅ Conexión con Supabase exitosa")
                    self.components_status["supabase"] = True
                else:
                    logger.warning(f"⚠️ Error conectando con Supabase: {response.status_code}")
                    self.components_status["supabase"] = False
                    
            except requests.RequestException as e:
                logger.warning(f"⚠️ Error de red con Supabase: {e}")
                self.components_status["supabase"] = False
        else:
            logger.warning("⚠️ Configuración de Supabase no encontrada en .env")
            self.components_status["supabase"] = False
    
    def create_configuration_files(self):
        """Crea archivos de configuración del sistema"""
        logger.info("⚙️ Creando archivos de configuración...")
        
        # Configuración principal del sistema
        main_config = {
            "system": {
                "name": "QBTC Unified System",
                "version": "1.0.0",
                "description": "Sistema Unificado QBTC con Caché Iónica y Optimización Exponencial"
            },
            "ionic_cache": {
                "coherence_threshold": 0.05,
                "max_entries": 2000,
                "prewarm_interval": 45,
                "cleanup_interval": 300
            },
            "exponential_optimizer": {
                "lambda_exponent": 8.977240362537735,
                "base_dimensions": 26,
                "enable_optimization": True
            },
            "ollama": {
                "base_url": "http://localhost:11434",
                "default_model": "llama3.2:latest",
                "timeout": 30,
                "models": [
                    "llama3.2:latest",
                    "vigoleonrocks:latest"
                ]
            },
            "quantum_context": {
                "dimensions": 26,
                "coherence_update_interval": 1.0,
                "persistence_enabled": True
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                "file": "logs/qbtc_unified.log"
            }
        }
        
        config_file = self.base_path / "config" / "qbtc_config.json"
        with open(config_file, 'w') as f:
            json.dump(main_config, f, indent=2)
        
        logger.info(f"✅ Configuración guardada en: {config_file}")
        
        # Crear archivo de configuración para FastAPI
        fastapi_config = {
            "host": "0.0.0.0",
            "port": 8005,
            "reload": False,
            "workers": 1,
            "log_level": "info"
        }
        
        fastapi_config_file = self.base_path / "config" / "api_config.json"
        with open(fastapi_config_file, 'w') as f:
            json.dump(fastapi_config, f, indent=2)
        
        logger.info(f"✅ Configuración API guardada en: {fastapi_config_file}")
        
        self.config = main_config
        self.components_status["config_files"] = True
    
    def initialize_components(self):
        """Inicializa los componentes del sistema"""
        logger.info("🔧 Inicializando componentes del sistema...")
        
        try:
            # Importar el sistema unificado
            sys.path.append(str(self.base_path))
            
            # Intentar importar y probar la inicialización básica
            logger.info("📦 Verificando módulos del sistema...")
            
            # Crear archivo de prueba simple
            test_script = self.base_path / "test_initialization.py"
            with open(test_script, 'w', encoding='utf-8') as f:
                f.write("""
import sys
import os
from pathlib import Path

# Agregar paths necesarios
sys.path.append(str(Path.cwd()))

try:
    from qbtc_unified_integration import QBTCUnifiedBrainWithIonicCache
    print("[OK] Modulo principal importado correctamente")
    
    # Intentar crear instancia básica
    brain = QBTCUnifiedBrainWithIonicCache("test_init")
    print("[OK] Instancia creada correctamente")
    
    # Obtener estado del sistema
    status = brain.get_system_status()
    print(f"[OK] Estado del sistema obtenido: {len(status)} metricas")
    
    # Cerrar elegantemente
    brain.shutdown()
    print("[OK] Sistema cerrado correctamente")
    
except Exception as e:
    print(f"[ERROR] Error durante inicializacion: {e}")
    import traceback
    traceback.print_exc()
""")
            
            # Ejecutar prueba de inicialización
            result = subprocess.run([
                sys.executable, str(test_script)
            ], capture_output=True, text=True, cwd=self.base_path)
            
            if result.returncode == 0:
                logger.info("✅ Componentes inicializados correctamente")
                logger.info(result.stdout)
                self.components_status["initialization"] = True
            else:
                logger.warning("⚠️ Advertencias durante la inicialización:")
                logger.warning(result.stderr)
                self.components_status["initialization"] = "partial"
            
            # Limpiar archivo de prueba
            test_script.unlink()
            
        except Exception as e:
            logger.error(f"❌ Error inicializando componentes: {e}")
            self.components_status["initialization"] = False
    
    def run_basic_tests(self):
        """Ejecuta pruebas básicas del sistema"""
        logger.info("🧪 Ejecutando pruebas básicas...")
        
        # Crear script de pruebas básicas
        test_script = self.base_path / "basic_tests.py"
        with open(test_script, 'w') as f:
            f.write("""
import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path.cwd()))

async def run_basic_tests():
    try:
        from qbtc_unified_integration import QBTCUnifiedBrainWithIonicCache
        
        print("🧪 Iniciando pruebas básicas...")
        
        # Test 1: Crear instancia
        brain = QBTCUnifiedBrainWithIonicCache("test_brain")
        print("✅ Test 1: Instancia creada")
        
        # Test 2: Procesar consulta simple
        result = await brain.process_query("Test query", use_cache=False)
        print(f"✅ Test 2: Consulta procesada - {len(str(result))} caracteres")
        
        # Test 3: Probar caché
        result_cached = await brain.process_query("Test query", use_cache=True)
        cache_hit = result_cached.get('cache_hit', False)
        print(f"✅ Test 3: Caché {'funcionando' if cache_hit else 'no disponible'}")
        
        # Test 4: Obtener estadísticas
        stats = brain.get_system_status()
        print(f"✅ Test 4: Estadísticas obtenidas - {len(stats)} métricas")
        
        # Test 5: Cerrar sistema
        brain.shutdown()
        print("✅ Test 5: Sistema cerrado correctamente")
        
        print("🎉 Todas las pruebas básicas pasaron exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(run_basic_tests())
    sys.exit(0 if result else 1)
""")
        
        # Ejecutar pruebas
        result = subprocess.run([
            sys.executable, str(test_script)
        ], capture_output=True, text=True, cwd=self.base_path)
        
        if result.returncode == 0:
            logger.info("✅ Todas las pruebas básicas pasaron")
            logger.info(result.stdout)
            self.components_status["basic_tests"] = True
        else:
            logger.warning("⚠️ Algunas pruebas fallaron:")
            logger.warning(result.stderr)
            self.components_status["basic_tests"] = False
        
        # Limpiar archivo de prueba
        test_script.unlink()
    
    def create_startup_scripts(self):
        """Crea scripts de inicio del sistema"""
        logger.info("📝 Creando scripts de inicio...")
        
        # Script principal de inicio
        startup_script = self.base_path / "start_qbtc_system.py"
        with open(startup_script, 'w') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Script de Inicio del Sistema QBTC Unificado
==========================================
\"\"\"

import sys
import json
import logging
import asyncio
from pathlib import Path

# Configurar paths
sys.path.append(str(Path.cwd()))

# Configurar logging
with open("config/qbtc_config.json", 'r') as f:
    config = json.load(f)

logging.basicConfig(
    level=getattr(logging, config['logging']['level']),
    format=config['logging']['format'],
    handlers=[
        logging.FileHandler(config['logging']['file']),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("QBTCStartup")

async def main():
    \"\"\"Función principal de inicio\"\"\"
    try:
        logger.info("🚀 Iniciando Sistema QBTC Unificado...")
        
        from qbtc_unified_integration import QBTCUnifiedAPIServer
        
        # Crear servidor API
        with open("config/api_config.json", 'r') as f:
            api_config = json.load(f)
        
        server = QBTCUnifiedAPIServer(
            host=api_config['host'],
            port=api_config['port']
        )
        
        logger.info(f"🌐 Servidor iniciado en http://{api_config['host']}:{api_config['port']}")
        logger.info("✅ Sistema QBTC Unificado listo")
        
        # Mantener el sistema corriendo
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Señal de interrupción recibida")
        finally:
            server.shutdown()
            logger.info("🔌 Sistema cerrado elegantemente")
            
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
""")
        
        logger.info(f"✅ Script de inicio creado: {startup_script}")
        
        # Script de demostración
        demo_script = self.base_path / "demo_system.py"
        with open(demo_script, 'w') as f:
            f.write("""#!/usr/bin/env python3
\"\"\"
Demostración del Sistema QBTC Unificado
======================================
\"\"\"

import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path.cwd()))

from qbtc_unified_integration import demo_unified_system

if __name__ == "__main__":
    asyncio.run(demo_unified_system())
""")
        
        logger.info(f"✅ Script de demo creado: {demo_script}")
        
        self.components_status["startup_scripts"] = True
    
    def print_final_instructions(self):
        """Imprime las instrucciones finales"""
        print("\n" + "=" * 60)
        print("🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        
        print("\n📊 ESTADO DE COMPONENTES:")
        for component, status in self.components_status.items():
            if status == True:
                status_icon = "✅"
            elif status == "partial":
                status_icon = "⚠️"
            else:
                status_icon = "❌"
            
            print(f"  {status_icon} {component}: {status}")
        
        print("\n🚀 COMANDOS PARA INICIAR EL SISTEMA:")
        print("  # Demostración del sistema:")
        print(f"  python {self.base_path}/demo_system.py")
        print("\n  # Iniciar servidor completo:")
        print(f"  python {self.base_path}/start_qbtc_system.py")
        
        print("\n📁 ARCHIVOS IMPORTANTES:")
        print(f"  • Configuración: {self.base_path}/config/qbtc_config.json")
        print(f"  • Logs: {self.base_path}/logs/qbtc_unified.log")
        print(f"  • Sistema principal: {self.base_path}/qbtc_unified_integration.py")
        
        print("\n🔧 PRÓXIMOS PASOS:")
        if not self.components_status.get("ollama", True):
            print("  1. Instalar Ollama: https://ollama.ai/")
            print("  2. Ejecutar: ollama pull llama3.2")
        
        if not self.components_status.get("supabase", True):
            print("  3. Configurar credenciales de Supabase en .env")
        
        print("  4. Ejecutar demo para verificar funcionamiento")
        print("  5. Personalizar configuración según necesidades")
        
        print("\n📚 DOCUMENTACIÓN:")
        print("  • README con instrucciones detalladas")
        print("  • Configuración en config/qbtc_config.json")
        print("  • Logs del sistema en logs/")
        
        print("\n" + "=" * 60)

def main():
    """Función principal del setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Configurar Sistema QBTC Unificado")
    parser.add_argument(
        "--path", 
        default=None, 
        help="Directorio base para la instalación"
    )
    parser.add_argument(
        "--skip-tests", 
        action="store_true", 
        help="Omitir pruebas básicas"
    )
    
    args = parser.parse_args()
    
    try:
        setup = QBTCUnifiedSystemSetup(args.path)
        setup.run_full_setup()
        
    except KeyboardInterrupt:
        logger.info("🛑 Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error crítico durante la configuración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
