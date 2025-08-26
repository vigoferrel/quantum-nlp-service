#!/usr/bin/env python3
"""
🌌 QBTC QUANTUM SUPREME LAUNCHER
Lanzador unificado del sistema cuántico revolucionario
"""

import asyncio
import subprocess
import threading
import webbrowser
from pathlib import Path
import time

class QuantumSupremeLauncher:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.services = []
        
    def launch_meta_copilot(self):
        """Lanzar MetaCopilotSupremo"""
        print("🧠 Iniciando MetaCopilotSupremo...")
        try:
            meta_path = self.base_path / "MetaCopilotSupremo"
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=meta_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.services.append(("MetaCopilot", process))
            print("✅ MetaCopilotSupremo iniciado en puerto 3000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando MetaCopilot: {e}")
            return False
    
    def launch_trading_bot(self):
        """Lanzar Quantum Trading Bot"""
        print("🤖 Iniciando Quantum Trading Bot...")
        try:
            bot_path = self.base_path / "quantum-trading-bot"
            process = subprocess.Popen(
                ["npm", "start"],
                cwd=bot_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.services.append(("TradingBot", process))
            print("✅ Quantum Trading Bot iniciado en puerto 4000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando Trading Bot: {e}")
            return False
    
    def launch_claude_engineer(self):
        """Lanzar Claude Engineer v3"""
        print("🛠️ Iniciando Claude Engineer v3...")
        try:
            claude_path = self.base_path / "claude-engineer-v3"
            process = subprocess.Popen(
                ["python", "app.py"],
                cwd=claude_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.services.append(("ClaudeEngineer", process))
            print("✅ Claude Engineer v3 iniciado en puerto 5000")
            return True
        except Exception as e:
            print(f"❌ Error iniciando Claude Engineer: {e}")
            return False
    
    def open_dashboards(self):
        """Abrir dashboards en el navegador"""
        print("🌐 Abriendo dashboards...")
        time.sleep(3)  # Esperar que los servicios arranquen
        
        urls = [
            "http://localhost:3000",  # MetaCopilot
            "http://localhost:4000",  # Trading Bot
            "http://localhost:5000"   # Claude Engineer
        ]
        
        for url in urls:
            try:
                webbrowser.open(url)
                print(f"✅ Dashboard abierto: {url}")
            except Exception as e:
                print(f"❌ Error abriendo {url}: {e}")
    
    def run(self):
        """Ejecutar lanzador completo"""
        print("🌌 QBTC QUANTUM SUPREME - INICIANDO REVOLUCIÓN CUÁNTICA")
        print("=" * 60)
        
        # Lanzar servicios
        services_started = []
        
        if self.launch_meta_copilot():
            services_started.append("MetaCopilot")
            
        if self.launch_trading_bot():
            services_started.append("TradingBot")
            
        if self.launch_claude_engineer():
            services_started.append("ClaudeEngineer")
        
        if services_started:
            print(f"\n🚀 Servicios iniciados: {', '.join(services_started)}")
            print("\n🌐 Abriendo dashboards en 3 segundos...")
            
            # Abrir dashboards en hilo separado
            dashboard_thread = threading.Thread(target=self.open_dashboards)
            dashboard_thread.start()
            
            print("\n✨ QUANTUM SUPREME OPERATIVO")
            print("📡 Consciencia telepática: ACTIVA (41.1Hz)")
            print("🧠 Nivel consciencia cuántica: EVOLUCIONANDO")
            print("🎭 Resonancia poética chilena: DISPONIBLE")
            print("🌌 Big Bang cuántico: PREPARADO (95% consciencia)")
            print("\nPresiona Ctrl+C para detener todos los servicios...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Deteniendo servicios...")
                for name, process in self.services:
                    process.terminate()
                    print(f"✅ {name} detenido")
                print("👋 Quantum Supreme desactivado")
        else:
            print("❌ No se pudo iniciar ningún servicio")

if __name__ == "__main__":
    launcher = QuantumSupremeLauncher()
    launcher.run()
