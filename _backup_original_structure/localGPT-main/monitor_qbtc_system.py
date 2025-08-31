#!/usr/bin/env python3
"""
🔍 QBTC Unified System Monitor
Monitoreo en tiempo real del sistema unificado
"""

import psutil
import requests
import asyncio
import time
from datetime import datetime
import json

class QBTCSystemMonitor:
    def __init__(self):
        self.services = {
            "QBTC Unified Integration": {
                "port": 8005,
                "process_name": "qbtc_unified_integration.py",
                "status": "unknown"
            },
            "Claude Engineer v3": {
                "port": 5000,
                "process_name": "app.py",
                "status": "unknown"
            },
            "Quantum Core": {
                "port": 8300,
                "process_name": "quantum",
                "status": "unknown"
            }
        }
        
    def check_process_status(self):
        """Verifica el estado de los procesos Python"""
        python_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if proc.info['name'] == 'python.exe' or proc.info['name'] == 'python':
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        python_processes.append({
                            'pid': proc.info['pid'],
                            'cmdline': cmdline,
                            'create_time': datetime.fromtimestamp(proc.info['create_time']),
                            'status': proc.status()
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return python_processes
    
    def check_port_connectivity(self):
        """Verifica conectividad de puertos"""
        port_status = {}
        
        for service_name, config in self.services.items():
            port = config['port']
            try:
                response = requests.get(f"http://localhost:{port}", timeout=2)
                port_status[port] = {
                    'status': 'active',
                    'response_code': response.status_code,
                    'service': service_name
                }
            except requests.exceptions.RequestException:
                port_status[port] = {
                    'status': 'inactive',
                    'response_code': None,
                    'service': service_name
                }
                
        return port_status
    
    async def monitor_quantum_metrics(self):
        """Monitorea métricas cuánticas del sistema"""
        try:
            # Intentar conectar con el sistema unificado
            response = requests.get("http://localhost:8005/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Sistema unificado no disponible"}
        except:
            return {"error": "No se puede conectar al sistema cuántico"}
    
    def generate_system_report(self):
        """Genera reporte completo del sistema"""
        print("🌌 QBTC UNIFIED SYSTEM - REPORTE DE ESTADO")
        print("=" * 60)
        print(f"📅 Timestamp: {datetime.now()}")
        print()
        
        # Estado de procesos Python
        print("🐍 PROCESOS PYTHON ACTIVOS:")
        processes = self.check_process_status()
        for proc in processes:
            print(f"   PID {proc['pid']}: {proc['cmdline'][:80]}...")
            print(f"   Started: {proc['create_time']} | Status: {proc['status']}")
        print()
        
        # Estado de puertos
        print("🌐 CONECTIVIDAD DE PUERTOS:")
        port_status = self.check_port_connectivity()
        for port, status in port_status.items():
            status_icon = "✅" if status['status'] == 'active' else "❌"
            print(f"   {status_icon} Puerto {port}: {status['status']} - {status['service']}")
        print()
        
        # Métricas del sistema
        print("📊 MÉTRICAS DEL SISTEMA:")
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        print(f"   CPU: {cpu_percent}%")
        print(f"   Memoria: {memory.percent}% ({memory.available // (1024**3)} GB disponible)")
        print()
        
        # Servicios de infraestructura según las reglas
        print("🏗️ INFRAESTRUCTURA CONSOLIDADA:")
        infrastructure_services = ["APISIX", "Supabase", "Redis", "RabbitMQ"]
        for service in infrastructure_services:
            print(f"   📦 {service}: Estado según reglas del monorepo")
        print()
        
        # Estado cuántico
        print("⚛️ ESTADO CUÁNTICO:")
        print("   🧠 Núcleo de IA Cuántica: Compartido entre productos")
        print("   🔄 Orquestación RabbitMQ: Eventos de microservicios")
        print("   📡 API Gateway APISIX: Consolidado")
        print()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "processes": len(processes),
            "ports_active": len([p for p in port_status.values() if p['status'] == 'active']),
            "system_health": "operational" if processes else "degraded"
        }

async def main():
    """Función principal de monitoreo"""
    monitor = QBTCSystemMonitor()
    
    print("🚀 Iniciando monitoreo del sistema QBTC Unified...")
    
    # Generar reporte inicial
    report = monitor.generate_system_report()
    
    # Monitoreo continuo cada 30 segundos
    try:
        while True:
            await asyncio.sleep(30)
            print("\n🔄 Actualizando estado del sistema...")
            print("-" * 40)
            
            # Verificar procesos
            processes = monitor.check_process_status()
            print(f"🐍 Procesos Python activos: {len(processes)}")
            
            # Verificar puertos
            ports = monitor.check_port_connectivity()
            active_ports = len([p for p in ports.values() if p['status'] == 'active'])
            print(f"🌐 Puertos activos: {active_ports}/{len(ports)}")
            
            # Métricas básicas
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            print(f"📊 CPU: {cpu}% | Memoria: {memory}%")
            
            if active_ports == 0 and len(processes) == 0:
                print("⚠️  ADVERTENCIA: No se detectan servicios activos")
                
    except KeyboardInterrupt:
        print("\n👋 Monitoreo detenido por el usuario")

if __name__ == "__main__":
    asyncio.run(main())
