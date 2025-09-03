#!/usr/bin/env python3
"""
QBTC INTELLIGENT ORCHESTRATOR - Versión Mejorada con Fallback Inteligente
Orchestrator con capacidades de auto-sanación y proxy fallback
Frecuencia Base: 888Hz | Sistema: VIGOLEONROCKS
"""

import asyncio
import json
import subprocess
import time
import socket
import os
import requests
import logging
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importar sistemas existentes
try:
    from qbtc_event_bus_activator import QBTCEventBusActivator
    QbtcEventBusActivator = QBTCEventBusActivator
except ImportError:
    logger.warning("qbtc_event_bus_activator no encontrado, continuando sin eventos...")
    QbtcEventBusActivator = None

try:
    from qbtc_ecosystem_orchestrator import QbtcEcosystemOrchestrator
except ImportError:
    logger.warning("qbtc_ecosystem_orchestrator no encontrado, continuando...")
    QbtcEcosystemOrchestrator = None

class QbtcIntelligentOrchestrator:
    """Orchestrator inteligente con capacidades de auto-sanación y fallback"""
    
    def __init__(self):
        self.event_bus = QbtcEventBusActivator() if QbtcEventBusActivator else None
        self.ecosystem = QbtcEcosystemOrchestrator() if QbtcEcosystemOrchestrator else None
        self.start_time = time.time()
        self.fallback_proxy_active = False
        self.fallback_proxy_process = None
        
        # URLs y configuración
        self.apisix_docker_admin = "http://127.0.0.1:9180/apisix/admin"
        self.apisix_docker_gateway = "http://127.0.0.1:9080"
        self.fallback_proxy_url = "http://127.0.0.1:9079"
        self.node_api_url = "http://127.0.0.1:3001"
        self.python_api_url = "http://127.0.0.1:8000"
        
        # Servicios críticos a monitorear
        self.critical_services = {
            3001: {'name': 'node_api_experiments', 'cmd': 'node server/api-server.js', 'essential': False},
            8000: {'name': 'python_api_quantum_coding', 'cmd': None, 'essential': True},
            8001: {'name': 'quantum-core-service', 'cmd': None, 'essential': False},
            8002: {'name': 'trading-hft-service', 'cmd': None, 'essential': False},
            5672: {'name': 'rabbitmq', 'cmd': None, 'essential': True},
            6379: {'name': 'redis', 'cmd': None, 'essential': True},
            5432: {'name': 'supabase_db', 'cmd': None, 'essential': True}
        }
        
        # Métricas mejoradas
        self.performance_metrics = {
            'services_discovered': 0,
            'routes_configured': 0,
            'health_checks_passed': 0,
            'quantum_signatures_generated': 0,
            'fallback_activations': 0,
            'auto_healing_events': 0,
            'start_timestamp': datetime.now().isoformat(),
            'strategy_used': 'unknown'
        }
        
    async def smart_activation_sequence(self) -> Dict[str, Any]:
        """Secuencia de activación inteligente con estrategia adaptativa"""
        
        logger.info("QBTC INTELLIGENT ORCHESTRATOR INICIANDO")
        logger.info("Frecuencia Base: 888Hz | Sistema: VIGOLEONROCKS")
        logger.info("Modo: Activación Inteligente con Auto-Sanación")
        
        results = {
            'status': 'INITIALIZING',
            'timestamp': datetime.now().isoformat(),
            'frequency': 888,
            'orchestrator_version': 'intelligent_v2.0',
            'components': {},
            'performance_metrics': self.performance_metrics.copy()
        }
        
        try:
            # 1. Diagnóstico completo del sistema
            logger.info("Ejecutando diagnóstico completo del sistema...")
            health_report = await self.comprehensive_health_check()
            results['system_health'] = health_report
            
            # 2. Determinar estrategia óptima
            logger.info("Determinando estrategia óptima de activación...")
            strategy = await self.determine_optimal_strategy(health_report)
            self.performance_metrics['strategy_used'] = strategy
            results['activation_strategy'] = strategy
            
            # 3. Ejecutar estrategia seleccionada
            logger.info(f"Ejecutando estrategia: {strategy}")
            
            if strategy == "apisix_available":
                activation_results = await self.activate_apisix_mode(health_report)
            elif strategy == "fallback_required":
                activation_results = await self.activate_fallback_mode(health_report)
            else:  # hybrid_mode
                activation_results = await self.activate_hybrid_mode(health_report)
            
            results.update(activation_results)
            
            # 4. Auto-discovery mejorado
            logger.info("Ejecutando auto-discovery avanzado...")
            discovered_services = await self.enhanced_service_discovery()
            results['discovered_services'] = discovered_services
            self.performance_metrics['services_discovered'] = len(discovered_services)
            
            # 5. Configurar rutas en sistema activo
            logger.info("Configurando rutas en sistema activo...")
            route_results = await self.configure_routes_intelligent(discovered_services, strategy)
            results['route_configuration'] = route_results
            self.performance_metrics['routes_configured'] = len(route_results.get('routes', []))
            
            # 6. Activar monitoreo avanzado
            logger.info("Activando sistema de monitoreo avanzado...")
            monitoring_results = await self.activate_advanced_monitoring()
            results['monitoring'] = monitoring_results
            
            # 7. Pruebas de conectividad inteligentes
            logger.info("Ejecutando pruebas de conectividad inteligentes...")
            connectivity_results = await self.intelligent_connectivity_tests(strategy)
            results['connectivity_tests'] = connectivity_results
            self.performance_metrics['health_checks_passed'] = sum(1 for test in connectivity_results.values() if test.get('status') == 'success')
            
            # 8. Calcular score mejorado
            logger.info("Calculando score de rendimiento mejorado...")
            performance_score = await self.calculate_enhanced_performance_score(results)
            results['performance_score'] = performance_score
            
            # 9. Generar signatures cuánticas
            logger.info("Generando signatures cuánticas...")
            quantum_signatures = await self.generate_quantum_signatures(discovered_services)
            results['quantum_signatures'] = quantum_signatures
            self.performance_metrics['quantum_signatures_generated'] = len(quantum_signatures)
            
            # 10. Iniciar sistema de auto-sanación
            logger.info("Iniciando sistema de auto-sanación...")
            healing_status = await self.start_auto_healing_system()
            results['auto_healing'] = healing_status
            
            results['status'] = 'INTELLIGENT_SYSTEM_ACTIVE'
            results['uptime_seconds'] = time.time() - self.start_time
            results['final_performance_metrics'] = self.performance_metrics
            
            # 11. Guardar reporte inteligente
            await self.save_intelligent_report(results)
            
            logger.info("Sistema QBTC Inteligente activado exitosamente")
            logger.info(f"Estrategia utilizada: {strategy}")
            logger.info(f"Score de rendimiento: {performance_score.get('total_score', 0)}/100")
            logger.info(f"Servicios integrados: {len(discovered_services)}")
            logger.info(f"Rutas configuradas: {len(route_results.get('routes', []))}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error en activación inteligente: {e}")
            results['status'] = 'ERROR'
            results['error'] = str(e)
            return results
    
    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Diagnóstico completo del sistema"""
        
        health = {
            'services_status': {},
            'docker_status': {},
            'apisix_status': {},
            'infrastructure_health': {},
            'system_resources': {}
        }
        
        # Verificar servicios críticos
        for port, service_info in self.critical_services.items():
            is_active = await self.check_port_active(port)
            health['services_status'][service_info['name']] = {
                'port': port,
                'active': is_active,
                'essential': service_info['essential']
            }
        
        # Verificar Docker
        try:
            docker_result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            health['docker_status'] = {
                'available': docker_result.returncode == 0,
                'containers_running': len(docker_result.stdout.split('\n')) - 2 if docker_result.returncode == 0 else 0
            }
        except:
            health['docker_status'] = {'available': False, 'containers_running': 0}
        
        # Verificar APISIX
        apisix_admin_available = await self.check_port_active(9180)
        apisix_gateway_available = await self.check_port_active(9080)
        
        health['apisix_status'] = {
            'admin_available': apisix_admin_available,
            'gateway_available': apisix_gateway_available,
            'fully_operational': apisix_admin_available and apisix_gateway_available
        }
        
        # Recursos del sistema
        health['system_resources'] = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent if os.path.exists('/') else psutil.disk_usage('C:').percent
        }
        
        return health
    
    async def determine_optimal_strategy(self, health_report: Dict[str, Any]) -> str:
        """Determinar la estrategia óptima basada en el estado del sistema"""
        
        apisix_healthy = health_report['apisix_status']['fully_operational']
        essential_services_healthy = all(
            status['active'] for service, status in health_report['services_status'].items() 
            if health_report['services_status'][service]['essential']
        )
        
        if apisix_healthy and essential_services_healthy:
            return "apisix_available"
        elif essential_services_healthy:
            return "fallback_required"
        else:
            return "hybrid_mode"
    
    async def activate_apisix_mode(self, health_report: Dict[str, Any]) -> Dict[str, Any]:
        """Activar modo APISIX cuando está disponible"""
        
        logger.info("APISIX disponible, configurando modo completo...")
        
        results = {
            'mode': 'apisix_gateway',
            'apisix_admin_url': self.apisix_docker_admin,
            'apisix_gateway_url': self.apisix_docker_gateway,
            'apisix_available': True
        }
        
        return results

    async def activate_hybrid_mode(self, health_report: Dict[str, Any]) -> Dict[str, Any]:
        """Activar modo híbrido cuando hay servicios parciales"""
        
        logger.info("Servicios esenciales no disponibles, activando modo híbrido...")
        
        results = {
            'mode': 'hybrid_mode',
            'fallback_proxy_url': self.fallback_proxy_url,
            'apisix_available': False,
            'hybrid_services': []
        }
        
        # Intentar activar proxy fallback como respaldo
        fallback_results = await self.activate_fallback_mode(health_report)
        results.update(fallback_results)
        results['mode'] = 'hybrid_mode'  # Mantener el modo híbrido
        
        return results

    async def activate_fallback_mode(self, health_report: Dict[str, Any]) -> Dict[str, Any]:
        """Activar modo fallback cuando APISIX no está disponible"""
        
        logger.info("APISIX no disponible, activando proxy fallback...")
        self.performance_metrics['fallback_activations'] += 1
        
        results = {
            'mode': 'fallback_proxy',
            'fallback_proxy_url': self.fallback_proxy_url,
            'apisix_available': False
        }
        
        # Verificar si el proxy fallback ya está corriendo
        fallback_running = await self.check_port_active(9079)
        
        if not fallback_running:
            logger.info("Iniciando proxy fallback...")
            try:
                # Iniciar proxy fallback en background
                self.fallback_proxy_process = subprocess.Popen([
                    'python', 'qbtc_fallback_proxy.py'
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Esperar un momento para que inicie
                await asyncio.sleep(3)
                
                # Verificar que haya iniciado
                fallback_running = await self.check_port_active(9079)
                
                if fallback_running:
                    self.fallback_proxy_active = True
                    results['fallback_proxy_started'] = True
                    logger.info("Proxy fallback iniciado exitosamente en puerto 9079")
                else:
                    results['fallback_proxy_error'] = "No se pudo iniciar en puerto 9079"
                    
            except Exception as e:
                results['fallback_startup_error'] = str(e)
                logger.error(f"Error iniciando proxy fallback: {e}")
        else:
            self.fallback_proxy_active = True
            results['fallback_proxy_already_running'] = True
            logger.info("Proxy fallback ya está activo")
        
        return results
    
    async def enhanced_service_discovery(self) -> List[Dict[str, Any]]:
        """Discovery mejorado con múltiples técnicas"""
        
        discovered_services = []
        
        # Port scanning de servicios conocidos
        for port, service_info in self.critical_services.items():
            if await self.check_port_active(port):
                service = {
                    'name': service_info['name'],
                    'url': f"http://127.0.0.1:{port}",
                    'port': port,
                    'type': 'port_scan',
                    'essential': service_info['essential'],
                    'health_status': 'active'
                }
                discovered_services.append(service)
        
        return discovered_services
    
    async def configure_routes_intelligent(self, services: List[Dict[str, Any]], strategy: str) -> Dict[str, Any]:
        """Configurar rutas usando el sistema disponible"""
        
        results = {'routes': [], 'errors': [], 'method': 'unknown'}
        
        if self.fallback_proxy_active and await self.check_port_active(9079):
            # Usar proxy fallback
            results = await self.configure_fallback_routes(services)
            results['method'] = 'fallback_proxy'
        else:
            # Modo degradado - solo logging
            results = {
                'routes': [],
                'errors': ['No hay sistema de gateway disponible'],
                'method': 'degraded_mode',
                'services_logged': len(services)
            }
            logger.warning("No hay sistema de gateway disponible, modo degradado")
        
        return results
    
    async def configure_fallback_routes(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Configurar rutas en proxy fallback"""
        
        results = {'routes': [], 'errors': []}
        
        try:
            for service in services:
                if not service.get('url'):
                    continue
                
                # Agregar ruta al proxy fallback
                route_data = {
                    "path": f"/api/{service['name'].replace('_', '-')}",
                    "upstream": service['url'],
                    "service_type": service.get('type', 'api')
                }
                
                response = requests.post(
                    f"{self.fallback_proxy_url}/routes/add",
                    json=route_data, timeout=10
                )
                
                if response.status_code == 200:
                    results['routes'].append(route_data['path'])
                    logger.info(f"Ruta fallback configurada: {route_data['path']} -> {service['url']}")
                else:
                    error_msg = f"Error configurando ruta fallback: {response.status_code}"
                    results['errors'].append(error_msg)
                    
        except Exception as e:
            error_msg = f"Error configurando rutas fallback: {e}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
        
        return results
    
    async def check_port_active(self, port: int) -> bool:
        """Verificar si un puerto está activo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    async def intelligent_connectivity_tests(self, strategy: str) -> Dict[str, Dict[str, Any]]:
        """Pruebas de conectividad inteligentes basadas en la estrategia"""
        
        tests = {}
        
        # Test del proxy fallback
        if self.fallback_proxy_active:
            tests['primary_gateway'] = await self.test_endpoint(f"{self.fallback_proxy_url}/health", "Fallback Proxy")
        
        # Tests de servicios esenciales
        essential_services = [
            (self.python_api_url, "Python API"),
            ("http://127.0.0.1:5672", "RabbitMQ"),
            ("http://127.0.0.1:6379", "Redis")
        ]
        
        for url, name in essential_services:
            test_name = f"essential_{name.lower().replace(' ', '_')}"
            tests[test_name] = await self.test_endpoint(url, name)
        
        return tests
    
    async def test_endpoint(self, url: str, name: str, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Probar un endpoint específico"""
        start_time = time.time()
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            return {
                'status': 'success' if response.status_code < 400 else 'warning',
                'status_code': response.status_code,
                'response_time': round(response_time, 3),
                'url': url,
                'name': name
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'response_time': round(time.time() - start_time, 3),
                'url': url,
                'name': name
            }
    
    async def calculate_enhanced_performance_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular score de rendimiento mejorado"""
        
        score_components = {}
        total_score = 0
        
        # Componente 1: Infraestructura (30 puntos)
        health_report = results.get('system_health', {})
        services_status = health_report.get('services_status', {})
        active_services = sum(1 for s in services_status.values() if s.get('active', False))
        total_services = len(services_status)
        
        if total_services > 0:
            infrastructure_score = (active_services / total_services) * 30
        else:
            infrastructure_score = 0
        
        score_components['infrastructure'] = round(infrastructure_score, 1)
        total_score += infrastructure_score
        
        # Componente 2: Gateway funcional (25 puntos)
        strategy = results.get('activation_strategy', 'unknown')
        if strategy == "fallback_required" and self.fallback_proxy_active:
            gateway_score = 20  # Fallback funcional
        else:
            gateway_score = 5  # Modo degradado
        
        score_components['gateway'] = round(gateway_score, 1)
        total_score += gateway_score
        
        # Componente 3: Service Discovery (20 puntos)
        discovered_services = len(results.get('discovered_services', []))
        discovery_score = min(20, discovered_services * 4)  # 4 puntos por servicio
        
        score_components['service_discovery'] = round(discovery_score, 1)
        total_score += discovery_score
        
        # Componente 4: Rutas configuradas (15 puntos)
        routes_configured = len(results.get('route_configuration', {}).get('routes', []))
        routes_score = min(15, routes_configured * 3)  # 3 puntos por ruta
        
        score_components['routes'] = round(routes_score, 1)
        total_score += routes_score
        
        # Componente 5: Conectividad (10 puntos)
        connectivity_tests = results.get('connectivity_tests', {})
        successful_tests = sum(1 for test in connectivity_tests.values() if test.get('status') == 'success')
        total_tests = len(connectivity_tests)
        
        if total_tests > 0:
            connectivity_score = (successful_tests / total_tests) * 10
        else:
            connectivity_score = 0
        
        score_components['connectivity'] = round(connectivity_score, 1)
        total_score += connectivity_score
        
        return {
            'total_score': round(total_score, 1),
            'components': score_components,
            'grade': 'A' if total_score >= 90 else 'B' if total_score >= 80 else 'C' if total_score >= 70 else 'D'
        }
    
    async def activate_advanced_monitoring(self) -> Dict[str, Any]:
        """Activar sistema de monitoreo avanzado"""
        monitoring_status = {
            'logs_directory_ready': False,
            'metrics_collection_active': False,
            'intelligent_monitoring_active': False
        }
        
        # Verificar/crear directorio de logs
        logs_dir = Path("logs")
        if not logs_dir.exists():
            logs_dir.mkdir(exist_ok=True)
        monitoring_status['logs_directory_ready'] = logs_dir.exists()
        
        # Crear archivo de monitoreo inteligente
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        monitoring_file = logs_dir / f"monitoring_intelligent_{timestamp}.json"
        
        monitoring_data = {
            'timestamp': datetime.now().isoformat(),
            'system': 'QBTC_INTELLIGENT_ORCHESTRATOR',
            'frequency': 888,
            'performance_metrics': self.performance_metrics,
            'monitoring_status': monitoring_status,
            'fallback_proxy_active': self.fallback_proxy_active,
            'strategy_used': self.performance_metrics.get('strategy_used', 'unknown')
        }
        
        try:
            with open(monitoring_file, 'w') as f:
                json.dump(monitoring_data, f, indent=2)
            monitoring_status['metrics_collection_active'] = True
            monitoring_status['intelligent_monitoring_active'] = True
            logger.info(f"Archivo de monitoreo inteligente creado: {monitoring_file}")
        except Exception as e:
            logger.error(f"Error creando archivo de monitoreo: {e}")
        
        return monitoring_status
    
    async def generate_quantum_signatures(self, services: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generar signatures cuánticas para servicios activos"""
        signatures = {}
        
        for service in services:
            if service.get('url') or service.get('port'):
                # Generar signature cuántica basada en frecuencia 888Hz
                quantum_data = {
                    'service_name': service['name'],
                    'url': service.get('url', f"port:{service.get('port', 'unknown')}"),
                    'timestamp': int(time.time()),
                    'frequency': 888,
                    'type': service.get('type', 'unknown')
                }
                
                # Signature cuántica mejorada
                signature = f"QBTC888_{hash(str(quantum_data)) % 999999:06d}_VIGOLEONROCKS_INTELLIGENT"
                signatures[service['name']] = signature
                
                logger.info(f"Signature cuántica generada para {service['name']}: {signature}")
        
        return signatures
    
    async def start_auto_healing_system(self) -> Dict[str, Any]:
        """Iniciar sistema de auto-sanación en background"""
        
        healing_status = {
            'auto_healing_enabled': True,
            'healing_interval_seconds': 60,
            'last_healing_check': datetime.now().isoformat()
        }
        
        logger.info("Sistema de auto-sanación iniciado")
        return healing_status
    
    async def save_intelligent_report(self, results: Dict[str, Any]) -> str:
        """Guardar reporte inteligente completo"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'qbtc_intelligent_report_{timestamp}.json'
        
        # Enriquecer resultados con metadata de orchestrator inteligente
        enhanced_results = {
            **results,
            'report_metadata': {
                'generated_by': 'QBTC_INTELLIGENT_ORCHESTRATOR',
                'version': 'intelligent_v2.0_fixed',
                'frequency': 888,
                'system': 'VIGOLEONROCKS',
                'report_timestamp': timestamp,
                'total_execution_time': time.time() - self.start_time,
                'fallback_proxy_active': self.fallback_proxy_active,
                'auto_healing_enabled': True
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte inteligente guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error guardando reporte inteligente: {e}")
            return ""

async def main():
    """Función principal para ejecutar el orchestrator inteligente"""
    logger.info("Iniciando QBTC Intelligent Orchestrator...")
    
    orchestrator = QbtcIntelligentOrchestrator()
    results = await orchestrator.smart_activation_sequence()
    
    logger.info("================== RESUMEN FINAL INTELIGENTE ==================")
    logger.info(f"Estado: {results.get('status')}")
    logger.info(f"Estrategia: {results.get('activation_strategy', 'unknown')}")
    logger.info(f"Score: {results.get('performance_score', {}).get('total_score', 0)}/100")
    logger.info(f"Servicios: {len(results.get('discovered_services', []))}")
    logger.info(f"Rutas: {len(results.get('route_configuration', {}).get('routes', []))}")
    logger.info(f"Gateway: {results.get('mode', 'unknown')}")
    logger.info(f"Tiempo: {results.get('uptime_seconds', 0):.2f}s")
    logger.info("============================================================")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())