#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Dokploy API Deployment Script
Script para deploy automático usando la API de Dokploy
"""

import os
import json
import requests
import time
from typing import Dict, Any, Optional
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DokployDeployer:
    def __init__(self, server_url: str, api_token: str):
        self.server_url = server_url.rstrip('/')
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Hace una petición a la API de Dokploy"""
        url = f"{self.server_url}/api{endpoint}"

        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url)
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición API: {e}")
            raise

    def list_projects(self) -> Dict:
        """Lista todos los proyectos"""
        return self._make_request('GET', '/projects')

    def create_project(self, name: str, description: str = "") -> Dict:
        """Crea un nuevo proyecto"""
        data = {
            'name': name,
            'description': description
        }
        return self._make_request('POST', '/projects', data)

    def get_project(self, project_id: str) -> Dict:
        """Obtiene información de un proyecto"""
        return self._make_request('GET', f'/projects/{project_id}')

    def create_service(self, project_id: str, service_data: Dict) -> Dict:
        """Crea un nuevo servicio en un proyecto"""
        return self._make_request('POST', f'/projects/{project_id}/services', service_data)

    def deploy_service(self, project_id: str, service_id: str, image: str, env_vars: Dict = None) -> Dict:
        """Despliega un servicio"""
        data = {
            'image': image,
            'environment': env_vars or {}
        }
        return self._make_request('POST', f'/projects/{project_id}/services/{service_id}/deploy', data)

    def get_service_status(self, project_id: str, service_id: str) -> Dict:
        """Obtiene el estado de un servicio"""
        return self._make_request('GET', f'/projects/{project_id}/services/{service_id}/status')

    def create_database(self, project_id: str, db_config: Dict) -> Dict:
        """Crea una base de datos"""
        return self._make_request('POST', f'/projects/{project_id}/databases', db_config)

    def setup_vigoleonrocks_project(self) -> Dict:
        """Configura el proyecto completo de VIGOLEONROCKS"""
        logger.info("🚀 Iniciando configuración de VIGOLEONROCKS en Dokploy...")

        # 1. Crear proyecto
        project_data = self.create_project(
            name='vigoleonrocks',
            description='Sistema de IA Cuántica VIGOLEONROCKS - Quantum NLP Service'
        )
        project_id = project_data['id']
        logger.info(f"✅ Proyecto creado: {project_id}")

        # 2. Crear base de datos PostgreSQL
        postgres_config = {
            'type': 'postgresql',
            'name': 'vigoleonrocks-postgres',
            'version': '15',
            'environment': {
                'POSTGRES_DB': 'vigoleonrocks',
                'POSTGRES_USER': 'vigoleonrocks',
                'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD', 'quantum2024')
            }
        }
        postgres_data = self.create_database(project_id, postgres_config)
        logger.info(f"✅ Base de datos PostgreSQL creada: {postgres_data['id']}")

        # 3. Crear servicio Redis
        redis_config = {
            'name': 'vigoleonrocks-redis',
            'image': 'redis:7-alpine',
            'ports': [{'published': 6379, 'target': 6379}],
            'environment': {}
        }
        redis_data = self.create_service(project_id, redis_config)
        logger.info(f"✅ Servicio Redis creado: {redis_data['id']}")

        # 4. Crear servicio principal
        app_config = {
            'name': 'vigoleonrocks-app',
            'image': 'ghcr.io/vigoferrel/quantum-nlp-service:latest',
            'ports': [{'published': 5000, 'target': 5000}],
            'environment': {
                'FLASK_ENV': 'production',
                'DATABASE_URL': f"postgresql://vigoleonrocks:{os.getenv('POSTGRES_PASSWORD', 'quantum2024')}@vigoleonrocks-postgres:5432/vigoleonrocks",
                'REDIS_URL': 'redis://vigoleonrocks-redis:6379',
                'SECRET_KEY': os.getenv('SECRET_KEY', 'generate-random-key'),
                'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY', '')
            },
            'healthcheck': {
                'test': ['CMD', 'curl', '-f', 'http://localhost:5000/api/status'],
                'interval': '30s',
                'timeout': '10s',
                'retries': 3
            }
        }
        app_data = self.create_service(project_id, app_config)
        logger.info(f"✅ Servicio principal creado: {app_data['id']}")

        # 5. Crear servicio Nginx
        nginx_config = {
            'name': 'vigoleonrocks-nginx',
            'image': 'nginx:alpine',
            'ports': [
                {'published': 80, 'target': 80},
                {'published': 443, 'target': 443}
            ],
            'volumes': [{
                'type': 'bind',
                'source': './nginx.conf',
                'target': '/etc/nginx/nginx.conf'
            }]
        }
        nginx_data = self.create_service(project_id, nginx_config)
        logger.info(f"✅ Servicio Nginx creado: {nginx_data['id']}")

        return {
            'project_id': project_id,
            'services': {
                'postgres': postgres_data['id'],
                'redis': redis_data['id'],
                'app': app_data['id'],
                'nginx': nginx_data['id']
            }
        }

    def deploy_all_services(self, project_id: str, services: Dict) -> Dict:
        """Despliega todos los servicios"""
        logger.info("🚀 Iniciando deployment de servicios...")

        results = {}

        # Deploy Redis
        results['redis'] = self.deploy_service(
            project_id,
            services['redis'],
            'redis:7-alpine'
        )
        logger.info("✅ Redis desplegado")

        # Deploy PostgreSQL
        results['postgres'] = self.deploy_service(
            project_id,
            services['postgres'],
            'postgres:15-alpine'
        )
        logger.info("✅ PostgreSQL desplegado")

        # Esperar a que las bases de datos estén listas
        logger.info("⏳ Esperando a que las bases de datos estén listas...")
        time.sleep(30)

        # Deploy aplicación principal
        results['app'] = self.deploy_service(
            project_id,
            services['app'],
            'ghcr.io/vigoferrel/quantum-nlp-service:latest',
            {
                'FLASK_ENV': 'production',
                'DATABASE_URL': f"postgresql://vigoleonrocks:{os.getenv('POSTGRES_PASSWORD', 'quantum2024')}@vigoleonrocks-postgres:5432/vigoleonrocks",
                'REDIS_URL': 'redis://vigoleonrocks-redis:6379',
                'SECRET_KEY': os.getenv('SECRET_KEY', 'generate-random-key'),
                'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY', '')
            }
        )
        logger.info("✅ Aplicación principal desplegada")

        # Deploy Nginx
        results['nginx'] = self.deploy_service(
            project_id,
            services['nginx'],
            'nginx:alpine'
        )
        logger.info("✅ Nginx desplegado")

        return results

    def wait_for_healthy(self, project_id: str, services: Dict, timeout: int = 300) -> bool:
        """Espera a que todos los servicios estén saludables"""
        logger.info("🏥 Verificando health checks...")

        start_time = time.time()
        healthy_services = set()

        while time.time() - start_time < timeout:
            all_healthy = True

            for service_name, service_id in services.items():
                try:
                    status = self.get_service_status(project_id, service_id)
                    if status.get('status') == 'healthy':
                        if service_name not in healthy_services:
                            logger.info(f"✅ {service_name} está saludable")
                            healthy_services.add(service_name)
                    else:
                        all_healthy = False
                except Exception as e:
                    logger.warning(f"⚠️  {service_name} aún no está listo: {e}")
                    all_healthy = False

            if all_healthy and len(healthy_services) == len(services):
                logger.info("🎉 Todos los servicios están saludables!")
                return True

            time.sleep(10)

        logger.error("❌ Timeout esperando que los servicios estén saludables")
        return False


def main():
    """Función principal"""
    # Configuración desde variables de entorno
    server_url = os.getenv('DOKPLOY_SERVER_URL', 'http://localhost:3000')
    api_token = os.getenv('DOKPLOY_API_TOKEN')

    if not api_token:
        logger.error("❌ DOKPLOY_API_TOKEN no está configurado")
        return 1

    # Inicializar deployer
    deployer = DokployDeployer(server_url, api_token)

    try:
        # Configurar proyecto
        project_info = deployer.setup_vigoleonrocks_project()

        # Desplegar servicios
        deploy_results = deployer.deploy_all_services(
            project_info['project_id'],
            project_info['services']
        )

        # Esperar a que estén saludables
        if deployer.wait_for_healthy(project_info['project_id'], project_info['services']):
            logger.info("🎉 Deployment completado exitosamente!")
            logger.info(f"📍 Proyecto ID: {project_info['project_id']}")
            return 0
        else:
            logger.error("❌ Deployment falló - servicios no saludables")
            return 1

    except Exception as e:
        logger.error(f"❌ Error durante el deployment: {e}")
        return 1


if __name__ == '__main__':
    exit(main())