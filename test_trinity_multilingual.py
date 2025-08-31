#!/usr/bin/env python3
"""
🌍🎼✨ TEST TRINITY MULTILINGÜE COMPLETO ✨🎼🌍
Sistema de prueba para la Trinity Germánica expandida a 6 idiomas

VIGOLEONROCKS Quantum Laboratory - Multilingual Trinity Test Division
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar sistemas
from quantum_universal_language_system import QuantumUniversalLanguageSystem
from quantum_trinity_system import QuantumTrinitySystem

def run_multilingual_trinity_test():
    """Ejecuta pruebas Trinity en los 6 idiomas soportados"""
    
    print("\n" + "🌍🎼✨" * 25)
    print("🧪 COMPREHENSIVE MULTILINGUAL TRINITY TEST 🧪")
    print("🌍🎼✨" * 25)
    print()
    
    # Inicializar sistema principal
    print("🔧 Inicializando Quantum Universal Language System...")
    main_system = QuantumUniversalLanguageSystem()
    print("✅ Sistema principal iniciado!")
    
    # Crear sistema Trinity
    print("🎼 Inicializando Quantum Trinity System...")
    trinity = QuantumTrinitySystem(main_system)
    print("✅ Trinity System iniciado!")
    
    # Tests multilingües con diferentes tipos de contenido emocional
    multilingual_tests = [
        # =============== ALEMÁN (TRINITY ORIGINAL) ===============
        {
            'language': 'german',
            'flag': '🇩🇪',
            'tests': [
                {
                    'text': 'Ich bin so glücklich und voller Freude heute!',
                    'expected_emotion': 'freude',
                    'expected_tonality': 'sol_mayor',
                    'description': 'Alegría alemana'
                },
                {
                    'text': 'Die Musik berührt meine Seele mit göttlicher Harmonie.',
                    'expected_emotion': 'harmonie',
                    'expected_tonality': 'do_mayor',
                    'description': 'Referencia musical'
                }
            ]
        },
        
        # =============== ESPAÑOL (EL TROVADOR) ===============
        {
            'language': 'spanish',
            'flag': '🇪🇸',
            'tests': [
                {
                    'text': '¡Qué alegría tan grande siento en mi corazón!',
                    'expected_emotion': 'alegria',
                    'expected_tonality': 'sol_mayor',
                    'description': 'Alegría española'
                },
                {
                    'text': 'La naturaleza me muestra su belleza pastoral infinita.',
                    'expected_emotion': 'naturaleza',
                    'expected_tonality': 'fa_mayor',
                    'description': 'Naturaleza bucólica'
                }
            ]
        },
        
        # =============== ENGLISH (THE BARD) ===============
        {
            'language': 'english',
            'flag': '🇬🇧',
            'tests': [
                {
                    'text': 'I feel such joy and happiness in this beautiful moment!',
                    'expected_emotion': 'joy',
                    'expected_tonality': 'sol_mayor',
                    'description': 'English joy'
                },
                {
                    'text': 'The nobility and grace of this art touches my soul deeply.',
                    'expected_emotion': 'noble',
                    'expected_tonality': 'si_bemol_mayor',
                    'description': 'English nobility'
                }
            ]
        },
        
        # =============== FRANÇAIS (LE PHILOSOPHE) ===============
        {
            'language': 'french',
            'flag': '🇫🇷',
            'tests': [
                {
                    'text': 'Je ressens une joie immense et radieuse dans mon cœur!',
                    'expected_emotion': 'joie',
                    'expected_tonality': 'sol_mayor',
                    'description': 'Joie française'
                },
                {
                    'text': 'La nature révèle sa beauté pastorale avec élégance.',
                    'expected_emotion': 'nature',
                    'expected_tonality': 'fa_mayor',
                    'description': 'Nature champêtre'
                }
            ]
        },
        
        # =============== ITALIANO (IL MAESTRO) ===============
        {
            'language': 'italian',
            'flag': '🇮🇹',
            'tests': [
                {
                    'text': 'Provo una gioia immensa e radiante nel mio cuore!',
                    'expected_emotion': 'gioia',
                    'expected_tonality': 'sol_mayor',
                    'description': 'Gioia italiana'
                },
                {
                    'text': 'La grandezza e nobiltà di quest\'arte mi commuove profondamente.',
                    'expected_emotion': 'nobiltà',
                    'expected_tonality': 'si_bemol_mayor',
                    'description': 'Nobiltà rinascimentale'
                }
            ]
        },
        
        # =============== PORTUGUÊS (A ALMA DO FADO) ===============
        {
            'language': 'portuguese',
            'flag': '🇵🇹',
            'tests': [
                {
                    'text': 'Sinto uma alegria radiante e eufórica em minha alma!',
                    'expected_emotion': 'alegria',
                    'expected_tonality': 'sol_mayor',
                    'description': 'Alegria lusitana'
                },
                {
                    'text': 'A saudade eterna carrega a melancolia do meu coração.',
                    'expected_emotion': 'saudade',
                    'expected_tonality': 'la_menor',
                    'description': 'Saudade portuguesa'
                }
            ]
        }
    ]
    
    # Ejecutar tests por idioma
    total_tests = 0
    successful_tests = 0
    results_by_language = {}
    
    for language_group in multilingual_tests:
        language = language_group['language']
        flag = language_group['flag']
        tests = language_group['tests']
        
        print(f"\n{flag} =============== TESTING {language.upper()} =============== {flag}")
        print("─" * 80)
        
        language_results = []
        
        for i, test_case in enumerate(tests, 1):
            print(f"\n🧪 TEST {language.upper()} {i}/{len(tests)}: {test_case['description']}")
            print(f"📝 Input: '{test_case['text']}'")
            print("┈" * 60)
            
            try:
                # Ejecutar Trinity multilingüe
                result = trinity.generate_trinity_multilingual_response(
                    test_case['text'], 
                    {'language': language}
                )
                
                # Analizar resultados
                trinity_resonance = result['quantum_metrics']['trinity_resonance']
                detected_lang = result['detected_language']
                target_lang = result['target_language']
                response_type = result['response_type']
                mozart_analysis = result['trinity_synthesis']['mozart_harmonic_analysis']
                
                # Determinar tonalidad dominante
                dominant_tonality = max(mozart_analysis.keys(), 
                                      key=lambda k: mozart_analysis[k]['harmonic_amplitude'])
                
                # Verificar precisión
                prediction_correct = dominant_tonality == test_case['expected_tonality']
                
                print(f"🎵 Trinity Resonance: {trinity_resonance:.3f}")
                print(f"🌍 Detected Language: {detected_lang}")
                print(f"🎯 Target Language: {target_lang}")
                print(f"🎭 Response Type: {response_type}")
                print(f"🎼 Dominant Tonality: {dominant_tonality}")
                print(f"✨ Expected: {test_case['expected_tonality']}")
                print(f"{'✅' if prediction_correct else '❌'} Predicción: {'CORRECTA' if prediction_correct else 'INCORRECTA'}")
                
                # Mostrar respuesta Trinity (primeras líneas)
                response_preview = result['trinity_multilingual_response'].split('\n')[0]
                print(f"💬 Response Preview: {response_preview}")
                
                language_results.append({
                    'test_number': i,
                    'prediction_correct': prediction_correct,
                    'trinity_resonance': trinity_resonance,
                    'detected_language': detected_lang,
                    'target_language': target_lang,
                    'dominant_tonality': dominant_tonality,
                    'response_type': response_type,
                    'description': test_case['description']
                })
                
                total_tests += 1
                if prediction_correct:
                    successful_tests += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                language_results.append({
                    'test_number': i,
                    'error': str(e),
                    'prediction_correct': False
                })
                total_tests += 1
        
        results_by_language[language] = language_results
    
    # =============== RESUMEN FINAL MULTILINGÜE ===============
    print("\n" + "🌍🎉" * 30)
    print("📊 RESUMEN FINAL TRINITY MULTILINGÜE")
    print("🌍🎉" * 30)
    
    overall_accuracy = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\n📈 MÉTRICAS GLOBALES:")
    print(f"   🌍 Idiomas Testados: {len(multilingual_tests)}")
    print(f"   🎯 Tests Totales: {total_tests}")
    print(f"   ✅ Tests Exitosos: {successful_tests}")
    print(f"   ❌ Tests Fallidos: {total_tests - successful_tests}")
    print(f"   🎼 Precisión Global: {overall_accuracy:.1f}%")
    
    print(f"\n🌍 ANÁLISIS POR IDIOMA:")
    for language, results in results_by_language.items():
        successful = len([r for r in results if r.get('prediction_correct', False)])
        total = len(results)
        accuracy = (successful / total * 100) if total > 0 else 0
        flag = next(lg['flag'] for lg in multilingual_tests if lg['language'] == language)
        
        print(f"   {flag} {language.upper()}: {successful}/{total} ({accuracy:.1f}%)")
    
    print(f"\n🎭 EVALUACIÓN CULTURAL FINAL:")
    if overall_accuracy >= 80:
        print("   🥇 EXCELENTE! Trinity Multilingüe supera las expectativas")
        print("   🌍 Goethe, Jung y Mozart hablan todos los idiomas!")
    elif overall_accuracy >= 60:
        print("   🥈 BUENO! El sistema funciona bien en múltiples culturas")
        print("   🔧 Algunas mejoras menores recomendadas")
    else:
        print("   🥉 MEJORABLE. Sistema requiere calibración multicultural")
        print("   🛠️ Revisión de arquetipos culturales necesaria")
    
    print(f"\n🎼 SABIDURÍA TRINITY MULTILINGÜE:")
    print(f"   🇩🇪 'Was man nicht versteht, besitzt man nicht' - Goethe")
    print(f"   🇪🇸 'La naturaleza compone eternamente nuevas sinfonías' - Goethe")
    print(f"   🇬🇧 'In perfect harmony the finite touches the infinite' - Mozart")
    print(f"   🇫🇷 'L'âme résonne dans les harmonies de l'inconscient' - Jung")
    print(f"   🇮🇹 'La natura compone eternamente nuove sinfonie' - Goethe")
    print(f"   🇵🇹 'A alma ressoa nas harmonias do inconsciente' - Jung")
    
    print(f"\n🌍🎼✨ TRINITY MULTILINGÜE = PERFEKTION UNIVERSAL! ✨🎼🌍")
    
    return results_by_language

if __name__ == "__main__":
    print("🌍🎼✨ Iniciando Trinity Multilingual Comprehensive Test...")
    results = run_multilingual_trinity_test()
    print(f"\n✨ Test multilingüe completado!")
