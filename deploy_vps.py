#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Deployment Script para VPS Específico
Configurado para: srv984842.hstgr.cloud (72.60.61.49)
"""

import os
import json
import requests
import time
from typing import Dict, Any, Optional
import logging

# Configuración del VPS específico
VPS_CONFIG = {
    'hostname': 'srv984842.hstgr.cloud',
    'ip': '72.60.61.49',
    'ipv6': '2a02:4780:66:bfe::1',
    'dokploy_url': 'http://72.60.61.49:3000',
    'domain': 'vigoleonrocks.com'  # Cambia esto por tu dominio real
}

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VPSDeployer:
    def __init__(self, dokploy_url: str, api_token: str):
        self.dokploy_url = dokploy_url.rstrip('/')
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def test_connection(self) -> bool:
        """Prueba la conexión con Dokploy"""
        try:
            response = self.session.get(f"{self.dokploy_url}/api/health")
            if response.status_code == 200:
                logger.info("✅ Conexión con Dokploy exitosa")
                return True
            else:
                logger.error(f"❌ Error de conexión: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Error conectando con Dokploy: {e}")
            return False

    def create_vigoleonrocks_project(self) -> Dict:
        """Crea el proyecto VIGOLEONROCKS en Dokploy"""
        logger.info("🚀 Creando proyecto VIGOLEONROCKS...")

        project_config = {
            'name': 'vigoleonrocks',
            'description': 'Sistema de IA Cuántica VIGOLEONROCKS - Quantum NLP Service',
            'repository': 'https://github.com/vigoferrel/quantum-nlp-service',
            'branch': 'main',
            'autoDeploy': True
        }

        try:
            response = self.session.post(
                f"{self.dokploy_url}/api/projects",
                json=project_config
            )
            response.raise_for_status()
            project_data = response.json()

            logger.info(f"✅ Proyecto creado: {project_data['id']}")
            return project_data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error creando proyecto: {e}")
            raise

    def configure_services(self, project_id: str) -> Dict:
        """Configura todos los servicios necesarios"""
        logger.info("⚙️ Configurando servicios...")

        services_config = {
            'database': {
                'type': 'postgres',
                'name': 'vigoleonrocks-postgres',
                'version': '15',
                'port': 5432,
                'environment': {
                    'POSTGRES_DB': 'vigoleonrocks',
                    'POSTGRES_USER': 'vigoleonrocks',
                    'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD', 'quantum2024')
                }
            },
            'cache': {
                'type': 'redis',
                'name': 'vigoleonrocks-redis',
                'version': '7',
                'port': 6379
            },
            'app': {
                'type': 'docker',
                'name': 'vigoleonrocks-app',
                'image': 'ghcr.io/vigoferrel/quantum-nlp-service:latest',
                'port': 5000,
                'environment': {
                    'FLASK_ENV': 'production',
                    'DATABASE_URL': f"postgresql://vigoleonrocks:{os.getenv('POSTGRES_PASSWORD', 'quantum2024')}@vigoleonrocks-postgres:5432/vigoleonrocks",
                    'REDIS_URL': 'redis://vigoleonrocks-redis:6379',
                    'SECRET_KEY': os.getenv('SECRET_KEY', 'generate-random-key'),
                    'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY', '')
                },
                'healthcheck': {
                    'path': '/api/status',
                    'interval': '30s',
                    'timeout': '10s'
                }
            },
            'proxy': {
                'type': 'nginx',
                'name': 'vigoleonrocks-nginx',
                'ports': [80, 443],
                'ssl': True,
                'domain': VPS_CONFIG['domain']
            }
        }

        services_created = {}

        for service_name, config in services_config.items():
            try:
                response = self.session.post(
                    f"{self.dokploy_url}/api/projects/{project_id}/services",
                    json=config
                )
                response.raise_for_status()
                service_data = response.json()

                services_created[service_name] = service_data['id']
                logger.info(f"✅ Servicio {service_name} creado: {service_data['id']}")

            except Exception as e:
                logger.error(f"❌ Error creando servicio {service_name}: {e}")
                raise

        return services_created

    def deploy_services(self, project_id: str, services: Dict) -> Dict:
        """Despliega todos los servicios"""
        logger.info("🚀 Iniciando deployment de servicios...")

        deployment_results = {}

        # Orden de deployment: database -> cache -> app -> proxy
        deployment_order = ['database', 'cache', 'app', 'proxy']

        for service_name in deployment_order:
            if service_name in services:
                try:
                    service_id = services[service_name]

                    # Para la app, usar la imagen específica
                    if service_name == 'app':
                        deploy_config = {
                            'image': 'ghcr.io/vigoferrel/quantum-nlp-service:latest'
                        }
                    else:
                        deploy_config = {}

                    response = self.session.post(
                        f"{self.dokploy_url}/api/projects/{project_id}/services/{service_id}/deploy",
                        json=deploy_config
                    )
                    response.raise_for_status()

                    deployment_results[service_name] = response.json()
                    logger.info(f"✅ {service_name} desplegado exitosamente")

                    # Esperar entre deployments
                    if service_name in ['database', 'cache']:
                        logger.info("⏳ Esperando a que el servicio esté listo...")
                        time.sleep(30)

                except Exception as e:
                    logger.error(f"❌ Error desplegando {service_name}: {e}")
                    raise

        return deployment_results

    def configure_domain(self, project_id: str, domain: str) -> bool:
        """Configura el dominio personalizado"""
        logger.info(f"🌐 Configurando dominio: {domain}")

        domain_config = {
            'domain': domain,
            'ssl': True,
            'redirect_https': True
        }

        try:
            response = self.session.post(
                f"{self.dokploy_url}/api/projects/{project_id}/domain",
                json=domain_config
            )
            response.raise_for_status()

            logger.info(f"✅ Dominio configurado: https://{domain}")
            return True

        except Exception as e:
            logger.error(f"❌ Error configurando dominio: {e}")
            return False

    def get_deployment_status(self, project_id: str) -> Dict:
        """Obtiene el estado completo del deployment"""
        try:
            response = self.session.get(f"{self.dokploy_url}/api/projects/{project_id}/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"❌ Error obteniendo estado: {e}")
            return {}

    def wait_for_healthy_deployment(self, project_id: str, timeout: int = 600) -> bool:
        """Espera a que todos los servicios estén saludables"""
        logger.info("🏥 Verificando health checks...")

        start_time = time.time()
        last_status = {}

        while time.time() - start_time < timeout:
            try:
                status = self.get_deployment_status(project_id)

                if status != last_status:
                    logger.info("📊 Estado actual:")
                    for service, service_status in status.items():
                        logger.info(f"   {service}: {service_status}")
                    last_status = status

                # Verificar si todos los servicios están healthy
                all_healthy = all(
                    service_status.get('status') == 'healthy'
                    for service_status in status.values()
                )

                if all_healthy:
                    logger.info("🎉 Todos los servicios están saludables!")
                    return True

            except Exception as e:
                logger.warning(f"⚠️ Error verificando estado: {e}")

            time.sleep(15)

        logger.error("❌ Timeout esperando que los servicios estén saludables")
        return False


def main():
    """Función principal de deployment"""
    print("🚀 VIGOLEONROCKS - Deployment para VPS")
    print(f"📍 VPS: {VPS_CONFIG['hostname']} ({VPS_CONFIG['ip']})")
    print(f"🔗 Dokploy: {VPS_CONFIG['dokploy_url']}")
    print("-" * 50)

    # Obtener token de API
    api_token = os.getenv('DOKPLOY_API_TOKEN')
    if not api_token:
        print("❌ Error: DOKPLOY_API_TOKEN no está configurado")
        print("Configura la variable de entorno:")
        print("export DOKPLOY_API_TOKEN='tu-token-aqui'")
        return 1

    # Crear deployer
    deployer = VPSDeployer(VPS_CONFIG['dokploy_url'], api_token)

    # Probar conexión
    if not deployer.test_connection():
        print("❌ No se puede conectar con Dokploy")
        print("Verifica que Dokploy esté ejecutándose en el VPS")
        return 1

    try:
        # Crear proyecto
        print("\n📦 Creando proyecto...")
        project = deployer.create_vigoleonrocks_project()
        project_id = project['id']

        # Configurar servicios
        print("\n⚙️ Configurando servicios...")
        services = deployer.configure_services(project_id)

        # Desplegar servicios
        print("\n🚀 Desplegando servicios...")
        deployments = deployer.deploy_services(project_id, services)

        # Configurar dominio (opcional)
        if VPS_CONFIG['domain'] != 'vigoleonrocks.com':
            print(f"\n🌐 Configurando dominio: {VPS_CONFIG['domain']}")
            deployer.configure_domain(project_id, VPS_CONFIG['domain'])

        # Esperar a que esté saludable
        print("\n🏥 Verificando deployment...")
        if deployer.wait_for_healthy_deployment(project_id):
            print("\n" + "="*50)
            print("🎉 DEPLOYMENT COMPLETADO EXITOSAMENTE!")
            print("="*50)
            print(f"📍 URL de la aplicación: http://{VPS_CONFIG['ip']}")
            print(f"🔗 Dashboard Dokploy: {VPS_CONFIG['dokploy_url']}")
            print(f"📊 API Status: http://{VPS_CONFIG['ip']}/api/status")
            if VPS_CONFIG['domain'] != 'vigoleonrocks.com':
                print(f"🌐 Dominio: https://{VPS_CONFIG['domain']}")
            print("="*50)
            return 0
        else:
            print("❌ Deployment falló - servicios no saludables")
            return 1

    except Exception as e:
        print(f"❌ Error durante el deployment: {e}")
        return 1


if __name__ == '__main__':
    exit(main())