#!/usr/bin/env python3
"""
QBTC QUANTUM INFRASTRUCTURE ACTIVATOR
Activador completo de la infraestructura Docker Quantum + APISIX
Frecuencia Base: 888Hz | Sistema: VIGOLEONROCKS
"""

import asyncio
import json
import subprocess
import time
import socket
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QbtcQuantumInfrastructureActivator:
    """Activador completo de la infraestructura cuántica Docker"""
    
    def __init__(self):
        self.start_time = time.time()
        self.docker_compose_path = Path("C:/Users/Hp/Desktop/qbtc-unified-quantum-system/QBTC-VIGOLEONROCKS-UNIFIED/server/quantum-infrastructure")
        self.fallback_proxy_active = False
        
        # URLs de la infraestructura real Docker
        self.infrastructure_urls = {
            'quantum_api': 'http://127.0.0.1:3000',          # Quantum API Server
            'quantum_coding_api': 'http://127.0.0.1:8000',   # Quantum Coding API  
            'quantum_dashboard': 'http://127.0.0.1:8080',    # Dashboard
            'apisix_gateway': 'http://127.0.0.1:9080',       # APISIX Gateway
            'apisix_admin': 'http://127.0.0.1:9180',         # APISIX Admin
            'rabbitmq': 'http://127.0.0.1:15672',            # RabbitMQ Management
            'redis': 'http://127.0.0.1:6379',                # Redis
            'supabase_db': 'http://127.0.0.1:5432'           # Supabase DB
        }
        
        # Servicios críticos con puertos Docker correctos
        self.critical_services = {
            3000: {'name': 'quantum_api', 'essential': True},
            8000: {'name': 'quantum_coding_api', 'essential': True},
            8080: {'name': 'quantum_dashboard', 'essential': False},
            9080: {'name': 'apisix_gateway', 'essential': True},
            9180: {'name': 'apisix_admin', 'essential': True},
            5672: {'name': 'rabbitmq', 'essential': True},
            15672: {'name': 'rabbitmq_management', 'essential': False},
            6379: {'name': 'redis', 'essential': True},
            5432: {'name': 'supabase_db', 'essential': True}
        }
        
        self.performance_metrics = {
            'docker_services_started': 0,
            'services_health_checked': 0,
            'routes_configured': 0,
            'total_containers': 0,
            'infrastructure_score': 0,
            'activation_time': 0
        }
    
    async def activate_quantum_infrastructure(self) -> Dict[str, Any]:
        """Activar infraestructura cuántica completa"""
        
        logger.info("QBTC QUANTUM INFRASTRUCTURE ACTIVATOR INICIANDO")
        logger.info("Activando infraestructura Docker completa...")
        
        results = {
            'status': 'INITIALIZING',
            'timestamp': datetime.now().isoformat(),
            'frequency': 888,
            'system': 'VIGOLEONROCKS',
            'infrastructure_type': 'docker_quantum_complete'
        }
        
        try:
            # 1. Verificar Docker disponible
            logger.info("Verificando Docker...")
            docker_status = await self.verify_docker_available()
            results['docker_status'] = docker_status
            
            if not docker_status['available']:
                logger.error("Docker no está disponible")
                results['status'] = 'ERROR'
                results['error'] = 'Docker no disponible'
                return results
            
            # 2. Activar infraestructura Docker
            logger.info("Activando infraestructura Docker...")
            activation_results = await self.start_docker_infrastructure()
            results['activation'] = activation_results
            
            # 3. Esperar que servicios estén listos
            logger.info("Esperando servicios Docker...")
            await asyncio.sleep(30)  # Dar tiempo para que inicien
            
            # 4. Verificar servicios activos
            logger.info("Verificando servicios activos...")
            services_status = await self.verify_services_health()
            results['services_status'] = services_status
            
            # 5. Configurar APISIX si está disponible
            logger.info("Configurando APISIX...")
            apisix_config = await self.configure_apisix_routes()
            results['apisix_configuration'] = apisix_config
            
            # 6. Activar proxy fallback si APISIX no funciona
            if not apisix_config.get('success', False):
                logger.info("APISIX no disponible, activando proxy fallback...")
                fallback_results = await self.activate_fallback_proxy()
                results['fallback_proxy'] = fallback_results
            
            # 7. Calcular score final
            logger.info("Calculando score de infraestructura...")
            infrastructure_score = await self.calculate_infrastructure_score(results)
            results['infrastructure_score'] = infrastructure_score
            
            # 8. Generar reporte
            await self.save_infrastructure_report(results)
            
            results['status'] = 'QUANTUM_INFRASTRUCTURE_ACTIVE'
            results['uptime_seconds'] = time.time() - self.start_time
            results['performance_metrics'] = self.performance_metrics
            
            logger.info("Infraestructura cuántica activada exitosamente")
            logger.info(f"Score de infraestructura: {infrastructure_score.get('total_score', 0)}/100")
            
            return results
            
        except Exception as e:
            logger.error(f"Error activando infraestructura: {e}")
            results['status'] = 'ERROR'
            results['error'] = str(e)
            return results
    
    async def verify_docker_available(self) -> Dict[str, Any]:
        """Verificar que Docker esté disponible"""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=10)
            docker_available = result.returncode == 0
            
            if docker_available:
                # Verificar Docker Compose
                compose_result = subprocess.run(['docker', 'compose', '--version'], capture_output=True, text=True, timeout=10)
                compose_available = compose_result.returncode == 0
            else:
                compose_available = False
            
            return {
                'available': docker_available,
                'compose_available': compose_available,
                'version': result.stdout.strip() if docker_available else None
            }
        except Exception as e:
            logger.error(f"Error verificando Docker: {e}")
            return {'available': False, 'error': str(e)}
    
    async def start_docker_infrastructure(self) -> Dict[str, Any]:
        """Iniciar infraestructura Docker"""
        try:
            # Cambiar al directorio de infraestructura
            original_cwd = Path.cwd()
            
            if not self.docker_compose_path.exists():
                return {'success': False, 'error': f'Path no existe: {self.docker_compose_path}'}
            
            # Parar servicios existentes
            logger.info("Parando servicios existentes...")
            subprocess.run([
                'docker', 'compose', 'down'
            ], cwd=self.docker_compose_path, capture_output=True)
            
            # Iniciar servicios
            logger.info("Iniciando servicios Docker...")
            result = subprocess.run([
                'docker', 'compose', 'up', '-d', '--build'
            ], cwd=self.docker_compose_path, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("Servicios Docker iniciados exitosamente")
                
                # Contar contenedores activos
                containers_result = subprocess.run([
                    'docker', 'ps', '--format', '{{.Names}}'
                ], capture_output=True, text=True)
                
                if containers_result.returncode == 0:
                    containers = [c for c in containers_result.stdout.strip().split('\n') if c and 'quantum' in c]
                    self.performance_metrics['total_containers'] = len(containers)
                    self.performance_metrics['docker_services_started'] = len(containers)
                
                return {
                    'success': True, 
                    'containers_started': self.performance_metrics['total_containers'],
                    'output': result.stdout
                }
            else:
                logger.error(f"Error iniciando Docker: {result.stderr}")
                return {
                    'success': False, 
                    'error': result.stderr,
                    'output': result.stdout
                }
                
        except Exception as e:
            logger.error(f"Error en start_docker_infrastructure: {e}")
            return {'success': False, 'error': str(e)}
    
    async def verify_services_health(self) -> Dict[str, Any]:
        """Verificar salud de servicios"""
        services_status = {}
        healthy_services = 0
        
        for port, service_info in self.critical_services.items():
            service_name = service_info['name']
            is_healthy = await self.check_port_active(port)
            
            services_status[service_name] = {
                'port': port,
                'healthy': is_healthy,
                'essential': service_info['essential'],
                'url': self.infrastructure_urls.get(service_name, f'http://127.0.0.1:{port}')
            }
            
            if is_healthy:
                healthy_services += 1
                logger.info(f"Servicio saludable: {service_name} en puerto {port}")
            else:
                logger.warning(f"Servicio no disponible: {service_name} en puerto {port}")
        
        self.performance_metrics['services_health_checked'] = len(services_status)
        
        return {
            'services': services_status,
            'healthy_count': healthy_services,
            'total_count': len(services_status),
            'health_percentage': (healthy_services / len(services_status)) * 100
        }
    
    async def configure_apisix_routes(self) -> Dict[str, Any]:
        """Configurar rutas APISIX para servicios cuánticos"""
        
        if not await self.check_port_active(9180):
            return {'success': False, 'error': 'APISIX Admin API no disponible'}
        
        try:
            admin_headers = {"X-API-KEY": "edd1c9f034335f136f87ad84b625c8f1", "Content-Type": "application/json"}
            routes_configured = []
            
            # Configurar rutas para servicios cuánticos
            quantum_routes = [
                {
                    'id': 'quantum-api-route',
                    'name': 'Quantum API Server',
                    'uri': '/api/quantum/*',
                    'upstream_url': '127.0.0.1:3000'
                },
                {
                    'id': 'quantum-coding-route', 
                    'name': 'Quantum Coding API',
                    'uri': '/api/generate-code/*',
                    'upstream_url': '127.0.0.1:8000'
                },
                {
                    'id': 'quantum-dashboard-route',
                    'name': 'Quantum Dashboard',
                    'uri': '/dashboard/*',
                    'upstream_url': '127.0.0.1:8080'
                }
            ]
            
            for route_config in quantum_routes:
                # Crear upstream
                upstream_config = {
                    "type": "roundrobin",
                    "nodes": {route_config['upstream_url']: 1},
                    "timeout": {"connect": 60, "send": 60, "read": 60}
                }
                
                upstream_response = requests.put(
                    f"http://127.0.0.1:9180/apisix/admin/upstreams/{route_config['id']}-upstream",
                    headers=admin_headers,
                    json=upstream_config,
                    timeout=30
                )
                
                # Crear ruta
                route_data = {
                    "name": route_config['name'],
                    "uri": route_config['uri'],
                    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                    "upstream_id": f"{route_config['id']}-upstream",
                    "plugins": {
                        "cors": {
                            "allow_origins": "**",
                            "allow_methods": "**", 
                            "allow_headers": "**"
                        }
                    },
                    "labels": {
                        "quantum_frequency": "888",
                        "vigoleonrocks": "true"
                    }
                }
                
                route_response = requests.put(
                    f"http://127.0.0.1:9180/apisix/admin/routes/{route_config['id']}",
                    headers=admin_headers,
                    json=route_data,
                    timeout=30
                )
                
                if route_response.status_code in [200, 201]:
                    routes_configured.append(route_config['id'])
                    logger.info(f"Ruta APISIX configurada: {route_config['name']}")
                else:
                    logger.error(f"Error configurando ruta {route_config['id']}: {route_response.status_code}")
            
            self.performance_metrics['routes_configured'] = len(routes_configured)
            
            return {
                'success': len(routes_configured) > 0,
                'routes_configured': routes_configured,
                'total_routes': len(quantum_routes)
            }
            
        except Exception as e:
            logger.error(f"Error configurando APISIX: {e}")
            return {'success': False, 'error': str(e)}
    
    async def activate_fallback_proxy(self) -> Dict[str, Any]:
        """Activar proxy fallback si APISIX no está disponible"""
        
        if await self.check_port_active(9079):
            logger.info("Proxy fallback ya está activo")
            self.fallback_proxy_active = True
            return {'already_active': True, 'port': 9079}
        
        try:
            # Iniciar proxy fallback
            process = subprocess.Popen([
                'python', 'qbtc_fallback_proxy.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar y verificar
            await asyncio.sleep(5)
            
            if await self.check_port_active(9079):
                self.fallback_proxy_active = True
                
                # Configurar rutas en proxy fallback
                routes_added = await self.configure_fallback_routes()
                
                return {
                    'started': True,
                    'port': 9079,
                    'routes_configured': routes_added
                }
            else:
                return {'started': False, 'error': 'No se pudo iniciar en puerto 9079'}
                
        except Exception as e:
            logger.error(f"Error activando proxy fallback: {e}")
            return {'started': False, 'error': str(e)}
    
    async def configure_fallback_routes(self) -> int:
        """Configurar rutas en proxy fallback"""
        routes_added = 0
        
        quantum_services = [
            {'name': 'quantum-api', 'path': '/api/quantum', 'url': 'http://127.0.0.1:3000'},
            {'name': 'quantum-coding', 'path': '/api/generate-code', 'url': 'http://127.0.0.1:8000'},
            {'name': 'quantum-dashboard', 'path': '/dashboard', 'url': 'http://127.0.0.1:8080'}
        ]
        
        for service in quantum_services:
            try:
                response = requests.post(
                    'http://127.0.0.1:9079/routes/add',
                    json={
                        'path': service['path'],
                        'upstream': service['url'],
                        'service_type': 'quantum_service'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    routes_added += 1
                    logger.info(f"Ruta fallback configurada: {service['name']}")
                    
            except Exception as e:
                logger.error(f"Error configurando ruta fallback {service['name']}: {e}")
        
        return routes_added
    
    async def check_port_active(self, port: int) -> bool:
        """Verificar si un puerto está activo"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    async def calculate_infrastructure_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calcular score de infraestructura"""
        
        score_components = {}
        total_score = 0
        
        # Componente 1: Docker Services (25 puntos)
        containers_started = self.performance_metrics.get('docker_services_started', 0)
        docker_score = min(25, containers_started * 3)  # 3 puntos por servicio Docker
        score_components['docker_services'] = docker_score
        total_score += docker_score
        
        # Componente 2: Services Health (30 puntos)  
        services_status = results.get('services_status', {})
        health_percentage = services_status.get('health_percentage', 0)
        health_score = (health_percentage / 100) * 30
        score_components['services_health'] = round(health_score, 1)
        total_score += health_score
        
        # Componente 3: Gateway Configuration (25 puntos)
        apisix_config = results.get('apisix_configuration', {})
        fallback_proxy = results.get('fallback_proxy', {})
        
        if apisix_config.get('success', False):
            gateway_score = 25
        elif fallback_proxy.get('started', False):
            gateway_score = 20
        else:
            gateway_score = 0
            
        score_components['gateway'] = gateway_score
        total_score += gateway_score
        
        # Componente 4: Routes Configured (20 puntos)
        routes_count = self.performance_metrics.get('routes_configured', 0)
        routes_score = min(20, routes_count * 7)  # 7 puntos por ruta
        score_components['routes'] = routes_score
        total_score += routes_score
        
        self.performance_metrics['infrastructure_score'] = round(total_score, 1)
        
        return {
            'total_score': round(total_score, 1),
            'components': score_components,
            'grade': 'A' if total_score >= 90 else 'B' if total_score >= 80 else 'C' if total_score >= 70 else 'D'
        }
    
    async def save_infrastructure_report(self, results: Dict[str, Any]) -> str:
        """Guardar reporte de infraestructura"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'qbtc_quantum_infrastructure_report_{timestamp}.json'
        
        enhanced_results = {
            **results,
            'report_metadata': {
                'generated_by': 'QBTC_QUANTUM_INFRASTRUCTURE_ACTIVATOR',
                'version': 'quantum_docker_v1.0',
                'frequency': 888,
                'system': 'VIGOLEONROCKS',
                'report_timestamp': timestamp,
                'total_execution_time': time.time() - self.start_time,
                'docker_infrastructure': True
            }
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(enhanced_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte de infraestructura guardado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            return ""

async def main():
    """Función principal para activar infraestructura cuántica"""
    logger.info("Iniciando QBTC Quantum Infrastructure Activator...")
    
    activator = QbtcQuantumInfrastructureActivator()
    results = await activator.activate_quantum_infrastructure()
    
    logger.info("================== RESUMEN INFRAESTRUCTURA ==================")
    logger.info(f"Estado: {results.get('status')}")
    logger.info(f"Score: {results.get('infrastructure_score', {}).get('total_score', 0)}/100")
    logger.info(f"Contenedores: {activator.performance_metrics.get('total_containers', 0)}")
    logger.info(f"Servicios saludables: {results.get('services_status', {}).get('healthy_count', 0)}")
    logger.info(f"Rutas configuradas: {activator.performance_metrics.get('routes_configured', 0)}")
    logger.info(f"Tiempo: {results.get('uptime_seconds', 0):.2f}s")
    logger.info("============================================================")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())