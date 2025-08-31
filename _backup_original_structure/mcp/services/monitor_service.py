#!/usr/bin/env python3
"""
📊 SERVICIO DE MONITOREO MCP
Monitoreo y métricas del sistema
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import psutil
import threading

class MonitorMCPService:
    """Servicio de monitoreo MCP"""
    
    def __init__(self):
        self.name = "monitor"
        self.version = "1.0.0"
        self.is_initialized = False
        self.metrics = {}
        self.alerts = []
        self.monitoring_task = None
        self.is_monitoring = False
        
    async def initialize(self):
        """Inicializar el servicio"""
        self.is_initialized = True
        await self.start_monitoring()
        return True
    
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Obtener herramientas disponibles"""
        return [
            {
                "name": "get_system_metrics",
                "description": "Obtener métricas del sistema",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "include_processes": {
                            "type": "boolean",
                            "description": "Incluir información de procesos",
                            "default": False
                        }
                    }
                }
            },
            {
                "name": "get_performance_metrics",
                "description": "Obtener métricas de rendimiento",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "timeframe": {
                            "type": "string",
                            "description": "Ventana de tiempo",
                            "enum": ["1m", "5m", "15m", "1h"],
                            "default": "5m"
                        }
                    }
                }
            },
            {
                "name": "get_alerts",
                "description": "Obtener alertas activas",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "severity": {
                            "type": "string",
                            "description": "Filtrar por severidad",
                            "enum": ["info", "warning", "error", "critical"],
                            "default": "all"
                        }
                    }
                }
            },
            {
                "name": "set_alert_threshold",
                "description": "Establecer umbral de alerta",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "metric": {
                            "type": "string",
                            "description": "Métrica a monitorear",
                            "required": True
                        },
                        "threshold": {
                            "type": "number",
                            "description": "Umbral de alerta",
                            "required": True
                        },
                        "severity": {
                            "type": "string",
                            "description": "Severidad de la alerta",
                            "enum": ["warning", "error", "critical"],
                            "default": "warning"
                        }
                    },
                    "required": ["metric", "threshold"]
                }
            }
        ]
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Ejecutar una herramienta"""
        if not self.is_initialized:
            return {"error": "Servicio no inicializado"}
        
        try:
            if tool_name == "get_system_metrics":
                return await self._get_system_metrics(arguments)
            elif tool_name == "get_performance_metrics":
                return await self._get_performance_metrics(arguments)
            elif tool_name == "get_alerts":
                return await self._get_alerts(arguments)
            elif tool_name == "set_alert_threshold":
                return await self._set_alert_threshold(arguments)
            else:
                return {"error": f"Herramienta no encontrada: {tool_name}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_system_metrics(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener métricas del sistema"""
        include_processes = arguments.get("include_processes", False)
        
        # Métricas del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "usage_percent": cpu_percent,
                "count": psutil.cpu_count(),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100
            },
            "network": {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
        }
        
        if include_processes:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Ordenar por uso de CPU
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            metrics["processes"] = processes[:10]  # Top 10
        
        return {"content": metrics}
    
    async def _get_performance_metrics(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener métricas de rendimiento"""
        timeframe = arguments.get("timeframe", "5m")
        
        # Simulación de métricas históricas
        now = datetime.now()
        
        if timeframe == "1m":
            start_time = now - timedelta(minutes=1)
            interval = timedelta(seconds=10)
        elif timeframe == "5m":
            start_time = now - timedelta(minutes=5)
            interval = timedelta(minutes=1)
        elif timeframe == "15m":
            start_time = now - timedelta(minutes=15)
            interval = timedelta(minutes=3)
        else:  # 1h
            start_time = now - timedelta(hours=1)
            interval = timedelta(minutes=10)
        
        metrics = []
        current_time = start_time
        
        while current_time <= now:
            metrics.append({
                "timestamp": current_time.isoformat(),
                "cpu_percent": 30 + (current_time.second % 30),  # Simulación
                "memory_percent": 60 + (current_time.second % 20),
                "disk_io": 1000 + (current_time.second % 500),
                "network_io": 500 + (current_time.second % 300)
            })
            current_time += interval
        
        return {
            "content": {
                "timeframe": timeframe,
                "metrics": metrics,
                "summary": {
                    "avg_cpu": sum(m["cpu_percent"] for m in metrics) / len(metrics),
                    "avg_memory": sum(m["memory_percent"] for m in metrics) / len(metrics),
                    "peak_cpu": max(m["cpu_percent"] for m in metrics),
                    "peak_memory": max(m["memory_percent"] for m in metrics)
                }
            }
        }
    
    async def _get_alerts(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Obtener alertas activas"""
        severity_filter = arguments.get("severity", "all")
        
        if severity_filter == "all":
            filtered_alerts = self.alerts
        else:
            filtered_alerts = [alert for alert in self.alerts if alert["severity"] == severity_filter]
        
        return {
            "content": {
                "alerts": filtered_alerts,
                "total_alerts": len(filtered_alerts),
                "severity_counts": {
                    "info": len([a for a in self.alerts if a["severity"] == "info"]),
                    "warning": len([a for a in self.alerts if a["severity"] == "warning"]),
                    "error": len([a for a in self.alerts if a["severity"] == "error"]),
                    "critical": len([a for a in self.alerts if a["severity"] == "critical"])
                }
            }
        }
    
    async def _set_alert_threshold(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Establecer umbral de alerta"""
        metric = arguments.get("metric")
        threshold = arguments.get("threshold")
        severity = arguments.get("severity", "warning")
        
        # Aquí se configuraría el umbral
        # Por ahora es una simulación
        
        return {
            "content": {
                "message": f"Umbral configurado para {metric}",
                "metric": metric,
                "threshold": threshold,
                "severity": severity,
                "status": "configured"
            }
        }
    
    async def get_resources(self) -> List[Dict[str, Any]]:
        """Obtener recursos disponibles"""
        return [
            {
                "uri": "monitor://dashboard",
                "name": "Monitor Dashboard",
                "description": "Dashboard de monitoreo en tiempo real",
                "mimeType": "application/json"
            },
            {
                "uri": "monitor://alerts",
                "name": "Alertas",
                "description": "Configuración de alertas",
                "mimeType": "application/json"
            }
        ]
    
    async def read_resource(self, uri: str) -> Optional[Dict[str, Any]]:
        """Leer un recurso"""
        if uri == "monitor://dashboard":
            return {
                "content": await self._get_system_metrics({}),
                "mimeType": "application/json"
            }
        elif uri == "monitor://alerts":
            return {
                "content": {
                    "alerts": self.alerts,
                    "thresholds": {},  # Configuración de umbrales
                    "settings": {
                        "monitoring_enabled": self.is_monitoring,
                        "alert_channels": ["console", "email"]
                    }
                },
                "mimeType": "application/json"
            }
        
        return None
    
    async def start_monitoring(self):
        """Iniciar monitoreo en background"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Detener monitoreo"""
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
    
    async def _monitoring_loop(self):
        """Loop de monitoreo"""
        while self.is_monitoring:
            try:
                # Obtener métricas actuales
                metrics = await self._get_system_metrics({})
                
                # Verificar umbrales y generar alertas
                await self._check_thresholds(metrics["content"])
                
                # Guardar métricas
                self.metrics[datetime.now().isoformat()] = metrics["content"]
                
                # Limpiar métricas antiguas (mantener solo 1 hora)
                cutoff = datetime.now() - timedelta(hours=1)
                self.metrics = {
                    k: v for k, v in self.metrics.items() 
                    if datetime.fromisoformat(k) > cutoff
                }
                
                await asyncio.sleep(30)  # Monitorear cada 30 segundos
                
            except Exception as e:
                print(f"Error en monitoreo: {e}")
                await asyncio.sleep(60)
    
    async def _check_thresholds(self, metrics: Dict[str, Any]):
        """Verificar umbrales y generar alertas"""
        # Ejemplo de verificación de umbrales
        cpu_percent = metrics["cpu"]["usage_percent"]
        memory_percent = metrics["memory"]["percent"]
        
        if cpu_percent > 80:
            self._add_alert("CPU usage high", "warning", {"cpu_percent": cpu_percent})
        elif cpu_percent > 95:
            self._add_alert("CPU usage critical", "critical", {"cpu_percent": cpu_percent})
        
        if memory_percent > 85:
            self._add_alert("Memory usage high", "warning", {"memory_percent": memory_percent})
        elif memory_percent > 95:
            self._add_alert("Memory usage critical", "critical", {"memory_percent": memory_percent})
    
    def _add_alert(self, message: str, severity: str, context: Dict[str, Any]):
        """Agregar alerta"""
        alert = {
            "id": f"alert_{len(self.alerts)}",
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "severity": severity,
            "context": context
        }
        
        self.alerts.append(alert)
        
        # Mantener solo las últimas 100 alertas
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    async def health_check(self) -> bool:
        """Health check del servicio"""
        return self.is_initialized and self.is_monitoring
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del servicio"""
        return {
            "is_monitoring": self.is_monitoring,
            "metrics_count": len(self.metrics),
            "alerts_count": len(self.alerts),
            "last_metric_time": max(self.metrics.keys()) if self.metrics else None
        }

# Instancia global del servicio
monitor_service = MonitorMCPService()
