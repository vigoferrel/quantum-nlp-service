#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Integración API Hostinger
Automatización completa de configuración de dominio y DNS
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional

class HostingerAPI:
    """
    Integración completa con API de Hostinger para automatización de deployment
    """

    def __init__(self, api_key: str, base_url: str = "https://api.hostinger.com"):
        """
        Inicializar cliente API de Hostinger

        Args:
            api_key: API Key de Hostinger
            base_url: URL base de la API
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Hacer petición a la API de Hostinger

        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint de la API
            data: Datos para enviar (opcional)

        Returns:
            Respuesta de la API en formato JSON
        """
        url = f"{self.base_url}{endpoint}"

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
            print(f"❌ Error en petición API: {e}")
            return {}

    def get_domains(self) -> List[Dict]:
        """
        Obtener lista de dominios

        Returns:
            Lista de dominios
        """
        print("🔍 Obteniendo lista de dominios...")
        response = self._make_request('GET', '/domains')
        return response.get('domains', [])

    def get_domain_info(self, domain: str) -> Dict:
        """
        Obtener información de un dominio específico

        Args:
            domain: Nombre del dominio

        Returns:
            Información del dominio
        """
        print(f"📋 Obteniendo información del dominio: {domain}")
        response = self._make_request('GET', f'/domains/{domain}')
        return response

    def update_dns_records(self, domain: str, records: List[Dict]) -> bool:
        """
        Actualizar registros DNS de un dominio

        Args:
            domain: Nombre del dominio
            records: Lista de registros DNS

        Returns:
            True si se actualizó correctamente
        """
        print(f"🔧 Actualizando registros DNS para {domain}...")

        # Obtener registros DNS actuales
        current_records = self.get_dns_records(domain)

        # Crear mapa de registros actuales por nombre y tipo
        current_map = {}
        for record in current_records:
            key = f"{record['name']}_{record['type']}"
            current_map[key] = record

        # Actualizar o crear registros
        for record in records:
            key = f"{record['name']}_{record['type']}"

            if key in current_map:
                # Actualizar registro existente
                record_id = current_map[key]['id']
                update_data = {
                    'name': record['name'],
                    'type': record['type'],
                    'content': record['content'],
                    'ttl': record.get('ttl', 3600),
                    'priority': record.get('priority')
                }
                self._make_request('PUT', f'/domains/{domain}/dns/{record_id}', update_data)
                print(f"✅ Actualizado: {record['type']} {record['name']} -> {record['content']}")
            else:
                # Crear nuevo registro
                create_data = {
                    'name': record['name'],
                    'type': record['type'],
                    'content': record['content'],
                    'ttl': record.get('ttl', 3600),
                    'priority': record.get('priority')
                }
                self._make_request('POST', f'/domains/{domain}/dns', create_data)
                print(f"✅ Creado: {record['type']} {record['name']} -> {record['content']}")

        return True

    def get_dns_records(self, domain: str) -> List[Dict]:
        """
        Obtener registros DNS de un dominio

        Args:
            domain: Nombre del dominio

        Returns:
            Lista de registros DNS
        """
        response = self._make_request('GET', f'/domains/{domain}/dns')
        return response.get('records', [])

    def create_subdomain(self, domain: str, subdomain: str, target: str) -> bool:
        """
        Crear subdominio apuntando a una IP

        Args:
            domain: Dominio principal
            subdomain: Subdominio a crear
            target: IP objetivo

        Returns:
            True si se creó correctamente
        """
        print(f"🌐 Creando subdominio: {subdomain}.{domain} -> {target}")

        record = {
            'name': subdomain,
            'type': 'A',
            'content': target,
            'ttl': 3600
        }

        return self.update_dns_records(domain, [record])

    def setup_domain_for_vps(self, domain: str, vps_ip: str) -> bool:
        """
        Configurar dominio completo para VPS

        Args:
            domain: Nombre del dominio
            vps_ip: IP del VPS

        Returns:
            True si se configuró correctamente
        """
        print(f"🚀 Configurando {domain} para VPS {vps_ip}")

        # Registros DNS necesarios
        dns_records = [
            {
                'name': '@',
                'type': 'A',
                'content': vps_ip,
                'ttl': 3600
            },
            {
                'name': 'www',
                'type': 'A',
                'content': vps_ip,
                'ttl': 3600
            },
            {
                'name': 'api',
                'type': 'A',
                'content': vps_ip,
                'ttl': 3600
            },
            {
                'name': '*',
                'type': 'CNAME',
                'content': f'{domain}.',
                'ttl': 3600
            }
        ]

        success = self.update_dns_records(domain, dns_records)

        if success:
            print("✅ Dominio configurado correctamente")
            print(f"🌐 DNS apuntará a: {vps_ip}")
            print("⏱️  Propagación DNS: 5-30 minutos")
        return success

    def verify_dns_propagation(self, domain: str, expected_ip: str, max_attempts: int = 10) -> bool:
        """
        Verificar propagación DNS

        Args:
            domain: Dominio a verificar
            expected_ip: IP esperada
            max_attempts: Máximo número de intentos

        Returns:
            True si DNS se propagó correctamente
        """
        print(f"🔍 Verificando propagación DNS para {domain}...")

        import socket

        for attempt in range(max_attempts):
            try:
                actual_ip = socket.gethostbyname(domain)
                if actual_ip == expected_ip:
                    print(f"✅ DNS propagado correctamente: {domain} -> {actual_ip}")
                    return True
                else:
                    print(f"⏳ Intento {attempt + 1}/{max_attempts}: {domain} -> {actual_ip} (esperado: {expected_ip})")
            except socket.gaierror:
                print(f"⏳ Intento {attempt + 1}/{max_attempts}: DNS no resuelto aún")

            if attempt < max_attempts - 1:
                time.sleep(30)  # Esperar 30 segundos entre intentos

        print(f"❌ DNS no se propagó después de {max_attempts} intentos")
        return False

    def get_ssl_certificates(self, domain: str) -> List[Dict]:
        """
        Obtener certificados SSL para un dominio

        Args:
            domain: Nombre del dominio

        Returns:
            Lista de certificados SSL
        """
        print(f"🔒 Obteniendo certificados SSL para {domain}...")
        response = self._make_request('GET', f'/domains/{domain}/ssl')
        return response.get('certificates', [])

    def request_ssl_certificate(self, domain: str) -> bool:
        """
        Solicitar certificado SSL para un dominio

        Args:
            domain: Nombre del dominio

        Returns:
            True si se solicitó correctamente
        """
        print(f"🔒 Solicitando certificado SSL para {domain}...")

        data = {
            'domain': domain,
            'validation_method': 'http-01'
        }

        response = self._make_request('POST', f'/domains/{domain}/ssl', data)
        return bool(response)

    def get_hosting_accounts(self) -> List[Dict]:
        """
        Obtener cuentas de hosting

        Returns:
            Lista de cuentas de hosting
        """
        print("🏠 Obteniendo cuentas de hosting...")
        response = self._make_request('GET', '/hosting/accounts')
        return response.get('accounts', [])

    def create_database(self, account_id: str, db_name: str, db_user: str, db_password: str) -> bool:
        """
        Crear base de datos en cuenta de hosting

        Args:
            account_id: ID de la cuenta de hosting
            db_name: Nombre de la base de datos
            db_user: Usuario de la base de datos
            db_password: Contraseña del usuario

        Returns:
            True si se creó correctamente
        """
        print(f"🗄️ Creando base de datos: {db_name}")

        data = {
            'name': db_name,
            'user': db_user,
            'password': db_password,
            'type': 'postgresql'
        }

        response = self._make_request('POST', f'/hosting/accounts/{account_id}/databases', data)
        return bool(response)

def main():
    """
    Función principal para demostrar el uso de la API
    """
    print("🚀 VIGOLEONROCKS - Configuración Automática con API Hostinger")
    print("=" * 60)

    # Configuración
    API_KEY = input("🔑 Ingresa tu API Key de Hostinger: ").strip()
    DOMAIN = "vigoleonrocks.com"
    VPS_IP = "72.60.61.49"

    if not API_KEY:
        print("❌ API Key requerida")
        sys.exit(1)

    # Inicializar cliente API
    hostinger = HostingerAPI(API_KEY)

    try:
        # Verificar conexión
        print("🔗 Verificando conexión con API...")
        domains = hostinger.get_domains()
        print(f"✅ Conectado. Dominios encontrados: {len(domains)}")

        # Configurar dominio para VPS
        print(f"\n🚀 Configurando {DOMAIN} para VPS {VPS_IP}...")
        success = hostinger.setup_domain_for_vps(DOMAIN, VPS_IP)

        if success:
            print("\n⏱️  Esperando propagación DNS...")
            propagated = hostinger.verify_dns_propagation(DOMAIN, VPS_IP)

            if propagated:
                print("\n🎉 ¡Configuración completada exitosamente!")
                print("✅ Dominio configurado")
                print("✅ DNS propagado")
                print(f"🌐 {DOMAIN} apunta a {VPS_IP}")
            else:
                print("\n⚠️  DNS no se propagó completamente, pero la configuración está aplicada")
                print("🔄 Puede tomar hasta 30 minutos en propagarse globalmente")
        else:
            print("\n❌ Error en la configuración del dominio")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()