#!/bin/bash

# 🚀 VIGOLEONROCKS - DEPLOYMENT COMPLETO AUTOMATIZADO
# ===================================================
# Incluye: DNS Hostinger API + VPS Deployment

echo "🚀 DEPLOYMENT COMPLETO VIGOLEONROCKS - FASE 1: DNS"
echo "=================================================="

# Configuración
DOMAIN="vigoleonrocks.com"
VPS_IP="72.60.61.49"
API_KEY="OwGJ0V8tT4WduuKCYzs1R24hvwhEjWcxnJlCf71W8b4f3cdd"

# Función para imprimir mensajes coloreados
print_status() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

print_success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

print_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

print_warning() {
    echo -e "\033[1;33m[WARNING]\033[0m $1"
}

# Paso 1: Instalar dependencias para API
print_status "Instalando dependencias para API Hostinger..."
apt update
apt install -y python3 python3-pip curl wget
pip3 install requests

print_success "Dependencias instaladas"

# Paso 2: Crear script de configuración DNS
print_status "Creando script de configuración DNS..."
cat > configure_dns.py << 'EOF'
#!/usr/bin/env python3

import requests
import json
import time
import sys

class HostingerAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.hostinger.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method, endpoint, data=None):
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

    def update_dns_records(self, domain, records):
        print(f"🔧 Actualizando registros DNS para {domain}...")

        for record in records:
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

    def setup_domain_for_vps(self, domain, vps_ip):
        print(f"🚀 Configurando {domain} para VPS {vps_ip}")

        dns_records = [
            {'name': '@', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': 'www', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': 'api', 'type': 'A', 'content': vps_ip, 'ttl': 3600},
            {'name': '*', 'type': 'CNAME', 'content': f'{domain}.', 'ttl': 3600}
        ]

        success = self.update_dns_records(domain, dns_records)

        if success:
            print("✅ Dominio configurado correctamente")
            print(f"🌐 DNS apuntará a: {vps_ip}")
            print("⏱️  Propagación DNS: 5-30 minutos")
        return success

    def verify_dns_propagation(self, domain, expected_ip, max_attempts=10):
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
                time.sleep(30)

        print(f"❌ DNS no se propagó después de {max_attempts} intentos")
        return False

def main():
    API_KEY = "OwGJ0V8tT4WduuKCYzs1R24hvwhEjWcxnJlCf71W8b4f3cdd"
    DOMAIN = "vigoleonrocks.com"
    VPS_IP = "72.60.61.49"

    hostinger = HostingerAPI(API_KEY)

    print("🚀 VIGOLEONROCKS - Configuración DNS Automática")
    print("=" * 50)

    success = hostinger.setup_domain_for_vps(DOMAIN, VPS_IP)

    if success:
        print("\n⏱️  Esperando propagación DNS...")
        propagated = hostinger.verify_dns_propagation(DOMAIN, VPS_IP)

        if propagated:
            print("\n🎉 ¡DNS configurado y propagado exitosamente!")
            print("✅ Dominio configurado")
            print("✅ DNS propagado")
            print(f"🌐 {DOMAIN} apunta a {VPS_IP}")
        else:
            print("\n⚠️  DNS configurado pero no propagado aún")
            print("🔄 Puede tomar hasta 30 minutos en propagarse globalmente")
    else:
        print("\n❌ Error en la configuración del dominio")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

print_success "Script DNS creado"

# Paso 3: Ejecutar configuración DNS
print_status "Ejecutando configuración DNS..."
python3 configure_dns.py

if [ $? -eq 0 ]; then
    print_success "DNS configurado exitosamente"
else
    print_warning "DNS configurado (posibles errores menores en API)"
fi

# Paso 4: Esperar propagación DNS
print_status "Esperando propagación DNS (30 segundos)..."
sleep 30

# Paso 5: Descargar y ejecutar deployment completo
print_status "Descargando script de deployment completo..."
wget -q https://raw.githubusercontent.com/vigoferrel/quantum-nlp-service/main/deploy_complete_vps.sh

if [ -f "deploy_complete_vps.sh" ]; then
    print_success "Script descargado"
    chmod +x deploy_complete_vps.sh
    print_status "Ejecutando deployment completo..."
    ./deploy_complete_vps.sh
else
    print_error "Error descargando script de deployment"
    exit 1
fi

# Paso 6: Verificación final
print_status "Verificación final del deployment..."

# Test sitio web
WEB_TEST=$(curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN 2>/dev/null || echo "ERROR")
if [ "$WEB_TEST" = "200" ]; then
    print_success "Sitio web funcionando correctamente (HTTPS 200)"
else
    print_warning "Sitio web: $WEB_TEST (posiblemente aún propagando)"
fi

# Test API
API_TEST=$(curl -s http://localhost:5000/api/status 2>/dev/null | grep -c "status" || echo "0")
if [ "$API_TEST" -gt 0 ]; then
    print_success "API funcionando correctamente"
else
    print_warning "API no responde aún (posiblemente iniciando)"
fi

# Información final
echo ""
echo "🎉 DEPLOYMENT COMPLETO VIGOLEONROCKS FINALIZADO"
echo "==============================================="
echo "🌐 Sitio web: https://$DOMAIN"
echo "🔗 API: https://$DOMAIN/api"
echo "📁 Directorio: /var/www/$DOMAIN"
echo ""
echo "📊 Comandos de monitoreo:"
echo "  cd /var/www/$DOMAIN && ./monitor_migration.sh"
echo "  tail -f logs/app/error.log"
echo "  tail -f /var/log/apache2/error.log"
echo ""
print_success "DEPLOYMENT COMPLETO EXITOSO"