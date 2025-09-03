#!/usr/bin/env python3
"""
QBTC APISIX UNIFIED ORCHESTRATOR
Orchestrator maestro que unifica APISIX MCP + Docker + Servicios CIO
Sin duplicar funcionalidades, aprovechando toda la infraestructura existente

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
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configurar logging primero
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

class QbtcApisixUnifiedOrchestrator:
    """Orchestrator maestro que unifica APISIX MCP + Docker + Servicios CIO"""
    
    def __init__(self):
        self.event_bus = QbtcEventBusActivator() if QbtcEventBusActivator else None
        self.ecosystem = QbtcEcosystemOrchestrator() if QbtcEcosystemOrchestrator else None
        self.start_time = time.time()
        
        # URLs y configuración
        self.apisix_docker_admin = "http://127.0.0.1:9180/apisix/admin"
        self.apisix_docker_gateway = "http://127.0.0.1:9080"
        self.node_api_url = "http://127.0.0.1:3001"
        self.python_api_url = "http://127.0.0.1:8000"
        self.rabbitmq_url = "amqp://quantum_user:VIGOLEONROCKS_888HZ@127.0.0.1:5672/quantum_vhost"
        
        # Puertos de servicios conocidos
        self.service_ports = {
            3001: 'node_api_experiments',
            8000: 'python_api_quantum_coding',
            9080: 'apisix_gateway',
            9180: 'apisix_admin',
            5672: 'rabbitmq',
            15672: 'rabbitmq_management',
            6379: 'redis',
            5432: 'supabase_db'
        }
        
        # Contadores de rendimiento
        self.performance_metrics = {
            'services_discovered': 0,
            'routes_configured': 0,
            'health_checks_passed': 0,
            'quantum_signatures_generated': 0,
            'start_timestamp': datetime.now().isoformat()
        }
        
    async def activate_unified_system(self) -> Dict[str, Any]:
        """Activar sistema unificado completo sin duplicar funcionalidades"""
        
        logger.info("QBTC APISIX UNIFIED ORCHESTRATOR INICIANDO")
        logger.info("Frecuencia Base: 888Hz | Sistema: VIGOLEONROCKS")
        
        results = {
            'status': 'INITIALIZING',
            'timestamp': datetime.now().isoformat(),
            'frequency': 888,
            'components': {},
            'performance_metrics': self.performance_metrics.copy()
        }
        
        try:
            # 1. Verificar infraestructura existente
            logger.info("Verificando infraestructura existente...")
            infrastructure_status = await self.verify_existing_infrastructure()
            results['infrastructure_status'] = infrastructure_status
            active_services = sum(infrastructure_status.values())
            logger.info(f"Infraestructura verificada: {active_services} servicios activos")
            
            # 2. Detectar y configurar APISIX MCP (si está disponible)
            logger.info("Verificando APISIX MCP...")
            mcp_status = await self.check_apisix_mcp()
            results['apisix_mcp_status'] = mcp_status
            
            # 3. Verificar y configurar APISIX Docker
            logger.info("Verificando APISIX Docker...")
            docker_status = await self.verify_and_configure_docker_apisix()
            results['apisix_docker_status'] = docker_status
            
            # 4. Auto-discovery de servicios activos
            logger.info("Iniciando auto-discovery de servicios...")
            discovered_services = await self.discover_active_services()
            results['discovered_services'] = discovered_services
            self.performance_metrics['services_discovered'] = len(discovered_services)
            
            # 5. Configurar rutas APISIX para servicios encontrados
            logger.info("Configurando rutas APISIX...")
            route_config_results = await self.configure_apisix_routes(discovered_services)
            results['route_configuration'] = route_config_results
            self.performance_metrics['routes_configured'] = len(route_config_results.get('routes', []))
            
            # 6. Activar monitoreo unificado
            logger.info("Activando monitoreo unificado...")
            monitoring_status = await self.activate_unified_monitoring()
            results['monitoring'] = monitoring_status
            
            # 7. Verificar conectividad end-to-end
            logger.info("Ejecutando pruebas de conectividad...")
            connectivity_tests = await self.run_connectivity_tests()
            results['connectivity_tests'] = connectivity_tests
            self.performance_metrics['health_checks_passed'] = sum(1 for test in connectivity_tests.values() if test.get('status') == 'success')
            
            # 8. Calcular score de rendimiento mejorado
            logger.info("Calculando score de rendimiento...")
            performance_score = await self.calculate_performance_score(results)
            results['performance_score'] = performance_score
            
            # 9. Generar signatures cuánticas para servicios activos
            logger.info("Generando signatures cuánticas...")
            quantum_signatures = await self.generate_quantum_signatures(discovered_services)
            results['quantum_signatures'] = quantum_signatures
            self.performance_metrics['quantum_signatures_generated'] = len(quantum_signatures)
            
            results['status'] = 'UNIFIED_SYSTEM_ACTIVE'
            results['uptime_seconds'] = time.time() - self.start_time
            results['final_performance_metrics'] = self.performance_metrics
            
            # 10. Guardar reporte completo
            await self.save_unified_report(results)
            
            logger.info("Sistema QBTC Unificado activado exitosamente")
            logger.info(f"Score de rendimiento: {performance_score.get('total_score', 0)}/100")
            logger.info(f"Servicios integrados: {len(discovered_services)}")
            logger.info(f"Rutas configuradas: {len(route_config_results.get('routes', []))}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error en activación del sistema unificado: {e}")
            results['status'] = 'ERROR'
            results['error'] = str(e)
            return results
    
    async def verify_existing_infrastructure(self) -> Dict[str, bool]:
        """Verificar qué componentes de infraestructura ya están activos"""
        status = {}
        
        # Verificar puertos activos de forma concurrente
        async def check_service_port(port, service_name):
            is_active = await self.check_port_active(port)
            if is_active:
                logger.info(f"{service_name} activo en puerto {port}")
            return service_name, is_active
        
        port_checks = [check_service_port(port, service_name) for port, service_name in self.service_ports.items()]
        results = await asyncio.gather(*port_checks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, tuple):
                service_name, is_active = result
                status[service_name] = is_active
        
        # Verificar servicios Docker si está disponible
        try:
            result = subprocess.run(['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                docker_output = result.stdout.lower()
                status['docker_available'] = True
                status['quantum_infrastructure_containers'] = 'quantum' in docker_output
                if 'quantum-rabbitmq' in docker_output:
                    status['rabbitmq_container'] = True
                if 'quantum-apisix' in docker_output:
                    status['apisix_container'] = True
                if 'quantum-api' in docker_output:
                    status['api_containers'] = True
            else:
                status['docker_available'] = False
        except Exception as e:
            logger.warning(f"No se pudo verificar Docker: {e}")
            status['docker_available'] = False
        
        return status
    
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
    
    async def check_apisix_mcp(self) -> Dict[str, Any]:
        """Verificar el estado del APISIX MCP"""
        mcp_dir = Path("scripts/apisix-mcp-main")
        
        status = {
            'directory_exists': mcp_dir.exists(),
            'package_json_exists': (mcp_dir / "package.json").exists(),
            'main_file_exists': (mcp_dir / "src/quantum-apisix-vigoleonrocks-final.ts").exists(),
            'build_ready': False,
            'node_modules_exists': (mcp_dir / "node_modules").exists()
        }
        
        if status['directory_exists'] and status['package_json_exists']:
            # Verificar si hay package-lock.json (indica build exitoso)
            status['build_ready'] = (mcp_dir / "package-lock.json").exists()
            
            if status['build_ready']:
                logger.info("APISIX MCP está listo y construido exitosamente")
            else:
                logger.info("APISIX MCP existe pero necesita build")
        
        return status
    
    async def verify_and_configure_docker_apisix(self) -> Dict[str, Any]:
        """Verificar y configurar APISIX Docker"""
        status = {
            'admin_api_accessible': False,
            'gateway_accessible': False,
            'configuration_files_exist': False,
            'routes_configured': 0
        }
        
        # Verificar accesibilidad del Admin API
        try:
            response = requests.get(f"{self.apisix_docker_admin}/routes", 
                                  headers={"X-API-KEY": "qbtc-888hz-vigoleonrocks-unified"},
                                  timeout=5)
            if response.status_code == 200:
                status['admin_api_accessible'] = True
                routes_data = response.json()
                status['routes_configured'] = len(routes_data.get('list', []))
                logger.info(f"APISIX Admin API accesible, {status['routes_configured']} rutas configuradas")
        except Exception as e:
            logger.warning(f"APISIX Admin API no accesible: {e}")
        
        # Verificar accesibilidad del Gateway
        try:
            response = requests.get(self.apisix_docker_gateway, timeout=5)
            status['gateway_accessible'] = response.status_code in [200, 404]  # 404 es normal sin rutas
            if status['gateway_accessible']:
                logger.info("APISIX Gateway accesible")
        except Exception as e:
            logger.warning(f"APISIX Gateway no accesible: {e}")
        
        # Verificar archivos de configuración
        config_dir = Path("server/quantum-infrastructure/apisix_conf")
        status['configuration_files_exist'] = config_dir.exists()
        
        return status
    
    async def discover_active_services(self) -> List[Dict[str, Any]]:
        """Descubrir servicios activos en el ecosistema"""
        discovered_services = []
        
        # Servicios conocidos para probar
        known_services = [
            {
                'name': 'quantum-api-node',
                'url': self.node_api_url,
                'type': 'experiments_api',
                'health_endpoint': '/health'
            },
            {
                'name': 'quantum-api-python',
                'url': self.python_api_url,
                'type': 'quantum_coding_api',
                'health_endpoint': '/health'
            },
            {
                'name': 'llm-api-service',
                'url': 'http://127.0.0.1:8000',
                'type': 'llm_service',
                'health_endpoint': '/v1/models'
            }
        ]
        
        for service in known_services:
            try:
                # Intentar conectar al servicio
                response = requests.get(service['url'], timeout=3)
                if response.status_code in [200, 404, 405]:  # Muchas APIs devuelven 404/405 en GET /
                    service['status'] = 'active'
                    service['response_time'] = response.elapsed.total_seconds()
                    
                    # Intentar health check si está disponible
                    if service.get('health_endpoint'):
                        try:
                            health_response = requests.get(f"{service['url']}{service['health_endpoint']}", timeout=2)
                            service['health_status'] = health_response.status_code
                        except:
                            service['health_status'] = 'unknown'
                    
                    discovered_services.append(service)
                    logger.info(f"✅ Servicio descubierto: {service['name']} en {service['url']}")
                
            except Exception as e:
                logger.debug(f"Servicio {service['name']} no disponible: {e}")
                service['status'] = 'inactive'
        
        return discovered_services
    
    async def configure_apisix_routes(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Configurar rutas APISIX para servicios descubiertos"""
        results = {
            'routes': [],
            'upstreams': [],
            'errors': []
        }
        
        admin_headers = {"X-API-KEY": "qbtc-888hz-vigoleonrocks-unified", "Content-Type": "application/json"}
        
        for service in services:
            if service.get('status') != 'active':
                continue
                
            try:
                # Configurar upstream
                upstream_id = f"upstream-{service['name']}"
                upstream_config = {
                    "type": "roundrobin",
                    "nodes": {
                        service['url'].replace('http://', ''): 1
                    },
                    "timeout": {
                        "connect": 5,
                        "send": 5,
                        "read": 30
                    }
                }
                
                upstream_response = requests.put(
                    f"{self.apisix_docker_admin}/upstreams/{upstream_id}",
                    headers=admin_headers,
                    json=upstream_config,
                    timeout=10
                )
                
                if upstream_response.status_code in [200, 201]:
                    results['upstreams'].append(upstream_id)
                    logger.info(f"✅ Upstream configurado: {upstream_id}")
                
                # Configurar ruta
                route_id = f"route-{service['name']}"
                route_config = {
                    "name": f"QBTC Route for {service['name']}",
                    "uri": f"/api/{service['type']}/*",
                    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                    "upstream_id": upstream_id,
                    "plugins": {
                        "cors": {
                            "allow_origins": "**",
                            "allow_methods": "**",
                            "allow_headers": "**"
                        },
                        "prometheus": {
                            "enable": True
                        }
                    },
                    "labels": {
                        "quantum_frequency": "888",
                        "vigoleonrocks_enhanced": "true",
                        "qbtc_service": service['type']
                    }
                }
                
                route_response = requests.put(
                    f"{self.apisix_docker_admin}/routes/{route_id}",
                    headers=admin_headers,
                    json=route_config,
                    timeout=10
                )
                
                if route_response.status_code in [200, 201]:
                    results['routes'].append(route_id)
                    logger.info(f"✅ Ruta configurada: {route_id} -> {service['url']}")
                else:
                    error_msg = f"Error configurando ruta {route_id}: {route_response.status_code}"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
                
            except Exception as e:
                error_msg = f"Error configurando servicio {service['name']}: {e}"
                results['errors'].append(error_msg)
                logger.error(error_msg)
        
        return results
    
    async def activate_unified_monitoring(self) -> Dict[str, Any]:
        """Activar sistema de monitoreo unificado"""
        monitoring_status = {
            'logs_directory_ready': False,
            'metrics_collection_active': False,
            'apisix_metrics_accessible': False
        }
        
        # Verificar/crear directorio de logs
        logs_dir = Path("logs")
        if not logs_dir.exists():
            logs_dir.mkdir(exist_ok=True)
        monitoring_status['logs_directory_ready'] = logs_dir.exists()
        
        # Verificar métricas de APISIX
        try:
            metrics_response = requests.get(f"{self.apisix_docker_gateway}/apisix/prometheus/metrics", timeout=5)
            monitoring_status['apisix_metrics_accessible'] = metrics_response.status_code == 200
            if monitoring_status['apisix_metrics_accessible']:
                logger.info("✅ Métricas APISIX accesibles")
        except Exception as e:
            logger.warning(f"Métricas APISIX no accesibles: {e}")
        
        # Escribir archivo de monitoreo unificado
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        monitoring_file = logs_dir / f"monitoring_unified_{timestamp}.json"
        
        monitoring_data = {
            'timestamp': datetime.now().isoformat(),
            'system': 'QBTC_UNIFIED_APISIX',
            'frequency': 888,
            'performance_metrics': self.performance_metrics,
            'monitoring_status': monitoring_status
        }
        
        try:
            with open(monitoring_file, 'w') as f:
                json.dump(monitoring_data, f, indent=2)
            monitoring_status['metrics_collection_active'] = True
            logger.info(f"✅ Archivo de monitoreo creado: {monitoring_file}")
        except Exception as e:
            logger.error(f"Error creando archivo de monitoreo: {e}")
        
        return monitoring_status
    
    async def run_connectivity_tests(self) -> Dict[str, Dict[str, Any]]:
        """Ejecutar pruebas de conectividad end-to-end"""
        tests = {}
        
        # Test 1: APISIX Gateway health
        tests['apisix_gateway'] = await self.test_endpoint(self.apisix_docker_gateway, "APISIX Gateway")
        
        # Test 2: APISIX Admin API
        tests['apisix_admin'] = await self.test_endpoint(
            f"{self.apisix_docker_admin}/routes", 
            "APISIX Admin API",
            headers={"X-API-KEY": "qbtc-888hz-vigoleonrocks-unified"}
        )
        
        # Test 3: Servicios API a través de APISIX (si están configurados)
        gateway_routes = [
            f"{self.apisix_docker_gateway}/api/experiments_api/health",
            f"{self.apisix_docker_gateway}/api/quantum_coding_api/health"
        ]
        
        for i, route in enumerate(gateway_routes):
            test_name = f"gateway_route_{i+1}"
            tests[test_name] = await self.test_endpoint(route, f"Gateway Route {i+1}")
        
        # Test 4: RabbitMQ (si está disponible)
        if await self.check_port_active(15672):
            tests['rabbitmq_management'] = await self.test_endpoint(
                "http://127.0.0.1:15672/api/overview", 
                "RabbitMQ Management",
                auth=('quantum_user', 'VIGOLEONROCKS_888HZ')
            )
        
        return tests
    
    async def test_endpoint(self, url: str, name: str, headers: Optional[Dict] = None, auth: Optional[tuple] = None) -> Dict[str, Any]:
        """Probar un endpoint específico"""
        start_time = time.time()
        try:
            response = requests.get(url, headers=headers, auth=auth, timeout=10)
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
    
    async def calculate_performance_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular score de rendimiento del sistema unificado"""
        score_components = {}
        total_score = 0
        
        # Componente 1: Infraestructura activa (30 puntos)
        infrastructure_active = sum(results.get('infrastructure_status', {}).values())
        infrastructure_total = len(results.get('infrastructure_status', {}))
        if infrastructure_total > 0:
            infrastructure_score = min(30, (infrastructure_active / infrastructure_total) * 30)
        else:
            infrastructure_score = 0
        score_components['infrastructure'] = round(infrastructure_score, 1)
        total_score += infrastructure_score
        
        # Componente 2: Servicios descubiertos (25 puntos)
        services_discovered = len(results.get('discovered_services', []))
        services_score = min(25, services_discovered * 8)  # 8 puntos por servicio, max 25
        score_components['services_discovery'] = round(services_score, 1)
        total_score += services_score
        
        # Componente 3: Rutas APISIX configuradas (20 puntos)
        routes_configured = len(results.get('route_configuration', {}).get('routes', []))
        routes_score = min(20, routes_configured * 10)  # 10 puntos por ruta, max 20
        score_components['apisix_routes'] = round(routes_score, 1)
        total_score += routes_score
        
        # Componente 4: Pruebas de conectividad (15 puntos)
        connectivity_tests = results.get('connectivity_tests', {})
        successful_tests = sum(1 for test in connectivity_tests.values() if test.get('status') == 'success')
        total_tests = len(connectivity_tests)
        if total_tests > 0:
            connectivity_score = (successful_tests / total_tests) * 15
        else:
            connectivity_score = 0
        score_components['connectivity'] = round(connectivity_score, 1)
        total_score += connectivity_score
        
        # Componente 5: Monitoreo activo (10 puntos)
        monitoring = results.get('monitoring', {})
        monitoring_active = sum(monitoring.values())
        monitoring_total = len(monitoring)
        if monitoring_total > 0:
            monitoring_score = (monitoring_active / monitoring_total) * 10
        else:
            monitoring_score = 0
        score_components['monitoring'] = round(monitoring_score, 1)
        total_score += monitoring_score
        
        return {
            'total_score': round(total_score, 1),
            'components': score_components,
            'grade': 'A' if total_score >= 90 else 'B' if total_score >= 80 else 'C' if total_score >= 70 else 'D',
            'improvement_suggestions': await self.generate_improvement_suggestions(score_components)
        }
    
    async def generate_improvement_suggestions(self, score_components: Dict[str, float]) -> List[str]:
        """Generar sugerencias de mejora basadas en el score"""
        suggestions = []
        
        if score_components.get('infrastructure', 0) < 25:
            suggestions.append("Activar más componentes de infraestructura (Docker, RabbitMQ, Redis)")
        
        if score_components.get('services_discovery', 0) < 20:
            suggestions.append("Iniciar más servicios API para mejorar el auto-discovery")
        
        if score_components.get('apisix_routes', 0) < 15:
            suggestions.append("Configurar más rutas APISIX para servicios activos")
        
        if score_components.get('connectivity', 0) < 12:
            suggestions.append("Verificar conectividad de red y configuración de puertos")
        
        if score_components.get('monitoring', 0) < 8:
            suggestions.append("Activar sistema de métricas y monitoreo completo")
        
        return suggestions
    
    async def generate_quantum_signatures(self, services: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generar signatures cuánticas para servicios activos"""
        signatures = {}
        
        for service in services:
            if service.get('status') == 'active':
                # Generar signature cuántica basada en frecuencia 888Hz
                quantum_data = {
                    'service_name': service['name'],
                    'url': service['url'],
                    'timestamp': int(time.time()),
                    'frequency': 888
                }
                
                # Signature cuántica simple (en producción sería más compleja)
                signature = f"QBTC888_{hash(str(quantum_data)) % 999999:06d}_VIGOLEONROCKS"
                signatures[service['name']] = signature
                
                logger.info(f"🔮 Signature cuántica generada para {service['name']}: {signature}")
        
        return signatures
    
    async def save_unified_report(self, results: Dict[str, Any]) -> str:
        """Guardar reporte completo del sistema unificado"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'qbtc_unified_apisix_report_{timestamp}.json'
        
        # Enriquecer resultados con metadata adicional
        enhanced_results = {
            **results,
            'report_metadata': {
                'generated_by': 'QBTC_APISIX_UNIFIED_ORCHESTRATOR',
                'version': '888.1.0-UNIFIED',
                'frequency': 888,
                'system': 'VIGOLEONROCKS',
                'report_timestamp': timestamp,
                'total_execution_time': time.time() - self.start_time
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📄 Reporte unificado guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            return ""


async def main():
    """Función principal para ejecutar el orchestrator"""
    print("🚀 Iniciando QBTC APISIX Unified Orchestrator...")
    
    orchestrator = QbtcApisixUnifiedOrchestrator()
    results = await orchestrator.activate_unified_system()
    
    print("\n🌌 ================== RESUMEN FINAL ==================")
    print(f"🎯 Estado: {results.get('status')}")
    print(f"📊 Score: {results.get('performance_score', {}).get('total_score', 0)}/100")
    print(f"🔧 Servicios: {len(results.get('discovered_services', []))}")
    print(f"🛣️ Rutas: {len(results.get('route_configuration', {}).get('routes', []))}")
    print(f"⚡ Tiempo: {results.get('uptime_seconds', 0):.2f}s")
    print("🌌 ================================================")
    
    return results


if __name__ == "__main__":
    asyncio.run(main())