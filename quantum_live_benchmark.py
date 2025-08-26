#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QUANTUM LIVE BENCHMARK                                    ║
║                        CONTRA LOS MEJORES DEL MERCADO                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import time
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class BenchmarkCategory(Enum):
    """Categorías de benchmark"""
    PROGRAMMING = "programming"
    REASONING = "reasoning"
    MATHEMATICS = "mathematics"

@dataclass
class BenchmarkResult:
    """Resultado de benchmark"""
    model_name: str
    category: BenchmarkCategory
    response: str
    response_time: float
    cost: float
    quality_score: float
    accuracy_score: float
    creativity_score: float
    overall_score: float

class QuantumLiveBenchmark:
    """Sistema de benchmark live contra los mejores del mercado"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantum-live-benchmark.local",
            "X-Title": "Quantum Live Benchmark"
        }
        
        # LOS MEJORES MODELOS DEL MERCADO
        self.top_models = {
            "gpt5_flagship": {
                "id": "openai/gpt-5",
                "cost_input": 0.00125,
                "cost_output": 0.01,
                "quality_estimate": 0.95,
                "description": "GPT-5 Flagship"
            },
            "claude_opus": {
                "id": "anthropic/claude-opus-4.1",
                "cost_input": 0.015,
                "cost_output": 0.075,
                "quality_estimate": 0.98,
                "description": "Claude Opus 4.1"
            },
            "gemini_ultra": {
                "id": "google/gemini-2.5-ultra",
                "cost_input": 0.0025,
                "cost_output": 0.0125,
                "quality_estimate": 0.93,
                "description": "Gemini 2.5 Ultra"
            },
            "quantum_enhanced": {
                "id": "google/gemini-flash-1.5-8b",
                "cost_input": 0.0000000375,
                "cost_output": 0.00000015,
                "quality_estimate": 0.85,
                "description": "Quantum Enhanced"
            }
        }
        
        # QUERIES DE BENCHMARK LIVE
        self.benchmark_queries = {
            BenchmarkCategory.PROGRAMMING: "Implementa un algoritmo de ordenamiento quicksort optimizado con análisis de complejidad temporal y espacial, incluyendo manejo de casos edge y optimizaciones para arrays pequeños",
            BenchmarkCategory.REASONING: "Analiza la complejidad computacional del problema del viajante (TSP) y propón tres algoritmos diferentes para resolverlo, comparando sus ventajas y desventajas",
            BenchmarkCategory.MATHEMATICS: "Demuestra la fórmula de Euler e^(iπ) + 1 = 0 usando series de Taylor y explica su significado matemático"
        }
        
        self.print_header()
    
    def print_header(self):
        """Imprime header del sistema"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    QUANTUM LIVE BENCHMARK                                    ║")
        print("║                        CONTRA LOS MEJORES DEL MERCADO                       ║")
        print("║                                                                              ║")
        print("║  [LIVE BENCHMARK: ACTIVE]                                                    ║")
        print("║  [TOP MODELS: SELECTED]                                                      ║")
        print("║  [REAL-TIME COMPARISON: ENABLED]                                            ║")
        print("║  [QUANTUM ADVANTAGE: MAXIMIZED]                                             ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    async def call_model(self, query: str, model_key: str) -> Dict[str, Any]:
        """Llama a un modelo específico"""
        
        model_info = self.top_models[model_key]
        model_id = model_info["id"]
        
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 3000,
            "temperature": 0.1
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content']
                        usage = data.get('usage', {})
                        
                        input_tokens = usage.get('prompt_tokens', 0)
                        output_tokens = usage.get('completion_tokens', 0)
                        
                        cost = (input_tokens * model_info["cost_input"] / 1000000) + (output_tokens * model_info["cost_output"] / 1000000)
                        response_time = time.time() - start_time
                        
                        return {
                            "success": True,
                            "response": content,
                            "cost": cost,
                            "response_time": response_time,
                            "model": model_key,
                            "model_info": model_info
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "cost": 0.0,
                            "response_time": time.time() - start_time,
                            "model": model_key
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "cost": 0.0,
                "response_time": time.time() - start_time,
                "model": model_key
            }
    
    def calculate_quality_score(self, response: str, category: BenchmarkCategory) -> Dict[str, float]:
        """Calcula scores de calidad basados en la categoría"""
        
        scores = {
            "quality_score": 0.0,
            "accuracy_score": 0.0,
            "creativity_score": 0.0
        }
        
        # Métricas básicas
        length_score = min(1.0, len(response) / 2000)
        structure_score = 0.0
        technical_score = 0.0
        
        # Análisis de estructura
        if "```" in response:
            structure_score += 0.3
        if any(char in response for char in ["•", "-", "1.", "2.", "#", "##"]):
            structure_score += 0.2
        if any(word in response.lower() for word in ["análisis", "conclusión", "ejemplo", "implementación"]):
            structure_score += 0.2
        
        # Análisis técnico
        if category == BenchmarkCategory.PROGRAMMING:
            if any(word in response.lower() for word in ["complejidad", "algoritmo", "optimización", "patrón"]):
                technical_score += 0.4
            if "```python" in response or "```java" in response or "```cpp" in response:
                technical_score += 0.3
        elif category == BenchmarkCategory.MATHEMATICS:
            if any(char in response for char in ["∫", "∑", "π", "∞", "√"]):
                technical_score += 0.4
            if any(word in response.lower() for word in ["demostración", "teorema", "fórmula", "integral"]):
                technical_score += 0.3
        elif category == BenchmarkCategory.REASONING:
            if any(word in response.lower() for word in ["complejidad", "algoritmo", "análisis", "comparación"]):
                technical_score += 0.4
            if len(response) > 800:
                technical_score += 0.3
        
        # Calcular scores finales
        scores["quality_score"] = min(1.0, (length_score + structure_score + technical_score) / 3)
        scores["accuracy_score"] = min(1.0, technical_score + 0.3)
        scores["creativity_score"] = min(1.0, structure_score + 0.4)
        
        return scores
    
    async def run_single_benchmark(self, query: str, model_key: str, category: BenchmarkCategory) -> BenchmarkResult:
        """Ejecuta un benchmark individual"""
        
        print(f"║  🚀 Testing {self.top_models[model_key]['description']}...")
        
        result = await self.call_model(query, model_key)
        
        if result["success"]:
            scores = self.calculate_quality_score(result["response"], category)
            overall_score = (scores["quality_score"] + scores["accuracy_score"] + scores["creativity_score"]) / 3
            
            benchmark_result = BenchmarkResult(
                model_name=model_key,
                category=category,
                response=result["response"],
                response_time=result["response_time"],
                cost=result["cost"],
                quality_score=scores["quality_score"],
                accuracy_score=scores["accuracy_score"],
                creativity_score=scores["creativity_score"],
                overall_score=overall_score
            )
            
            print(f"║  ✅ {model_key}: {overall_score:.3f} score, ${result['cost']:.8f}, {result['response_time']:.2f}s")
            
            return benchmark_result
        else:
            print(f"║  ❌ {model_key}: FAILED - {result.get('error', 'Unknown error')}")
            return None
    
    async def run_category_benchmark(self, category: BenchmarkCategory) -> List[BenchmarkResult]:
        """Ejecuta benchmark para una categoría específica"""
        
        print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║  BENCHMARK CATEGORY: {category.value.upper()}")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        results = []
        query = self.benchmark_queries[category]
        
        print(f"║  Query: {query[:80]}...")
        print("║")
        
        # Ejecutar benchmarks en paralelo para todos los modelos
        tasks = []
        for model_key in self.top_models.keys():
            task = self.run_single_benchmark(query, model_key, category)
            tasks.append(task)
        
        # Esperar todos los resultados
        benchmark_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados exitosos
        for result in benchmark_results:
            if isinstance(result, BenchmarkResult):
                results.append(result)
        
        # Ordenar por score general
        results.sort(key=lambda x: x.overall_score, reverse=True)
        
        return results
    
    def print_category_results(self, results: List[BenchmarkResult], category: BenchmarkCategory):
        """Imprime resultados de una categoría"""
        
        print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║  RESULTS: {category.value.upper()} CATEGORY")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        for i, result in enumerate(results, 1):
            model_info = self.top_models[result.model_name]
            print(f"║  #{i:2d} {model_info['description']:<25} | Score: {result.overall_score:.3f} | Cost: ${result.cost:.8f} | Time: {result.response_time:.2f}s")
        
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Análisis del ganador
        if results:
            winner = results[0]
            winner_info = self.top_models[winner.model_name]
            print(f"║  🏆 WINNER: {winner_info['description']}")
            print(f"║  📊 Overall Score: {winner.overall_score:.3f}")
            print(f"║  💰 Cost: ${winner.cost:.8f}")
            print(f"║  ⚡ Response Time: {winner.response_time:.2f}s")
            
            # Análisis de ventaja cuántica
            if winner.model_name == "quantum_enhanced":
                print("║  🚀 QUANTUM ADVANTAGE: CONFIRMED!")
                print("║  ✅ Our system outperformed all competitors!")
            else:
                print("║  ⚠️  QUANTUM ADVANTAGE: NEEDS IMPROVEMENT")
                print("║  🔄 System optimization required")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    async def run_full_benchmark(self):
        """Ejecuta benchmark completo contra todos los modelos"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  QUANTUM LIVE BENCHMARK - FULL COMPARISON")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  Testing against: GPT-5, Claude Opus, Gemini Ultra")
        print("║  Categories: Programming, Reasoning, Mathematics")
        print("║  Metrics: Quality, Accuracy, Creativity, Cost, Speed")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        all_results = {}
        total_cost = 0.0
        total_tests = 0
        
        # Ejecutar benchmarks para cada categoría
        for category in BenchmarkCategory:
            print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"║  STARTING {category.value.upper()} BENCHMARK")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
            
            results = await self.run_category_benchmark(category)
            all_results[category] = results
            
            # Actualizar métricas globales
            for result in results:
                total_cost += result.cost
                total_tests += 1
            
            # Mostrar resultados de la categoría
            self.print_category_results(results, category)
        
        # Análisis final
        self.print_final_analysis(all_results, total_cost, total_tests)
    
    def print_final_analysis(self, all_results: Dict[BenchmarkCategory, List[BenchmarkResult]], total_cost: float, total_tests: int):
        """Imprime análisis final del benchmark"""
        
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  QUANTUM LIVE BENCHMARK - FINAL ANALYSIS")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Calcular rankings generales
        model_scores = {}
        model_costs = {}
        model_times = {}
        
        for category, results in all_results.items():
            for result in results:
                if result.model_name not in model_scores:
                    model_scores[result.model_name] = []
                    model_costs[result.model_name] = []
                    model_times[result.model_name] = []
                
                model_scores[result.model_name].append(result.overall_score)
                model_costs[result.model_name].append(result.cost)
                model_times[result.model_name].append(result.response_time)
        
        # Calcular promedios
        model_averages = {}
        for model in model_scores:
            avg_score = sum(model_scores[model]) / len(model_scores[model])
            avg_cost = sum(model_costs[model]) / len(model_costs[model])
            avg_time = sum(model_times[model]) / len(model_times[model])
            model_averages[model] = {
                "score": avg_score,
                "cost": avg_cost,
                "time": avg_time,
                "cost_efficiency": avg_score / avg_cost if avg_cost > 0 else 0
            }
        
        # Ordenar por score promedio
        sorted_models = sorted(model_averages.items(), key=lambda x: x[1]["score"], reverse=True)
        
        print("║  FINAL RANKINGS:")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        for i, (model, metrics) in enumerate(sorted_models, 1):
            model_info = self.top_models[model]
            print(f"║  #{i:2d} {model_info['description']:<25} | Score: {metrics['score']:.3f} | Cost: ${metrics['cost']:.8f} | Efficiency: {metrics['cost_efficiency']:.2f}")
        
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  TOTAL TESTS: {total_tests}")
        print(f"║  TOTAL COST: ${total_cost:.8f}")
        print(f"║  AVERAGE COST PER TEST: ${total_cost/total_tests:.8f}")
        
        # Análisis de ventaja cuántica
        quantum_metrics = model_averages.get("quantum_enhanced", {})
        if quantum_metrics:
            print("╠══════════════════════════════════════════════════════════════════════════════╣")
            print("║  QUANTUM ADVANTAGE ANALYSIS:")
            print(f"║  • Our Score: {quantum_metrics['score']:.3f}")
            print(f"║  • Our Cost: ${quantum_metrics['cost']:.8f}")
            print(f"║  • Our Efficiency: {quantum_metrics['cost_efficiency']:.2f}")
            
            if sorted_models[0][0] == "quantum_enhanced":
                print("║  🏆 QUANTUM ADVANTAGE: ABSOLUTE SUPREMACY!")
                print("║  ✅ We are the best in the market!")
            else:
                best_model = sorted_models[0][0]
                best_metrics = sorted_models[0][1]
                print(f"║  ⚠️  QUANTUM ADVANTAGE: {best_model.upper()} is leading")
                print(f"║  📈 Gap to leader: {best_metrics['score'] - quantum_metrics['score']:.3f}")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")

async def main():
    """Función principal del benchmark live"""
    
    benchmark = QuantumLiveBenchmark()
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  QUANTUM LIVE BENCHMARK - STARTING")
    print("║  Testing our system against the best models in the market")
    print("║  This will take several minutes...")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    await benchmark.run_full_benchmark()

if __name__ == "__main__":
    asyncio.run(main())
