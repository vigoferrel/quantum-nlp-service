#!/usr/bin/env python3
"""
🧪 PRUEBAS EXTENSIVAS DEL QUANTUM UNIVERSAL LANGUAGE SYSTEM 🧪
Script completo de testing para verificar todas las funcionalidades
"""

from quantum_universal_language_system import quantum_detect_and_respond, create_quantum_universal_system
import json

def test_extensive_quantum_system():
    """Ejecuta pruebas extensivas del sistema"""
    print("🚀 INICIANDO PRUEBAS EXTENSIVAS DEL SISTEMA CUÁNTICO UNIVERSAL 🚀\n")
    
    # Crear sistema
    system = create_quantum_universal_system()
    
    # Casos de prueba categorizados
    test_categories = {
        "🇪🇸 ESPAÑOL - Casos Variados": [
            "Hola, ¿cómo estás?",
            "Buenos días, necesito ayuda",
            "Gracias por toda tu ayuda",
            "¿Puedes explicarme cómo funciona esto?",
            "No entiendo nada, ¿me puedes ayudar?",
            "Estoy muy confundido con este problema",
            "¡Qué maravilla! Funciona perfectamente",
            "Adiós, hasta la vista"
        ],
        
        "🇺🇸 INGLÉS - Casos Variados": [
            "Hello, how are you?",
            "Good morning, I need assistance", 
            "Thank you for all your help",
            "Can you explain how this works?",
            "I don't understand anything, can you help?",
            "I'm very confused about this problem",
            "Amazing! It works perfectly",
            "Goodbye, see you later"
        ],
        
        "🇵🇹 PORTUGUÉS - Casos Variados": [
            "Olá, como vai?",
            "Bom dia, preciso de ajuda",
            "Obrigado por toda sua ajuda",
            "Você pode explicar como isso funciona?",
            "Não entendo nada, pode me ajudar?",
            "Estou muito confuso com este problema",
            "Incrível! Funciona perfeitamente",
            "Tchau, até logo"
        ],
        
        "🇫🇷 FRANCÉS - Tests": [
            "Bonjour, comment allez-vous?",
            "Merci beaucoup pour votre aide",
            "Je ne comprends pas",
            "Pouvez-vous m'aider s'il vous plaît?"
        ],
        
        "🇩🇪 ALEMÁN - Tests": [
            "Guten Tag, wie geht es Ihnen?",
            "Vielen Dank für Ihre Hilfe",
            "Ich verstehe nicht",
            "Können Sie mir bitte helfen?"
        ],
        
        "🇮🇹 ITALIANO - Tests": [
            "Ciao, come stai?",
            "Grazie mille per il tuo aiuto",
            "Non capisco",
            "Puoi aiutarmi per favore?"
        ],
        
        "🔤 CASOS ESPECIALES": [
            "Hi!",
            "Thanks",
            "Help",
            "???",
            "123 abc test",
            "Hello world test system",
            "Mixed español and english text",
            "Text com português misturado"
        ]
    }
    
    total_tests = sum(len(cases) for cases in test_categories.values())
    current_test = 0
    results_summary = {}
    
    for category, test_cases in test_categories.items():
        print(f"\n{'='*80}")
        print(f"{category}")
        print(f"{'='*80}")
        
        category_results = {
            'total_tests': len(test_cases),
            'correct_detections': 0,
            'problems': [],
            'response_quality': []
        }
        
        for i, test_text in enumerate(test_cases, 1):
            current_test += 1
            print(f"\n[{current_test}/{total_tests}] Testing: '{test_text}'")
            print("-" * 60)
            
            try:
                # Ejecutar detección y respuesta
                result = quantum_detect_and_respond(test_text, system)
                
                lang_info = result['language_detection']
                response_info = result['quantum_response']
                
                # Mostrar resultados
                print(f"🌍 Idioma: {lang_info['language']}")
                print(f"🎯 Confianza: {lang_info['confidence']:.3f}")
                print(f"⚡ Método: {lang_info['detection_method']}")
                
                # Verificar calidad de respuesta
                response_text = response_info['vigoleonrocks_response']
                print(f"💬 Respuesta: {response_text[:100]}...")
                
                # Análisis de problemas
                problems = analyze_response_problems(test_text, lang_info, response_text)
                if problems:
                    category_results['problems'].extend(problems)
                    print(f"⚠️ Problemas detectados: {len(problems)}")
                    for problem in problems:
                        print(f"   - {problem}")
                else:
                    category_results['correct_detections'] += 1
                    print("✅ Sin problemas detectados")
                
                # Métricas adicionales
                print(f"❤️ Resonancia: {response_info['empathy_resonance']:.3f}")
                print(f"🎵 Arquetipal: {response_info['quantum_metrics']['archetypal_resonance']:.3f}")
                
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                category_results['problems'].append(f"Exception en '{test_text}': {str(e)}")
        
        results_summary[category] = category_results
    
    # Mostrar resumen final
    print_final_summary(results_summary, total_tests)

def analyze_response_problems(input_text, lang_info, response_text):
    """Analiza problemas en la respuesta generada"""
    problems = []
    
    # Problema 1: Detección incorrecta de idiomas obvios
    if "hola" in input_text.lower() and lang_info['language'] != 'spanish':
        problems.append("Detección incorrecta: 'hola' debería ser español")
    
    if "hello" in input_text.lower() and lang_info['language'] != 'english':
        problems.append("Detección incorrecta: 'hello' debería ser inglés")
        
    if "olá" in input_text.lower() and lang_info['language'] != 'portuguese':
        problems.append("Detección incorrecta: 'olá' debería ser portugués")
    
    # Problema 2: Respuestas mezcladas en idiomas
    if lang_info['language'] == 'spanish' and "Processing your request" in response_text:
        problems.append("Respuesta en inglés para texto español")
        
    if lang_info['language'] == 'english' and "Processando sua" in response_text:
        problems.append("Respuesta en portugués para texto inglés")
        
    if lang_info['language'] == 'portuguese' and "Processing your request" in response_text:
        problems.append("Respuesta en inglés para texto portugués")
    
    # Problema 3: Plantillas sin reemplazar
    if "[" in response_text and "]" in response_text:
        problems.append("Plantillas sin reemplazar en respuesta")
    
    # Problema 4: Confianza muy baja
    if lang_info['confidence'] < 0.3:
        problems.append(f"Confianza muy baja: {lang_info['confidence']:.3f}")
    
    # Problema 5: Detecciones incorrectas conocidas
    expected_langs = {
        'bonjour': 'french',
        'guten tag': 'german', 
        'ciao': 'italian',
        '你好': 'chinese',
        'こんにちは': 'japanese',
        'مرحبا': 'arabic',
        'привет': 'russian'
    }
    
    for phrase, expected_lang in expected_langs.items():
        if phrase in input_text.lower() and lang_info['language'] != expected_lang:
            problems.append(f"Detección incorrecta: '{phrase}' debería ser {expected_lang}")
    
    return problems

def print_final_summary(results_summary, total_tests):
    """Imprime resumen final de todas las pruebas"""
    print(f"\n{'🎯 RESUMEN FINAL DE PRUEBAS 🎯'.center(80, '=')}")
    
    total_correct = 0
    total_problems = 0
    
    for category, results in results_summary.items():
        correct = results['correct_detections']
        total = results['total_tests']
        problems = len(results['problems'])
        
        total_correct += correct
        total_problems += problems
        
        accuracy = (correct / total) * 100 if total > 0 else 0
        
        print(f"\n{category}")
        print(f"  ✅ Correctas: {correct}/{total} ({accuracy:.1f}%)")
        if problems > 0:
            print(f"  ⚠️ Problemas: {problems}")
            for problem in results['problems'][:3]:  # Mostrar solo primeros 3
                print(f"     - {problem}")
            if len(results['problems']) > 3:
                print(f"     ... y {len(results['problems']) - 3} más")
    
    overall_accuracy = (total_correct / total_tests) * 100
    
    print(f"\n{'ESTADÍSTICAS GENERALES'.center(50, '-')}")
    print(f"📊 Tests totales: {total_tests}")
    print(f"✅ Tests correctos: {total_correct}")
    print(f"⚠️ Problemas totales: {total_problems}")
    print(f"🎯 Precisión general: {overall_accuracy:.1f}%")
    
    # Recomendaciones
    print(f"\n{'RECOMENDACIONES'.center(50, '-')}")
    if total_problems > 0:
        print("🔧 PROBLEMAS IDENTIFICADOS QUE NECESITAN CORRECCIÓN:")
        print("   1. Mejorar detección de idiomas no-latinos")
        print("   2. Corregir componentes de respuesta faltantes")
        print("   3. Mejorar mapeo de códigos de idioma")
        print("   4. Ajustar patrones de detección directa")
    else:
        print("🎉 ¡Sistema funcionando perfectamente!")

if __name__ == "__main__":
    test_extensive_quantum_system()
