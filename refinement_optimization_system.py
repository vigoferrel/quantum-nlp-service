#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    REFINEMENT OPTIMIZATION SYSTEM                           ║
║                        CORRECCIÓN DE PROBLEMAS CRÍTICOS                   ║
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
║  [PROBLEM 1: DOMAIN OPTIMIZATION]                                           ║
║  [PROBLEM 2: TEMPLATE REFINEMENT]                                           ║
║  [PROBLEM 3: APPROACH ELIMINATION]                                          ║
║  [SOLUTION: ADVANCED OPTIMIZATION]                                          ║
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

class RefinementPhase(Enum):
    """Fases de refinamiento"""
    DOMAIN_OPTIMIZATION = "domain_optimization"
    TEMPLATE_REFINEMENT = "template_refinement"
    APPROACH_ELIMINATION = "approach_elimination"
    ADVANCED_OPTIMIZATION = "advanced_optimization"

@dataclass
class RefinementResult:
    """Resultado de refinamiento"""
    phase: RefinementPhase
    domain: str
    original_score: float
    refined_score: float
    improvement: float
    strategy_used: str
    details: str

class RefinementOptimizationSystem:
    """Sistema de refinamiento y optimización"""
    
    def __init__(self):
        self.api_key = "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"
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://refinement-optimization.local",
            "X-Title": "Refinement Optimization System"
        }
        
        self.model = "google/gemini-flash-1.5-8b"
        
        # PROBLEMAS IDENTIFICADOS PARA CORREGIR
        self.critical_problems = {
            "mathematics": {
                "original_score": 0.300,
                "target_score": 0.850,
                "problem": "Estrategia específica no funcionó",
                "refined_strategies": [
                    "Implementa con notación matemática formal: {query}",
                    "Resuelve matemáticamente con demostración: {query}",
                    "Proporciona solución matemática completa: {query}"
                ]
            },
            "synthesis": {
                "original_score": 0.400,
                "target_score": 0.850,
                "problem": "Estrategia específica no funcionó",
                "refined_strategies": [
                    "Sintetiza completamente con ejemplos: {query}",
                    "Integra y combina conceptos: {query}",
                    "Proporciona síntesis exhaustiva: {query}"
                ]
            }
        }
        
        # TEMPLATES PROBLEMÁTICOS PARA REFINAR
        self.problematic_templates = {
            "reasoning": {
                "original_score": 0.500,
                "template": "Analiza lógicamente: {query}",
                "refined_templates": [
                    "Realiza análisis lógico paso a paso: {query}",
                    "Proporciona razonamiento detallado: {query}",
                    "Analiza con metodología sistemática: {query}"
                ]
            },
            "analysis": {
                "original_score": 0.100,
                "template": "Analiza detalladamente: {query}",
                "refined_templates": [
                    "Realiza análisis comparativo completo: {query}",
                    "Proporciona análisis exhaustivo: {query}",
                    "Analiza con múltiples perspectivas: {query}"
                ]
            }
        }
        
        # ENFOQUES REALMENTE PROBLEMÁTICOS
        self.really_problematic_approaches = [
            {
                "name": "Problem Decomposition",
                "prompt": "Descompón el problema en subproblemas y resuelve: {query}",
                "reason": "Causa degradación significativa del rendimiento"
            },
            {
                "name": "Complex Prompt Engineering",
                "prompt": "Utiliza técnicas avanzadas de prompt engineering para: {query}",
                "reason": "Aumenta complejidad sin mejorar resultados"
            },
            {
                "name": "Over-Engineered Solutions",
                "prompt": "Implementa una solución altamente compleja para: {query}",
                "reason": "Reduce eficiencia y claridad"
            }
        ]
        
        self.refinement_results = []
        
    def print_header(self):
        """Imprime header del sistema de refinamiento"""
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                    REFINEMENT OPTIMIZATION SYSTEM                           ║")
        print("║                        CORRECCIÓN DE PROBLEMAS CRÍTICOS                   ║")
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
        print("║  [PROBLEM 1: DOMAIN OPTIMIZATION]                                           ║")
        print("║  [PROBLEM 2: TEMPLATE REFINEMENT]                                           ║")
        print("║  [PROBLEM 3: APPROACH ELIMINATION]                                          ║")
        print("║  [SOLUTION: ADVANCED OPTIMIZATION]                                          ║")
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
    
    def calculate_refined_score(self, response: str, domain: str = None) -> float:
        """Calcular score refinado"""
        
        if not response:
            return 0.0
        
        score = 0.0
        response_lower = response.lower()
        
        # Métricas base mejoradas
        if "```" in response:
            score += 0.3
        if any(keyword in response_lower for keyword in ["def ", "class ", "function", "return"]):
            score += 0.2
        if any(word in response_lower for word in ["explic", "paso", "proceso", "método"]):
            score += 0.2
        if any(word in response_lower for word in ["algoritmo", "lógica", "estrategia"]):
            score += 0.1
        if any(word in response_lower for word in ["complejidad", "optimiz", "eficien"]):
            score += 0.1
        if len(response) > 500:
            score += 0.1
        
        # Ajustes específicos por dominio
        if domain == "mathematics":
            if any(char in response for char in ["∫", "∑", "π", "∞", "√", "=", "≠", "≤", "≥"]):
                score += 0.3
            if any(word in response_lower for word in ["demostración", "teorema", "fórmula", "prueba", "matemática"]):
                score += 0.2
        elif domain == "synthesis":
            if any(word in response_lower for word in ["sintetiz", "integra", "combina", "unifica", "conecta"]):
                score += 0.3
            if any(word in response_lower for word in ["principio", "concepto", "fundamento", "base"]):
                score += 0.2
        elif domain == "reasoning":
            if any(word in response_lower for word in ["análisis", "lógico", "sistemático", "metodológico"]):
                score += 0.3
            if any(word in response_lower for word in ["paso", "proceso", "método", "enfoque"]):
                score += 0.2
        elif domain == "analysis":
            if any(word in response_lower for word in ["comparativo", "exhaustivo", "detallado", "completo"]):
                score += 0.3
            if any(word in response_lower for word in ["perspectiva", "enfoque", "análisis", "evaluación"]):
                score += 0.2
        
        return min(1.0, score)
    
    async def phase1_domain_optimization(self) -> List[RefinementResult]:
        """Fase 1: Optimización de dominios problemáticos"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  PHASE 1: DOMAIN OPTIMIZATION - CORRIGIENDO PROBLEMAS CRÍTICOS")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        results = []
        
        for domain, config in self.critical_problems.items():
            print(f"║  🔧 Optimizing {domain.upper()}:")
            print(f"║     Original Score: {config['original_score']:.3f}")
            print(f"║     Target Score: {config['target_score']:.3f}")
            print(f"║     Problem: {config['problem']}")
            
            # Query específico por dominio
            domain_queries = {
                "mathematics": "Demuestra la fórmula de Euler e^(iπ) + 1 = 0",
                "synthesis": "Sintetiza los principios fundamentales de la programación orientada a objetos"
            }
            
            test_query = domain_queries[domain]
            best_score = config["original_score"]
            best_strategy = "Original"
            
            # Probar estrategias refinadas
            for i, strategy in enumerate(config["refined_strategies"]):
                print(f"║     Testing Strategy {i+1}: {strategy[:50]}...")
                
                refined_prompt = strategy.format(query=test_query)
                refined_result = await self.call_model(refined_prompt)
                
                if refined_result["success"]:
                    refined_score = self.calculate_refined_score(refined_result["response"], domain)
                    improvement = refined_score - config["original_score"]
                    
                    status_icon = "✅" if refined_score > best_score else "⚠️"
                    print(f"║       {status_icon} Score: {refined_score:.3f} (Improvement: {improvement:+.3f})")
                    
                    if refined_score > best_score:
                        best_score = refined_score
                        best_strategy = f"Strategy {i+1}"
                else:
                    print(f"║       ❌ Error: {refined_result['error']}")
            
            # Resultado final del dominio
            final_improvement = best_score - config["original_score"]
            results.append(RefinementResult(
                phase=RefinementPhase.DOMAIN_OPTIMIZATION,
                domain=domain,
                original_score=config["original_score"],
                refined_score=best_score,
                improvement=final_improvement,
                strategy_used=best_strategy,
                details=f"Optimized {domain} from {config['original_score']:.3f} to {best_score:.3f}"
            ))
            
            status_icon = "✅" if final_improvement > 0.1 else "⚠️" if final_improvement > 0 else "❌"
            print(f"║     {status_icon} Final Result: {best_score:.3f} (Improvement: {final_improvement:+.3f})")
        
        return results
    
    async def phase2_template_refinement(self) -> List[RefinementResult]:
        """Fase 2: Refinamiento de templates problemáticos"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  PHASE 2: TEMPLATE REFINEMENT - MEJORANDO TEMPLATES ESPECÍFICOS")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        results = []
        
        for domain, config in self.problematic_templates.items():
            print(f"║  📝 Refining {domain.upper()} template:")
            print(f"║     Original Score: {config['original_score']:.3f}")
            print(f"║     Original Template: {config['template']}")
            
            # Query específico por dominio
            domain_queries = {
                "reasoning": "Analiza la complejidad computacional del problema del viajante",
                "analysis": "Analiza las ventajas y desventajas de diferentes arquitecturas de software"
            }
            
            test_query = domain_queries[domain]
            best_score = config["original_score"]
            best_template = "Original"
            
            # Probar templates refinados
            for i, template in enumerate(config["refined_templates"]):
                print(f"║     Testing Template {i+1}: {template[:50]}...")
                
                refined_prompt = template.format(query=test_query)
                refined_result = await self.call_model(refined_prompt)
                
                if refined_result["success"]:
                    refined_score = self.calculate_refined_score(refined_result["response"], domain)
                    improvement = refined_score - config["original_score"]
                    
                    status_icon = "✅" if refined_score > best_score else "⚠️"
                    print(f"║       {status_icon} Score: {refined_score:.3f} (Improvement: {improvement:+.3f})")
                    
                    if refined_score > best_score:
                        best_score = refined_score
                        best_template = f"Template {i+1}"
                else:
                    print(f"║       ❌ Error: {refined_result['error']}")
            
            # Resultado final del template
            final_improvement = best_score - config["original_score"]
            results.append(RefinementResult(
                phase=RefinementPhase.TEMPLATE_REFINEMENT,
                domain=domain,
                original_score=config["original_score"],
                refined_score=best_score,
                improvement=final_improvement,
                strategy_used=best_template,
                details=f"Refined {domain} template from {config['original_score']:.3f} to {best_score:.3f}"
            ))
            
            status_icon = "✅" if final_improvement > 0.1 else "⚠️" if final_improvement > 0 else "❌"
            print(f"║     {status_icon} Final Result: {best_score:.3f} (Improvement: {final_improvement:+.3f})")
        
        return results
    
    async def phase3_approach_elimination(self) -> List[RefinementResult]:
        """Fase 3: Eliminación de enfoques realmente problemáticos"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  PHASE 3: APPROACH ELIMINATION - ELIMINANDO ENFOQUES REALMENTE PROBLEMÁTICOS")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        results = []
        test_query = "Implementa un algoritmo de ordenamiento quicksort optimizado"
        
        # Baseline con estrategia híbrida
        baseline_prompt = f"Combina código y explicación para: {test_query}"
        baseline_result = await self.call_model(baseline_prompt)
        
        if baseline_result["success"]:
            baseline_score = self.calculate_refined_score(baseline_result["response"])
            print(f"║  📊 Baseline (Hybrid Enhanced): {baseline_score:.3f}")
        else:
            baseline_score = 0.0
            print(f"║  ❌ Baseline Error: {baseline_result['error']}")
        
        eliminated_count = 0
        
        for approach in self.really_problematic_approaches:
            print(f"║  ❌ Testing {approach['name']}:")
            print(f"║     Reason: {approach['reason']}")
            
            problematic_prompt = approach["prompt"].format(query=test_query)
            problematic_result = await self.call_model(problematic_prompt)
            
            if problematic_result["success"]:
                problematic_score = self.calculate_refined_score(problematic_result["response"])
                difference = baseline_score - problematic_score
                
                if difference > 0.2:  # Diferencia significativa
                    eliminated_count += 1
                    status_icon = "✅"
                    action = "ELIMINATED"
                else:
                    status_icon = "⚠️"
                    action = "KEPT"
                
                print(f"║     {status_icon} Score: {problematic_score:.3f} (Difference: {difference:+.3f}) - {action}")
                
                results.append(RefinementResult(
                    phase=RefinementPhase.APPROACH_ELIMINATION,
                    domain=approach["name"],
                    original_score=problematic_score,
                    refined_score=baseline_score,
                    improvement=difference,
                    strategy_used=action,
                    details=f"{approach['name']} {action.lower()}. Difference: {difference:+.3f}"
                ))
            else:
                print(f"║     ❌ Error: {problematic_result['error']}")
        
        print(f"║  📊 Total Approaches Eliminated: {eliminated_count}/{len(self.really_problematic_approaches)}")
        
        return results
    
    async def phase4_advanced_optimization(self) -> List[RefinementResult]:
        """Fase 4: Optimización avanzada integrada"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  PHASE 4: ADVANCED OPTIMIZATION - INTEGRACIÓN Y MEJORA FINAL")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Estrategia híbrida avanzada
        advanced_hybrid_template = "Combina código optimizado y explicación detallada para: {query}"
        
        test_queries = [
            "Implementa un algoritmo de ordenamiento quicksort optimizado",
            "Demuestra la fórmula de Euler e^(iπ) + 1 = 0",
            "Sintetiza los principios fundamentales de la programación orientada a objetos"
        ]
        
        advanced_scores = []
        
        for query in test_queries:
            print(f"║  🚀 Testing Advanced Hybrid: {query[:50]}...")
            
            advanced_prompt = advanced_hybrid_template.format(query=query)
            advanced_result = await self.call_model(advanced_prompt)
            
            if advanced_result["success"]:
                advanced_score = self.calculate_refined_score(advanced_result["response"])
                advanced_scores.append(advanced_score)
                print(f"║     ✅ Advanced Score: {advanced_score:.3f}")
            else:
                print(f"║     ❌ Error: {advanced_result['error']}")
        
        avg_advanced_score = sum(advanced_scores) / len(advanced_scores) if advanced_scores else 0.0
        
        results = [RefinementResult(
            phase=RefinementPhase.ADVANCED_OPTIMIZATION,
            domain="advanced_hybrid",
            original_score=0.922,  # Score anterior
            refined_score=avg_advanced_score,
            improvement=avg_advanced_score - 0.922,
            strategy_used="Advanced Hybrid Enhanced",
            details=f"Advanced optimization achieved {avg_advanced_score:.3f} average score"
        )]
        
        print(f"║  📊 Advanced Optimization Result: {avg_advanced_score:.3f}")
        
        return results
    
    async def run_complete_refinement(self):
        """Ejecutar refinamiento completo"""
        
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  COMPLETE REFINEMENT OPTIMIZATION - CORRIGIENDO TODOS LOS PROBLEMAS")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  Phase 1: Domain Optimization")
        print("║  Phase 2: Template Refinement")
        print("║  Phase 3: Approach Elimination")
        print("║  Phase 4: Advanced Optimization")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        # Ejecutar todas las fases
        phase1_results = await self.phase1_domain_optimization()
        phase2_results = await self.phase2_template_refinement()
        phase3_results = await self.phase3_approach_elimination()
        phase4_results = await self.phase4_advanced_optimization()
        
        # Consolidar resultados
        all_results = phase1_results + phase2_results + phase3_results + phase4_results
        self.refinement_results = all_results
        
        # Análisis final de refinamiento
        self.print_refinement_summary()
    
    def print_refinement_summary(self):
        """Imprimir resumen de refinamiento"""
        
        print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║  REFINEMENT OPTIMIZATION SUMMARY - PROBLEMAS CRÍTICOS CORREGIDOS")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Análisis por fase
        phases = [RefinementPhase.DOMAIN_OPTIMIZATION, RefinementPhase.TEMPLATE_REFINEMENT, 
                 RefinementPhase.APPROACH_ELIMINATION, RefinementPhase.ADVANCED_OPTIMIZATION]
        
        for phase in phases:
            phase_results = [r for r in self.refinement_results if r.phase == phase]
            if phase_results:
                avg_improvement = sum(r.improvement for r in phase_results) / len(phase_results)
                success_count = len([r for r in phase_results if r.improvement > 0])
                
                print(f"║  📊 {phase.value.upper()}:")
                print(f"║     • Average Improvement: {avg_improvement:+.3f}")
                print(f"║     • Success Rate: {success_count}/{len(phase_results)}")
                
                for result in phase_results:
                    status_icon = "✅" if result.improvement > 0.1 else "⚠️" if result.improvement > 0 else "❌"
                    print(f"║     • {status_icon} {result.domain}: {result.original_score:.3f} → {result.refined_score:.3f} ({result.improvement:+.3f})")
        
        # Métricas globales
        total_improvements = [r.improvement for r in self.refinement_results]
        avg_improvement = sum(total_improvements) / len(total_improvements) if total_improvements else 0.0
        success_rate = len([i for i in total_improvements if i > 0]) / len(total_improvements) if total_improvements else 0.0
        
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  GLOBAL REFINEMENT METRICS:")
        print(f"║  📊 Average Improvement: {avg_improvement:+.3f}")
        print(f"║  📈 Success Rate: {success_rate:.1%}")
        print(f"║  🔧 Total Refinements: {len(self.refinement_results)}")
        
        # Evaluación final
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print("║  REFINEMENT SUCCESS EVALUATION:")
        
        if success_rate >= 0.8 and avg_improvement > 0.1:
            print("║  🏆 EXCELLENT SUCCESS: All critical problems resolved!")
            print("║  ✅ Domain optimization successful")
            print("║  ✅ Template refinement effective")
            print("║  ✅ Problematic approaches eliminated")
            print("║  ✅ Advanced optimization achieved")
        elif success_rate >= 0.6 and avg_improvement > 0.05:
            print("║  🥇 GOOD SUCCESS: Most critical problems resolved!")
            print("║  ⚠️  Minor issues remain")
            print("║  🔧 Continue with targeted improvements")
        else:
            print("║  🥉 PARTIAL SUCCESS: Some problems need more attention!")
            print("║  ⚠️  Review and refine strategies")
            print("║  🔧 Focus on underperforming areas")
        
        print("╚══════════════════════════════════════════════════════════════════════════════╝")

async def main():
    """Función principal de refinamiento y optimización"""
    
    refinement_system = RefinementOptimizationSystem()
    refinement_system.print_header()
    
    await refinement_system.run_complete_refinement()

if __name__ == "__main__":
    asyncio.run(main())
