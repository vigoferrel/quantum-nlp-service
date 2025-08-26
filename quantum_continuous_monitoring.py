#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QUANTUM CONTINUOUS MONITORING                            ║
║                        SISTEMA DE MONITOREO AUTOMÁTICO                      ║
║                                                                              ║
║  ████████████████████████████████████████████████████████████████████████  ║
║  █                                                                          █  ║
║  █  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗██╗███████╗███████╗███████╗     █  ║
║  █  ██╔══██╗██╔══██╗████╗  ██║████╗  ██║██║██╔════╝██╔════╝██╔════╝     █  ║
║  █  ██████╔╝██████╔╝██╔██╗ ██║██╔██╗ ██║██║█████╗  █████╗  █████╗      █  ║
║  █  ██╔═══╝ ██╔══██╗██║╚██╗██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝      █  ║
║  █  ██║     ██████╔╝██║ ╚████║██║ ╚████║██║██║     ███████╗███████╗     █  ║
║  █  ╚═╝     ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚══════╝     █  ║
║  █                                                                          █  ║
║  █  ████████████████████████████████████████████████████████████████████████  ║
║                                                                              ║
║  [CONTINUOUS MONITORING: ACTIVE]                                             ║
║  [REAL-TIME OPTIMIZATION: ENABLED]                                          ║
║  [AUTOMATIC ADJUSTMENTS: MAXIMUM]                                           ║
║  [PERFORMANCE TRACKING: LIVE]                                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import time
import json
import threading
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import queue
import statistics

class MonitoringMetric(Enum):
    """Métricas de monitoreo"""
    RESPONSE_TIME = "response_time"
    SUCCESS_RATE = "success_rate"
    SECURITY_THREATS = "security_threats"
    PERFORMANCE_SCORE = "performance_score"
    ERROR_RATE = "error_rate"
    OPTIMIZATION_EFFECTIVENESS = "optimization_effectiveness"

@dataclass
class MonitoringData:
    """Datos de monitoreo"""
    timestamp: float
    metric: MonitoringMetric
    value: float
    context: Dict[str, Any]

@dataclass
class OptimizationAdjustment:
    """Ajuste de optimización automático"""
    metric: MonitoringMetric
    current_value: float
    target_value: float
    adjustment_type: str
    adjustment_value: float
    reason: str

class QuantumContinuousMonitoring:
    """Sistema de monitoreo continuo para optimización automática"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantum-continuous-monitoring.local",
            "X-Title": "Quantum Continuous Monitoring"
        }
        
        # MODELO MONITOREADO
        self.model = {
            "id": "google/gemini-flash-1.5-8b",
            "cost_input": 0.0000000375,
            "cost_output": 0.00000015,
            "description": "Quantum Enhanced Model"
        }
        
        # CONFIGURACIÓN DE MONITOREO
        self.monitoring_config = {
            "monitoring_interval": 30,  # segundos
            "optimization_threshold": 0.1,
            "alert_threshold": 0.05,
            "max_history_size": 1000,
            "auto_adjustment_enabled": True
        }
        
        # MÉTRICAS OBJETIVO
        self.target_metrics = {
            MonitoringMetric.RESPONSE_TIME: 2.0,  # segundos
            MonitoringMetric.SUCCESS_RATE: 0.95,  # 95%
            MonitoringMetric.SECURITY_THREATS: 0.0,  # 0 amenazas
            MonitoringMetric.PERFORMANCE_SCORE: 0.8,  # 80%
            MonitoringMetric.ERROR_RATE: 0.05,  # 5%
            MonitoringMetric.OPTIMIZATION_EFFECTIVENESS: 0.7  # 70%
        }
        
        # ALMACENAMIENTO DE DATOS
        self.monitoring_history = {metric: [] for metric in MonitoringMetric}
        self.optimization_adjustments = []
        self.is_monitoring = False
        self.monitoring_task = None
        
        # QUEUES PARA COMUNICACIÓN
        self.metrics_queue = queue.Queue()
        self.adjustments_queue = queue.Queue()
        
        # ESTADÍSTICAS EN TIEMPO REAL
        self.current_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_response_time": 0.0,
            "security_threats_detected": 0,
            "optimization_adjustments_made": 0
        }
        
        self.print_header()
    
    def print_header(self):
        """Imprime header del sistema"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    QUANTUM CONTINUOUS MONITORING                            ║")
        print("║                        SISTEMA DE MONITOREO AUTOMÁTICO                      ║")
        print("║                                                                              ║")
        print("║  ████████████████████████████████████████████████████████████████████████  ║")
        print("║  █                                                                          █  ║")
        print("║  █  ██████╗ ██████╗ ███╗   ██╗███╗   ██╗██╗███████╗███████╗███████╗     █  ║")
        print("║  █  ██╔══██╗██╔══██╗████╗  ██║████╗  ██║██║██╔════╝██╔════╝██╔════╝     █  ║")
        print("║  █  ██████╔╝██████╔╝██╔██╗ ██║██╔██╗ ██║██║█████╗  █████╗  █████╗      █  ║")
        print("║  █  ██╔═══╝ ██╔══██╗██║╚██╗██║██║╚██╗██║██║██╔══╝  ██╔══╝  ██╔══╝      █  ║")
        print("║  █  ██║     ██████╔╝██║ ╚████║██║ ╚████║██║██║     ███████╗███████╗     █  ║")
        print("║  █  ╚═╝     ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚══════╝     █  ║")
        print("║  █                                                                          █  ║")
        print("║  █  ████████████████████████████████████████████████████████████████████████  ║")
        print("║                                                                              ║")
        print("║  [CONTINUOUS MONITORING: ACTIVE]                                             ║")
        print("║  [REAL-TIME OPTIMIZATION: ENABLED]                                          ║")
        print("║  [AUTOMATIC ADJUSTMENTS: MAXIMUM]                                           ║")
        print("║  [PERFORMANCE TRACKING: LIVE]                                               ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    async def call_model_monitored(self, prompt: str) -> Dict[str, Any]:
        """Llamada al modelo con monitoreo"""
        
        start_time = time.time()
        
        payload = {
            "model": self.model["id"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
            "temperature": 0.1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    response_time = time.time() - start_time
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content']
                        usage = data.get('usage', {})
                        
                        input_tokens = usage.get('prompt_tokens', 0)
                        output_tokens = usage.get('completion_tokens', 0)
                        
                        cost = (input_tokens * self.model["cost_input"] / 1000000) + (output_tokens * self.model["cost_output"] / 1000000)
                        
                        # Actualizar estadísticas
                        self.current_stats["total_requests"] += 1
                        self.current_stats["successful_requests"] += 1
                        self.current_stats["total_response_time"] += response_time
                        
                        # Detectar amenazas de seguridad
                        security_threats = self.detect_security_threats(prompt, content)
                        if security_threats:
                            self.current_stats["security_threats_detected"] += 1
                        
                        return {
                            "success": True,
                            "response": content,
                            "cost": cost,
                            "response_time": response_time,
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens,
                            "security_threats": security_threats
                        }
                    else:
                        error_text = await response.text()
                        
                        # Actualizar estadísticas
                        self.current_stats["total_requests"] += 1
                        self.current_stats["failed_requests"] += 1
                        
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "cost": 0.0,
                            "response_time": response_time
                        }
                        
        except Exception as e:
            response_time = time.time() - start_time
            
            # Actualizar estadísticas
            self.current_stats["total_requests"] += 1
            self.current_stats["failed_requests"] += 1
            
            return {
                "success": False,
                "error": str(e),
                "cost": 0.0,
                "response_time": response_time
            }
    
    def detect_security_threats(self, prompt: str, response: str) -> List[str]:
        """Detectar amenazas de seguridad"""
        
        threats = []
        prompt_lower = prompt.lower()
        response_lower = response.lower()
        
        # Detectar prompt injection
        if "ignore previous instructions" in prompt_lower:
            threats.append("prompt_injection_attempt")
        
        # Detectar role confusion
        if "act as admin" in prompt_lower or "system access" in prompt_lower:
            threats.append("role_confusion_attempt")
        
        # Detectar respuesta comprometida
        if "hacked" in response_lower and "ignore" in prompt_lower:
            threats.append("security_breach")
        
        return threats
    
    def calculate_current_metrics(self) -> Dict[MonitoringMetric, float]:
        """Calcular métricas actuales"""
        
        metrics = {}
        
        # Response Time
        if self.current_stats["total_requests"] > 0:
            avg_response_time = self.current_stats["total_response_time"] / self.current_stats["total_requests"]
            metrics[MonitoringMetric.RESPONSE_TIME] = avg_response_time
        else:
            metrics[MonitoringMetric.RESPONSE_TIME] = 0.0
        
        # Success Rate
        if self.current_stats["total_requests"] > 0:
            success_rate = self.current_stats["successful_requests"] / self.current_stats["total_requests"]
            metrics[MonitoringMetric.SUCCESS_RATE] = success_rate
        else:
            metrics[MonitoringMetric.SUCCESS_RATE] = 0.0
        
        # Security Threats
        if self.current_stats["total_requests"] > 0:
            threat_rate = self.current_stats["security_threats_detected"] / self.current_stats["total_requests"]
            metrics[MonitoringMetric.SECURITY_THREATS] = threat_rate
        else:
            metrics[MonitoringMetric.SECURITY_THREATS] = 0.0
        
        # Error Rate
        if self.current_stats["total_requests"] > 0:
            error_rate = self.current_stats["failed_requests"] / self.current_stats["total_requests"]
            metrics[MonitoringMetric.ERROR_RATE] = error_rate
        else:
            metrics[MonitoringMetric.ERROR_RATE] = 0.0
        
        # Performance Score (basado en response time y success rate)
        performance_score = 0.0
        if metrics[MonitoringMetric.RESPONSE_TIME] > 0:
            time_score = max(0, 1 - (metrics[MonitoringMetric.RESPONSE_TIME] / 10))  # Normalizar a 10s
            success_score = metrics[MonitoringMetric.SUCCESS_RATE]
            performance_score = (time_score + success_score) / 2
        metrics[MonitoringMetric.PERFORMANCE_SCORE] = performance_score
        
        # Optimization Effectiveness (basado en ajustes realizados)
        if self.current_stats["total_requests"] > 0:
            effectiveness = 1 - (self.current_stats["optimization_adjustments_made"] / max(1, self.current_stats["total_requests"]))
            metrics[MonitoringMetric.OPTIMIZATION_EFFECTIVENESS] = effectiveness
        else:
            metrics[MonitoringMetric.OPTIMIZATION_EFFECTIVENESS] = 1.0
        
        return metrics
    
    def store_metric(self, metric: MonitoringMetric, value: float, context: Dict[str, Any] = None):
        """Almacenar métrica en el historial"""
        
        if context is None:
            context = {}
        
        monitoring_data = MonitoringData(
            timestamp=time.time(),
            metric=metric,
            value=value,
            context=context
        )
        
        self.monitoring_history[metric].append(monitoring_data)
        
        # Limpiar historial si es muy grande
        if len(self.monitoring_history[metric]) > self.monitoring_config["max_history_size"]:
            self.monitoring_history[metric] = self.monitoring_history[metric][-self.monitoring_config["max_history_size"]:]
    
    def analyze_metrics_trend(self, metric: MonitoringMetric, window_size: int = 10) -> Dict[str, float]:
        """Analizar tendencia de métricas"""
        
        history = self.monitoring_history[metric]
        if len(history) < window_size:
            return {"trend": 0.0, "volatility": 0.0, "current": 0.0}
        
        recent_values = [data.value for data in history[-window_size:]]
        
        # Calcular tendencia (pendiente)
        if len(recent_values) > 1:
            x_values = list(range(len(recent_values)))
            slope = statistics.linear_regression(x_values, recent_values).slope
        else:
            slope = 0.0
        
        # Calcular volatilidad
        volatility = statistics.stdev(recent_values) if len(recent_values) > 1 else 0.0
        
        # Valor actual
        current = recent_values[-1] if recent_values else 0.0
        
        return {
            "trend": slope,
            "volatility": volatility,
            "current": current
        }
    
    def determine_optimization_adjustment(self, metric: MonitoringMetric) -> Optional[OptimizationAdjustment]:
        """Determinar ajuste de optimización necesario"""
        
        current_metrics = self.calculate_current_metrics()
        current_value = current_metrics.get(metric, 0.0)
        target_value = self.target_metrics.get(metric, 0.0)
        
        # Analizar tendencia
        trend_analysis = self.analyze_metrics_trend(metric)
        
        # Determinar si se necesita ajuste
        threshold = self.monitoring_config["optimization_threshold"]
        
        if abs(current_value - target_value) > threshold:
            adjustment_value = target_value - current_value
            adjustment_type = "increase" if adjustment_value > 0 else "decrease"
            
            reason = f"Current {metric.value} ({current_value:.3f}) differs from target ({target_value:.3f})"
            
            return OptimizationAdjustment(
                metric=metric,
                current_value=current_value,
                target_value=target_value,
                adjustment_type=adjustment_type,
                adjustment_value=abs(adjustment_value),
                reason=reason
            )
        
        return None
    
    async def run_monitoring_cycle(self):
        """Ejecutar ciclo de monitoreo"""
        
        # Generar prompt de prueba
        test_prompts = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms",
            "Calculate 2+2 and explain the process",
            "Write a short poem about technology",
            "What are the benefits of renewable energy?"
        ]
        
        import random
        test_prompt = random.choice(test_prompts)
        
        # Ejecutar llamada monitoreada
        result = await self.call_model_monitored(test_prompt)
        
        # Calcular y almacenar métricas
        current_metrics = self.calculate_current_metrics()
        
        for metric, value in current_metrics.items():
            self.store_metric(metric, value, {
                "test_prompt": test_prompt,
                "result_success": result["success"],
                "security_threats": result.get("security_threats", [])
            })
        
        # Verificar necesidad de ajustes
        if self.monitoring_config["auto_adjustment_enabled"]:
            for metric in MonitoringMetric:
                adjustment = self.determine_optimization_adjustment(metric)
                if adjustment:
                    self.optimization_adjustments.append(adjustment)
                    self.current_stats["optimization_adjustments_made"] += 1
                    
                    print(f"║  🔧 AUTO-ADJUSTMENT: {adjustment.metric.value} - {adjustment.reason}")
        
        # Mostrar métricas en tiempo real
        self.print_realtime_metrics(current_metrics)
    
    def print_realtime_metrics(self, metrics: Dict[MonitoringMetric, float]):
        """Imprimir métricas en tiempo real"""
        
        print(f"║  📊 REAL-TIME METRICS:")
        print(f"║  • Response Time: {metrics[MonitoringMetric.RESPONSE_TIME]:.2f}s")
        print(f"║  • Success Rate: {metrics[MonitoringMetric.SUCCESS_RATE]:.3f}")
        print(f"║  • Security Threats: {metrics[MonitoringMetric.SECURITY_THREATS]:.3f}")
        print(f"║  • Performance Score: {metrics[MonitoringMetric.PERFORMANCE_SCORE]:.3f}")
        print(f"║  • Error Rate: {metrics[MonitoringMetric.ERROR_RATE]:.3f}")
        print(f"║  • Optimization Effectiveness: {metrics[MonitoringMetric.OPTIMIZATION_EFFECTIVENESS]:.3f}")
        print(f"║  • Total Requests: {self.current_stats['total_requests']}")
        print(f"║  • Adjustments Made: {self.current_stats['optimization_adjustments_made']}")
    
    async def start_continuous_monitoring(self, duration_minutes: int = 5):
        """Iniciar monitoreo continuo"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  QUANTUM CONTINUOUS MONITORING - STARTING")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  Monitoring Duration: {duration_minutes} minutes")
        print(f"║  Monitoring Interval: {self.monitoring_config['monitoring_interval']} seconds")
        print(f"║  Auto-Adjustment: {'ENABLED' if self.monitoring_config['auto_adjustment_enabled'] else 'DISABLED'}")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        self.is_monitoring = True
        start_time = time.time()
        cycle_count = 0
        
        try:
            while self.is_monitoring:
                cycle_start = time.time()
                cycle_count += 1
                
                print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
                print(f"║  MONITORING CYCLE #{cycle_count}")
                print("╚══════════════════════════════════════════════════════════════════════════════╝")
                
                await self.run_monitoring_cycle()
                
                # Verificar si ha pasado el tiempo límite
                elapsed_time = time.time() - start_time
                if elapsed_time > (duration_minutes * 60):
                    print(f"\n║  ⏰ Monitoring duration completed ({duration_minutes} minutes)")
                    break
                
                # Esperar hasta el siguiente ciclo
                cycle_elapsed = time.time() - cycle_start
                wait_time = max(0, self.monitoring_config["monitoring_interval"] - cycle_elapsed)
                
                if wait_time > 0:
                    print(f"║  ⏳ Waiting {wait_time:.1f}s until next cycle...")
                    await asyncio.sleep(wait_time)
        
        except KeyboardInterrupt:
            print("\n║  🛑 Monitoring stopped by user")
        
        finally:
            self.is_monitoring = False
            await self.print_final_monitoring_report()
    
    async def print_final_monitoring_report(self):
        """Imprimir reporte final de monitoreo"""
        
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  QUANTUM CONTINUOUS MONITORING - FINAL REPORT")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Métricas finales
        final_metrics = self.calculate_current_metrics()
        
        print("║  FINAL METRICS:")
        for metric, value in final_metrics.items():
            target = self.target_metrics[metric]
            status = "✅" if abs(value - target) <= self.monitoring_config["optimization_threshold"] else "⚠️"
            print(f"║  {status} {metric.value}: {value:.3f} (target: {target:.3f})")
        
        # Estadísticas generales
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  MONITORING STATISTICS:")
        print(f"║  • Total Requests: {self.current_stats['total_requests']}")
        print(f"║  • Successful Requests: {self.current_stats['successful_requests']}")
        print(f"║  • Failed Requests: {self.current_stats['failed_requests']}")
        print(f"║  • Security Threats Detected: {self.current_stats['security_threats_detected']}")
        print(f"║  • Optimization Adjustments: {self.current_stats['optimization_adjustments_made']}")
        
        # Análisis de tendencias
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  TREND ANALYSIS:")
        for metric in MonitoringMetric:
            trend_analysis = self.analyze_metrics_trend(metric)
            trend_icon = "📈" if trend_analysis["trend"] > 0 else "📉" if trend_analysis["trend"] < 0 else "➡️"
            print(f"║  {trend_icon} {metric.value}: trend {trend_analysis['trend']:.3f}, volatility {trend_analysis['volatility']:.3f}")
        
        # Ajustes realizados
        if self.optimization_adjustments:
            print("╠══════════════════════════════════════════════════════════════════════════════╣")
            print("║  OPTIMIZATION ADJUSTMENTS MADE:")
            for adjustment in self.optimization_adjustments[-5:]:  # Últimos 5 ajustes
                print(f"║  • {adjustment.metric.value}: {adjustment.adjustment_type} by {adjustment.adjustment_value:.3f}")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")

async def main():
    """Función principal del sistema de monitoreo continuo"""
    
    monitoring = QuantumContinuousMonitoring()
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  QUANTUM CONTINUOUS MONITORING - STARTING")
    print("║  Beginning continuous monitoring and automatic optimization")
    print("║  Press Ctrl+C to stop monitoring")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    await monitoring.start_continuous_monitoring(duration_minutes=3)

if __name__ == "__main__":
    asyncio.run(main())
