#!/usr/bin/env python3
"""
📊 MONITOR DE CONEXIONES VIGOLEONROCKS
Sistema de monitoreo en tiempo real de conexiones al modelo
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging
from collections import defaultdict, deque
import psutil
import requests

logger = logging.getLogger(__name__)

@dataclass
class ConnectionEvent:
    """Evento de conexión"""
    timestamp: datetime
    api_key: str
    user_name: str
    query_type: str
    query_length: int
    response_time: float
    success: bool
    error_message: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

@dataclass
class UserStats:
    """Estadísticas por usuario"""
    user_name: str
    api_key: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_response_time: float
    avg_response_time: float
    last_request: Optional[datetime]
    requests_per_hour: int
    requests_per_day: int

class ConnectionMonitor:
    """Monitor de conexiones en tiempo real"""
    
    def __init__(self, max_events: int = 10000):
        self.max_events = max_events
        self.connection_events = deque(maxlen=max_events)
        self.user_stats = {}
        self.system_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "peak_concurrent_users": 0,
            "current_concurrent_users": 0,
            "start_time": datetime.now(),
            "uptime": "0:00:00"
        }
        self.hourly_stats = defaultdict(lambda: {"requests": 0, "errors": 0})
        self.daily_stats = defaultdict(lambda: {"requests": 0, "errors": 0})
        self.active_connections = set()
        self.lock = threading.Lock()
        
        # Iniciar monitoreo de sistema
        self.start_system_monitoring()
    
    def record_connection(self, event: ConnectionEvent):
        """Registrar evento de conexión"""
        with self.lock:
            # Agregar evento
            self.connection_events.append(event)
            
            # Actualizar estadísticas del usuario
            self._update_user_stats(event)
            
            # Actualizar estadísticas del sistema
            self._update_system_stats(event)
            
            # Actualizar estadísticas por hora/día
            self._update_time_stats(event)
            
            # Actualizar conexiones activas
            if event.success:
                self.active_connections.add(event.api_key)
            else:
                self.active_connections.discard(event.api_key)
    
    def _update_user_stats(self, event: ConnectionEvent):
        """Actualizar estadísticas del usuario"""
        if event.api_key not in self.user_stats:
            self.user_stats[event.api_key] = UserStats(
                user_name=event.user_name,
                api_key=event.api_key,
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                total_response_time=0.0,
                avg_response_time=0.0,
                last_request=None,
                requests_per_hour=0,
                requests_per_day=0
            )
        
        stats = self.user_stats[event.api_key]
        stats.total_requests += 1
        stats.total_response_time += event.response_time
        stats.avg_response_time = stats.total_response_time / stats.total_requests
        stats.last_request = event.timestamp
        
        if event.success:
            stats.successful_requests += 1
        else:
            stats.failed_requests += 1
    
    def _update_system_stats(self, event: ConnectionEvent):
        """Actualizar estadísticas del sistema"""
        self.system_stats["total_requests"] += 1
        
        if event.success:
            self.system_stats["successful_requests"] += 1
        else:
            self.system_stats["failed_requests"] += 1
        
        # Calcular tiempo promedio de respuesta
        total_time = self.system_stats["total_requests"] * self.system_stats["avg_response_time"]
        total_time += event.response_time
        self.system_stats["avg_response_time"] = total_time / self.system_stats["total_requests"]
        
        # Actualizar usuarios concurrentes
        self.system_stats["current_concurrent_users"] = len(self.active_connections)
        if len(self.active_connections) > self.system_stats["peak_concurrent_users"]:
            self.system_stats["peak_concurrent_users"] = len(self.active_connections)
        
        # Actualizar uptime
        uptime = datetime.now() - self.system_stats["start_time"]
        self.system_stats["uptime"] = str(uptime).split('.')[0]
    
    def _update_time_stats(self, event: ConnectionEvent):
        """Actualizar estadísticas por tiempo"""
        hour_key = event.timestamp.strftime("%Y-%m-%d %H:00")
        day_key = event.timestamp.strftime("%Y-%m-%d")
        
        self.hourly_stats[hour_key]["requests"] += 1
        self.daily_stats[day_key]["requests"] += 1
        
        if not event.success:
            self.hourly_stats[hour_key]["errors"] += 1
            self.daily_stats[day_key]["errors"] += 1
    
    def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Obtener eventos recientes"""
        with self.lock:
            events = list(self.connection_events)[-limit:]
            return [asdict(event) for event in events]
    
    def get_user_stats(self, api_key: Optional[str] = None) -> Dict:
        """Obtener estadísticas de usuarios"""
        with self.lock:
            if api_key:
                return asdict(self.user_stats.get(api_key, {}))
            else:
                return {key: asdict(stats) for key, stats in self.user_stats.items()}
    
    def get_system_stats(self) -> Dict:
        """Obtener estadísticas del sistema"""
        with self.lock:
            stats = self.system_stats.copy()
            
            # Agregar métricas adicionales
            stats["success_rate"] = (
                stats["successful_requests"] / stats["total_requests"] * 100 
                if stats["total_requests"] > 0 else 0
            )
            stats["error_rate"] = (
                stats["failed_requests"] / stats["total_requests"] * 100 
                if stats["total_requests"] > 0 else 0
            )
            
            # Agregar estadísticas de rendimiento
            stats["requests_per_minute"] = self._calculate_rpm()
            stats["requests_per_hour"] = self._calculate_rph()
            
            return stats
    
    def get_performance_metrics(self) -> Dict:
        """Obtener métricas de rendimiento"""
        with self.lock:
            recent_events = list(self.connection_events)[-100:]  # Últimos 100 eventos
            
            if not recent_events:
                return {
                    "avg_response_time": 0.0,
                    "min_response_time": 0.0,
                    "max_response_time": 0.0,
                    "response_time_percentiles": {}
                }
            
            response_times = [event.response_time for event in recent_events if event.success]
            
            if not response_times:
                return {
                    "avg_response_time": 0.0,
                    "min_response_time": 0.0,
                    "max_response_time": 0.0,
                    "response_time_percentiles": {}
                }
            
            response_times.sort()
            
            return {
                "avg_response_time": sum(response_times) / len(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "response_time_percentiles": {
                    "50th": response_times[int(len(response_times) * 0.5)],
                    "90th": response_times[int(len(response_times) * 0.9)],
                    "95th": response_times[int(len(response_times) * 0.95)],
                    "99th": response_times[int(len(response_times) * 0.99)]
                }
            }
    
    def _calculate_rpm(self) -> float:
        """Calcular requests por minuto"""
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        recent_requests = sum(
            1 for event in self.connection_events 
            if event.timestamp >= one_minute_ago
        )
        
        return recent_requests
    
    def _calculate_rph(self) -> float:
        """Calcular requests por hora"""
        now = datetime.now()
        one_hour_ago = now - timedelta(hours=1)
        
        recent_requests = sum(
            1 for event in self.connection_events 
            if event.timestamp >= one_hour_ago
        )
        
        return recent_requests
    
    def get_alerts(self) -> List[Dict]:
        """Obtener alertas del sistema"""
        alerts = []
        
        with self.lock:
            # Alerta por alta tasa de errores
            if self.system_stats["total_requests"] > 0:
                error_rate = self.system_stats["failed_requests"] / self.system_stats["total_requests"]
                if error_rate > 0.1:  # Más del 10% de errores
                    alerts.append({
                        "type": "HIGH_ERROR_RATE",
                        "message": f"Alta tasa de errores: {error_rate:.2%}",
                        "severity": "WARNING",
                        "timestamp": datetime.now()
                    })
            
            # Alerta por tiempo de respuesta alto
            if self.system_stats["avg_response_time"] > 10.0:  # Más de 10 segundos
                alerts.append({
                    "type": "HIGH_RESPONSE_TIME",
                    "message": f"Tiempo de respuesta alto: {self.system_stats['avg_response_time']:.2f}s",
                    "severity": "WARNING",
                    "timestamp": datetime.now()
                })
            
            # Alerta por muchos usuarios concurrentes
            if self.system_stats["current_concurrent_users"] > 50:
                alerts.append({
                    "type": "HIGH_CONCURRENT_USERS",
                    "message": f"Muchos usuarios concurrentes: {self.system_stats['current_concurrent_users']}",
                    "severity": "INFO",
                    "timestamp": datetime.now()
                })
        
        return alerts
    
    def start_system_monitoring(self):
        """Iniciar monitoreo del sistema"""
        def monitor_system():
            while True:
                try:
                    # Monitorear uso de CPU y memoria
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    
                    # Agregar métricas del sistema
                    with self.lock:
                        self.system_stats["cpu_usage"] = cpu_percent
                        self.system_stats["memory_usage"] = memory.percent
                        self.system_stats["memory_available"] = memory.available
                    
                    time.sleep(30)  # Actualizar cada 30 segundos
                    
                except Exception as e:
                    logger.error(f"Error en monitoreo del sistema: {e}")
                    time.sleep(60)
        
        # Iniciar thread de monitoreo
        monitor_thread = threading.Thread(target=monitor_system, daemon=True)
        monitor_thread.start()
    
    def export_stats(self, filename: str = "vigoleonrocks_stats.json"):
        """Exportar estadísticas a archivo"""
        with self.lock:
            export_data = {
                "timestamp": datetime.now().isoformat(),
                "system_stats": self.system_stats,
                "user_stats": {key: asdict(stats) for key, stats in self.user_stats.items()},
                "recent_events": self.get_recent_events(100),
                "performance_metrics": self.get_performance_metrics(),
                "alerts": self.get_alerts()
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Estadísticas exportadas a {filename}")

# Instancia global del monitor
connection_monitor = ConnectionMonitor()

def record_api_request(api_key: str, user_name: str, query_type: str, 
                      query_length: int, response_time: float, success: bool,
                      error_message: Optional[str] = None, ip_address: Optional[str] = None,
                      user_agent: Optional[str] = None):
    """Función helper para registrar requests API"""
    event = ConnectionEvent(
        timestamp=datetime.now(),
        api_key=api_key,
        user_name=user_name,
        query_type=query_type,
        query_length=query_length,
        response_time=response_time,
        success=success,
        error_message=error_message,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    connection_monitor.record_connection(event)

if __name__ == "__main__":
    # Demo del monitor
    print("📊 MONITOR DE CONEXIONES VIGOLEONROCKS")
    print("=" * 50)
    
    # Simular algunas conexiones
    record_api_request(
        api_key="vk_live_test_key_123",
        user_name="kjacome24",
        query_type="text",
        query_length=50,
        response_time=2.5,
        success=True
    )
    
    record_api_request(
        api_key="vk_live_dev_key_456",
        user_name="Desarrollador",
        query_type="quantum",
        query_length=100,
        response_time=3.2,
        success=True
    )
    
    # Mostrar estadísticas
    print("📈 Estadísticas del Sistema:")
    stats = connection_monitor.get_system_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n👥 Estadísticas de Usuarios:")
    user_stats = connection_monitor.get_user_stats()
    for api_key, stats in user_stats.items():
        print(f"  {stats['user_name']}: {stats['total_requests']} requests")
    
    print("\n⚡ Métricas de Rendimiento:")
    perf_metrics = connection_monitor.get_performance_metrics()
    for key, value in perf_metrics.items():
        print(f"  {key}: {value}")
    
    print("\n🚨 Alertas:")
    alerts = connection_monitor.get_alerts()
    for alert in alerts:
        print(f"  {alert['severity']}: {alert['message']}")
    
    # Exportar estadísticas
    connection_monitor.export_stats()
    print(f"\n✅ Estadísticas exportadas a vigoleonrocks_stats.json")
