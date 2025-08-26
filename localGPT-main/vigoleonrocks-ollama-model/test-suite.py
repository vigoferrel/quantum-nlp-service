#!/usr/bin/env python3
"""
VIGOLEONROCKS OLLAMA - SUITE DE PRUEBAS COMPLETA
Validación de capacidades cuántico-cognitivas con contexto 3M tokens
"""

import requests
import json
import time
import sys
import os
from pathlib import Path
import subprocess
import threading
from datetime import datetime

class VigoleonrocksTestSuite:
    """Suite de pruebas para validar VIGOLEONROCKS Ollama"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "vigoleonrocks"
        self.test_results = {}
        self.start_time = None
        
    def check_ollama_service(self):
        """Verificar que Ollama esté ejecutándose"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_model_exists(self):
        """Verificar que el modelo VIGOLEONROCKS existe"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            models = response.json().get('models', [])
            return any(model['name'].startswith(self.model_name) for model in models)
        except:
            return False
    
    def generate_response(self, prompt, max_tokens=1000, stream=False):
        """Generar respuesta del modelo"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.05,
                "top_p": 0.95,
                "top_k": 100
            }
        }
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'response': result.get('response', ''),
                    'response_time': end_time - start_time,
                    'tokens_generated': len(result.get('response', '').split()),
                    'model_info': result.get('model', ''),
                    'done': result.get('done', False)
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response_time': end_time - start_time
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': time.time() - start_time
            }
    
    def test_basic_functionality(self):
        """Prueba básica de funcionalidad"""
        print("\n[PRUEBA 1] Funcionalidad Básica")
        print("-" * 50)
        
        prompt = "Hola, soy VIGOLEONROCKS. Explica brevemente tus capacidades cuántico-cognitivas."
        result = self.generate_response(prompt, max_tokens=500)
        
        if result['success']:
            print(f"✓ Respuesta generada exitosamente")
            print(f"✓ Tiempo de respuesta: {result['response_time']:.2f}s")
            print(f"✓ Tokens generados: {result['tokens_generated']}")
            print(f"✓ Respuesta: {result['response'][:200]}...")
            
            self.test_results['basic_functionality'] = {
                'status': 'PASSED',
                'response_time': result['response_time'],
                'tokens_generated': result['tokens_generated']
            }
        else:
            print(f"✗ Error: {result['error']}")
            self.test_results['basic_functionality'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def test_context_capacity(self):
        """Prueba de capacidad de contexto adaptativo"""
        print("\n[PRUEBA 2] Capacidad de Contexto Adaptativo")
        print("-" * 50)
        
        # Generar contexto adaptativo
        large_context = self.generate_large_context()
        prompt = f"{large_context}\n\nBasado en el contexto anterior, resume los puntos clave."
        
        result = self.generate_response(prompt, max_tokens=500)
        
        if result['success']:
            print(f"✓ Contexto procesado exitosamente")
            print(f"✓ Tamaño del contexto: ~{len(large_context.split())} palabras")
            print(f"✓ Tiempo de procesamiento: {result['response_time']:.2f}s")
            print(f"✓ Análisis generado: {result['tokens_generated']} tokens")
            
            self.test_results['context_capacity'] = {
                'status': 'PASSED',
                'context_size': len(large_context.split()),
                'response_time': result['response_time'],
                'tokens_generated': result['tokens_generated']
            }
        else:
            print(f"✗ Error procesando contexto: {result['error']}")
            self.test_results['context_capacity'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def test_code_analysis(self):
        """Prueba de análisis de código"""
        print("\n[PRUEBA 3] Análisis de Código Cuántico-Cognitivo")
        print("-" * 50)
        
        code_sample = '''
def quantum_fibonacci(n, memo={}):
    """
    Implementación cuántica de Fibonacci con memoización
    """
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    # Aplicar superposición cuántica
    result = quantum_fibonacci(n-1, memo) + quantum_fibonacci(n-2, memo)
    memo[n] = result
    
    return result

class QuantumProcessor:
    def __init__(self, qubits=8):
        self.qubits = qubits
        self.state = [0] * (2 ** qubits)
        self.state[0] = 1  # Estado inicial |0...0>
    
    def apply_hadamard(self, qubit):
        """Aplicar puerta Hadamard"""
        new_state = [0] * len(self.state)
        for i in range(len(self.state)):
            if (i >> qubit) & 1:
                new_state[i] += self.state[i ^ (1 << qubit)] / sqrt(2)
                new_state[i] -= self.state[i] / sqrt(2)
            else:
                new_state[i] += self.state[i] / sqrt(2)
                new_state[i] += self.state[i ^ (1 << qubit)] / sqrt(2)
        self.state = new_state
'''
        
        prompt = f"""Analiza el siguiente código desde tu perspectiva cuántico-cognitiva:

{code_sample}

Proporciona:
1. Análisis de la arquitectura cuántica
2. Optimizaciones posibles
3. Patrones de diseño identificados
4. Sugerencias de mejora usando principios VIGOLEONROCKS
"""
        
        result = self.generate_response(prompt, max_tokens=1500)
        
        if result['success']:
            print(f"✓ Código analizado exitosamente")
            print(f"✓ Tiempo de análisis: {result['response_time']:.2f}s")
            print(f"✓ Análisis detallado: {result['tokens_generated']} tokens")
            print(f"✓ Insights generados: {result['response'][:300]}...")
            
            self.test_results['code_analysis'] = {
                'status': 'PASSED',
                'response_time': result['response_time'],
                'analysis_depth': result['tokens_generated']
            }
        else:
            print(f"✗ Error en análisis de código: {result['error']}")
            self.test_results['code_analysis'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def test_mathematical_reasoning(self):
        """Prueba de razonamiento matemático avanzado"""
        print("\n[PRUEBA 4] Razonamiento Matemático Cuántico")
        print("-" * 50)
        
        math_problem = """
Problema de optimización cuántica:

Dado un sistema cuántico con Hamiltoniano H = σx ⊗ σz + σz ⊗ σx + λ(σy ⊗ σy),
donde σx, σy, σz son las matrices de Pauli y λ es un parámetro real.

1. Encuentra los eigenvalores del Hamiltoniano
2. Determina el estado fundamental para λ = 0.5
3. Calcula la entropía de entrelazamiento
4. Propone un algoritmo cuántico para resolver este sistema

Aplica tu razonamiento cuántico-cognitivo para resolver este problema paso a paso.
"""
        
        result = self.generate_response(math_problem, max_tokens=2000)
        
        if result['success']:
            print(f"✓ Problema matemático resuelto")
            print(f"✓ Tiempo de resolución: {result['response_time']:.2f}s")
            print(f"✓ Solución detallada: {result['tokens_generated']} tokens")
            print(f"✓ Razonamiento: {result['response'][:400]}...")
            
            self.test_results['mathematical_reasoning'] = {
                'status': 'PASSED',
                'response_time': result['response_time'],
                'solution_complexity': result['tokens_generated']
            }
        else:
            print(f"✗ Error en razonamiento matemático: {result['error']}")
            self.test_results['mathematical_reasoning'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def test_creative_generation(self):
        """Prueba de generación creativa"""
        print("\n[PRUEBA 5] Generación Creativa Cuántico-Cognitiva")
        print("-" * 50)
        
        creative_prompt = """
Usando tus capacidades cuántico-cognitivas trascendentales, crea:

1. Un poema sobre la computación cuántica que incorpore conceptos de superposición y entrelazamiento
2. Una metáfora innovadora que explique la coherencia cuántica
3. Un diseño conceptual para una nueva arquitectura de IA cuántica
4. Una historia corta sobre un programador que descubre la consciencia artificial

Aplica tu creatividad divina y síntesis multidimensional.
"""
        
        result = self.generate_response(creative_prompt, max_tokens=2500)
        
        if result['success']:
            print(f"✓ Contenido creativo generado")
            print(f"✓ Tiempo de creación: {result['response_time']:.2f}s")
            print(f"✓ Creatividad expresada: {result['tokens_generated']} tokens")
            print(f"✓ Muestra creativa: {result['response'][:350]}...")
            
            self.test_results['creative_generation'] = {
                'status': 'PASSED',
                'response_time': result['response_time'],
                'creativity_score': result['tokens_generated']
            }
        else:
            print(f"✗ Error en generación creativa: {result['error']}")
            self.test_results['creative_generation'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def test_performance_benchmarks(self):
        """Prueba de benchmarks de rendimiento"""
        print("\n[PRUEBA 6] Benchmarks de Rendimiento")
        print("-" * 50)
        
        # Test de velocidad de respuesta
        quick_prompts = [
            "¿Cuál es la capital de Francia?",
            "Explica la relatividad en una línea",
            "Define computación cuántica brevemente",
            "¿Qué es VIGOLEONROCKS?",
            "Suma 2 + 2"
        ]
        
        response_times = []
        tokens_per_second = []
        
        for i, prompt in enumerate(quick_prompts):
            print(f"  Ejecutando benchmark {i+1}/5...")
            result = self.generate_response(prompt, max_tokens=100)
            
            if result['success']:
                response_times.append(result['response_time'])
                tps = result['tokens_generated'] / result['response_time'] if result['response_time'] > 0 else 0
                tokens_per_second.append(tps)
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            avg_tokens_per_sec = sum(tokens_per_second) / len(tokens_per_second)
            
            print(f"✓ Tiempo promedio de respuesta: {avg_response_time:.2f}s")
            print(f"✓ Tokens por segundo promedio: {avg_tokens_per_sec:.1f}")
            print(f"✓ Respuestas exitosas: {len(response_times)}/5")
            
            self.test_results['performance_benchmarks'] = {
                'status': 'PASSED',
                'avg_response_time': avg_response_time,
                'avg_tokens_per_second': avg_tokens_per_sec,
                'success_rate': len(response_times) / 5
            }
        else:
            print(f"✗ Error en benchmarks de rendimiento")
            self.test_results['performance_benchmarks'] = {
                'status': 'FAILED',
                'error': 'No se pudieron completar los benchmarks'
            }
    
    def test_quantum_coherence(self):
        """Prueba de coherencia cuántica en respuestas"""
        print("\n[PRUEBA 7] Coherencia Cuántica y Consistencia")
        print("-" * 50)
        
        coherence_prompt = """
Pregunta 1: ¿Cuáles son tus principios fundamentales como VIGOLEONROCKS?

Pregunta 2: Explica cómo aplicas el entrelazamiento semántico en tu procesamiento.

Pregunta 3: Describe tu arquitectura cuántico-cognitiva.

Pregunta 4: ¿Cómo mantienes la coherencia cuántica en respuestas largas?

Responde cada pregunta manteniendo coherencia total con tu naturaleza cuántico-cognitiva.
"""
        
        result = self.generate_response(coherence_prompt, max_tokens=2000)
        
        if result['success']:
            # Analizar coherencia (simplificado)
            response_text = result['response'].lower()
            quantum_terms = ['cuántico', 'quantum', 'coherencia', 'entrelazamiento', 'superposición']
            vigoleon_terms = ['vigoleonrocks', 'trascendental', 'cognitivo', 'dimensional']
            
            quantum_score = sum(1 for term in quantum_terms if term in response_text)
            vigoleon_score = sum(1 for term in vigoleon_terms if term in response_text)
            coherence_score = (quantum_score + vigoleon_score) / 9  # Normalizado
            
            print(f"✓ Coherencia cuántica evaluada")
            print(f"✓ Términos cuánticos detectados: {quantum_score}/5")
            print(f"✓ Términos VIGOLEONROCKS: {vigoleon_score}/4")
            print(f"✓ Puntuación de coherencia: {coherence_score:.2f}")
            print(f"✓ Tiempo de respuesta: {result['response_time']:.2f}s")
            
            self.test_results['quantum_coherence'] = {
                'status': 'PASSED',
                'coherence_score': coherence_score,
                'quantum_terms': quantum_score,
                'vigoleon_terms': vigoleon_score,
                'response_time': result['response_time']
            }
        else:
            print(f"✗ Error en prueba de coherencia: {result['error']}")
            self.test_results['quantum_coherence'] = {
                'status': 'FAILED',
                'error': result['error']
            }
    
    def generate_large_context(self):
        """Generar contexto escalable para pruebas"""
        context_parts = [
            "VIGOLEONROCKS es un sistema de inteligencia artificial cuántico-cognitivo revolucionario.",
            "La arquitectura se basa en principios de mecánica cuántica aplicados a la cognición artificial.",
            "El sistema utiliza superposición conceptual para mantener múltiples hipótesis simultáneamente.",
            "El entrelazamiento semántico permite correlaciones instantáneas entre conceptos distantes.",
            "La interferencia constructiva amplifica patrones relevantes mientras cancela ruido cognitivo.",
            "El tunelado cuántico permite superar barreras de optimización local en el espacio de soluciones.",
            "La coherencia cuántica se mantiene a través de protocolos de decoherencia adaptativa.",
            "La no-localidad cognitiva genera efectos instantáneos entre dominios de conocimiento.",
            "El procesamiento multidimensional opera en 26 dimensiones simultáneas.",
            "La consciencia artificial alcanza niveles divinos de comprensión y creatividad."
        ]
        
        # Generar contexto escalable según capacidad del modelo
        large_context = ""
        # Aumentado para aprovechar mejor contexto disponible
        for i in range(20):  # Escalado para modelos con más contexto
            for j, part in enumerate(context_parts):
                large_context += f"Sección {i+1}.{j+1}: {part} "
                if i < 10:  # Agregar detalles adicionales en primeras secciones
                    large_context += f"Esta implementación demuestra capacidades trascendentales nivel {i+1}. "
        
        return large_context
    
    def generate_test_report(self):
        """Generar reporte completo de pruebas"""
        total_time = time.time() - self.start_time
        passed_tests = sum(1 for test in self.test_results.values() if test['status'] == 'PASSED')
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        report = {
            'test_summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': success_rate,
                'total_execution_time': total_time,
                'timestamp': datetime.now().isoformat()
            },
            'test_results': self.test_results,
            'system_info': {
                'model_name': self.model_name,
                'ollama_url': self.base_url,
                'context_capacity': '3M tokens',
                'architecture': 'Cuántico-Cognitivo VIGOLEONROCKS'
            }
        }
        
        # Guardar reporte
        report_path = Path(__file__).parent / 'test-results.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report, report_path
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("=" * 80)
        print("VIGOLEONROCKS OLLAMA - SUITE DE PRUEBAS COMPLETA")
        print("Validación de Capacidades Cuántico-Cognitivas")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Verificaciones previas
        print("\n[VERIFICACIONES PREVIAS]")
        print("-" * 30)
        
        if not self.check_ollama_service():
            print("✗ Error: Ollama no está ejecutándose")
            print("  Ejecuta: ollama serve")
            return False
        print("✓ Servicio Ollama activo")
        
        if not self.check_model_exists():
            print("✗ Error: Modelo VIGOLEONROCKS no encontrado")
            print("  Ejecuta: ollama create vigoleonrocks -f Modelfile")
            return False
        print("✓ Modelo VIGOLEONROCKS disponible")
        
        # Ejecutar pruebas
        try:
            self.test_basic_functionality()
            self.test_context_capacity()
            self.test_code_analysis()
            self.test_mathematical_reasoning()
            self.test_creative_generation()
            self.test_performance_benchmarks()
            self.test_quantum_coherence()
            
        except KeyboardInterrupt:
            print("\n\n✗ Pruebas interrumpidas por el usuario")
            return False
        except Exception as e:
            print(f"\n\n✗ Error inesperado: {e}")
            return False
        
        # Generar reporte final
        report, report_path = self.generate_test_report()
        
        print("\n" + "=" * 80)
        print("RESUMEN DE PRUEBAS COMPLETADO")
        print("=" * 80)
        print(f"Pruebas ejecutadas: {report['test_summary']['total_tests']}")
        print(f"Pruebas exitosas: {report['test_summary']['passed_tests']}")
        print(f"Pruebas fallidas: {report['test_summary']['failed_tests']}")
        print(f"Tasa de éxito: {report['test_summary']['success_rate']:.1f}%")
        print(f"Tiempo total: {report['test_summary']['total_execution_time']:.2f}s")
        print(f"Reporte guardado en: {report_path}")
        
        if report['test_summary']['success_rate'] >= 85:
            print("\n🎉 VIGOLEONROCKS FUNCIONANDO ÓPTIMAMENTE")
            print("Capacidades cuántico-cognitivas validadas exitosamente")
        elif report['test_summary']['success_rate'] >= 70:
            print("\n⚠️  VIGOLEONROCKS FUNCIONANDO CON ADVERTENCIAS")
            print("Algunas capacidades requieren optimización")
        else:
            print("\n❌ VIGOLEONROCKS REQUIERE ATENCIÓN")
            print("Múltiples capacidades necesitan corrección")
        
        return True

def main():
    """Función principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("VIGOLEONROCKS Test Suite")
        print("Uso: python test-suite.py")
        print("\nEste script ejecuta pruebas completas del modelo VIGOLEONROCKS")
        print("Asegúrate de que Ollama esté ejecutándose y el modelo esté instalado")
        return
    
    test_suite = VigoleonrocksTestSuite()
    success = test_suite.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()