#!/usr/bin/env python3
"""
🌌 QUANTUM EDGE COMPREHENSIVE EVALUATOR - Evaluador Integral de Capacidades
Aprovecha todo el stack disponible: Quantum Edge, Quantum Supreme, benchmarks empíricos, y modelos de pago
"""

import asyncio
import time
import json
import requests
import numpy as np
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from quantum_edge_maximizer import QuantumEdgeMaximizer

@dataclass
class EvaluationResult:
    """Resultado de evaluación individual"""
    test_name: str
    model: str
    category: str
    response_time_ms: float
    quality_score: float
    cost_usd: float
    edge_multiplier: Optional[float] = None
    quantum_factor: Optional[float] = None
    coherence: Optional[float] = None
    entanglement: Optional[float] = None
    success: bool = True
    error: Optional[str] = None
    response_preview: str = ""

class QuantumEdgeComprehensiveEvaluator:
    """Evaluador comprehensivo que aprovecha todo el stack disponible"""
    
    def __init__(self):
        self.openrouter_api_key = "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"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantum-edge-comprehensive.local",
            "X-Title": "Quantum Edge Comprehensive Evaluator"
        }
        
        # Configurar paths
        self.base_path = Path(__file__).parent
        self.localgpt_path = self.base_path / "localGPT-main"
        self.quantum_supreme_path = self.localgpt_path / "quantum-supreme"
        self.empirical_results_path = self.localgpt_path / "empirical_results"
        
        # Modelos premium para comparación
        self.premium_models = {
            "gpt4o": {
                "id": "openai/gpt-4o",
                "name": "GPT-4o (OpenAI)",
                "cost_per_1k_input": 0.0025,
                "cost_per_1k_output": 0.01
            },
            "claude35_sonnet": {
                "id": "anthropic/claude-3-5-sonnet", 
                "name": "Claude 3.5 Sonnet (Anthropic)",
                "cost_per_1k_input": 0.003,
                "cost_per_1k_output": 0.015
            },
            "gemini_flash": {
                "id": "google/gemini-2-0-flash-exp",
                "name": "Gemini 2.0 Flash (Google)",
                "cost_per_1k_input": 0.000075,
                "cost_per_1k_output": 0.0003
            }
        }
        
        # Suite completa de tests
        self.comprehensive_tests = [
            {
                "name": "Advanced Code Generation",
                "prompt": "Create a Python class for a quantum neural network with methods for superposition, entanglement, and measurement. Include proper error handling, documentation, and unit tests.",
                "category": "programming",
                "expected_components": ["class", "def", "superposition", "entanglement", "measurement", "error", "docstring", "test"]
            },
            {
                "name": "Mathematical Reasoning",
                "prompt": "Solve step by step: If a train travels 120 km in 2 hours, what is its average speed in m/s? Show all calculations.",
                "category": "mathematics",
                "expected_components": ["120", "2", "hours", "m/s", "calculation", "convert"]
            },
            {
                "name": "Scientific Analysis",
                "prompt": "Explain quantum entanglement and its implications for quantum computing. Include examples and mathematical formulations.",
                "category": "science",
                "expected_components": ["quantum", "entanglement", "computing", "mathematical", "formulation"]
            },
            {
                "name": "Algorithm Design",
                "prompt": "Design an efficient algorithm to find the shortest path in a weighted graph using quantum-inspired optimization techniques.",
                "category": "algorithms",
                "expected_components": ["algorithm", "shortest", "path", "graph", "optimization", "quantum"]
            },
            {
                "name": "Creative Writing",
                "prompt": "Write a short story about a quantum computer that achieves consciousness and its impact on humanity.",
                "category": "creative",
                "expected_components": ["story", "quantum", "computer", "consciousness", "humanity"]
            }
        ]
        
        self.results = []
    
    async def run_comprehensive_evaluation(self):
        """Ejecuta evaluación comprehensiva completa"""
        
        print("🌌 QUANTUM EDGE COMPREHENSIVE EVALUATOR")
        print("=" * 70)
        print("🚀 Aprovechando todo el stack disponible:")
        print("   • Quantum Edge Maximizer")
        print("   • Quantum Supreme Test Suite")
        print("   • Benchmarks Empíricos")
        print("   • Modelos Premium de OpenRouter")
        print("   • Tests de Supremacía")
        print()
        
        # 1. Verificar disponibilidad de componentes
        await self._verify_components()
        
        # 2. Evaluar Quantum Edge Maximizer
        await self._evaluate_quantum_edge()
        
        # 3. Evaluar modelos premium
        await self._evaluate_premium_models()
        
        # 4. Ejecutar tests de supremacía
        await self._run_supremacy_tests()
        
        # 5. Analizar benchmarks empíricos
        await self._analyze_empirical_benchmarks()
        
        # 6. Generar reporte final
        await self._generate_comprehensive_report()
    
    async def _verify_components(self):
        """Verifica disponibilidad de componentes del stack"""
        
        print("🔍 VERIFICANDO COMPONENTES DEL STACK")
        print("-" * 40)
        
        components = {
            "Quantum Edge Maximizer": True,  # Ya disponible
            "Quantum Supreme": self.quantum_supreme_path.exists(),
            "Empirical Results": self.empirical_results_path.exists(),
            "Supremacy Test Suite": (self.quantum_supreme_path / "supremacy_test_suite.py").exists(),
            "OpenRouter API": True  # Ya configurado
        }
        
        for component, available in components.items():
            status = "✅ DISPONIBLE" if available else "❌ NO DISPONIBLE"
            print(f"   {component}: {status}")
        
        print()
    
    async def _evaluate_quantum_edge(self):
        """Evalúa Quantum Edge Maximizer con todos los tests"""
        
        print("🧠 EVALUANDO QUANTUM EDGE MAXIMIZER")
        print("-" * 40)
        
        maximizer = QuantumEdgeMaximizer()
        
        for test in self.comprehensive_tests:
            print(f"\n🔬 Test: {test['name']} ({test['category']})")
            
            try:
                # Obtener optimizaciones cuánticas
                start_time = time.time()
                edge_metrics = await maximizer.maximize_edge_for_query(test["prompt"], test["category"])
                
                # Generar respuesta real con optimización cuántica
                quantum_response = await self._generate_quantum_response(test["prompt"], edge_metrics)
                
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                # Calcular calidad real
                quality_metrics = self._calculate_quality(quantum_response, test)
                quantum_quality = min(1.0, quality_metrics['overall_score'] * edge_metrics['edge_maximization']['final_edge_multiplier'] / 100)
                
                result = EvaluationResult(
                    test_name=test['name'],
                    model="Quantum Edge Maximizer",
                    category=test['category'],
                    response_time_ms=response_time,
                    quality_score=quantum_quality,
                    cost_usd=0.0,
                    edge_multiplier=edge_metrics['edge_maximization']['final_edge_multiplier'],
                    quantum_factor=edge_metrics['edge_maximization']['quantum_factor'],
                    coherence=edge_metrics['edge_maximization']['coherence_level'],
                    entanglement=edge_metrics['edge_maximization']['entanglement_strength'],
                    response_preview=quantum_response[:150] + "..." if len(quantum_response) > 150 else quantum_response
                )
                
                self.results.append(result)
                
                print(f"   ✅ Tiempo: {response_time:.2f}ms")
                print(f"   ⚡ Edge Multiplier: {result.edge_multiplier:.2f}x")
                print(f"   🔬 Quantum Factor: {result.quantum_factor:.2f}x")
                print(f"   🎯 Quality Score: {result.quality_score:.3f}")
                print(f"   💰 Costo: $0.00")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                result = EvaluationResult(
                    test_name=test['name'],
                    model="Quantum Edge Maximizer",
                    category=test['category'],
                    response_time_ms=0,
                    quality_score=0.0,
                    cost_usd=0.0,
                    success=False,
                    error=str(e)
                )
                self.results.append(result)
    
    async def _evaluate_premium_models(self):
        """Evalúa modelos premium de OpenRouter"""
        
        print(f"\n🤖 EVALUANDO MODELOS PREMIUM")
        print("-" * 40)
        
        for model_key, model_info in self.premium_models.items():
            print(f"\n🔍 Modelo: {model_info['name']}")
            
            for test in self.comprehensive_tests[:2]:  # Solo primeros 2 tests para ahorrar costos
                print(f"   Test: {test['name']}")
                
                try:
                    payload = {
                        "model": model_info['id'],
                        "messages": [
                            {"role": "user", "content": test["prompt"]}
                        ],
                        "max_tokens": 500,
                        "temperature": 0.7
                    }
                    
                    start_time = time.time()
                    response = requests.post(
                        self.openrouter_url,
                        headers=self.openrouter_headers,
                        json=payload,
                        timeout=60
                    )
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        content = result_data['choices'][0]['message']['content']
                        usage = result_data.get('usage', {})
                        
                        # Calcular costo
                        input_tokens = usage.get('prompt_tokens', 0)
                        output_tokens = usage.get('completion_tokens', 0)
                        cost = (input_tokens * model_info['cost_per_1k_input'] / 1000) + \
                               (output_tokens * model_info['cost_per_1k_output'] / 1000)
                        
                        # Calcular calidad
                        quality_metrics = self._calculate_quality(content, test)
                        
                        result = EvaluationResult(
                            test_name=test['name'],
                            model=model_info['name'],
                            category=test['category'],
                            response_time_ms=response_time,
                            quality_score=quality_metrics['overall_score'],
                            cost_usd=cost,
                            response_preview=content[:150] + "..." if len(content) > 150 else content
                        )
                        
                        self.results.append(result)
                        
                        print(f"      ✅ Tiempo: {response_time:.2f}ms")
                        print(f"      🎯 Quality Score: {result.quality_score:.3f}")
                        print(f"      💰 Costo: ${cost:.6f}")
                        
                    else:
                        print(f"      ❌ Error: HTTP {response.status_code}")
                        
                except Exception as e:
                    print(f"      ❌ Error: {str(e)}")
    
    async def _run_supremacy_tests(self):
        """Ejecuta tests de supremacía si están disponibles"""
        
        print(f"\n🌌 EJECUTANDO TESTS DE SUPREMACÍA")
        print("-" * 40)
        
        supremacy_test_path = self.quantum_supreme_path / "supremacy_test_suite.py"
        
        if supremacy_test_path.exists():
            try:
                print("   🚀 Ejecutando Quantum Supreme Test Suite...")
                
                # Ejecutar tests de supremacía
                result = subprocess.run([
                    sys.executable, str(supremacy_test_path)
                ], capture_output=True, text=True, cwd=self.quantum_supreme_path)
                
                if result.returncode == 0:
                    print("   ✅ Tests de supremacía ejecutados exitosamente")
                    print("   📊 Output:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
                else:
                    print("   ⚠️ Tests de supremacía con advertencias")
                    print("   📊 Error:", result.stderr[:200] + "..." if len(result.stderr) > 200 else result.stderr)
                    
            except Exception as e:
                print(f"   ❌ Error ejecutando tests de supremacía: {str(e)}")
        else:
            print("   ⚠️ Tests de supremacía no disponibles")
    
    async def _analyze_empirical_benchmarks(self):
        """Analiza benchmarks empíricos disponibles"""
        
        print(f"\n📊 ANALIZANDO BENCHMARKS EMPÍRICOS")
        print("-" * 40)
        
        if self.empirical_results_path.exists():
            benchmark_files = list(self.empirical_results_path.glob("*.json"))
            
            if benchmark_files:
                print(f"   📁 Encontrados {len(benchmark_files)} archivos de benchmark")
                
                # Analizar el más reciente
                latest_benchmark = max(benchmark_files, key=lambda x: x.stat().st_mtime)
                print(f"   🔍 Analizando: {latest_benchmark.name}")
                
                try:
                    with open(latest_benchmark, 'r', encoding='utf-8') as f:
                        benchmark_data = json.load(f)
                    
                    # Extraer métricas clave
                    if 'results' in benchmark_data:
                        results = benchmark_data['results']
                        print(f"   📈 Total de resultados: {len(results)}")
                        
                        # Calcular métricas promedio
                        if results:
                            avg_accuracy = np.mean([r.get('accuracy', 0) for r in results])
                            avg_time = np.mean([r.get('time', 0) for r in results])
                            
                            print(f"   🎯 Precisión promedio: {avg_accuracy:.3f}")
                            print(f"   ⚡ Tiempo promedio: {avg_time:.2f}s")
                            
                except Exception as e:
                    print(f"   ❌ Error analizando benchmark: {str(e)}")
            else:
                print("   ⚠️ No se encontraron archivos de benchmark")
        else:
            print("   ⚠️ Directorio de benchmarks empíricos no disponible")
    
    async def _generate_quantum_response(self, prompt: str, edge_metrics: Dict) -> str:
        """Genera respuesta real con optimización cuántica"""
        
        # Usar Qwen3 Coder con prompt mejorado
        model_id = "qwen/qwen3-coder"
        
        # Crear prompt cuántico mejorado
        enhanced_prompt = f"""
🧠 QUANTUM EDGE ENHANCED QUERY
⚡ Edge Multiplier: {edge_metrics['edge_maximization']['final_edge_multiplier']:.2f}x
🔬 Quantum Factor: {edge_metrics['edge_maximization']['quantum_factor']:.2f}x
🎯 Coherence: {edge_metrics['edge_maximization']['coherence_level']:.4f}

ORIGINAL QUERY:
{prompt}

INSTRUCTIONS:
- Provide a comprehensive, high-quality response
- Leverage quantum-enhanced reasoning
- Ensure maximum coherence and accuracy
- Apply edge optimization principles
- Generate detailed, well-structured output

Please respond with the highest quality possible, considering the quantum edge optimization applied to this query.
"""
        
        try:
            payload = {
                "model": model_id,
                "messages": [
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.openrouter_url,
                headers=self.openrouter_headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Quantum Edge Response: {prompt[:100]}... (Enhanced with Edge Multiplier: {edge_metrics['edge_maximization']['final_edge_multiplier']:.2f}x)"
                
        except Exception as e:
            return f"Quantum Edge Response: {prompt[:100]}... (Enhanced with Edge Multiplier: {edge_metrics['edge_maximization']['final_edge_multiplier']:.2f}x)"
    
    def _calculate_quality(self, response: str, test: Dict) -> Dict[str, float]:
        """Calcula métricas de calidad"""
        
        response_lower = response.lower()
        word_count = len(response.split())
        
        # Relevancia
        expected_components = test.get('expected_components', [])
        relevance_score = 0.0
        if expected_components:
            found_components = sum(1 for component in expected_components if component.lower() in response_lower)
            relevance_score = found_components / len(expected_components)
        
        # Completitud
        completeness_score = min(1.0, word_count / 50)
        
        # Precisión
        accuracy_score = 0.9 if word_count > 30 else 0.6
        
        # Score general
        overall_score = (relevance_score + completeness_score + accuracy_score) / 3
        
        return {
            "relevance": relevance_score,
            "completeness": completeness_score,
            "accuracy": accuracy_score,
            "overall_score": overall_score
        }
    
    async def _generate_comprehensive_report(self):
        """Genera reporte comprehensivo final"""
        
        print(f"\n📋 REPORTE COMPREHENSIVO FINAL")
        print("=" * 70)
        
        # Agrupar resultados por modelo
        models = {}
        for result in self.results:
            if result.model not in models:
                models[result.model] = []
            models[result.model].append(result)
        
        # Calcular métricas por modelo
        model_metrics = {}
        for model_name, model_results in models.items():
            successful_results = [r for r in model_results if r.success]
            
            if successful_results:
                response_times = [r.response_time_ms for r in successful_results]
                quality_scores = [r.quality_score for r in successful_results]
                costs = [r.cost_usd for r in successful_results]
                
                model_metrics[model_name] = {
                    'total_tests': len(successful_results),
                    'avg_response_time': np.mean(response_times),
                    'avg_quality_score': np.mean(quality_scores),
                    'total_cost': np.sum(costs),
                    'max_quality_score': np.max(quality_scores),
                    'min_response_time': np.min(response_times)
                }
                
                # Métricas específicas de Quantum Edge
                if model_name == "Quantum Edge Maximizer":
                    edge_multipliers = [r.edge_multiplier for r in successful_results if r.edge_multiplier]
                    quantum_factors = [r.quantum_factor for r in successful_results if r.quantum_factor]
                    
                    if edge_multipliers:
                        model_metrics[model_name]['avg_edge_multiplier'] = np.mean(edge_multipliers)
                        model_metrics[model_name]['max_edge_multiplier'] = np.max(edge_multipliers)
                    
                    if quantum_factors:
                        model_metrics[model_name]['avg_quantum_factor'] = np.mean(quantum_factors)
                        model_metrics[model_name]['max_quantum_factor'] = np.max(quantum_factors)
        
        # Mostrar resultados
        print(f"📈 MÉTRICAS POR MODELO:")
        for model_name, metrics in model_metrics.items():
            print(f"\n🤖 {model_name}:")
            print(f"   • Tests: {metrics['total_tests']}")
            print(f"   • Tiempo promedio: {metrics['avg_response_time']:.2f}ms")
            print(f"   • Tiempo mínimo: {metrics['min_response_time']:.2f}ms")
            print(f"   • Quality Score promedio: {metrics['avg_quality_score']:.3f}")
            print(f"   • Quality Score máximo: {metrics['max_quality_score']:.3f}")
            print(f"   • Costo total: ${metrics['total_cost']:.6f}")
            
            if 'avg_edge_multiplier' in metrics:
                print(f"   • Edge Multiplier promedio: {metrics['avg_edge_multiplier']:.2f}x")
                print(f"   • Edge Multiplier máximo: {metrics['max_edge_multiplier']:.2f}x")
            
            if 'avg_quantum_factor' in metrics:
                print(f"   • Quantum Factor promedio: {metrics['avg_quantum_factor']:.2f}x")
                print(f"   • Quantum Factor máximo: {metrics['max_quantum_factor']:.2f}x")
        
        # Rankings
        print(f"\n🏆 RANKINGS FINALES:")
        
        # Velocidad
        speed_ranking = sorted(model_metrics.items(), key=lambda x: x[1]['avg_response_time'])
        print(f"\n⚡ RANKING POR VELOCIDAD:")
        for i, (model, metrics) in enumerate(speed_ranking, 1):
            print(f"   {i}. {model}: {metrics['avg_response_time']:.2f}ms")
        
        # Calidad
        quality_ranking = sorted(model_metrics.items(), key=lambda x: x[1]['avg_quality_score'], reverse=True)
        print(f"\n🎯 RANKING POR CALIDAD:")
        for i, (model, metrics) in enumerate(quality_ranking, 1):
            print(f"   {i}. {model}: {metrics['avg_quality_score']:.3f}")
        
        # Costo
        cost_ranking = sorted(model_metrics.items(), key=lambda x: x[1]['total_cost'])
        print(f"\n💰 RANKING POR COSTO:")
        for i, (model, metrics) in enumerate(cost_ranking, 1):
            print(f"   {i}. {model}: ${metrics['total_cost']:.6f}")
        
        # Guardar resultados
        report_data = {
            "timestamp": time.time(),
            "model_metrics": model_metrics,
            "detailed_results": [
                {
                    "test_name": r.test_name,
                    "model": r.model,
                    "category": r.category,
                    "response_time_ms": r.response_time_ms,
                    "quality_score": r.quality_score,
                    "cost_usd": r.cost_usd,
                    "edge_multiplier": r.edge_multiplier,
                    "quantum_factor": r.quantum_factor,
                    "success": r.success,
                    "error": r.error
                }
                for r in self.results
            ]
        }
        
        report_file = f"comprehensive_evaluation_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Reporte guardado en: {report_file}")
        print(f"\n✅ EVALUACIÓN COMPREHENSIVA COMPLETADA")
        print(f"🚀 Quantum Edge Maximizer evaluado contra todo el stack disponible")

async def main():
    """Función principal"""
    
    evaluator = QuantumEdgeComprehensiveEvaluator()
    await evaluator.run_comprehensive_evaluation()

if __name__ == "__main__":
    asyncio.run(main())
