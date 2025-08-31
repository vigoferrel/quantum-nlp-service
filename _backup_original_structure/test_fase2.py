#!/usr/bin/env python3
"""
🧪 TEST FASE 2 - OPTIMIZACIÓN DE RENDIMIENTO
=============================================
"""

import time
import requests
import json

def test_optimizacion_fase2():
    """Probar las optimizaciones de la Fase 2"""
    print("🧪 TESTEANDO OPTIMIZACIONES FASE 2")
    print("=" * 50)
    
    # Test 1: Tiempo de respuesta
    print("📊 Test 1: Tiempo de respuesta...")
    start_time = time.time()
    
    try:
        response = requests.post(
            'http://localhost:5004/api/process_text',
            json={
                'text': 'Hola, ¿cómo estás?',
                'session_id': 'test_fase2'
            },
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"   ⏱️ Tiempo de respuesta: {response_time:.3f}s")
        print(f"   📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('success')}")
            print(f"   🧠 NLP Analysis: {data.get('nlp_analysis') is not None}")
            print(f"   ⚛️ Quantum Analysis: {data.get('quantum_analysis') is not None}")
            
            if data.get('nlp_analysis'):
                print(f"   📝 Sentiment: {data['nlp_analysis']['sentiment']['level']}")
                print(f"   🎯 Intent: {data['nlp_analysis']['intent']['type']}")
            
            if data.get('quantum_analysis'):
                print(f"   🌌 Quantum Score: {data['quantum_analysis']['quantum_score']}")
                print(f"   ⚛️ Quantum State: {data['quantum_analysis']['quantum_state']}")
        
        # Test 2: Múltiples requests para medir consistencia
        print("\n📊 Test 2: Consistencia de rendimiento...")
        times = []
        for i in range(3):
            start = time.time()
            response = requests.post(
                'http://localhost:5004/api/process_text',
                json={
                    'text': f'Test request {i+1}',
                    'session_id': f'test_fase2_{i+1}'
                },
                timeout=30
            )
            end = time.time()
            times.append(end - start)
            print(f"   Request {i+1}: {times[-1]:.3f}s")
        
        avg_time = sum(times) / len(times)
        print(f"   📈 Tiempo promedio: {avg_time:.3f}s")
        print(f"   📊 Variabilidad: {max(times) - min(times):.3f}s")
        
        # Test 3: Cache performance
        print("\n📊 Test 3: Performance de cache...")
        cache_times = []
        for i in range(3):
            start = time.time()
            response = requests.post(
                'http://localhost:5004/api/process_text',
                json={
                    'text': 'Mismo texto para cache',
                    'session_id': 'cache_test'
                },
                timeout=30
            )
            end = time.time()
            cache_times.append(end - start)
            print(f"   Cache request {i+1}: {cache_times[-1]:.3f}s")
        
        cache_avg = sum(cache_times) / len(cache_times)
        print(f"   📈 Tiempo promedio con cache: {cache_avg:.3f}s")
        
        # Evaluación
        print("\n📋 EVALUACIÓN FASE 2:")
        print("=" * 30)
        
        if response_time < 5.0:
            print("   ✅ Tiempo de respuesta: EXCELENTE")
        elif response_time < 8.0:
            print("   ⚠️ Tiempo de respuesta: BUENO")
        else:
            print("   ❌ Tiempo de respuesta: NECESITA MEJORA")
        
        if avg_time < 6.0:
            print("   ✅ Consistencia: EXCELENTE")
        elif avg_time < 10.0:
            print("   ⚠️ Consistencia: BUENA")
        else:
            print("   ❌ Consistencia: NECESITA MEJORA")
        
        if cache_avg < avg_time * 0.8:
            print("   ✅ Cache: FUNCIONANDO")
        else:
            print("   ⚠️ Cache: NECESITA OPTIMIZACIÓN")
        
        print(f"\n🎯 RESULTADO FINAL: FASE 2 {'EXITOSA' if response_time < 8.0 else 'PARCIALMENTE EXITOSA'}")
        
    except Exception as e:
        print(f"   ❌ Error en test: {e}")
        print("   🚨 El servidor puede no estar funcionando")

if __name__ == "__main__":
    test_optimizacion_fase2()
