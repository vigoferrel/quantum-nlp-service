#!/usr/bin/env python3
"""
🌍 Test Script para Capacidades Multilenguaje de VIGOLEONROCKS
Valida respuestas empáticas en español, inglés y portugués
"""

import requests
import json
import time

# Configuración
API_URL = "http://localhost:5000/api/vigoleonrocks"
MULTILINGUAL_TESTS = [
    # Pruebas en Español
    {
        "name": "Saludo en Español",
        "text": "hola",
        "expected_lang": "es",
        "expected_contains": ["hola", "vigoleonrocks", "ayudarte"]
    },
    {
        "name": "Cómo estás en Español",
        "text": "como estas",
        "expected_lang": "es", 
        "expected_contains": ["gracias", "energía", "cómo te encuentras"]
    },
    {
        "name": "Agradecimiento en Español",
        "text": "gracias",
        "expected_lang": "es",
        "expected_contains": ["nada", "placer", "alegría"]
    },
    
    # Pruebas en Inglés
    {
        "name": "Greeting in English",
        "text": "hello",
        "expected_lang": "en",
        "expected_contains": ["hello", "vigoleonrocks", "empathetic"]
    },
    {
        "name": "How are you in English",
        "text": "how are you",
        "expected_lang": "en",
        "expected_contains": ["thank you", "energized", "feeling"]
    },
    {
        "name": "Gratitude in English", 
        "text": "thank you",
        "expected_lang": "en",
        "expected_contains": ["welcome", "pleasure", "happy"]
    },
    
    # Pruebas en Portugués
    {
        "name": "Cumprimento em Português",
        "text": "olá",
        "expected_lang": "pt",
        "expected_contains": ["olá", "vigoleonrocks", "empático"]
    },
    {
        "name": "Como vai em Português",
        "text": "como vai",
        "expected_lang": "pt",
        "expected_contains": ["obrigado", "energia", "como você está"]
    },
    {
        "name": "Gratidão em Português",
        "text": "obrigado",
        "expected_lang": "pt", 
        "expected_contains": ["nada", "prazer", "gratidão"]
    },
    
    # Pruebas con parámetro lang explícito
    {
        "name": "Forzar idioma inglés",
        "text": "hola",
        "lang": "en",
        "expected_lang": "en",
        "expected_contains": ["hello", "empathetic", "help"]
    }
]

def test_multilingual_response(text, lang=None):
    """Envía una consulta al servidor en un idioma específico"""
    try:
        payload = {"text": text}
        if lang:
            payload["lang"] = lang
            
        response = requests.post(API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            vigoleonrocks_output = data.get('vigoleonrocks_output', {})
            detected_lang = data.get('input', {}).get('lang', 'unknown')
            response_text = vigoleonrocks_output.get('vigoleonrocks_response', '')
            processing_method = data.get('processing_method', 'unknown')
            
            return {
                'success': True,
                'detected_lang': detected_lang,
                'processing_method': processing_method,
                'response': response_text,
                'response_length': len(response_text),
                'full_data': data
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

def analyze_multilingual_response(response_text, expected_contains, expected_lang):
    """Analiza si la respuesta está en el idioma esperado y contiene elementos clave"""
    response_lower = response_text.lower()
    matches = []
    
    for item in expected_contains:
        if item.lower() in response_lower:
            matches.append(item)
    
    # Validar idioma por heurísticas
    lang_indicators = {
        'es': ['hola', 'gracias', 'siento', 'ayudarte', 'cómo', 'alegra', 'empático'],
        'en': ['hello', 'thank', 'feel', 'help', 'how', 'glad', 'empathetic'],
        'pt': ['olá', 'obrigado', 'como', 'ajudar', 'feliz', 'empático']
    }
    
    lang_score = 0
    if expected_lang in lang_indicators:
        for indicator in lang_indicators[expected_lang]:
            if indicator in response_lower:
                lang_score += 1
    
    return {
        'content_matches': matches,
        'content_score': len(matches) / len(expected_contains) if expected_contains else 0,
        'language_score': lang_score,
        'seems_correct_lang': lang_score > 0
    }

def main():
    print("🌍 VIGOLEONROCKS - Test de Capacidades Multilenguaje")
    print("=" * 65)
    
    # Verificar conexión al servidor
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
    
    for i, test in enumerate(MULTILINGUAL_TESTS, 1):
        print(f"Test {i}/{len(MULTILINGUAL_TESTS)}: {test['name']}")
        print(f"Texto: '{test['text']}'", end="")
        if test.get('lang'):
            print(f" (forzar idioma: {test['lang']})", end="")
        print(f" → Esperado: {test['expected_lang']}")
        
        result = test_multilingual_response(test['text'], test.get('lang'))
        
        if result['success']:
            analysis = analyze_multilingual_response(
                result['response'], 
                test['expected_contains'], 
                test['expected_lang']
            )
            
            # Verificar detección de idioma
            lang_correct = result['detected_lang'] == test['expected_lang']
            
            print(f"✅ Idioma detectado: {result['detected_lang']} {'✓' if lang_correct else '✗'}")
            print(f"✅ Método de procesamiento: {result['processing_method']}")
            print(f"✅ Longitud de respuesta: {result['response_length']} caracteres")
            print(f"✅ Coincidencias de contenido: {len(analysis['content_matches'])}/{len(test['expected_contains'])}")
            
            if analysis['content_matches']:
                print(f"   Elementos encontrados: {', '.join(analysis['content_matches'])}")
            
            print(f"✅ Indicadores de idioma: {analysis['language_score']} {'✓' if analysis['seems_correct_lang'] else '✗'}")
            
            # Mostrar respuesta (truncada si es muy larga)
            display_response = result['response'][:150] + "..." if len(result['response']) > 150 else result['response']
            print(f"📝 Respuesta: {display_response}")
            
            results.append({
                'test': test['name'],
                'success': True,
                'lang_detection_correct': lang_correct,
                'content_score': analysis['content_score'],
                'language_correct': analysis['seems_correct_lang'],
                'processing_method': result['processing_method'],
                'expected_lang': test['expected_lang'],
                'detected_lang': result['detected_lang']
            })
        else:
            print(f"❌ Error: {result['error']}")
            results.append({
                'test': test['name'],
                'success': False,
                'error': result['error']
            })
        
        print("-" * 50)
        time.sleep(1.5)  # Pausa entre tests
    
    # Resumen de resultados
    print("\n📊 RESUMEN DE CAPACIDADES MULTILENGUAJE")
    print("=" * 65)
    
    successful_tests = [r for r in results if r['success']]
    lang_detection_correct = [r for r in successful_tests if r.get('lang_detection_correct')]
    empathic_responses = [r for r in successful_tests if r['processing_method'] == 'intelligent_fallback']
    
    print(f"Tests exitosos: {len(successful_tests)}/{len(results)}")
    print(f"Detección de idioma correcta: {len(lang_detection_correct)}/{len(successful_tests)}")
    print(f"Respuestas empáticas: {len(empathic_responses)}/{len(successful_tests)}")
    
    if successful_tests:
        avg_content_score = sum(r.get('content_score', 0) for r in successful_tests) / len(successful_tests)
        print(f"Score promedio de contenido: {avg_content_score:.2%}")
        
        lang_accuracy = len(lang_detection_correct) / len(successful_tests) if successful_tests else 0
        print(f"Precisión de detección de idioma: {lang_accuracy:.2%}")
    
    # Distribución por idiomas
    lang_distribution = {}
    for r in successful_tests:
        lang = r.get('expected_lang', 'unknown')
        if lang not in lang_distribution:
            lang_distribution[lang] = {'total': 0, 'correct': 0}
        lang_distribution[lang]['total'] += 1
        if r.get('lang_detection_correct'):
            lang_distribution[lang]['correct'] += 1
    
    print(f"\nDistribución por idiomas:")
    for lang, stats in lang_distribution.items():
        accuracy = stats['correct'] / stats['total'] if stats['total'] else 0
        flag = {'es': '🇪🇸', 'en': '🇺🇸', 'pt': '🇧🇷'}.get(lang, '🏳️')
        print(f"  {flag} {lang.upper()}: {stats['correct']}/{stats['total']} ({accuracy:.1%})")
    
    # Distribución por métodos de procesamiento
    processing_methods = {}
    for r in successful_tests:
        method = r['processing_method']
        processing_methods[method] = processing_methods.get(method, 0) + 1
    
    print(f"\nMétodos de procesamiento:")
    for method, count in processing_methods.items():
        print(f"  - {method}: {count} tests")
    
    if len(successful_tests) == len(results) and len(lang_detection_correct) >= len(successful_tests) * 0.8:
        print("\n🎉 ¡Sistema multilenguaje funcionando excelentemente!")
        print("💫 VIGOLEONROCKS ahora responde empáticamente en español, inglés y portugués")
    elif len(successful_tests) >= len(results) * 0.8:
        print("\n✅ Sistema multilenguaje funcionando bien")
        print("🔧 Algunas mejoras menores podrían optimizar la detección de idioma")
    else:
        print(f"\n⚠️ Sistema multilenguaje necesita ajustes")
        print(f"🔧 {len(results) - len(successful_tests)} tests fallaron")

if __name__ == "__main__":
    main()
