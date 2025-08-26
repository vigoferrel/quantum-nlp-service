#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROGRAMMING DIAGNOSTIC ANALYSIS                          ║
║                        ANÁLISIS DETALLADO DE NUDOS                         ║
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
║  [PROBLEM: PROGRAMMING DEGRADATION]                                         ║
║  [ANALYSIS: DEEP DIAGNOSTIC]                                                ║
║  [SOLUTION: DIFFERENT APPROACH]                                             ║
║  [FOCUS: NODE IDENTIFICATION]                                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import aiohttp
import time
import json
import re
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np

class ProgrammingApproach(Enum):
    """Enfoques diferentes para programación"""
    SIMPLE_DIRECT = "simple_direct"
    STEP_BY_STEP = "step_by_step"
    PATTERN_BASED = "pattern_based"
    PROBLEM_DECOMPOSITION = "problem_decomposition"
    ALGORITHMIC_THINKING = "algorithmic_thinking"
    CODE_FIRST = "code_first"
    EXPLANATION_FIRST = "explanation_first"
    HYBRID_APPROACH = "hybrid_approach"

@dataclass
class ProgrammingTest:
    """Test de programación con enfoque específico"""
    approach: ProgrammingApproach
    query: str
    prompt: str
    response: str
    score: float
    code_quality: float
    explanation_quality: float
    implementation_quality: float
    details: str

class ProgrammingDiagnosticAnalysis:
    """Análisis diagnóstico detallado de programación"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://programming-diagnostic.local",
            "X-Title": "Programming Diagnostic Analysis"
        }
        
        self.model = "google/gemini-flash-1.5-8b"
        
        # ENFOQUES DIFERENTES PARA PROGRAMACIÓN
        self.programming_approaches = {
            ProgrammingApproach.SIMPLE_DIRECT: {
                "name": "Simple Direct",
                "description": "Prompt directo y simple",
                "template": "Implementa: {query}"
            },
            ProgrammingApproach.STEP_BY_STEP: {
                "name": "Step by Step",
                "description": "Descomposición paso a paso",
                "template": "Resuelve paso a paso: {query}. Explica cada paso antes de implementar."
            },
            ProgrammingApproach.PATTERN_BASED: {
                "name": "Pattern Based",
                "description": "Basado en patrones de diseño",
                "template": "Identifica el patrón de diseño apropiado y implementa: {query}"
            },
            ProgrammingApproach.PROBLEM_DECOMPOSITION: {
                "name": "Problem Decomposition",
                "description": "Descomposición del problema",
                "template": "Descompón el problema en subproblemas y resuelve: {query}"
            },
            ProgrammingApproach.ALGORITHMIC_THINKING: {
                "name": "Algorithmic Thinking",
                "description": "Pensamiento algorítmico",
                "template": "Piensa algorítmicamente y optimiza: {query}"
            },
            ProgrammingApproach.CODE_FIRST: {
                "name": "Code First",
                "description": "Código primero, explicación después",
                "template": "Escribe el código directamente para: {query}"
            },
            ProgrammingApproach.EXPLANATION_FIRST: {
                "name": "Explanation First",
                "description": "Explicación primero, código después",
                "template": "Explica la solución antes de implementar: {query}"
            },
            ProgrammingApproach.HYBRID_APPROACH: {
                "name": "Hybrid Approach",
                "description": "Enfoque híbrido",
                "template": "Combina explicación y código para: {query}"
            }
        }
        
        # PROBLEMAS DE PROGRAMACIÓN ESPECÍFICOS
        self.programming_problems = [
            "Implementa un algoritmo de ordenamiento quicksort optimizado",
            "Diseña un sistema de caché eficiente para una aplicación web",
            "Optimiza una consulta SQL compleja para máximo rendimiento",
            "Implementa un patrón Observer en Python",
            "Crea una función de validación de email robusta",
            "Implementa un algoritmo de búsqueda binaria",
            "Diseña una clase para manejar transacciones bancarias",
            "Optimiza un algoritmo de Fibonacci con memoización"
        ]
        
        self.diagnostic_results = []
        
    def print_header(self):
        """Imprime header del análisis diagnóstico"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    PROGRAMMING DIAGNOSTIC ANALYSIS                          ║")
        print("║                        ANÁLISIS DETALLADO DE NUDOS                         ║")
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
        print("║  [PROBLEM: PROGRAMMING DEGRADATION]                                         ║")
        print("║  [ANALYSIS: DEEP DIAGNOSTIC]                                                ║")
        print("║  [SOLUTION: DIFFERENT APPROACH]                                             ║")
        print("║  [FOCUS: NODE IDENTIFICATION]                                               ║")
        print("║                                                                              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
    
    async def call_model(self, prompt: str) -> Dict[str, Any]:
        """Llamada al modelo"""
        
        payload = {
            "model": self.model,
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
                        
                        cost = (input_tokens * 0.0000000375 / 1000000) + (output_tokens * 0.00000015 / 1000000)
                        response_time = time.time() - start_time
                        
                        return {
                            "success": True,
                            "response": content,
                            "cost": cost,
                            "response_time": response_time,
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "cost": 0.0,
                            "response_time": time.time() - start_time
                        }
                        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "cost": 0.0,
                "response_time": time.time() - start_time
            }
    
    def analyze_code_quality(self, response: str) -> Dict[str, float]:
        """Análisis detallado de calidad de código"""
        
        if not response:
            return {
                "code_quality": 0.0,
                "explanation_quality": 0.0,
                "implementation_quality": 0.0
            }
        
        # Análisis de código
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', response, re.DOTALL)
        has_code = len(code_blocks) > 0
        
        # Métricas de código
        code_quality = 0.0
        if has_code:
            code_quality += 0.3  # Tiene bloques de código
            if any(keyword in response.lower() for keyword in ["def ", "class ", "function", "return"]):
                code_quality += 0.2  # Estructura básica
            if any(keyword in response.lower() for keyword in ["import", "from", "require"]):
                code_quality += 0.1  # Imports
            if any(keyword in response.lower() for keyword in ["#", "//", "/*"]):
                code_quality += 0.1  # Comentarios
            if len(response) > 500:
                code_quality += 0.2  # Longitud
            if any(keyword in response.lower() for keyword in ["optimiz", "eficien", "complejidad"]):
                code_quality += 0.1  # Consideraciones de optimización
        
        # Métricas de explicación
        explanation_quality = 0.0
        if any(word in response.lower() for word in ["explic", "paso", "proceso", "método"]):
            explanation_quality += 0.3
        if any(word in response.lower() for word in ["algoritmo", "lógica", "estrategia"]):
            explanation_quality += 0.3
        if any(word in response.lower() for word in ["complejidad", "tiempo", "espacio"]):
            explanation_quality += 0.2
        if any(word in response.lower() for word in ["ejemplo", "caso", "uso"]):
            explanation_quality += 0.2
        
        # Métricas de implementación
        implementation_quality = 0.0
        if has_code:
            implementation_quality += 0.4
        if explanation_quality > 0.5:
            implementation_quality += 0.3
        if code_quality > 0.5:
            implementation_quality += 0.3
        
        return {
            "code_quality": min(1.0, code_quality),
            "explanation_quality": min(1.0, explanation_quality),
            "implementation_quality": min(1.0, implementation_quality)
        }
    
    def calculate_programming_score(self, response: str) -> float:
        """Calcular score de programación"""
        
        if not response:
            return 0.0
        
        score = 0.0
        response_lower = response.lower()
        
        # Código
        if "```" in response:
            score += 0.3
        if any(keyword in response_lower for keyword in ["def ", "class ", "function", "return"]):
            score += 0.2
        if any(keyword in response_lower for keyword in ["import", "from", "require"]):
            score += 0.1
        
        # Explicación
        if any(word in response_lower for word in ["explic", "paso", "proceso"]):
            score += 0.2
        if any(word in response_lower for word in ["algoritmo", "lógica", "estrategia"]):
            score += 0.1
        if any(word in response_lower for word in ["complejidad", "optimiz"]):
            score += 0.1
        
        return min(1.0, score)
    
    async def test_programming_approach(self, query: str, approach: ProgrammingApproach) -> ProgrammingTest:
        """Probar enfoque específico de programación"""
        
        approach_info = self.programming_approaches[approach]
        prompt = approach_info["template"].format(query=query)
        
        print(f"║  🔍 Testing {approach_info['name']}: {approach_info['description']}")
        
        result = await self.call_model(prompt)
        
        if not result["success"]:
            return ProgrammingTest(
                approach=approach,
                query=query,
                prompt=prompt,
                response="",
                score=0.0,
                code_quality=0.0,
                explanation_quality=0.0,
                implementation_quality=0.0,
                details=f"Error: {result['error']}"
            )
        
        response = result["response"]
        score = self.calculate_programming_score(response)
        quality_analysis = self.analyze_code_quality(response)
        
        return ProgrammingTest(
            approach=approach,
            query=query,
            prompt=prompt,
            response=response,
            score=score,
            code_quality=quality_analysis["code_quality"],
            explanation_quality=quality_analysis["explanation_quality"],
            implementation_quality=quality_analysis["implementation_quality"],
            details=f"Score: {score:.3f}, Code: {quality_analysis['code_quality']:.3f}, Explanation: {quality_analysis['explanation_quality']:.3f}"
        )
    
    async def run_detailed_programming_analysis(self):
        """Ejecutar análisis detallado de programación"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  DETAILED PROGRAMMING ANALYSIS - IDENTIFICANDO NUDOS CRÍTICOS")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  Testing different programming approaches")
        print("║  Identifying critical nodes and bottlenecks")
        print("║  Analyzing performance degradation patterns")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Análisis por problema específico
        for i, problem in enumerate(self.programming_problems[:3]):  # Primeros 3 problemas
            print(f"\n╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"║  PROBLEM {i+1}: {problem[:60]}...")
            print("╚══════════════════════════════════════════════════════════════════════════════╝")
            
            problem_results = []
            
            # Probar todos los enfoques
            for approach in ProgrammingApproach:
                test_result = await self.test_programming_approach(problem, approach)
                problem_results.append(test_result)
                self.diagnostic_results.append(test_result)
                
                status_icon = "✅" if test_result.score > 0.7 else "⚠️" if test_result.score > 0.4 else "❌"
                print(f"║  {status_icon} {approach.value}: {test_result.score:.3f} (Code: {test_result.code_quality:.3f}, Explanation: {test_result.explanation_quality:.3f})")
            
            # Análisis del problema
            best_approach = max(problem_results, key=lambda x: x.score)
            worst_approach = min(problem_results, key=lambda x: x.score)
            
            print(f"║  📊 Best: {best_approach.approach.value} ({best_approach.score:.3f})")
            print(f"║  📊 Worst: {worst_approach.approach.value} ({worst_approach.score:.3f})")
            print(f"║  📊 Range: {best_approach.score - worst_approach.score:.3f}")
        
        # Análisis diagnóstico final
        self.print_diagnostic_analysis()
    
    def print_diagnostic_analysis(self):
        """Imprimir análisis diagnóstico final"""
        
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  PROGRAMMING DIAGNOSTIC ANALYSIS - NUDOS CRÍTICOS IDENTIFICADOS")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Análisis por enfoque
        approach_analysis = {}
        for result in self.diagnostic_results:
            if result.approach not in approach_analysis:
                approach_analysis[result.approach] = []
            approach_analysis[result.approach].append(result)
        
        print("║  APPROACH PERFORMANCE ANALYSIS:")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        approach_scores = []
        for approach, results in approach_analysis.items():
            avg_score = sum(r.score for r in results) / len(results)
            avg_code = sum(r.code_quality for r in results) / len(results)
            avg_explanation = sum(r.explanation_quality for r in results) / len(results)
            avg_implementation = sum(r.implementation_quality for r in results) / len(results)
            
            approach_scores.append((approach, avg_score, avg_code, avg_explanation, avg_implementation))
            
            status_icon = "✅" if avg_score > 0.7 else "⚠️" if avg_score > 0.4 else "❌"
            print(f"║  {status_icon} {approach.value}: {avg_score:.3f} (Code: {avg_code:.3f}, Explanation: {avg_explanation:.3f}, Implementation: {avg_implementation:.3f})")
        
        # Identificar nudos críticos
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  CRITICAL NODES IDENTIFIED:")
        
        best_approach = max(approach_scores, key=lambda x: x[1])
        worst_approach = min(approach_scores, key=lambda x: x[1])
        
        print(f"║  🏆 BEST APPROACH: {best_approach[0].value} ({best_approach[1]:.3f})")
        print(f"║  ❌ WORST APPROACH: {worst_approach[0].value} ({worst_approach[1]:.3f})")
        print(f"║  📊 PERFORMANCE RANGE: {best_approach[1] - worst_approach[1]:.3f}")
        
        # Análisis de nudos
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  NODE ANALYSIS:")
        
        # Nudo 1: Complejidad de prompts
        complex_prompts = [r for r in self.diagnostic_results if len(r.prompt) > 100]
        simple_prompts = [r for r in self.diagnostic_results if len(r.prompt) <= 100]
        
        if complex_prompts and simple_prompts:
            avg_complex = sum(r.score for r in complex_prompts) / len(complex_prompts)
            avg_simple = sum(r.score for r in simple_prompts) / len(simple_prompts)
            print(f"║  🔍 NUDO 1 - COMPLEXITY: Complex prompts ({avg_complex:.3f}) vs Simple prompts ({avg_simple:.3f})")
            print(f"║     Difference: {avg_complex - avg_simple:.3f}")
        
        # Nudo 2: Enfoque vs rendimiento
        explanation_first = [r for r in self.diagnostic_results if "explic" in r.prompt.lower()]
        code_first = [r for r in self.diagnostic_results if "código" in r.prompt.lower() or "code" in r.prompt.lower()]
        
        if explanation_first and code_first:
            avg_explanation = sum(r.score for r in explanation_first) / len(explanation_first)
            avg_code = sum(r.score for r in code_first) / len(code_first)
            print(f"║  🔍 NUDO 2 - APPROACH: Explanation first ({avg_explanation:.3f}) vs Code first ({avg_code:.3f})")
            print(f"║     Difference: {avg_explanation - avg_code:.3f}")
        
        # Nudo 3: Calidad de código vs explicación
        high_code_quality = [r for r in self.diagnostic_results if r.code_quality > 0.7]
        high_explanation_quality = [r for r in self.diagnostic_results if r.explanation_quality > 0.7]
        
        if high_code_quality and high_explanation_quality:
            avg_code_score = sum(r.score for r in high_code_quality) / len(high_code_quality)
            avg_explanation_score = sum(r.score for r in high_explanation_quality) / len(high_explanation_quality)
            print(f"║  🔍 NUDO 3 - QUALITY: High code quality ({avg_code_score:.3f}) vs High explanation quality ({avg_explanation_score:.3f})")
            print(f"║     Difference: {avg_code_score - avg_explanation_score:.3f}")
        
        # Recomendaciones específicas
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  SPECIFIC RECOMMENDATIONS:")
        
        if best_approach[1] > 0.7:
            print("║  🎯 OPTIMAL APPROACH FOUND:")
            print(f"║     • Use {best_approach[0].value} as primary approach")
            print(f"║     • Score: {best_approach[1]:.3f}")
            print(f"║     • Code Quality: {best_approach[2]:.3f}")
            print(f"║     • Explanation Quality: {best_approach[3]:.3f}")
        else:
            print("║  ⚠️  NO OPTIMAL APPROACH FOUND:")
            print("║     • All approaches need improvement")
            print("║     • Consider hybrid strategies")
            print("║     • Focus on specific problem types")
        
        print("║  🔧 IMPLEMENTATION STRATEGY:")
        print("║     • Eliminate worst performing approaches")
        print("║     • Optimize best performing approaches")
        print("║     • Create domain-specific hybrids")
        print("║     • Focus on code quality over complexity")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")

async def main():
    """Función principal del análisis diagnóstico"""
    
    diagnostic = ProgrammingDiagnosticAnalysis()
    diagnostic.print_header()
    
    await diagnostic.run_detailed_programming_analysis()

if __name__ == "__main__":
    asyncio.run(main())
