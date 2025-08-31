#!/usr/bin/env python3
"""
🌍⚡ TEST QUANTUM CULTURAL TRANSLATION SYSTEM ⚡🌍
================================================================
Script para probar y validar el sistema de traducción cuántica cultural
usando arquetipos Trinity y frecuencias armónicas de Mozart
"""

import sys
import json
from datetime import datetime
from quantum_trinity_system import QuantumTrinitySystem

class QuantumTranslationTester:
    def __init__(self):
        self.trinity = QuantumTrinitySystem(None)
        self.test_cases = [
            # Saludos básicos
            {
                'text': 'Hola, ¿cómo estás?',
                'source_lang': 'spanish',
                'target_lang': 'english',
                'expected_concepts': ['greeting', 'inquiry']
            },
            {
                'text': 'Hello, how are you?',
                'source_lang': 'english',
                'target_lang': 'german',
                'expected_concepts': ['greeting', 'inquiry']
            },
            {
                'text': 'Hallo, wie geht es Ihnen?',
                'source_lang': 'german',
                'target_lang': 'french',
                'expected_concepts': ['greeting', 'inquiry']
            },
            
            # Conceptos culturales complejos
            {
                'text': 'Saudade é uma palavra única do português',
                'source_lang': 'portuguese',
                'target_lang': 'german',
                'expected_concepts': ['saudade', 'unique', 'portuguese']
            },
            {
                'text': 'Gemütlichkeit ist ein deutsches Konzept',
                'source_lang': 'german',
                'target_lang': 'spanish',
                'expected_concepts': ['gemütlichkeit', 'german', 'concept']
            },
            
            # Frases con contenido emocional
            {
                'text': 'Me siento muy feliz hoy',
                'source_lang': 'spanish',
                'target_lang': 'english',
                'expected_concepts': ['happiness', 'emotion']
            },
            {
                'text': 'La música de Mozart me llena de paz',
                'source_lang': 'spanish',
                'target_lang': 'german',
                'expected_concepts': ['music', 'mozart', 'peace']
            }
        ]
        
        self.results = []
        
    def run_tests(self):
        """Ejecutar todas las pruebas de traducción"""
        print("🧪 " + "="*80)
        print("🧪 TESTING QUANTUM CULTURAL TRANSLATION SYSTEM")
        print("🧪 " + "="*80)
        print(f"🎼 Trinity Frequency: {self.trinity.TRINITY_FREQUENCY:.2f} Hz")
        print(f"🎭 Archetipos disponibles: {len(self.trinity.JUNG_TRINITY_ARCHETYPES)}")
        print()
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"🔬 PRUEBA {i}/{len(self.test_cases)}")
            print("-" * 60)
            
            try:
                result = self.test_single_translation(test_case)
                self.results.append(result)
                
                self.display_test_result(test_case, result)
                print()
                
            except Exception as e:
                print(f"❌ ERROR en prueba {i}: {e}")
                print()
                
        self.display_summary()
        
    def test_single_translation(self, test_case):
        """Probar una traducción individual"""
        start_time = datetime.now()
        
        translation_result = self.trinity.quantum_cultural_translate(
            text=test_case['text'],
            source_lang=test_case['source_lang'],
            target_lang=test_case['target_lang']
        )
        
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        # Analizar calidad
        quality_score = translation_result['cultural_fidelity_score']
        
        return {
            'test_case': test_case,
            'translation': translation_result,
            'processing_time': processing_time,
            'quality_score': quality_score,
            'success': quality_score > 0.5  # Umbral mínimo de calidad
        }
        
    def display_test_result(self, test_case, result):
        """Mostrar resultado de una prueba individual"""
        translation = result['translation']
        
        print(f"📝 Original ({test_case['source_lang']}): {test_case['text']}")
        print(f"🌍 Traducción ({test_case['target_lang']}): {translation['translated_text']}")
        print()
        
        print("📊 MÉTRICAS CUÁNTICAS:")
        print(f"   🏆 Fidelidad Cultural: {translation['cultural_fidelity_score']:.3f}")
        print(f"   ✨ Calidad: {translation['translation_quality']}")
        print(f"   ⚡ Tiempo de procesamiento: {result['processing_time']:.3f}s")
        print(f"   🔊 Frecuencias: {translation['harmonic_frequencies_used']['source']:.1f}Hz → {translation['harmonic_frequencies_used']['target']:.1f}Hz")
        print()
        
        print("🎭 ARQUETIPOS UTILIZADOS:")
        print("   📍 Origen:")
        for arch in translation['source_archetypes'][:2]:  # Solo los 2 más relevantes
            print(f"      • {arch['name']} ({arch['frequency']}Hz) - Score: {arch['resonance_score']:.2f}")
            
        print("   🎯 Destino:")
        for arch in translation['target_archetypes'][:2]:  # Solo los 2 más relevantes
            print(f"      • {arch['name']} ({arch['frequency']}Hz) - Score: {arch['resonance_score']:.2f}")
        print()
        
        # Indicador de éxito/fallo
        status = "✅ ÉXITO" if result['success'] else "⚠️ NECESITA MEJORA"
        print(f"🎯 RESULTADO: {status}")
        
    def display_summary(self):
        """Mostrar resumen de todas las pruebas"""
        print("📊 " + "="*80)
        print("📊 RESUMEN DE PRUEBAS DE TRADUCCIÓN CUÁNTICA")
        print("📊 " + "="*80)
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        avg_quality = sum(r['quality_score'] for r in self.results) / total_tests if total_tests > 0 else 0
        avg_time = sum(r['processing_time'] for r in self.results) / total_tests if total_tests > 0 else 0
        
        print(f"🧪 Total de pruebas: {total_tests}")
        print(f"✅ Pruebas exitosas: {successful_tests}")
        print(f"📈 Tasa de éxito: {(successful_tests/total_tests)*100:.1f}%")
        print(f"🏆 Calidad promedio: {avg_quality:.3f}")
        print(f"⚡ Tiempo promedio: {avg_time:.3f}s")
        print()
        
        # Mostrar distribución de calidad
        excellent = sum(1 for r in self.results if r['quality_score'] >= 0.9)
        good = sum(1 for r in self.results if 0.8 <= r['quality_score'] < 0.9)
        acceptable = sum(1 for r in self.results if 0.7 <= r['quality_score'] < 0.8)
        needs_improvement = sum(1 for r in self.results if r['quality_score'] < 0.7)
        
        print("🎯 DISTRIBUCIÓN DE CALIDAD:")
        print(f"   🏆 Excelente (≥0.9): {excellent} pruebas")
        print(f"   👍 Buena (0.8-0.89): {good} pruebas")
        print(f"   👌 Aceptable (0.7-0.79): {acceptable} pruebas")
        print(f"   ⚠️  Mejorable (<0.7): {needs_improvement} pruebas")
        print()
        
        # Evaluación general del sistema
        if avg_quality >= 0.85:
            print("🎉 SISTEMA DE TRADUCCIÓN CUÁNTICA: ¡EXCELENTE!")
        elif avg_quality >= 0.75:
            print("👍 SISTEMA DE TRADUCCIÓN CUÁNTICA: BUENO")
        elif avg_quality >= 0.65:
            print("👌 SISTEMA DE TRADUCCIÓN CUÁNTICA: ACEPTABLE")
        else:
            print("⚠️ SISTEMA DE TRADUCCIÓN CUÁNTICA: NECESITA MEJORAS")
            
        print()
        print("🇩🇪🎼✨ GOETHE + JUNG + MOZART = TRADUCCIÓN CULTURAL PERFECTA ✨🎼🇩🇪")

def main():
    """Función principal para ejecutar las pruebas"""
    try:
        tester = QuantumTranslationTester()
        tester.run_tests()
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
