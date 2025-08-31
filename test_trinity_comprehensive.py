#!/usr/bin/env python3
"""
🧪🇩🇪🎼 TEST TRINITY SYSTEM: GOETHE-JUNG-MOZART 🎼🇩🇪🧪
Prueba completa del Sistema Cuántico Trinity con textos alemanes

VIGOLEONROCKS Quantum Laboratory - Trinity Test Division
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar sistemas
from quantum_universal_language_system import QuantumUniversalLanguageSystem
from quantum_trinity_system import QuantumTrinitySystem, test_trinity_system

def run_comprehensive_trinity_test():
    """Ejecuta pruebas completas del Trinity System"""
    
    print("\n" + "🇩🇪🎼✨" * 25)
    print("🧪 COMPREHENSIVE TRINITY SYSTEM TEST 🧪")
    print("🇩🇪🎼✨" * 25)
    print()
    
    # Inicializar sistema principal
    print("🔧 Inicializando Quantum Universal Language System...")
    main_system = QuantumUniversalLanguageSystem()
    print("✅ Sistema principal iniciado!")
    
    # Textos alemanes de prueba con diferentes tonalidades emocionales
    test_texts = [
        {
            'text': 'Guten Tag! Ich freue mich sehr, Sie kennenzulernen. Wie geht es Ihnen heute?',
            'expected_emotion': 'freude/alegria',
            'expected_tonality': 'sol_mayor',
            'description': 'Saludo alegre - debería activar Sol Mayor (alegría celestial)'
        },
        {
            'text': 'Die Musik Mozarts berührt meine Seele mit himmlischer Harmonie und göttlicher Schönheit.',
            'expected_emotion': 'divine_harmony',
            'expected_tonality': 'do_mayor',
            'description': 'Referencia a Mozart - debería activar alta resonancia Trinity'
        },
        {
            'text': 'Die Natur zeigt uns die verborgenen Gesetze der Morphologie in ihrer ewigen Metamorphose.',
            'expected_emotion': 'philosophical_depth',
            'expected_tonality': 'fa_mayor',
            'description': 'Filosofía natural de Goethe - debería activar Fa Mayor (pastoral)'
        },
        {
            'text': 'In den Tiefen meiner Seele erkenne ich die Archetypen des kollektiven Unbewussten.',
            'expected_emotion': 'psychological_depth',
            'expected_tonality': 'la_menor',
            'description': 'Psicología Jungiana - debería activar La menor (introspección)'
        },
        {
            'text': 'Es tut mir leid zu hören, dass Sie traurig sind. Ich verstehe Ihren Schmerz.',
            'expected_emotion': 'melancholia',
            'expected_tonality': 'la_menor',
            'description': 'Empatía con tristeza - debería activar La menor (melancolía sublime)'
        },
        {
            'text': 'Mit höchster Würde und Anmut betrachte ich die Schönheit dieser adeligen Kunst.',
            'expected_emotion': 'nobility',
            'expected_tonality': 'si_bemol_mayor',
            'description': 'Nobleza imperial - debería activar Si♭ Mayor'
        }
    ]
    
    print(f"\n🎯 Ejecutando {len(test_texts)} pruebas Trinity...")
    print("=" * 100)
    
    results = []
    
    for i, test_case in enumerate(test_texts, 1):
        print(f"\n🧪 TEST {i}/{len(test_texts)}: {test_case['description']}")
        print(f"📝 Input: '{test_case['text']}'")
        print("─" * 90)
        
        try:
            # Ejecutar test Trinity
            result = test_trinity_system(main_system, test_case['text'])
            
            # Analizar resultados
            trinity_resonance = result['quantum_metrics']['trinity_resonance']
            response_type = result['response_type']
            mozart_analysis = result['trinity_synthesis']['mozart_harmonic_analysis']
            
            # Determinar tonalidad dominante
            dominant_tonality = max(mozart_analysis.keys(), 
                                  key=lambda k: mozart_analysis[k]['harmonic_amplitude'])
            
            print(f"\n📊 RESULTADOS TEST {i}:")
            print(f"   🎵 Trinity Resonance: {trinity_resonance:.3f}")
            print(f"   🎭 Response Type: {response_type}")
            print(f"   🎼 Tonalidad Dominante: {dominant_tonality}")
            print(f"   ✨ Expected: {test_case['expected_tonality']}")
            
            # Verificar si la predicción fue correcta
            prediction_correct = dominant_tonality == test_case['expected_tonality']
            print(f"   {'✅' if prediction_correct else '❌'} Predicción: {'CORRECTA' if prediction_correct else 'INCORRECTA'}")
            
            results.append({
                'test_number': i,
                'text': test_case['text'],
                'expected_tonality': test_case['expected_tonality'],
                'detected_tonality': dominant_tonality,
                'trinity_resonance': trinity_resonance,
                'response_type': response_type,
                'prediction_correct': prediction_correct,
                'description': test_case['description']
            })
            
        except Exception as e:
            print(f"❌ ERROR en test {i}: {str(e)}")
            results.append({
                'test_number': i,
                'error': str(e),
                'prediction_correct': False
            })
        
        print("\n" + "─" * 90)
    
    # Resumen final de resultados
    print("\n" + "🎉" * 30)
    print("📊 RESUMEN FINAL TRINITY SYSTEM TEST")
    print("🎉" * 30)
    
    successful_tests = [r for r in results if not r.get('error') and r.get('prediction_correct')]
    total_tests = len(results)
    accuracy = (len(successful_tests) / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n📈 MÉTRICAS GENERALES:")
    print(f"   🎯 Tests Ejecutados: {total_tests}")
    print(f"   ✅ Tests Exitosos: {len(successful_tests)}")
    print(f"   ❌ Tests Fallidos: {total_tests - len(successful_tests)}")
    print(f"   🎼 Precisión Trinity: {accuracy:.1f}%")
    
    if successful_tests:
        avg_resonance = sum([r['trinity_resonance'] for r in successful_tests]) / len(successful_tests)
        print(f"   ⚡ Resonancia Promedio: {avg_resonance:.3f}")
    
    print(f"\n🎵 ANÁLISIS POR TONALIDAD:")
    tonality_stats = {}
    for result in successful_tests:
        detected = result['detected_tonality']
        if detected not in tonality_stats:
            tonality_stats[detected] = 0
        tonality_stats[detected] += 1
    
    for tonality, count in tonality_stats.items():
        print(f"   🎹 {tonality}: {count} detecciones")
    
    print(f"\n🇩🇪 EVALUACIÓN FINAL:")
    if accuracy >= 80:
        print("   🥇 EXCELENTE! Trinity System funciona perfectamente")
        print("   🎼 Mozart, Goethe y Jung estarían orgullosos!")
    elif accuracy >= 60:
        print("   🥈 BIEN! El sistema necesita ajustes menores")
        print("   🔧 Considerando optimizaciones...")
    else:
        print("   🥉 MEJORABLE. El sistema requiere calibración")
        print("   🛠️ Revisión de algoritmos necesaria")
    
    print(f"\n🎭 'Die Vollendung liegt nicht daran, dass nichts mehr hinzuzufügen ist,'")
    print(f"   'sondern dass nichts mehr wegzunehmen ist.' - Goethe")
    print(f"🎼 'Die Musik drückt das aus, was nicht gesagt werden kann.' - Mozart")  
    print(f"🧠 'Wer nach außen schaut, träumt. Wer nach innen schaut, erwacht.' - Jung")
    print(f"\n🇩🇪🎼✨ TRINITY SYSTEM TEST ABGESCHLOSSEN! ✨🎼🇩🇪")
    
    return results

if __name__ == "__main__":
    print("🇩🇪🎼✨ Iniciando Trinity System Comprehensive Test...")
    results = run_comprehensive_trinity_test()
    print(f"\n✨ Test completado con {len(results)} casos de prueba!")
