#!/usr/bin/env python3
"""
QBTC Real Infrastructure Benchmark Arena
Pruebas contra la infraestructura Docker que ya está corriendo
"""

import requests
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, Any, List

class QBTCRealGladiator:
    """
    Gladiador que prueba contra la infraestructura REAL que está corriendo
    """
    
    def __init__(self):
        # Puertos REALES detectados en la infraestructura Docker
        self.endpoints = {
            'kong_gateway': 'http://localhost:8000',
            'api_server': 'http://localhost:5001', 
            'aics_service': 'http://localhost:8001',
            'quantum_core': 'http://localhost:8002'
        }
        self.session = requests.Session()
    
    def test_endpoint_connectivity(self, endpoint_name: str, url: str) -> Dict[str, Any]:
        """Probar conectividad básica de un endpoint"""
        start_time = time.time()
        
        try:
            # Probar diferentes endpoints comunes
            test_paths = ['/', '/health', '/status', '/api/health']
            
            for path in test_paths:
                try:
                    full_url = f"{url}{path}"
                    response = self.session.get(full_url, timeout=10)
                    response_time = time.time() - start_time
                    
                    return {
                        "endpoint": endpoint_name,
                        "url": full_url,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "success": True,
                        "response_length": len(response.text),
                        "content_preview": response.text[:200]
                    }
                except requests.exceptions.RequestException:
                    continue
            
            # Si ningún path funciona, reportar error
            return {
                "endpoint": endpoint_name,
                "url": url,
                "status_code": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": "No accessible paths found"
            }
            
        except Exception as e:
            return {
                "endpoint": endpoint_name,
                "url": url,
                "status_code": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }
    
    def test_api_functionality(self, endpoint_name: str, url: str) -> Dict[str, Any]:
        """Probar funcionalidad de API específica"""
        start_time = time.time()
        
        # Test queries específicas según el endpoint
        test_cases = {
            'kong_gateway': {
                'method': 'POST',
                'path': '/',
                'data': {'query': 'Test message for Kong gateway'}
            },
            'api_server': {
                'method': 'GET',
                'path': '/health',
                'data': None
            },
            'aics_service': {
                'method': 'GET', 
                'path': '/health',
                'data': None
            },
            'quantum_core': {
                'method': 'GET',
                'path': '/health',
                'data': None
            }
        }
        
        test_config = test_cases.get(endpoint_name, {'method': 'GET', 'path': '/', 'data': None})
        
        try:
            full_url = f"{url}{test_config['path']}"
            
            if test_config['method'] == 'POST':
                response = self.session.post(
                    full_url, 
                    json=test_config['data'], 
                    timeout=30
                )
            else:
                response = self.session.get(full_url, timeout=30)
            
            response_time = time.time() - start_time
            
            return {
                "endpoint": endpoint_name,
                "url": full_url,
                "method": test_config['method'],
                "status_code": response.status_code,
                "response_time": response_time,
                "success": response.status_code < 400,
                "response_preview": response.text[:500]
            }
            
        except Exception as e:
            return {
                "endpoint": endpoint_name,
                "url": url,
                "method": test_config['method'],
                "status_code": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }

def run_real_infrastructure_benchmark():
    """Ejecutar benchmark contra infraestructura real"""
    print("QBTC Real Infrastructure Benchmark Arena")
    print("=" * 60)
    print("Probando infraestructura Docker que está corriendo...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    gladiator = QBTCRealGladiator()
    
    # Fase 1: Test de conectividad
    print("FASE 1: Testing conectividad de endpoints")
    print("-" * 40)
    
    connectivity_results = []
    for endpoint_name, url in gladiator.endpoints.items():
        print(f"Testing {endpoint_name} ({url})...")
        result = gladiator.test_endpoint_connectivity(endpoint_name, url)
        connectivity_results.append(result)
        
        status = "SUCCESS" if result['success'] else "FAILED"
        print(f"  {status}: {result.get('status_code', 'N/A')} - {result.get('response_time', 0):.3f}s")
        if result['success']:
            print(f"  Response: {result.get('content_preview', '')[:100]}...")
        else:
            print(f"  Error: {result.get('error', 'Unknown error')}")
        print()
    
    # Fase 2: Test de funcionalidad API
    print("FASE 2: Testing funcionalidad de APIs")
    print("-" * 40)
    
    api_results = []
    for endpoint_name, url in gladiator.endpoints.items():
        print(f"Testing API functionality {endpoint_name}...")
        result = gladiator.test_api_functionality(endpoint_name, url)
        api_results.append(result)
        
        status = "SUCCESS" if result['success'] else "FAILED"
        print(f"  {status}: {result.get('method', 'GET')} {result.get('status_code', 'N/A')} - {result.get('response_time', 0):.3f}s")
        if not result['success']:
            print(f"  Error: {result.get('error', 'Unknown error')}")
        print()
    
    # Compilar resultados finales
    successful_connectivity = sum(1 for r in connectivity_results if r['success'])
    successful_api = sum(1 for r in api_results if r['success'])
    
    avg_response_time = sum(r.get('response_time', 0) for r in connectivity_results) / len(connectivity_results)
    
    final_report = {
        "timestamp": datetime.now().isoformat(),
        "infrastructure_status": {
            "endpoints_tested": len(gladiator.endpoints),
            "connectivity_success": successful_connectivity,
            "api_functionality_success": successful_api,
            "connectivity_rate": successful_connectivity / len(gladiator.endpoints) * 100,
            "api_success_rate": successful_api / len(gladiator.endpoints) * 100,
            "avg_response_time": avg_response_time
        },
        "detailed_results": {
            "connectivity_tests": connectivity_results,
            "api_functionality_tests": api_results
        }
    }
    
    # Mostrar resumen final
    print("=" * 60)
    print("RESUMEN FINAL - INFRAESTRUCTURA REAL")
    print("=" * 60)
    print(f"Endpoints probados: {len(gladiator.endpoints)}")
    print(f"Conectividad exitosa: {successful_connectivity}/{len(gladiator.endpoints)} ({successful_connectivity/len(gladiator.endpoints)*100:.1f}%)")
    print(f"APIs funcionales: {successful_api}/{len(gladiator.endpoints)} ({successful_api/len(gladiator.endpoints)*100:.1f}%)")
    print(f"Tiempo promedio de respuesta: {avg_response_time:.3f}s")
    print()
    
    # Mostrar endpoints activos
    print("ENDPOINTS ACTIVOS:")
    for result in connectivity_results:
        if result['success']:
            print(f"  ✓ {result['endpoint']}: {result['url']} (Status: {result['status_code']})")
    
    print("\nENDPOINTS CON PROBLEMAS:")
    for result in connectivity_results:
        if not result['success']:
            print(f"  ✗ {result['endpoint']}: {result['url']} (Error: {result.get('error', 'Unknown')})")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"real_infrastructure_benchmark_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2, ensure_ascii=False)
    
    print(f"\nResultados guardados en: {filename}")
    print("=" * 60)
    
    return final_report

if __name__ == "__main__":
    run_real_infrastructure_benchmark()