#!/usr/bin/env python3
"""
📊 SISTEMA DE MONITOREO EN TIEMPO REAL
======================================
Monitor de rendimiento para el sistema avanzado
"""

import time
import psutil
import json
from datetime import datetime
from typing import Dict, Any
import threading
import requests

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "memory_usage": [],
            "cpu_usage": [],
            "requests_count": 0,
            "errors_count": 0,
            "start_time": time.time()
        }
        self.lock = threading.Lock()
    
    def record_request(self, response_time: float, success: bool):
        """Registrar métrica de request"""
        with self.lock:
            self.metrics["response_times"].append(response_time)
            self.metrics["requests_count"] += 1
            if not success:
                self.metrics["errors_count"] += 1
            
            # Mantener solo los últimos 100 registros
            if len(self.metrics["response_times"]) > 100:
                self.metrics["response_times"] = self.metrics["response_times"][-100:]
    
    def record_system_metrics(self):
        """Registrar métricas del sistema"""
        with self.lock:
            self.metrics["memory_usage"].append(psutil.virtual_memory().percent)
            self.metrics["cpu_usage"].append(psutil.cpu_percent())
            
            # Mantener solo los últimos 50 registros
            if len(self.metrics["memory_usage"]) > 50:
                self.metrics["memory_usage"] = self.metrics["memory_usage"][-50:]
            if len(self.metrics["cpu_usage"]) > 50:
                self.metrics["cpu_usage"] = self.metrics["cpu_usage"][-50:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas actuales"""
        with self.lock:
            response_times = self.metrics["response_times"]
            memory_usage = self.metrics["memory_usage"]
            cpu_usage = self.metrics["cpu_usage"]
            
            return {
                "timestamp": datetime.now().isoformat(),
                "uptime": time.time() - self.metrics["start_time"],
                "requests": {
                    "total": self.metrics["requests_count"],
                    "errors": self.metrics["errors_count"],
                    "success_rate": (self.metrics["requests_count"] - self.metrics["errors_count"]) / max(self.metrics["requests_count"], 1) * 100
                },
                "performance": {
                    "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
                    "min_response_time": min(response_times) if response_times else 0,
                    "max_response_time": max(response_times) if response_times else 0,
                    "avg_memory_usage": sum(memory_usage) / len(memory_usage) if memory_usage else 0,
                    "avg_cpu_usage": sum(cpu_usage) / len(cpu_usage) if cpu_usage else 0
                }
            }
    
    def start_monitoring(self):
        """Iniciar monitoreo en background"""
        def monitor_loop():
            while True:
                self.record_system_metrics()
                time.sleep(5)  # Registrar cada 5 segundos
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        print("📊 Monitoreo iniciado en background")

# Instancia global del monitor
performance_monitor = PerformanceMonitor()

def test_monitoring():
    """Probar el sistema de monitoreo"""
    print("🧪 PROBANDO SISTEMA DE MONITOREO")
    print("=" * 40)
    
    # Iniciar monitoreo
    performance_monitor.start_monitoring()
    
    # Simular algunos requests
    for i in range(5):
        time.sleep(1)
        performance_monitor.record_request(1.5 + i * 0.2, True)
        print(f"Request {i+1} registrado")
    
    # Obtener estadísticas
    stats = performance_monitor.get_stats()
    print("📊 Estadísticas actuales:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_monitoring()
