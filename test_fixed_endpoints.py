#!/usr/bin/env python3
"""
🧪 Test de Endpoints Reparados - VIGOLEONROCKS
Verificar que los endpoints principales están funcionando
"""

import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor

def test_endpoint(endpoint, expected_status=200, timeout=5):
    """Probar un endpoint específico"""
    try:
        url = f"http://localhost:5000{endpoint}"
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = (time.time() - start_time) * 1000
        
        status_emoji = "✅" if response.status_code == expected_status else "❌"
        
        return {
            'endpoint': endpoint,
            'status_code': response.status_code,
            'expected_status': expected_status,
            'success': response.status_code == expected_status,
            'response_time': response_time,
            'emoji': status_emoji,
            'content_length': len(response.content) if response.content else 0
        }
    
    except requests.exceptions.RequestException as e:
        return {
            'endpoint': endpoint,
            'status_code': 'ERROR',
            'expected_status': expected_status,
            'success': False,
            'response_time': 0,
            'emoji': '💥',
            'error': str(e),
            'content_length': 0
        }

def main():
    """Ejecutar pruebas de endpoints"""
    
    print("🧪 TESTING VIGOLEONROCKS ENDPOINTS REPARADOS")
    print("=" * 60)
    
    # Definir endpoints críticos que deben funcionar
    critical_endpoints = [
        ('/', 200, 'Página Principal'),
        ('/dashboard', 200, 'Dashboard'),
        ('/corporate', 200, 'Página Corporate'),
        ('/ui', 200, 'Interfaz Chat'),
        ('/api/status', 200, 'API Status (v1)'),
        ('/api/quantum-metrics', 200, 'Quantum Metrics'),
        ('/api/v2/docs', 200, 'API v2 Documentation'),
        ('/api/v2/openapi.json', 200, 'OpenAPI Spec'),
        ('/api/v2/system/health', 200, 'System Health'),
        ('/api/v2/system/models', 200, 'Models List'),
        ('/api/v2/metrics', 200, 'System Metrics'),
        ('/api/v2/cache/stats', 200, 'Cache Stats'),
        ('/api/v2/multimodal/status', 200, 'Multimodal Status'),
        ('/api/v2/performance/report', 200, 'Performance Report')
    ]
    
    # Ejecutar pruebas en paralelo para eficiencia
    print("🚀 Ejecutando pruebas en paralelo...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for endpoint, expected_status, description in critical_endpoints:
            future = executor.submit(test_endpoint, endpoint, expected_status)
            futures.append((future, description))
        
        # Recopilar resultados
        results = []
        for future, description in futures:
            result = future.result()
            result['description'] = description
            results.append(result)
    
    # Mostrar resultados
    print("\n📊 RESULTADOS DE PRUEBAS:")
    print("=" * 60)
    
    working_endpoints = []
    failing_endpoints = []
    
    for result in sorted(results, key=lambda x: x['endpoint']):
        endpoint = result['endpoint']
        status = result['status_code']
        emoji = result['emoji']
        response_time = result.get('response_time', 0)
        description = result['description']
        
        print(f"{emoji} {endpoint:<35} {status} - {description}")
        if result.get('response_time'):
            print(f"   └─ Tiempo: {response_time:.1f}ms, Tamaño: {result['content_length']} bytes")
        
        if result['success']:
            working_endpoints.append(result)
        else:
            failing_endpoints.append(result)
            if 'error' in result:
                print(f"   └─ Error: {result['error']}")
    
    # Resumen final
    total = len(results)
    working = len(working_endpoints)
    failing = len(failing_endpoints)
    
    print("\n" + "=" * 60)
    print("📈 RESUMEN FINAL")
    print("=" * 60)
    print(f"✅ Endpoints funcionando: {working}/{total} ({working/total*100:.1f}%)")
    print(f"❌ Endpoints con fallas: {failing}/{total} ({failing/total*100:.1f}%)")
    
    if working_endpoints:
        avg_response_time = sum(r.get('response_time', 0) for r in working_endpoints) / len(working_endpoints)
        print(f"⚡ Tiempo promedio de respuesta: {avg_response_time:.1f}ms")
    
    if failing > 0:
        print(f"\n🔴 ENDPOINTS CON PROBLEMAS:")
        for result in failing_endpoints:
            print(f"  ❌ {result['endpoint']} - Status: {result['status_code']}")
            if 'error' in result:
                print(f"     Error: {result['error']}")
    
    # Determinar estado general
    if failing == 0:
        print(f"\n🎉 ¡ÉXITO TOTAL! Todos los endpoints están funcionando.")
        return 0
    elif failing <= 2:
        print(f"\n🟡 ESTADO BUENO: Solo {failing} endpoints con problemas.")
        return 0
    elif failing <= 5:
        print(f"\n🟠 ESTADO REGULAR: {failing} endpoints necesitan atención.")
        return 1
    else:
        print(f"\n🔴 ESTADO CRÍTICO: {failing} endpoints fallando.")
        return 2

if __name__ == "__main__":
    print("💡 Nota: Asegúrate de que el servidor esté ejecutándose en localhost:5000")
    print("   Para iniciar: python main.py\n")
    
    try:
        exit_code = main()
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n🛑 Pruebas interrumpidas por el usuario")
        exit(130)
