#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        LIVE PERFORMANCE TESTING                             ║
║                        TESTING CON LOS MEJORES MODELOS                     ║
║                                                                              ║
║  ████████████████████████████████████████████████████████████████████████  ║
║  █                                                                          █  ║
║  █  ███████╗██╗███╗   ███╗██████╗ ██╗     ██╗███████╗██╗██████╗ ███████╗   █  ║
║  █  ██╔════╝██║████╗ ████║██╔══██╗██║     ██║██╔════╝██║██╔══██╗██╔════╝   █  ║
║  █  ██║     ██║██╔████╔██║██████╔╝██║     ██║███████╗██║██████╔╝█████╗     █  ║
║  █  ██║     ██║██║╚██╔╝██║██╔═══╝ ██║     ██║╚════██║██║██╔══██╗██╔══╝     █  ║
║  █  ╚██████╗██║██║ ╚═╝ ██║██║     ███████╗██║███████║██║██║  ██║███████╗   █  ║
║  █   ╚═════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝   █  ║
║  █                                                                          █  ║
║  █  ████████████████████████████████████████████████████████████████████████  ║
║                                                                              ║
║  [TESTING: Claude Opus 4.1, Gemini 2.5 Pro, GPT-5]                        ║
║  [DOMAINS: Programming, Reasoning, Mathematics]                            ║
║  [METRICS: Performance, Speed, Cost, Quality]                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum

class TestDomain(Enum):
    """Dominios de testing"""
    PROGRAMMING = "programming"
    REASONING = "reasoning"
    MATHEMATICS = "mathematics"

@dataclass
class TestResult:
    """Resultado de test individual"""
    model: str
    domain: TestDomain
    query: str
    response: str
    score: float
    response_time: float
    cost: float
    tokens_used: int
    success: bool
    error: str = None

class LivePerformanceTester:
    """Sistema de testing en vivo con los mejores modelos"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://live-performance-test.local",
            "X-Title": "Live Performance Testing"
        }
        
        # 🏆 LOS MEJORES MODELOS PREMIUM
        self.top_models = {
            "claude_opus_4_1": {
                "id": "anthropic/claude-opus-4.1",
                "name": "Claude Opus 4.1",
                "description": "Mejor modelo de código del mundo (74.5% SWE-bench)",
                "context": 200000,
                "cost_per_1k_input": 0.015,
                "cost_per_1k_output": 0.075
            },
            "gemini_2_5_pro": {
                "id": "google/gemini-2.5-pro",
                "name": "Gemini 2.5 Pro",
                "description": "Modelo multimodal con 1M tokens de contexto",
                "context": 1048576,
                "cost_per_1k_input": 0.00125,
                "cost_per_1k_output": 0.01
            },
            "gpt_5": {
                "id": "openai/gpt-5",
                "name": "GPT-5",
                "description": "Modelo más avanzado de OpenAI",
                "context": 400000,
                "cost_per_1k_input": 0.00000125,
                "cost_per_1k_output": 0.00001
            }
        }
        
        # 🎯 QUERIES DE TESTING POR DOMINIO
        self.test_queries = {
            TestDomain.PROGRAMMING: [
                "Implementa un algoritmo de ordenamiento quicksort optimizado en Python con análisis de complejidad",
                "Crea una función que detecte si un grafo es bipartito usando BFS",
                "Desarrolla un sistema de caché LRU con complejidad O(1) para todas las operaciones"
            ],
            TestDomain.REASONING: [
                "Analiza la complejidad computacional del problema del viajante y propón una solución aproximada",
                "Explica paso a paso cómo resolver el problema de las 8 reinas usando backtracking",
                "Demuestra por qué el algoritmo de Dijkstra no funciona con pesos negativos"
            ],
            TestDomain.MATHEMATICS: [
                "Demuestra la fórmula de Euler e^(iπ) + 1 = 0 usando series de Taylor",
                "Calcula la derivada de la función f(x) = ln(sin(x^2)) usando la regla de la cadena",
                "Resuelve la ecuación diferencial dy/dx + 2y = e^(-x) con condición inicial y(0) = 1"
            ]
        }
        
        self.results = []
        
    def print_header(self):
        """Imprime header del sistema de testing"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                        LIVE PERFORMANCE TESTING                             ║")
        print("║                        TESTING CON LOS MEJORES MODELOS                     ║")
        print("║                                                                              ║")
        print("║  ████████████████████████████████████████████████████████████████████████  ║")
        print("║  █                                                                          █  ║")
        print("║  █  ███████╗██╗███╗   ███╗██████╗ ██╗     ██╗███████╗██╗██████╗ ███████╗   █  ║")
        print("║  █  ██╔════╝██║████╗ ████║██╔══██╗██║     ██║██╔════╝██║██╔══██╗██╔════╝   █  ║")
        print("║  █  ██║     ██║██╔████╔██║██████╔╝██║     ██║███████╗██║██████╔╝█████╗     █  ║")
        print("║  █  ██║     ██║██║╚██╔╝██║██╔═══╝ ██║     ██║╚════██║██║██╔══██╗██╔══╝     █  ║")
        print("║  █  ╚██████╗██║██║ ╚═╝ ██║██║     ███████╗██║███████║██║██║  ██║███████╗   █  ║")
        print("║  █   ╚═════╝╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝   █  ║")
        print("║  █                                                                          █  ║")
        print("║  █  ████████████████████████████████████████████████████████████████████████  ║")
        print("║                                                                              ║")
        print("║  [TESTING: Claude Opus 4.1, Gemini 2.5 Pro, GPT-5]                        ║")
        print("║  [DOMAINS: Programming, Reasoning, Mathematics]                            ║")
        print("║  [METRICS: Performance, Speed, Cost, Quality]                             ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    async def call_model(self, model_id: str, prompt: str) -> Dict[str, Any]:
        """Llamada al modelo específico"""
        
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.1
        }
        
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        content = data['choices'][0]['message']['content']
                        usage = data.get('usage', {})
                        
                        input_tokens = usage.get('prompt_tokens', 0)
                        output_tokens = usage.get('completion_tokens', 0)
                        
                        response_time = time.time() - start_time
                        
                        return {
                            "success": True,
                            "response": content,
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens,
                            "response_time": response_time
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "response_time": time.time() - start_time
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    def calculate_score(self, response: str, domain: TestDomain) -> float:
        """Calcular score basado en la calidad de la respuesta"""
        
        if not response:
            return 0.0
        
        score = 0.0
        response_lower = response.lower()
        
        # Métricas base
        if "```" in response:
            score += 0.2
        if any(keyword in response_lower for keyword in ["def ", "class ", "function", "return"]):
            score += 0.15
        if any(word in response_lower for word in ["explic", "paso", "proceso", "método"]):
            score += 0.15
        if any(word in response_lower for word in ["algoritmo", "lógica", "estrategia"]):
            score += 0.1
        if any(word in response_lower for word in ["complejidad", "optimiz", "eficien"]):
            score += 0.1
        if len(response) > 500:
            score += 0.1
        
        # Ajustes específicos por dominio
        if domain == TestDomain.PROGRAMMING:
            if any(char in response for char in ["def ", "class ", "import ", "return"]):
                score += 0.2
            if any(word in response_lower for word in ["algoritmo", "complejidad", "tiempo", "espacio"]):
                score += 0.15
        elif domain == TestDomain.REASONING:
            if any(word in response_lower for word in ["análisis", "lógico", "sistemático", "metodológico"]):
                score += 0.2
            if any(word in response_lower for word in ["paso", "proceso", "método", "enfoque"]):
                score += 0.15
        elif domain == TestDomain.MATHEMATICS:
            if any(char in response for char in ["∫", "∑", "π", "∞", "√", "=", "≠", "≤", "≥"]):
                score += 0.2
            if any(word in response_lower for word in ["demostración", "teorema", "fórmula", "prueba", "matemática"]):
                score += 0.15
        
        return min(1.0, score)
    
    def calculate_cost(self, model_info: Dict, input_tokens: int, output_tokens: int) -> float:
        """Calcular costo de la llamada"""
        input_cost = (input_tokens / 1000) * model_info["cost_per_1k_input"]
        output_cost = (output_tokens / 1000) * model_info["cost_per_1k_output"]
        return input_cost + output_cost
    
    async def test_model_domain(self, model_key: str, domain: TestDomain) -> List[TestResult]:
        """Testear un modelo en un dominio específico"""
        
        model_info = self.top_models[model_key]
        results = []
        
        print(f"║  🧪 Testing {model_info['name']} en {domain.value.upper()}:")
        
        for i, query in enumerate(self.test_queries[domain], 1):
            print(f"║     Query {i}: {query[:60]}...")
            
            # Llamada al modelo
            response_data = await self.call_model(model_info["id"], query)
            
            if response_data["success"]:
                # Calcular métricas
                score = self.calculate_score(response_data["response"], domain)
                cost = self.calculate_cost(
                    model_info,
                    response_data["input_tokens"],
                    response_data["output_tokens"]
                )
                
                result = TestResult(
                    model=model_info["name"],
                    domain=domain,
                    query=query,
                    response=response_data["response"],
                    score=score,
                    response_time=response_data["response_time"],
                    cost=cost,
                    tokens_used=response_data["input_tokens"] + response_data["output_tokens"],
                    success=True
                )
                
                results.append(result)
                
                status_icon = "✅" if score > 0.7 else "⚠️" if score > 0.5 else "❌"
                print(f"║       {status_icon} Score: {score:.3f} | Time: {response_data['response_time']:.2f}s | Cost: ${cost:.6f}")
            else:
                result = TestResult(
                    model=model_info["name"],
                    domain=domain,
                    query=query,
                    response="",
                    score=0.0,
                    response_time=response_data["response_time"],
                    cost=0.0,
                    tokens_used=0,
                    success=False,
                    error=response_data["error"]
                )
                
                results.append(result)
                print(f"║       ❌ Error: {response_data['error']}")
        
        return results
    
    async def run_comprehensive_testing(self):
        """Ejecutar testing completo con todos los modelos"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  LIVE PERFORMANCE TESTING - INICIANDO TESTING COMPLETO")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  Modelos a testear:")
        for key, model in self.top_models.items():
            print(f"║  • {model['name']}: {model['description']}")
        print("║  Dominios: Programming, Reasoning, Mathematics")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Testing por modelo y dominio
        for model_key in self.top_models.keys():
            print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"║  TESTING {self.top_models[model_key]['name'].upper()}")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
            
            for domain in TestDomain:
                domain_results = await self.test_model_domain(model_key, domain)
                self.results.extend(domain_results)
                
                # Pausa entre dominios
                await asyncio.sleep(2)
            
            # Pausa entre modelos
            await asyncio.sleep(5)
        
        # Análisis de resultados
        self.analyze_results()
    
    def analyze_results(self):
        """Analizar y mostrar resultados del testing"""
        
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  ANÁLISIS DE RESULTADOS - LIVE PERFORMANCE TESTING")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Agrupar resultados por modelo
        model_results = {}
        for result in self.results:
            if result.model not in model_results:
                model_results[result.model] = []
            model_results[result.model].append(result)
        
        # Análisis por modelo
        for model_name, results in model_results.items():
            print(f"║  📊 {model_name}:")
            
            # Métricas generales
            successful_results = [r for r in results if r.success]
            if successful_results:
                avg_score = sum(r.score for r in successful_results) / len(successful_results)
                avg_time = sum(r.response_time for r in successful_results) / len(successful_results)
                total_cost = sum(r.cost for r in successful_results)
                total_tokens = sum(r.tokens_used for r in successful_results)
                
                print(f"║     • Score Promedio: {avg_score:.3f}")
                print(f"║     • Tiempo Promedio: {avg_time:.2f}s")
                print(f"║     • Costo Total: ${total_cost:.6f}")
                print(f"║     • Tokens Usados: {total_tokens:,}")
                print(f"║     • Tasa de Éxito: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.1f}%)")
            else:
                print(f"║     • ❌ Sin resultados exitosos")
            
            # Análisis por dominio
            for domain in TestDomain:
                domain_results = [r for r in results if r.domain == domain and r.success]
                if domain_results:
                    domain_avg_score = sum(r.score for r in domain_results) / len(domain_results)
                    print(f"║     • {domain.value.title()}: {domain_avg_score:.3f}")
        
        # Comparación entre modelos
        print("\n║  🏆 COMPARACIÓN ENTRE MODELOS:")
        print("║  " + "="*60)
        
        comparison_data = []
        for model_name, results in model_results.items():
            successful_results = [r for r in results if r.success]
            if successful_results:
                avg_score = sum(r.score for r in successful_results) / len(successful_results)
                avg_time = sum(r.response_time for r in successful_results) / len(successful_results)
                total_cost = sum(r.cost for r in successful_results)
                
                comparison_data.append({
                    "model": model_name,
                    "avg_score": avg_score,
                    "avg_time": avg_time,
                    "total_cost": total_cost
                })
        
        # Ordenar por score
        comparison_data.sort(key=lambda x: x["avg_score"], reverse=True)
        
        for i, data in enumerate(comparison_data, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            print(f"║  {medal} {data['model']}: Score {data['avg_score']:.3f} | Time {data['avg_time']:.2f}s | Cost ${data['total_cost']:.6f}")
        
        # Guardar resultados
        self.save_results()
    
    def save_results(self):
        """Guardar resultados en archivo"""
        
        results_data = {
            "timestamp": time.time(),
            "models_tested": list(self.top_models.keys()),
            "results": [
                {
                    "model": r.model,
                    "domain": r.domain.value,
                    "query": r.query,
                    "response": r.response,
                    "score": r.score,
                    "response_time": r.response_time,
                    "cost": r.cost,
                    "tokens_used": r.tokens_used,
                    "success": r.success,
                    "error": r.error
                }
                for r in self.results
            ]
        }
        
        filename = f"live_performance_results_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n║  💾 Resultados guardados en: {filename}")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")

async def main():
    """Función principal de testing en vivo"""
    
    tester = LivePerformanceTester()
    tester.print_header()
    
    await tester.run_comprehensive_testing()

if __name__ == "__main__":
    asyncio.run(main())
