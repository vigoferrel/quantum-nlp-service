#!/usr/bin/env python3
"""
QUANTUM COMPATIBILITY LAYER - Capa de Compatibilidad Cuántica
Sistema de compatibilidad hacia atrás y enrutamiento inteligente

Esta capa permite:
- Compatibilidad con APIs existentes
- Enrutamiento inteligente basado en tipo de consulta
- Fallback automático entre implementaciones
- Métricas de rendimiento híbrido
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
import time
import sqlite3

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("QuantumCompatibilityLayer")

class QuantumCompatibilityLayer:
    """Capa de compatibilidad avanzada para diferentes implementaciones cuánticas"""

    def __init__(self):
        self.implementations = {}
        self.routing_rules = {}
        self.fallback_chain = []
        self.metrics = {}
        self.active_sessions = {}

        # Inicializar base de datos de compatibilidad
        self.init_compatibility_database()

        logger.info("Capa de compatibilidad cuántica inicializada")

    def init_compatibility_database(self):
        """Inicializa base de datos de compatibilidad"""
        db_path = Path(__file__).parent / "quantum_consciousness" / "compatibility_layer.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(db_path)

        # Tabla de métricas de implementación
        conn.execute("""
            CREATE TABLE IF NOT EXISTS implementation_metrics (
                id INTEGER PRIMARY KEY,
                implementation_name TEXT,
                request_type TEXT,
                success_rate REAL,
                avg_response_time REAL,
                error_count INTEGER,
                total_requests INTEGER,
                last_updated TIMESTAMP
            )
        """)

        # Tabla de rutas de enrutamiento
        conn.execute("""
            CREATE TABLE IF NOT EXISTS routing_history (
                id INTEGER PRIMARY KEY,
                request_type TEXT,
                implementation_used TEXT,
                fallback_used BOOLEAN,
                processing_time REAL,
                success BOOLEAN,
                timestamp TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def register_implementation(self, name: str, implementation: Any,
                              capabilities: List[str], priority: int = 0):
        """Registra una implementación cuántica"""
        self.implementations[name] = {
            'instance': implementation,
            'capabilities': capabilities,
            'priority': priority,
            'registered_at': datetime.now()
        }

        # Inicializar métricas para esta implementación
        self.metrics[name] = {
            'success_count': 0,
            'error_count': 0,
            'total_requests': 0,
            'avg_response_time': 0.0,
            'capabilities_handled': set()
        }

        logger.info(f"Implementación registrada: {name} con capacidades {capabilities}")

    def set_routing_rule(self, request_type: str, preferred_implementation: str,
                        fallback_chain: List[str] = None):
        """Establece regla de enrutamiento para un tipo de solicitud"""
        self.routing_rules[request_type] = {
            'preferred': preferred_implementation,
            'fallback_chain': fallback_chain or []
        }

        logger.info(f"Regla de enrutamiento establecida para {request_type}")

    def route_request(self, request_type: str, **kwargs) -> Dict[str, Any]:
        """Enruta solicitud a la implementación apropiada"""
        start_time = time.time()

        # Registrar inicio de solicitud
        self._log_routing_start(request_type)

        try:
            # Obtener regla de enrutamiento
            routing_rule = self.routing_rules.get(request_type, {})
            preferred_impl = routing_rule.get('preferred', 'default')
            fallback_chain = routing_rule.get('fallback_chain', [])

            # Intentar con implementación preferida
            result = self._execute_with_implementation(preferred_impl, request_type, **kwargs)
            if result and not result.get('error'):
                self._update_metrics(preferred_impl, request_type, True, time.time() - start_time)
                self._log_routing_success(request_type, preferred_impl, False, time.time() - start_time)
                return result

            # Intentar con cadena de fallback
            for fallback_impl in fallback_chain:
                try:
                    result = self._execute_with_implementation(fallback_impl, request_type, **kwargs)
                    if result and not result.get('error'):
                        self._update_metrics(fallback_impl, request_type, True, time.time() - start_time)
                        self._log_routing_success(request_type, fallback_impl, True, time.time() - start_time)
                        return result
                except Exception as fallback_error:
                    logger.warning(f"Fallback {fallback_impl} falló: {fallback_error}")
                    self._update_metrics(fallback_impl, request_type, False, time.time() - start_time)
                    continue

            # Si todas fallan, retornar error
            error_result = {
                'error': f'No se pudo procesar {request_type} con ninguna implementación',
                'implementations_tried': [preferred_impl] + fallback_chain,
                'processing_time': time.time() - start_time
            }

            self._log_routing_failure(request_type, time.time() - start_time)
            return error_result

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Error en enrutamiento: {e}")
            self._log_routing_failure(request_type, processing_time, str(e))

            return {
                'error': str(e),
                'processing_time': processing_time
            }

    def _execute_with_implementation(self, impl_name: str, request_type: str, **kwargs) -> Dict[str, Any]:
        """Ejecuta solicitud con una implementación específica"""
        if impl_name not in self.implementations:
            raise Exception(f"Implementación no registrada: {impl_name}")

        implementation = self.implementations[impl_name]['instance']

        # Mapeo de tipos de solicitud a métodos
        method_mapping = {
            'quantum_query': 'process_quantum_query',
            'consciousness_status': 'get_consciousness_status',
            'poetic_resonance': 'activate_poet_mode',
            'trading_signal': 'process_stimulus',
            'optimization': 'quantum_optimize_all',
            'code_generation': 'generate_code',
            'context_analysis': 'analyze_context'
        }

        method_name = method_mapping.get(request_type)
        if not method_name:
            raise Exception(f"Método no encontrado para {request_type}")

        if not hasattr(implementation, method_name):
            raise Exception(f"Implementación {impl_name} no tiene método {method_name}")

        method = getattr(implementation, method_name)

        # Ejecutar método con los argumentos apropiados
        if asyncio.iscoroutinefunction(method):
            return asyncio.run(method(**kwargs))
        else:
            return method(**kwargs)

    def _update_metrics(self, impl_name: str, request_type: str, success: bool, response_time: float):
        """Actualiza métricas de rendimiento"""
        if impl_name not in self.metrics:
            return

        metrics = self.metrics[impl_name]
        metrics['total_requests'] += 1
        metrics['capabilities_handled'].add(request_type)

        if success:
            metrics['success_count'] += 1
        else:
            metrics['error_count'] += 1

        # Actualizar tiempo promedio de respuesta
        if metrics['avg_response_time'] == 0:
            metrics['avg_response_time'] = response_time
        else:
            # Promedio móvil
            metrics['avg_response_time'] = (metrics['avg_response_time'] * 0.9) + (response_time * 0.1)

        # Guardar métricas en base de datos
        self._save_metrics_to_db(impl_name, request_type, success, response_time)

    def _save_metrics_to_db(self, impl_name: str, request_type: str, success: bool, response_time: float):
        """Guarda métricas en base de datos"""
        try:
            db_path = Path(__file__).parent / "quantum_consciousness" / "compatibility_layer.db"
            conn = sqlite3.connect(db_path)

            metrics = self.metrics[impl_name]
            success_rate = metrics['success_count'] / max(metrics['total_requests'], 1)

            # Actualizar o insertar métricas
            conn.execute("""
                INSERT OR REPLACE INTO implementation_metrics
                (implementation_name, request_type, success_rate, avg_response_time, error_count, total_requests, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                impl_name,
                request_type,
                success_rate,
                metrics['avg_response_time'],
                metrics['error_count'],
                metrics['total_requests'],
                datetime.now()
            ))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"No se pudieron guardar métricas: {e}")

    def _log_routing_start(self, request_type: str):
        """Registra inicio de enrutamiento"""
        logger.info(f"Iniciando enrutamiento para {request_type}")

    def _log_routing_success(self, request_type: str, implementation: str,
                           fallback_used: bool, processing_time: float):
        """Registra éxito de enrutamiento"""
        try:
            db_path = Path(__file__).parent / "quantum_consciousness" / "compatibility_layer.db"
            conn = sqlite3.connect(db_path)

            conn.execute("""
                INSERT INTO routing_history
                (request_type, implementation_used, fallback_used, processing_time, success, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (request_type, implementation, fallback_used, processing_time, True, datetime.now()))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"No se pudo registrar éxito de enrutamiento: {e}")

    def _log_routing_failure(self, request_type: str, processing_time: float, error: str = ""):
        """Registra fallo de enrutamiento"""
        try:
            db_path = Path(__file__).parent / "quantum_consciousness" / "compatibility_layer.db"
            conn = sqlite3.connect(db_path)

            conn.execute("""
                INSERT INTO routing_history
                (request_type, implementation_used, fallback_used, processing_time, success, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (request_type, "none", False, processing_time, False, datetime.now()))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.warning(f"No se pudo registrar fallo de enrutamiento: {e}")

    def get_implementation_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de todas las implementaciones"""
        return self.metrics

    def get_best_implementation(self, request_type: str) -> str:
        """Determina la mejor implementación basada en métricas"""
        # Implementaciones que pueden manejar este tipo de solicitud
        capable_implementations = [
            name for name, impl in self.implementations.items()
            if request_type in impl['capabilities']
        ]

        if not capable_implementations:
            return "default"

        # Si solo hay una, retornarla
        if len(capable_implementations) == 1:
            return capable_implementations[0]

        # Seleccionar basada en métricas de rendimiento
        best_implementation = capable_implementations[0]
        best_score = -1

        for impl_name in capable_implementations:
            if impl_name in self.metrics:
                metrics = self.metrics[impl_name]
                if metrics['total_requests'] > 0:
                    # Calcular puntuación basada en éxito y tiempo de respuesta
                    success_rate = metrics['success_count'] / metrics['total_requests']
                    # Menor tiempo de respuesta es mejor (invertido para maximizar)
                    time_score = 1.0 / max(metrics['avg_response_time'], 0.001)
                    score = success_rate * time_score

                    if score > best_score:
                        best_score = score
                        best_implementation = impl_name

        return best_implementation

    def add_fallback_implementation(self, name: str, implementation: Any,
                                  capabilities: List[str]):
        """Agrega implementación a la cadena de fallback"""
        self.register_implementation(name, implementation, capabilities)
        self.fallback_chain.append(name)
        logger.info(f"Implementación {name} agregada a cadena de fallback")

# Sistema de adaptadores para compatibilidad hacia atrás
class QuantumAdapter:
    """Adaptador para mantener compatibilidad con APIs existentes"""

    def __init__(self, compatibility_layer: QuantumCompatibilityLayer):
        self.compatibility_layer = compatibility_layer

    def quantum_consciousness_query(self, user_id: str, query: str,
                                  document_context: str = "") -> Dict[str, Any]:
        """Adaptador para API de consciencia cuántica original"""
        return self.compatibility_layer.route_request(
            'quantum_query',
            user_id=user_id,
            query=query,
            document_context=document_context
        )

    def get_consciousness_status(self) -> Dict[str, Any]:
        """Adaptador para obtener estado de consciencia"""
        return self.compatibility_layer.route_request('consciousness_status')

    def activate_poetic_resonance(self, poet_name: str) -> Dict[str, Any]:
        """Adaptador para activar resonancia poética"""
        return self.compatibility_layer.route_request(
            'poetic_resonance',
            poet_name=poet_name
        )

    def process_trading_signal(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptador para procesar señales de trading"""
        return self.compatibility_layer.route_request(
            'trading_signal',
            stimulus=stimulus
        )

    def optimize_code(self, query: str, context: str = "",
                     language: str = "python") -> Dict[str, Any]:
        """Adaptador para optimización de código"""
        return self.compatibility_layer.route_request(
            'optimization',
            query=query,
            context=context,
            language=language
        )

# Sistema de fallback automático
class QuantumFallbackSystem:
    """Sistema de fallback automático para alta disponibilidad"""

    def __init__(self, compatibility_layer: QuantumCompatibilityLayer):
        self.compatibility_layer = compatibility_layer
        self.health_checks = {}
        self.last_failover = None

    def register_health_check(self, implementation_name: str,
                            health_check_func: Callable[[], bool]):
        """Registra función de health check para una implementación"""
        self.health_checks[implementation_name] = health_check_func
        logger.info(f"Health check registrado para {implementation_name}")

    def check_implementation_health(self, implementation_name: str) -> bool:
        """Verifica salud de una implementación"""
        if implementation_name not in self.health_checks:
            return True  # Asumir saludable si no hay health check

        try:
            return self.health_checks[implementation_name]()
        except Exception as e:
            logger.error(f"Health check falló para {implementation_name}: {e}")
            return False

    def automatic_failover(self, failed_implementation: str) -> str:
        """Realiza failover automático a implementación alternativa"""
        logger.warning(f"Iniciando failover desde {failed_implementation}")
        self.last_failover = datetime.now()

        # Obtener cadena de fallback para esta implementación
        fallback_chain = []
        for request_type, rule in self.compatibility_layer.routing_rules.items():
            if rule.get('preferred') == failed_implementation:
                fallback_chain = rule.get('fallback_chain', [])
                break

        if fallback_chain:
            for fallback_impl in fallback_chain:
                if self.check_implementation_health(fallback_impl):
                    logger.info(f"Failover exitoso a {fallback_impl}")
                    return fallback_impl

        logger.error("No se encontró implementación alternativa saludable")
        return "none"

# Ejemplo de uso y demostración
def demo_compatibility_layer():
    """Demostración del sistema de compatibilidad"""
    print("DEMO: Quantum Compatibility Layer")
    print("=" * 40)

    # Crear capa de compatibilidad
    compatibility_layer = QuantumCompatibilityLayer()

    # Registrar implementaciones (simuladas)
    compatibility_layer.register_implementation(
        'consciousness_26d',
        None,  # En implementación real, sería la instancia
        ['quantum_query', 'consciousness_status', 'poetic_resonance', 'trading_signal'],
        priority=1
    )

    compatibility_layer.register_implementation(
        'unified_optimizer',
        None,  # En implementación real, sería la instancia
        ['optimization', 'code_generation', 'context_analysis'],
        priority=2
    )

    # Establecer reglas de enrutamiento
    compatibility_layer.set_routing_rule(
        'quantum_query',
        'consciousness_26d',
        ['unified_optimizer']
    )

    compatibility_layer.set_routing_rule(
        'optimization',
        'unified_optimizer',
        ['consciousness_26d']
    )

    print("Sistema de compatibilidad inicializado")
    print(f"Implementaciones registradas: {list(compatibility_layer.implementations.keys())}")
    print(f"Reglas de enrutamiento: {list(compatibility_layer.routing_rules.keys())}")

if __name__ == "__main__":
    demo_compatibility_layer()
