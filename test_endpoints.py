#!/usr/bin/env python3
"""
🧪 Script de prueba para verificar endpoints del sistema VIGOLEONROCKS
"""

import requests
import json

def test_endpoints():
    """Prueba todos los endpoints principales"""
    print("🧪 TESTING VIGOLEONROCKS ENDPOINTS")
    print("=" * 50)
    
    # Lista de endpoints para probar
    endpoints = [
        # Endpoints básicos
        ('/', 'GET', 'Página Principal'),
        ('/api/status', 'GET', 'API Status'),
        ('/dashboard', 'GET', 'Dashboard'),
        ('/corporate', 'GET', 'Corporate Page'),
        ('/ui', 'GET', 'Chat Interface'),
        
        # APIs v1
        ('/api/quantum-metrics', 'GET', 'Quantum Metrics'),
        ('/api/multimodal/status', 'GET', 'Multimodal Status'),
        ('/api/performance/report', 'GET', 'Performance Report'),
        
        # APIs v2 nuevas
        ('/api/v2/docs', 'GET', 'API Documentation'),
        ('/api/v2/metrics', 'GET', 'Enhanced Metrics'),
        ('/api/v2/system/health', 'GET', 'System Health'),
        ('/api/v2/system/models', 'GET', 'Models List'),
        ('/api/v2/cache/stats', 'GET', 'Cache Stats'),
    ]
    
    results = []
    
    for endpoint, method, description in endpoints:
        try:
            url = f'http://localhost:5000{endpoint}'
            response = requests.get(url, timeout=5)
            
            status_emoji = "✅" if response.status_code == 200 else "⚠️" if response.status_code < 500 else "❌"
            
            result = {
                'endpoint': endpoint,
                'status': response.status_code,
                'description': description,
                'working': response.status_code == 200
            }
            results.append(result)
            
            print(f"{status_emoji} {endpoint:<30} {response.status_code} - {description}")
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint:<30} CONNECTION_ERROR - Server not running?")
            results.append({
                'endpoint': endpoint,
                'status': 'CONNECTION_ERROR',
                'description': description,
                'working': False
            })
        except Exception as e:
            print(f"❌ {endpoint:<30} ERROR - {str(e)[:30]}")
            results.append({
                'endpoint': endpoint,
                'status': 'ERROR',
                'description': description,
                'working': False
            })
    
    # Resumen
    working_endpoints = [r for r in results if r['working']]
    total_endpoints = len(results)
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    print(f"✅ Endpoints funcionando: {len(working_endpoints)}/{total_endpoints}")
    print(f"❌ Endpoints con problemas: {total_endpoints - len(working_endpoints)}")
    
    if working_endpoints:
        print("\n🟢 ENDPOINTS FUNCIONANDO:")
        for result in working_endpoints:
            print(f"  ✅ {result['endpoint']} - {result['description']}")
    
    broken_endpoints = [r for r in results if not r['working']]
    if broken_endpoints:
        print("\n🔴 ENDPOINTS CON PROBLEMAS:")
        for result in broken_endpoints:
            print(f"  ❌ {result['endpoint']} - {result['description']} (Status: {result['status']})")
    
    # Probar una respuesta JSON si está disponible
    try:
        response = requests.get('http://localhost:5000/api/status', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📋 EJEMPLO DE RESPUESTA (/api/status):")
            print(f"  Status: {data.get('status', 'N/A')}")
            print(f"  Version: {data.get('version', 'N/A')}")
            print(f"  Uptime: {data.get('uptime_seconds', 0):.1f}s")
            print(f"  Requests: {data.get('requests_served', 'N/A')}")
    except:
        pass
    
    return results

if __name__ == "__main__":
    test_endpoints()
