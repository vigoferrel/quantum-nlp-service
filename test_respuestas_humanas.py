#!/usr/bin/env python3
"""
🧪 TEST NxN - Respuestas Humanas Naturales
Verifica que VIGOLEONROCKS genere respuestas humanas sin overhead técnico
"""

import requests
import json
import time
from datetime import datetime

def test_human_responses():
    """Prueba NxN de respuestas humanas naturales"""
    base_url = "http://localhost:5000"
    
    print("🧪 INICIANDO TEST NxN - RESPUESTAS HUMANAS")
    print("=" * 60)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Servidor: {base_url}")
    print()
    
    # Casos de prueba para respuestas humanas
    test_cases = [
        # Saludos simples
        {"text": "Hola", "expected": "saludo", "lang": "es"},
        {"text": "Hello", "expected": "saludo", "lang": "en"},
        {"text": "Olá", "expected": "saludo", "lang": "pt"},
        
        # Preguntas de identidad
        {"text": "¿Quién eres?", "expected": "identidad", "lang": "es"},
        {"text": "Who are you?", "expected": "identidad", "lang": "en"},
        {"text": "Quem é você?", "expected": "identidad", "lang": "pt"},
        
        # Preguntas de capacidades
        {"text": "¿Qué puedes hacer?", "expected": "capacidades", "lang": "es"},
        {"text": "What can you do?", "expected": "capacidades", "lang": "en"},
        {"text": "O que você pode fazer?", "expected": "capacidades", "lang": "pt"},
        
        # Agradecimientos
        {"text": "Gracias", "expected": "gratitud", "lang": "es"},
        {"text": "Thank you", "expected": "gratitud", "lang": "en"},
        {"text": "Obrigado", "expected": "gratitud", "lang": "pt"},
        
        # Conversaciones casuales
        {"text": "¿Cómo estás?", "expected": "conversacional", "lang": "es"},
        {"text": "How are you?", "expected": "conversacional", "lang": "en"},
        {"text": "Como vai?", "expected": "conversacional", "lang": "pt"},
        
        # Consultas variadas
        {"text": "Me gusta hablar contigo", "expected": "fallback", "lang": "es"},
        {"text": "I like talking to you", "expected": "fallback", "lang": "en"},
        {"text": "Gosto de conversar com você", "expected": "fallback", "lang": "pt"}
    ]
    
    results = {
        'total_tests': len(test_cases),
        'passed': 0,
        'failed': 0,
        'human_responses': 0,
        'robotic_responses': 0,
        'details': []
    }
    
    print("🔍 PROBANDO RESPUESTAS HUMANAS")
    print("=" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}/{len(test_cases)}: '{test_case['text']}'")
        
        try:
            # Hacer petición al endpoint principal
            response = requests.post(
                f"{base_url}/api/vigoleonrocks",
                json={"text": test_case['text']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                detected_lang = data.get('language', '')
                processing_time = data.get('processing_time', 0)
                
                # Analizar si la respuesta es humana
                is_human = analyze_human_response(response_text)
                
                # Verificar idioma detectado
                lang_correct = detected_lang == test_case['lang']
                
                # Verificar que no hay overhead técnico
                has_overhead = check_technical_overhead(response_text)
                
                test_result = {
                    'input': test_case['text'],
                    'output': response_text,
                    'detected_lang': detected_lang,
                    'expected_lang': test_case['lang'],
                    'lang_correct': lang_correct,
                    'is_human': is_human,
                    'has_overhead': has_overhead,
                    'processing_time': processing_time,
                    'status': 'PASS' if is_human and not has_overhead else 'FAIL'
                }
                
                if test_result['status'] == 'PASS':
                    results['passed'] += 1
                    results['human_responses'] += 1
                    print(f"   ✅ HUMANA: {response_text[:50]}...")
                else:
                    results['failed'] += 1
                    results['robotic_responses'] += 1
                    print(f"   ❌ ROBÓTICA: {response_text[:50]}...")
                
                results['details'].append(test_result)
                
            else:
                print(f"   ❌ ERROR: {response.status_code}")
                results['failed'] += 1
                
        except Exception as e:
            print(f"   ❌ EXCEPCIÓN: {e}")
            results['failed'] += 1
        
        time.sleep(0.5)  # Pausa entre tests
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL - TEST NxN RESPUESTAS HUMANAS")
    print("=" * 60)
    print(f"🎯 Total tests: {results['total_tests']}")
    print(f"✅ Exitosos: {results['passed']}")
    print(f"❌ Fallidos: {results['failed']}")
    print(f"👤 Respuestas humanas: {results['human_responses']}")
    print(f"🤖 Respuestas robóticas: {results['robotic_responses']}")
    
    success_rate = (results['passed'] / results['total_tests']) * 100
    print(f"📈 Tasa de éxito: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 ¡EXCELENTE! Sistema genera respuestas humanas naturales")
    elif success_rate >= 70:
        print("👍 BUENO: Mayoría de respuestas son humanas")
    else:
        print("⚠️ MEJORABLE: Muchas respuestas son robóticas")
    
    # Mostrar ejemplos de respuestas
    print("\n📝 EJEMPLOS DE RESPUESTAS:")
    print("-" * 40)
    for detail in results['details'][:5]:  # Primeros 5 ejemplos
        status_icon = "✅" if detail['status'] == 'PASS' else "❌"
        print(f"{status_icon} '{detail['input']}' → '{detail['output'][:60]}...'")
    
    return results

def analyze_human_response(text):
    """Analiza si una respuesta es humana o robótica"""
    text_lower = text.lower()
    
    # Indicadores de respuesta robótica
    robotic_indicators = [
        'procesando', 'processing', 'arquitectura', 'architecture',
        'cuántica', 'quantum', 'sistema', 'system', 'algoritmo',
        'neural', 'redes', 'networks', 'supremacy', 'coherencia',
        'estados cuánticos', 'quantum states', 'frecuencia',
        'resonancia', 'entrelazamiento', 'superposición'
    ]
    
    # Indicadores de respuesta humana
    human_indicators = [
        'hola', 'hello', 'hi', 'olá', 'oi', '😊', '💝', '🙏',
        'gracias', 'thank', 'obrigado', 'de nada', 'welcome',
        'alegra', 'nice', 'prazer', 'ayudarte', 'help', 'ajudar'
    ]
    
    # Contar indicadores
    robotic_count = sum(1 for indicator in robotic_indicators if indicator in text_lower)
    human_count = sum(1 for indicator in human_indicators if indicator in text_lower)
    
    # Es humana si tiene más indicadores humanos que robóticos
    return human_count > robotic_count

def check_technical_overhead(text):
    """Verifica si hay overhead técnico en la respuesta"""
    text_lower = text.lower()
    
    overhead_indicators = [
        'procesando', 'processing', 'arquitectura', 'architecture',
        'cuántica', 'quantum', 'sistema', 'system', 'algoritmo',
        'neural', 'redes', 'networks', 'supremacy', 'coherencia',
        'estados cuánticos', 'quantum states', 'frecuencia',
        'resonancia', 'entrelazamiento', 'superposición',
        'debug', 'componentes', 'templates', 'reemplazado'
    ]
    
    return any(indicator in text_lower for indicator in overhead_indicators)

def test_empathic_responses():
    """Prueba respuestas empáticas"""
    base_url = "http://localhost:5000"
    
    print("\n💝 PROBANDO RESPUESTAS EMPÁTICAS")
    print("=" * 40)
    
    empathy_tests = [
        {"template": "greeting", "level": 3},
        {"template": "greeting", "level": 7},
        {"template": "greeting", "level": 10},
        {"template": "support", "level": 5},
        {"template": "support", "level": 8},
        {"template": "gratitude", "level": 6},
        {"template": "gratitude", "level": 9}
    ]
    
    for test in empathy_tests:
        try:
            response = requests.post(
                f"{base_url}/api/empathic-generate",
                json=test,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get('response', '')
                print(f"   💝 Nivel {test['level']} ({test['template']}): {response_text}")
            else:
                print(f"   ❌ Error en respuesta empática: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Excepción en respuesta empática: {e}")
        
        time.sleep(0.3)

if __name__ == "__main__":
    print("🧪 INICIANDO TEST COMPLETO DE RESPUESTAS HUMANAS")
    print("=" * 60)
    
    # Esperar que el servidor esté listo
    time.sleep(2)
    
    # Ejecutar tests
    results = test_human_responses()
    test_empathic_responses()
    
    print("\n" + "=" * 60)
    print("🏁 TEST COMPLETADO")
    print("=" * 60)
