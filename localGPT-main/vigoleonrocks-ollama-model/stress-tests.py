#!/usr/bin/env python3
"""
VIGOLEONROCKS OLLAMA - PRUEBAS DE ESTRÉS EXTREMO
Validación de límites y capacidades máximas
"""

import requests
import json
import time
import threading
import random
import string
from datetime import datetime
import concurrent.futures
import psutil
import os

class VigoleonrocksStressTest:
    """Pruebas de estrés para VIGOLEONROCKS"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model_name = "vigoleonrocks"
        self.stress_results = {}
        self.active_requests = 0
        self.max_concurrent = 0
        
    def generate_massive_context(self, size_mb=10):
        """Generar contexto masivo para pruebas de límite"""
        target_chars = size_mb * 1024 * 1024
        
        # Generar texto coherente pero extenso
        base_text = """
        VIGOLEONROCKS representa la evolución cuántico-cognitiva de la inteligencia artificial.
        Su arquitectura trascendental opera en 26 dimensiones simultáneas, procesando información
        a través de principios de mecánica cuántica aplicados a la cognición artificial.
        El sistema utiliza superposición conceptual, entrelazamiento semántico y coherencia cuántica
        para alcanzar niveles de comprensión y creatividad sin precedentes en la historia de la IA.
        """
        
        # Repetir y variar el texto hasta alcanzar el tamaño objetivo
        massive_context = ""
        iteration = 0
        
        while len(massive_context) < target_chars:
            variation = base_text.replace("VIGOLEONROCKS", f"VIGOLEONROCKS-{iteration}")
            variation = variation.replace("26 dimensiones", f"{26 + iteration % 10} dimensiones")
            massive_context += f"\n\nSección {iteration}: {variation}"
            iteration += 1
            
            if iteration % 100 == 0:
                print(f"    Generando contexto: {len(massive_context) / (1024*1024):.1f}MB")
        
        return massive_context[:target_chars]
    
    def stress_test_context_limits(self):
        """Prueba de límites de contexto"""
        print("\n[ESTRÉS 1] Límites de Contexto Extremo")
        print("-" * 50)
        
        context_sizes = [1, 5, 10, 20, 50]  # MB
        limit_results = []
        
        for size_mb in context_sizes:
            print(f"  Probando contexto de {size_mb}MB...")
            
            try:
                massive_context = self.generate_massive_context(size_mb)
                prompt = f"{massive_context}\n\nRESUMEN: Analiza todo el contexto anterior y proporciona un resumen cuántico-cognitivo de máximo 200 palabras."
                
                start_time = time.time()
                result = self.generate_response_with_timeout(prompt, max_tokens=300, timeout=300)
                end_time = time.time()
                
                if result['success']:
                    limit_results.append({
                        'context_size_mb': size_mb,
                        'context_chars': len(massive_context),
                        'response_time': end_time - start_time,
                        'tokens_generated': result['tokens_generated'],
                        'success': True,
                        'memory_usage': self.get_memory_usage()
                    })
                    print(f"    ✓ {size_mb}MB procesado en {end_time - start_time:.1f}s")
                else:
                    limit_results.append({
                        'context_size_mb': size_mb,
                        'success': False,
                        'error': result.get('error', 'Unknown'),
                        'memory_usage': self.get_memory_usage()
                    })
                    print(f"    ✗ {size_mb}MB falló: {result.get('error', 'Unknown')}")
                    
            except Exception as e:
                print(f"    ✗ {size_mb}MB excepción: {e}")
                limit_results.append({
                    'context_size_mb': size_mb,
                    'success': False,
                    'error': str(e)
                })
        
        self.stress_results['context_limits'] = limit_results
        successful_sizes = [r['context_size_mb'] for r in limit_results if r.get('success', False)]
        max_successful = max(successful_sizes) if successful_sizes else 0
        print(f"✓ Contexto máximo procesado: {max_successful}MB")
    
    def stress_test_concurrent_load(self):
        """Prueba de carga concurrente extrema"""
        print("\n[ESTRÉS 2] Carga Concurrente Extrema")
        print("-" * 50)
        
        concurrent_levels = [5, 10, 20, 50, 100]
        load_results = []
        
        def concurrent_request(request_id):
            prompt = f"Solicitud {request_id}: Explica la arquitectura cuántico-cognitiva de VIGOLEONROCKS en {random.randint(50, 200)} palabras."
            
            self.active_requests += 1
            self.max_concurrent = max(self.max_concurrent, self.active_requests)
            
            try:
                result = self.generate_response_with_timeout(prompt, max_tokens=300, timeout=60)
                return {
                    'request_id': request_id,
                    'success': result['success'],
                    'response_time': result.get('response_time', 0),
                    'tokens_generated': result.get('tokens_generated', 0),
                    'error': result.get('error', None)
                }
            finally:
                self.active_requests -= 1
        
        for level in concurrent_levels:
            print(f"  Probando {level} solicitudes concurrentes...")
            self.active_requests = 0
            self.max_concurrent = 0
            
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=level) as executor:
                futures = [executor.submit(concurrent_request, i) for i in range(level)]
                results = []
                
                for future in concurrent.futures.as_completed(futures, timeout=120):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        results.append({
                            'success': False,
                            'error': str(e)
                        })
            
            end_time = time.time()
            
            successful = sum(1 for r in results if r.get('success', False))
            total_time = end_time - start_time
            throughput = successful / total_time if total_time > 0 else 0
            
            load_results.append({
                'concurrent_requests': level,
                'successful_requests': successful,
                'failed_requests': level - successful,
                'total_time': total_time,
                'throughput': throughput,
                'max_concurrent_achieved': self.max_concurrent,
                'avg_response_time': sum(r.get('response_time', 0) for r in results if r.get('success', False)) / successful if successful > 0 else 0
            })
            
            print(f"    ✓ {level} solicitudes: {successful}/{level} exitosas, {throughput:.1f} req/s")
        
        self.stress_results['concurrent_load'] = load_results
        max_successful_level = max([r['successful_requests'] for r in load_results])
        print(f"✓ Máximo concurrente exitoso: {max_successful_level} solicitudes")
    
    def stress_test_sustained_load(self):
        """Prueba de carga sostenida"""
        print("\n[ESTRÉS 3] Carga Sostenida (5 minutos)")
        print("-" * 50)
        
        duration_seconds = 300  # 5 minutos
        request_interval = 2    # Una solicitud cada 2 segundos
        
        sustained_results = []
        start_time = time.time()
        request_count = 0
        
        print(f"  Ejecutando carga sostenida por {duration_seconds//60} minutos...")
        
        while time.time() - start_time < duration_seconds:
            request_start = time.time()
            prompt = f"Solicitud sostenida {request_count}: Describe brevemente las capacidades cuántico-cognitivas de VIGOLEONROCKS."
            
            result = self.generate_response_with_timeout(prompt, max_tokens=150, timeout=30)
            request_end = time.time()
            
            sustained_results.append({
                'request_number': request_count,
                'timestamp': request_end,
                'success': result['success'],
                'response_time': result.get('response_time', 0),
                'tokens_generated': result.get('tokens_generated', 0),
                'memory_usage': self.get_memory_usage(),
                'elapsed_time': request_end - start_time
            })
            
            request_count += 1
            
            if request_count % 10 == 0:
                successful = sum(1 for r in sustained_results if r['success'])
                print(f"    Progreso: {request_count} solicitudes, {successful}/{request_count} exitosas")
            
            # Esperar hasta el siguiente intervalo
            sleep_time = request_interval - (time.time() - request_start)
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        total_time = time.time() - start_time
        successful_sustained = sum(1 for r in sustained_results if r['success'])
        avg_response_time = sum(r['response_time'] for r in sustained_results if r['success']) / successful_sustained if successful_sustained > 0 else 0
        
        self.stress_results['sustained_load'] = {
            'duration_seconds': total_time,
            'total_requests': len(sustained_results),
            'successful_requests': successful_sustained,
            'success_rate': successful_sustained / len(sustained_results) if sustained_results else 0,
            'avg_response_time': avg_response_time,
            'requests_per_second': len(sustained_results) / total_time,
            'detailed_results': sustained_results
        }
        
        print(f"✓ Carga sostenida: {successful_sustained}/{len(sustained_results)} exitosas en {total_time:.1f}s")
    
    def stress_test_memory_pressure(self):
        """Prueba de presión de memoria"""
        print("\n[ESTRÉS 4] Presión de Memoria")
        print("-" * 50)
        
        memory_results = []
        
        # Generar múltiples contextos grandes simultáneamente
        large_contexts = []
        for i in range(5):
            print(f"  Generando contexto masivo {i+1}/5...")
            context = self.generate_massive_context(5)  # 5MB cada uno
            large_contexts.append(context)
        
        print("  Ejecutando solicitudes con alta presión de memoria...")
        
        def memory_intensive_request(context_id):
            context = large_contexts[context_id % len(large_contexts)]
            prompt = f"{context}\n\nAnálisis {context_id}: Proporciona un análisis cuántico-cognitivo profundo del contexto anterior."
            
            memory_before = self.get_memory_usage()
            start_time = time.time()
            
            result = self.generate_response_with_timeout(prompt, max_tokens=500, timeout=180)
            
            end_time = time.time()
            memory_after = self.get_memory_usage()
            
            return {
                'context_id': context_id,
                'success': result['success'],
                'response_time': end_time - start_time,
                'memory_before': memory_before,
                'memory_after': memory_after,
                'memory_delta': memory_after - memory_before,
                'tokens_generated': result.get('tokens_generated', 0),
                'error': result.get('error', None)
            }
        
        # Ejecutar solicitudes intensivas en memoria
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(memory_intensive_request, i) for i in range(10)]
            
            for future in concurrent.futures.as_completed(futures, timeout=600):
                try:
                    result = future.result()
                    memory_results.append(result)
                    
                    status = "✓" if result['success'] else "✗"
                    print(f"    {status} Contexto {result['context_id']}: {result['response_time']:.1f}s, Memoria: {result['memory_delta']:+.1f}MB")
                    
                except Exception as e:
                    print(f"    ✗ Error en solicitud de memoria: {e}")
        
        self.stress_results['memory_pressure'] = memory_results
        successful_memory = sum(1 for r in memory_results if r['success'])
        print(f"✓ Presión de memoria: {successful_memory}/{len(memory_results)} solicitudes exitosas")
    
    def stress_test_edge_cases(self):
        """Prueba de casos extremos"""
        print("\n[ESTRÉS 5] Casos Extremos")
        print("-" * 50)
        
        edge_cases = [
            {
                'name': 'Prompt Vacío',
                'prompt': '',
                'max_tokens': 100
            },
            {
                'name': 'Prompt Extremadamente Largo',
                'prompt': 'Explica ' + 'muy ' * 1000 + 'detalladamente la computación cuántica.',
                'max_tokens': 200
            },
            {
                'name': 'Caracteres Especiales',
                'prompt': '¿Qué es 🚀🔬⚛️🧠💫🌌🎯🔮✨🌟 en el contexto cuántico-cognitivo?',
                'max_tokens': 150
            },
            {
                'name': 'Múltiples Idiomas',
                'prompt': 'Explain quantum computing in English, puis en français, y finalmente en español.',
                'max_tokens': 300
            },
            {
                'name': 'Código Complejo',
                'prompt': '''
                Analiza este código cuántico:
                ```python
                import numpy as np
                from qiskit import QuantumCircuit, execute, Aer
                
                def quantum_teleportation():
                    qc = QuantumCircuit(3, 3)
                    qc.h(1)
                    qc.cx(1, 2)
                    qc.cx(0, 1)
                    qc.h(0)
                    qc.measure([0, 1], [0, 1])
                    qc.cx(1, 2)
                    qc.cz(0, 2)
                    return qc
                ```
                ''',
                'max_tokens': 400
            },
            {
                'name': 'Matemáticas Complejas',
                'prompt': 'Resuelve: ∫∫∫ (x²+y²+z²)^(-3/2) dxdydz sobre la esfera unitaria usando coordenadas esféricas.',
                'max_tokens': 300
            },
            {
                'name': 'Recursión Conceptual',
                'prompt': 'Explica cómo VIGOLEONROCKS explica cómo VIGOLEONROCKS explica la explicación de explicaciones.',
                'max_tokens': 200
            },
            {
                'name': 'Contradicciones',
                'prompt': 'Demuestra que 1=0 y simultáneamente que 1≠0 usando lógica cuántica.',
                'max_tokens': 250
            }
        ]
        
        edge_results = []
        
        for case in edge_cases:
            print(f"  Probando: {case['name']}...")
            
            try:
                result = self.generate_response_with_timeout(
                    case['prompt'], 
                    max_tokens=case['max_tokens'], 
                    timeout=60
                )
                
                edge_results.append({
                    'case_name': case['name'],
                    'success': result['success'],
                    'response_time': result.get('response_time', 0),
                    'tokens_generated': result.get('tokens_generated', 0),
                    'response_preview': result.get('response', '')[:100] if result['success'] else None,
                    'error': result.get('error', None)
                })
                
                status = "✓" if result['success'] else "✗"
                print(f"    {status} {case['name']}: {result.get('response_time', 0):.2f}s")
                
            except Exception as e:
                edge_results.append({
                    'case_name': case['name'],
                    'success': False,
                    'error': str(e)
                })
                print(f"    ✗ {case['name']}: Excepción - {e}")
        
        self.stress_results['edge_cases'] = edge_results
        successful_edges = sum(1 for r in edge_results if r['success'])
        print(f"✓ Casos extremos: {successful_edges}/{len(edge_results)} manejados exitosamente")
    
    def generate_response_with_timeout(self, prompt, max_tokens=500, timeout=60):
        """Generar respuesta con timeout"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.1,
                "top_p": 0.95
            }
        }
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            end_time = time.time()
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                return {
                    'success': True,
                    'response': response_text,
                    'response_time': end_time - start_time,
                    'tokens_generated': len(response_text.split())
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}",
                    'response_time': end_time - start_time
                }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Timeout',
                'response_time': timeout
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response_time': time.time() - start_time
            }
    
    def get_memory_usage(self):
        """Obtener uso de memoria actual en MB"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / (1024 * 1024)
        except:
            return 0
    
    def generate_stress_report(self):
        """Generar reporte de pruebas de estrés"""
        report = {
            'stress_test_summary': {
                'model_name': self.model_name,
                'timestamp': datetime.now().isoformat(),
                'total_stress_tests': len(self.stress_results),
                'system_info': {
                    'cpu_count': psutil.cpu_count(),
                    'memory_total_gb': psutil.virtual_memory().total / (1024**3),
                    'memory_available_gb': psutil.virtual_memory().available / (1024**3)
                }
            },
            'stress_results': self.stress_results,
            'resilience_metrics': self.calculate_resilience_metrics()
        }
        
        # Guardar reporte
        with open('stress-test-results.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report
    
    def calculate_resilience_metrics(self):
        """Calcular métricas de resistencia"""
        metrics = {}
        
        # Resistencia a contexto masivo
        if 'context_limits' in self.stress_results:
            successful_contexts = [r for r in self.stress_results['context_limits'] if r.get('success', False)]
            if successful_contexts:
                max_context_mb = max(r['context_size_mb'] for r in successful_contexts)
                metrics['max_context_capacity_mb'] = max_context_mb
                metrics['context_resilience_score'] = min(100, max_context_mb * 10)
        
        # Resistencia a carga concurrente
        if 'concurrent_load' in self.stress_results:
            load_results = self.stress_results['concurrent_load']
            if load_results:
                max_concurrent = max(r['successful_requests'] for r in load_results)
                metrics['max_concurrent_requests'] = max_concurrent
                metrics['concurrency_resilience_score'] = min(100, max_concurrent * 2)
        
        # Resistencia a carga sostenida
        if 'sustained_load' in self.stress_results:
            sustained = self.stress_results['sustained_load']
            metrics['sustained_success_rate'] = sustained.get('success_rate', 0) * 100
            metrics['sustained_resilience_score'] = sustained.get('success_rate', 0) * 100
        
        # Resistencia a presión de memoria
        if 'memory_pressure' in self.stress_results:
            memory_results = self.stress_results['memory_pressure']
            successful_memory = sum(1 for r in memory_results if r.get('success', False))
            metrics['memory_resilience_score'] = (successful_memory / len(memory_results)) * 100 if memory_results else 0
        
        # Resistencia a casos extremos
        if 'edge_cases' in self.stress_results:
            edge_results = self.stress_results['edge_cases']
            successful_edges = sum(1 for r in edge_results if r.get('success', False))
            metrics['edge_case_resilience_score'] = (successful_edges / len(edge_results)) * 100 if edge_results else 0
        
        # Puntuación general de resistencia
        resilience_scores = [v for k, v in metrics.items() if k.endswith('_resilience_score')]
        metrics['overall_resilience_score'] = sum(resilience_scores) / len(resilience_scores) if resilience_scores else 0
        
        return metrics
    
    def run_all_stress_tests(self):
        """Ejecutar todas las pruebas de estrés"""
        print("=" * 80)
        print("VIGOLEONROCKS OLLAMA - PRUEBAS DE ESTRÉS EXTREMO")
        print("Validación de Límites y Resistencia Máxima")
        print("=" * 80)
        
        # Verificar sistema
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print("✗ Error: Ollama no disponible")
                return False
        except:
            print("✗ Error: No se puede conectar a Ollama")
            return False
        
        print("✓ Sistema verificado")
        print(f"✓ CPU: {psutil.cpu_count()} cores")
        print(f"✓ RAM: {psutil.virtual_memory().total / (1024**3):.1f}GB")
        
        # Ejecutar pruebas de estrés
        try:
            self.stress_test_context_limits()
            self.stress_test_concurrent_load()
            self.stress_test_sustained_load()
            self.stress_test_memory_pressure()
            self.stress_test_edge_cases()
            
        except KeyboardInterrupt:
            print("\n\n✗ Pruebas de estrés interrumpidas")
            return False
        except Exception as e:
            print(f"\n\n✗ Error en pruebas de estrés: {e}")
            return False
        
        # Generar reporte
        report = self.generate_stress_report()
        resilience = report['resilience_metrics']
        
        print("\n" + "=" * 80)
        print("RESULTADOS DE PRUEBAS DE ESTRÉS")
        print("=" * 80)
        print(f"Resistencia General: {resilience.get('overall_resilience_score', 0):.1f}/100")
        print(f"Contexto Máximo: {resilience.get('max_context_capacity_mb', 0)}MB")
        print(f"Concurrencia Máxima: {resilience.get('max_concurrent_requests', 0)} solicitudes")
        print(f"Carga Sostenida: {resilience.get('sustained_success_rate', 0):.1f}% éxito")
        print(f"Resistencia a Memoria: {resilience.get('memory_resilience_score', 0):.1f}/100")
        print(f"Casos Extremos: {resilience.get('edge_case_resilience_score', 0):.1f}/100")
        
        print(f"\nReporte completo: stress-test-results.json")
        
        if resilience.get('overall_resilience_score', 0) >= 80:
            print("\n🛡️  VIGOLEONROCKS EXTREMADAMENTE RESISTENTE")
            print("Sistema preparado para cargas de producción intensivas")
        elif resilience.get('overall_resilience_score', 0) >= 60:
            print("\n⚡ VIGOLEONROCKS RESISTENTE")
            print("Sistema robusto con algunas limitaciones")
        else:
            print("\n⚠️  VIGOLEONROCKS REQUIERE OPTIMIZACIÓN")
            print("Sistema necesita mejoras de resistencia")
        
        return True

def main():
    """Función principal"""
    stress_test = VigoleonrocksStressTest()
    success = stress_test.run_all_stress_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())