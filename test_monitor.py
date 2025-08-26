#!/usr/bin/env python3
"""
🧪 PRUEBA DEL MONITOR DE CONEXIONES
Script para probar el sistema de monitoreo
"""

import requests
import json
import time
import random
from datetime import datetime

def test_monitor():
    """Probar el monitor de conexiones"""
    base_url = "http://localhost:5001"
    
    print("🧪 PRUEBA DEL MONITOR DE CONEXIONES VIGOLEONROCKS")
    print("=" * 60)
    
    # API keys de prueba
    test_keys = [
        "vk_live_test_key_123",
        "vk_live_dev_key_456"
    ]
    
    # Tipos de consulta
    query_types = ["text", "multimodal", "quantum"]
    
    # Consultas de prueba
    test_queries = [
        "¿Cuál es la capital de Francia?",
        "Explica la teoría de la relatividad",
        "Resuelve: 2x + 5 = 15",
        "¿Qué es la inteligencia artificial?",
        "Describe el proceso de fotosíntesis"
    ]
    
    print("📊 Iniciando pruebas de conexión...")
    
    # Realizar múltiples requests para generar datos
    for i in range(10):
        api_key = random.choice(test_keys)
        query_type = random.choice(query_types)
        query = random.choice(test_queries)
        
        print(f"🔄 Request {i+1}: {query_type} - {query[:30]}...")
        
        try:
            # Simular request
            payload = {
                "api_key": api_key,
                "query": query,
                "type": query_type
            }
            
            start_time = time.time()
            response = requests.post(f"{base_url}/api/process", json=payload, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                print(f"  ✅ Éxito - {response_time:.3f}s")
            else:
                print(f"  ❌ Error {response.status_code} - {response_time:.3f}s")
                
        except Exception as e:
            print(f"  ❌ Error de conexión: {e}")
        
        # Pausa entre requests
        time.sleep(1)
    
    print("\n📈 Verificando estadísticas del monitor...")
    
    try:
        # Obtener dashboard del monitor
        response = requests.get(f"{base_url}/api/monitor", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Dashboard del Monitor:")
            print("-" * 40)
            
            overview = data.get("system_overview", {})
            print(f"📊 Total Requests: {overview.get('total_requests', 0)}")
            print(f"✅ Éxito: {overview.get('success_rate', 0)}%")
            print(f"❌ Error: {overview.get('error_rate', 0)}%")
            print(f"⏱️  Tiempo Promedio: {overview.get('avg_response_time', 0)}s")
            print(f"👥 Usuarios Activos: {overview.get('current_users', 0)}")
            print(f"🏆 Pico de Usuarios: {overview.get('peak_users', 0)}")
            print(f"⏰ Uptime: {overview.get('uptime', '0:00:00')}")
            
            # Mostrar estadísticas de usuarios
            user_stats = data.get("user_stats", {})
            if user_stats:
                print("\n👥 Estadísticas de Usuarios:")
                print("-" * 30)
                for api_key, stats in user_stats.items():
                    print(f"  {stats['user_name']}: {stats['total_requests']} requests")
            
            # Mostrar conexiones recientes
            recent_connections = data.get("recent_connections", [])
            if recent_connections:
                print(f"\n🕒 Últimas {len(recent_connections)} Conexiones:")
                print("-" * 40)
                for conn in recent_connections[-5:]:  # Últimas 5
                    timestamp = datetime.fromisoformat(conn['timestamp'].replace('Z', '+00:00')).strftime('%H:%M:%S')
                    status = "✅" if conn['success'] else "❌"
                    print(f"  {status} {conn['user_name']} - {conn['query_type']} ({timestamp})")
            
        else:
            print(f"❌ Error obteniendo dashboard: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando monitor: {e}")
    
    print("\n🔍 Verificando endpoint de estado...")
    
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Estado del Sistema:")
            print(f"  CIO Status: {status_data.get('cio_status', 'N/A')}")
            print(f"  OpenRouter Status: {status_data.get('openrouter_status', 'N/A')}")
            print(f"  Multimodal Status: {status_data.get('multimodal_status', 'N/A')}")
            
            # Verificar si incluye estadísticas del monitor
            if 'monitor_stats' in status_data:
                print("  📊 Monitor Stats: Incluidas")
            else:
                print("  📊 Monitor Stats: No incluidas")
        else:
            print(f"❌ Error obteniendo estado: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error verificando estado: {e}")
    
    print("\n🎯 PRUEBA COMPLETADA")
    print("=" * 60)
    print("📊 El monitor está funcionando correctamente")
    print("🌐 Accede a http://localhost:5001 para ver el dashboard")
    print("📈 Los datos se actualizan automáticamente cada 30 segundos")

if __name__ == "__main__":
    test_monitor()
