#!/usr/bin/env python3
"""
🌟 Orquestador Python Cuántico Simplificado
Sistema de monitoreo y control para VigosuelDo Quantum

Enfoque: Máximo impacto con mínima complejidad
Métricas críticas: TranscendenceMetrics + QuantumConnectionState
"""

import os
import sys
import time
import json
import subprocess
import threading
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path
from flask_socketio import SocketIO, emit

# Importar módulos cuánticos
from quantum.metrics_collector import MetricsCollector
from quantum.dashboard_server import DashboardServer

class QuantumOrchestrator:
    """Orquestador principal del sistema cuántico"""
    
    def __init__(self):
        self.config = {
            'dashboard_port': 8000,
            'metrics_interval': 5,  # segundos
            'websocket_interval': 2,  # segundos
            'history_retention': 24,  # horas
            'alert_thresholds': {
                'ipp_min': 0.3,
                'wisdom_min': 0.1,
                'resonance_min': 0.3
            }
        }
        
        self.metrics_collector = MetricsCollector(self.config)
        self.dashboard_server = DashboardServer(self.config, self.metrics_collector)
        self.socketio = SocketIO(self.dashboard_server.app, cors_allowed_origins="*")
        self._setup_websocket_handlers()
        self.services_status = {}
        self.running = False
        
        print("[QUANTUM] Orquestador Cuantico Inicializado")
    
    def start(self, dashboard_only=False):
        """Inicia el orquestador completo"""
        print("[QUANTUM] Iniciando Orquestador Python Cuantico...")
        self.running = True
        
        try:
            # 1. Verificar dependencias
            self._check_dependencies()
            
            # 2. Iniciar servicios (si no es solo dashboard)
            if not dashboard_only:
                self._start_services()
            
            # 3. Iniciar recolector de métricas
            self._start_metrics_collection()
            
            # 4. Iniciar dashboard Flask
            self._start_dashboard()
            
            # 5. Abrir navegador automáticamente
            self._open_browser()
            
            # 6. Mantener vivo el orquestador
            self._keep_alive()
            
        except KeyboardInterrupt:
            print("\n[QUANTUM] Deteniendo Orquestador Cuantico...")
            self.stop()
        except Exception as e:
            print(f"[ERROR] Error en orquestador: {e}")
            self.stop()
    
    def stop(self):
        """Detiene el orquestador"""
        self.running = False
        self.dashboard_server.stop()
        print("[QUANTUM] Orquestador Cuantico Detenido")
    
    def _check_dependencies(self):
        """Verifica dependencias del sistema"""
        print("[SETUP] Verificando dependencias...")
        
        required_modules = ['flask', 'flask_socketio', 'requests', 'psutil']
        missing = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            print(f"[ERROR] Modulos faltantes: {', '.join(missing)}")
            print("[INFO] Instalar con: pip install " + " ".join(missing))
            sys.exit(1)
        
        print("[SETUP] Dependencias verificadas")
    
    def _start_services(self):
        """Inicia servicios del sistema"""
        print("[SERVICES] Iniciando servicios...")
        
        # Verificar y ejecutar quantum-cleaner.cjs
        if Path("quantum-cleaner.cjs").exists():
            try:
                result = subprocess.run(
                    ["node", "quantum-cleaner.cjs"], 
                    capture_output=True, 
                    text=True,
                    shell=True
                )
                if result.returncode == 0:
                    print("[SERVICES] quantum-cleaner.cjs ejecutado")
                    self.services_status['cleaner'] = 'success'
                else:
                    print(f"[WARNING] quantum-cleaner.cjs error: {result.stderr}")
                    self.services_status['cleaner'] = 'error'
            except Exception as e:
                print(f"[ERROR] Error ejecutando cleaner: {e}")
                self.services_status['cleaner'] = 'error'
        else:
            print("[WARNING] quantum-cleaner.cjs no encontrado")
            self.services_status['cleaner'] = 'not_found'
        
        # Verificar servicios en puertos conocidos
        self._check_service_ports()
    
    def _check_service_ports(self):
        """Verifica estado de servicios en puertos"""
        import socket
        
        ports_to_check = {
            'backend': 5000,
            'frontend': 3000,
            'vite': 5173
        }
        
        for service, port in ports_to_check.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                if result == 0:
                    print(f"[SERVICES] {service} activo en puerto {port}")
                    self.services_status[service] = 'running'
                else:
                    self.services_status[service] = 'stopped'
            except Exception:
                self.services_status[service] = 'error'
    
    def _start_metrics_collection(self):
        """Inicia recolección de métricas en hilo separado"""
        print("[METRICS] Iniciando recoleccion de metricas...")
        
        def metrics_loop():
            while self.running:
                try:
                    self.metrics_collector.collect_all_metrics()
                    time.sleep(self.config['metrics_interval'])
                except Exception as e:
                    print(f"[ERROR] Error recolectando metricas: {e}")
                    time.sleep(5)
        
        metrics_thread = threading.Thread(target=metrics_loop, daemon=True)
        metrics_thread.start()
        print("[METRICS] Recoleccion de metricas iniciada")
    
    def _setup_websocket_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            print('[WEBSOCKET] Cliente React conectado')
            emit('connection_established', {'status': 'connected'})
        
        @self.socketio.on('request_metrics')
        def handle_metrics_request():
            metrics = self.metrics_collector.get_latest_metrics()
            emit('metrics_update', metrics)

    def _emit_metrics_to_react(self):
        # Emitir métricas cada 2 segundos a React
        metrics = self.metrics_collector.get_latest_metrics()
        self.socketio.emit('metrics_update', metrics)

    def _start_dashboard(self):
        """Inicia servidor dashboard Flask con WebSocket"""
        print(f"[DASHBOARD] Iniciando dashboard en puerto {self.config['dashboard_port']}...")
        
        def dashboard_loop():
            self.socketio.run(self.dashboard_server.app,
                             host='localhost',
                             port=self.config['dashboard_port'],
                             debug=False)
        
        dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
        dashboard_thread.start()
        
        # Esperar a que el servidor esté listo
        time.sleep(2)
        print("[DASHBOARD] Dashboard con WebSocket iniciado")
    
    def _open_browser(self):
        """Abre el dashboard en el navegador"""
        dashboard_url = f"http://localhost:{self.config['dashboard_port']}"
        
        try:
            webbrowser.open(dashboard_url)
            print(f"[DASHBOARD] Dashboard abierto: {dashboard_url}")
        except Exception as e:
            print(f"[WARNING] No se pudo abrir navegador: {e}")
            print(f"[INFO] Accede manualmente a: {dashboard_url}")
    
    def _keep_alive(self):
        """Mantiene el orquestador vivo y emite métricas"""
        print("[QUANTUM] Orquestador activo. Presiona Ctrl+C para detener.")
        
        while self.running:
            try:
                time.sleep(self.config['websocket_interval'])  # Emitir cada 'websocket_interval' segundos
                
                # Emitir métricas a React
                self._emit_metrics_to_react()
                
                # Mostrar estado cada 30 segundos
                if int(time.time()) % 30 == 0:
                    self._show_status()
                    
            except KeyboardInterrupt:
                break
    
    def _show_status(self):
        """Muestra estado actual del sistema"""
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\n[STATUS] {current_time} - Estado del Sistema:")
        
        # Estado de servicios
        # Aquí usaremos el estado dinámico que MetricsCollector genera
        services_data = self.metrics_collector.get_latest_metrics().get('services', {})
        for service, status in services_data.items():
            status_icon = {
                'running': '[OK]',
                'stopped': '[STOP]',
                'error': '[ERROR]',
                'success': '[OK]',
                'not_found': '[WARN]',
                'unknown': '[?]'
            }.get(status, '[?]')
            print(f"  {status_icon} {service}: {status}")
        
        # Métricas actuales
        latest_metrics = self.metrics_collector.get_latest_metrics()
        if latest_metrics:
            transcendence = latest_metrics.get('transcendence', {})
            connection = latest_metrics.get('connection', {})
            
            ipp = transcendence.get('indicePrecisionProfetica', 0)
            wisdom = transcendence.get('sabiduriaAcumulada', 0)
            connected = connection.get('isConnected', False)
            prophetic = connection.get('isInPropheticMode', False)
            
            # Nuevas métricas financieras si existen
            financial_metrics = latest_metrics.get('financial', {})
            current_leverage = financial_metrics.get('currentLeverage', 0)
            leverage_risk = financial_metrics.get('leverageRiskStatus', 'N/D')
            trailing_stops_active = financial_metrics.get('trailingStopActivated', False)
            
            print(f"  [METRICS] IPP: {ipp:.1%} | Sabiduría: {wisdom:.1%}")
            print(f"  [CONNECTION] Conectado: {'SI' if connected else 'NO'} | Profetico: {'SI' if prophetic else 'NO'}")
            print(f"  [FINANCIAL] Apalancamiento: {current_leverage:.2f}x ({leverage_risk}) | Trailing Stops Activos: {'SI' if trailing_stops_active else 'NO'}")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Orquestador Python Cuántico')
    parser.add_argument('--dashboard-only', action='store_true', 
                       help='Solo ejecutar dashboard (sin servicios)')
    parser.add_argument('--debug', action='store_true',
                       help='Modo debug con logs detallados')
    
    args = parser.parse_args()
    
    if args.debug:
        os.environ['FLASK_ENV'] = 'development'
        print("[DEBUG] Modo debug activado")
    
    # Crear y ejecutar orquestador
    orchestrator = QuantumOrchestrator()
    orchestrator.start(dashboard_only=args.dashboard_only)

if __name__ == "__main__":
    main()
