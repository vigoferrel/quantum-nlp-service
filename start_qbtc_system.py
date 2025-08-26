#!/usr/bin/env python3
"""
🚀 QBTC SYSTEM LAUNCHER - Inicialización Robusta Simplificada
Script unificado para iniciar todo el sistema QBTC con manejo de errores
"""

import os
import sys
import subprocess
import time
import signal
import json
import platform
from pathlib import Path
from typing import Dict

class QBTCSystemLauncher:
    """Launcher robusto para el sistema QBTC"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.venv_path = self.project_root / ".venv"
        self.llm_system_path = self.project_root / "localGPT-main" / "integrated_llm_system"
        self.processes = {}
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Cargar configuración del sistema"""
        config_path = self.project_root / "qbtc_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando configuración: {e}")
        
        # Configuración por defecto
        return {
            "server": {
                "host": "127.0.0.1",
                "port": 5000,
                "debug": False
            },
            "ollama": {
                "host": "http://localhost:11434",
                "models": ["llama2", "gemma2", "mistral"]
            },
            "openrouter": {
                "api_key": "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"
            },
            "services": {
                "llm_core": True,
                "web_interface": True,
                "agents": True
            }
        }
    
    def save_config(self):
        """Guardar configuración actual"""
        config_path = self.project_root / "qbtc_config.json"
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error guardando configuración: {e}")
    
    def check_system_requirements(self) -> bool:
        """Verificar requisitos del sistema"""
        print("🔍 Verificando requisitos del sistema...")
        
        # Verificar Python
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ requerido")
            return False
        
        # Verificar virtual environment
        if not self.venv_path.exists():
            print("❌ Virtual environment no encontrado")
            return False
        
        # Verificar directorios críticos
        critical_paths = [
            self.llm_system_path,
            self.llm_system_path / "integrate.py",
            self.llm_system_path / "optimal_ui.py"
        ]
        
        for path in critical_paths:
            if not path.exists():
                print(f"❌ Ruta crítica no encontrada: {path}")
                return False
        
        print("✅ Requisitos del sistema verificados")
        return True
    
    def setup_environment(self) -> bool:
        """Configurar entorno de ejecución"""
        print("🔧 Configurando entorno...")
        
        try:
            # Activar virtual environment
            if platform.system() == "Windows":
                activate_script = self.venv_path / "Scripts" / "Activate.ps1"
                if activate_script.exists():
                    os.environ["VIRTUAL_ENV"] = str(self.venv_path)
                    os.environ["PATH"] = f"{self.venv_path / 'Scripts'};{os.environ['PATH']}"
            
            # Verificar dependencias básicas
            try:
                import flask
                import requests
                print("✅ Dependencias básicas verificadas")
            except ImportError as e:
                print(f"⚠️ Dependencia faltante: {e}")
                print("📦 Instalando dependencias básicas...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "flask", "flask-cors", "requests"
                ], check=True)
            
            print("✅ Entorno configurado")
            return True
            
        except Exception as e:
            print(f"❌ Error configurando entorno: {e}")
            return False
    
    def check_ollama_service(self) -> bool:
        """Verificar servicio Ollama"""
        print("🔍 Verificando servicio Ollama...")
        
        try:
            import requests
            response = requests.get(f"{self.config['ollama']['host']}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                print(f"✅ Ollama disponible con {len(models)} modelos")
                return True
        except Exception as e:
            print(f"⚠️ Ollama no disponible: {e}")
        
        return False
    
    def start_llm_server(self) -> bool:
        """Iniciar servidor LLM principal"""
        print("🚀 Iniciando servidor LLM...")
        
        try:
            # Cambiar al directorio correcto
            os.chdir(self.llm_system_path)
            
            # Iniciar servidor en segundo plano
            process = subprocess.Popen([
                sys.executable, "optimal_ui.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes["llm_server"] = process
            
            # Esperar a que el servidor esté listo
            time.sleep(5)
            
            # Verificar que el servidor esté funcionando
            try:
                import requests
                response = requests.get(f"http://{self.config['server']['host']}:{self.config['server']['port']}", timeout=5)
                if response.status_code == 200:
                    print("✅ Servidor LLM iniciado correctamente")
                    return True
            except Exception as e:
                print(f"⚠️ Error verificando servidor: {e}")
            
            # Verificar si el proceso sigue ejecutándose
            if process.poll() is None:
                print("✅ Servidor LLM iniciado (verificación pendiente)")
                return True
            else:
                print("❌ Servidor LLM no se pudo iniciar")
                return False
            
        except Exception as e:
            print(f"❌ Error iniciando servidor LLM: {e}")
            return False
    
    def show_status(self):
        """Mostrar estado del sistema"""
        print("\n" + "="*60)
        print("📊 ESTADO DEL SISTEMA QBTC")
        print("="*60)
        
        # Estado del servidor principal
        try:
            import requests
            response = requests.get(f"http://{self.config['server']['host']}:{self.config['server']['port']}", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor LLM: FUNCIONANDO")
                print(f"   URL: http://{self.config['server']['host']}:{self.config['server']['port']}")
            else:
                print("⚠️ Servidor LLM: ERROR")
        except Exception as e:
            print(f"❌ Servidor LLM: NO DISPONIBLE ({e})")
        
        # Estado de Ollama
        if self.check_ollama_service():
            print("✅ Ollama: DISPONIBLE")
        else:
            print("⚠️ Ollama: NO DISPONIBLE")
        
        # Procesos activos
        print(f"\n🔄 Procesos activos: {len(self.processes)}")
        for name, process in self.processes.items():
            if process.poll() is None:
                print(f"   ✅ {name}: ACTIVO (PID: {process.pid})")
            else:
                print(f"   ❌ {name}: DETENIDO")
        
        print("\n🎯 INTERFACES DISPONIBLES:")
        print("   🏠 Página Principal: /")
        print("   💬 Chat Inteligente: /chat")
        print("   🧠 Agentes BMAD: /agents")
        print("   🚀 Entrenamiento: /training")
        print("   📊 Evaluación: /evaluation")
        print("   🔧 Desarrollo: /development")
        
        print("="*60)
    
    def stop_all_services(self):
        """Detener todos los servicios"""
        print("🛑 Deteniendo todos los servicios...")
        
        for name, process in self.processes.items():
            try:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ {name} detenido")
                else:
                    print(f"⚠️ {name} ya estaba detenido")
            except Exception as e:
                print(f"❌ Error deteniendo {name}: {e}")
        
        self.processes.clear()
    
    def cleanup(self):
        """Limpieza al salir"""
        print("🧹 Limpiando recursos...")
        self.stop_all_services()
        self.save_config()
    
    def run(self):
        """Ejecutar el launcher principal"""
        print("🚀 INICIANDO SISTEMA QBTC")
        print("="*50)
        
        try:
            # Verificar requisitos
            if not self.check_system_requirements():
                print("❌ Requisitos no cumplidos. Abortando.")
                return False
            
            # Configurar entorno
            if not self.setup_environment():
                print("❌ Error configurando entorno. Abortando.")
                return False
            
            # Verificar Ollama
            self.check_ollama_service()
            
            # Iniciar servidor principal
            if not self.start_llm_server():
                print("❌ Error iniciando servidor principal. Abortando.")
                return False
            
            # Mostrar estado
            self.show_status()
            
            print("\n🎉 ¡SISTEMA QBTC INICIADO EXITOSAMENTE!")
            print("📱 Abre tu navegador en: http://127.0.0.1:5000")
            print("🔧 Presiona Ctrl+C para detener")
            
            # Mantener el sistema corriendo
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Detención solicitada por el usuario")
            
            return True
            
        except Exception as e:
            print(f"❌ Error crítico: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Función principal"""
    launcher = QBTCSystemLauncher()
    
    # Manejar señales de terminación
    def signal_handler(signum, frame):
        print(f"\n🛑 Señal recibida: {signum}")
        launcher.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Ejecutar launcher
    success = launcher.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
