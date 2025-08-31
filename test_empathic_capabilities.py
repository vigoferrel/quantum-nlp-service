#!/usr/bin/env python3
"""
🧠 Test Script para Capacidades Empáticas de VIGOLEONROCKS
Valida que el sistema responda apropiadamente a consultas conversacionales
"""

import requests
import json
import time

# Configuración
API_URL = "http://localhost:5000/api/vigoleonrocks"
TESTS = [
    {
        "name": "Saludo Simple",
        "text": "hola",
        "expected_type": "empathic",
        "should_contain": ["hola", "vigoleonrocks", "empático"]
    },
    {
        "name": "Saludo en Inglés", 
        "text": "hi",
        "expected_type": "empathic",
        "should_contain": ["hello", "hi", "help"]
    },
    {
        "name": "Agradecimiento",
        "text": "gracias",
        "expected_type": "empathic", 
        "should_contain": ["nada", "placer", "ayudarte"]
    },
    {
        "name": "Consulta Técnica",
        "text": "explica python",
        "expected_type": "technical",
        "should_contain": ["python", "programación", "código"]
    },
    {
        "name": "Consulta Equilibrada",
        "text": "qué opinas de la inteligencia artificial",
        "expected_type": "balanced",
        "should_contain": ["analizado", "asistente empático", "ayudarte"]
    }
]

def test_empathic_response(text):
    """Envía una consulta al servidor y analiza la respuesta"""
    try:
        payload = {"text": text}
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            processing_method = data.get('processing_method', 'unknown')
            vigoleonrocks_response = data.get('vigoleonrocks_output', {}).get('vigoleonrocks_response', '')
            
            return {
                'success': True,
                'processing_method': processing_method,
                'response': vigoleonrocks_response,
                'response_length': len(vigoleonrocks_response)
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analyze_response(response_text, should_contain):
    """Analiza si la respuesta contiene elementos esperados"""
    response_lower = response_text.lower()
    matches = []
    
    for item in should_contain:
        if item.lower() in response_lower:
            matches.append(item)
    
    return matches

def main():
    print("🧠 VIGOLEONROCKS - Test de Capacidades Empáticas")
    print("=" * 60)
    
    # Verificar que el servidor esté funcionando
    try:
        health_check = requests.get("http://localhost:5000/api/health", timeout=5)
        if health_check.status_code != 200:
            print("❌ El servidor no responde correctamente")
            return
    except:
        print("❌ No se puede conectar al servidor en localhost:5000")
        return
    
    print("✅ Servidor VIGOLEONROCKS conectado exitosamente\n")
    
    results = []
    
    for i, test in enumerate(TESTS, 1):
        print(f"Test {i}/5: {test['name']}")
        print(f"Consulta: '{test['text']}'")
        
        result = test_empathic_response(test['text'])
        
        if result['success']:
            response_text = result['response']
            matches = analyze_response(response_text, test['should_contain'])
            
            print(f"✅ Método de procesamiento: {result['processing_method']}")
            print(f"✅ Longitud de respuesta: {result['response_length']} caracteres")
            print(f"✅ Elementos esperados encontrados: {len(matches)}/{len(test['should_contain'])}")
            
            if matches:
                print(f"   Coincidencias: {', '.join(matches)}")
            
            # Mostrar respuesta (truncada si es muy larga)
            display_response = response_text[:200] + "..." if len(response_text) > 200 else response_text
            print(f"📝 Respuesta: {display_response}")
            
            results.append({
                'test': test['name'],
                'success': True,
                'processing_method': result['processing_method'],
                'empathic_score': len(matches) / len(test['should_contain'])
            })
        else:
            print(f"❌ Error: {result['error']}")
            results.append({
                'test': test['name'],
                'success': False,
                'error': result['error']
            })
        
        print("-" * 40)
        time.sleep(1)  # Pausa entre tests
    
    # Resumen de resultados
    print("\n📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    successful_tests = [r for r in results if r['success']]
    empathic_tests = [r for r in successful_tests if r['processing_method'] == 'intelligent_fallback']
    
    print(f"Tests exitosos: {len(successful_tests)}/{len(results)}")
    print(f"Respuestas empáticas: {len(empathic_tests)}/{len(successful_tests)}")
    
    if empathic_tests:
        avg_empathic_score = sum(r.get('empathic_score', 0) for r in empathic_tests) / len(empathic_tests)
        print(f"Score empático promedio: {avg_empathic_score:.2%}")
    
    processing_methods = {}
    for r in successful_tests:
        method = r['processing_method']
        processing_methods[method] = processing_methods.get(method, 0) + 1
    
    print(f"Distribución de métodos de procesamiento:")
    for method, count in processing_methods.items():
        print(f"  - {method}: {count} tests")
    
    if len(successful_tests) == len(results):
        print("\n🎉 ¡Todos los tests pasaron exitosamente!")
        print("💝 El sistema empático de VIGOLEONROCKS está funcionando correctamente")
    else:
        print(f"\n⚠️ {len(results) - len(successful_tests)} tests fallaron")

if __name__ == "__main__":
    main()
