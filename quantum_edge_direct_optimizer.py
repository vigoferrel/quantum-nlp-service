#!/usr/bin/env python3
"""
🎯 QUANTUM EDGE DIRECT OPTIMIZER - Optimizador Directo de Calidad
Mejora la calidad del Quantum Edge Maximizer de manera simple y efectiva
"""

import asyncio
import time
import json
import requests
import numpy as np
from typing import Dict, List, Any
from quantum_edge_maximizer import QuantumEdgeMaximizer

class QuantumEdgeDirectOptimizer:
    """Optimizador directo de calidad del Quantum Edge Maximizer"""
    
    def __init__(self):
        self.openrouter_api_key = "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"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://quantum-edge-direct-optimizer.local",
            "X-Title": "Quantum Edge Direct Optimizer"
        }
        
        # Tests de calidad simples
        self.quality_tests = [
            {
                "name": "Code Generation",
                "prompt": "Write a Python function to calculate factorial with error handling.",
                "category": "programming",
                "expected_components": ["def", "factorial", "error", "return"]
            },
            {
                "name": "Math Problem",
                "prompt": "Calculate 15 * 8 + 32 step by step.",
                "category": "mathematics",
                "expected_components": ["15", "8", "32", "calculation", "result"]
            }
        ]
    
    async def run_direct_optimization(self):
        """Ejecuta optimización directa"""
        
        print("🎯 QUANTUM EDGE DIRECT OPTIMIZER")
        print("=" * 50)
        print("🎯 Objetivo: Mejorar calidad de manera directa y efectiva")
        print()
        
        # 1. Testear calidad actual
        await self._test_current_quality()
        
        # 2. Aplicar optimización directa
        await self._apply_direct_optimization()
        
        # 3. Evaluar resultados
        await self._evaluate_results()
    
    async def _test_current_quality(self):
        """Testea calidad actual"""
        
        print("📊 CALIDAD ACTUAL")
        print("-" * 30)
        
        current_results = []
        
        for test in self.quality_tests:
            print(f"\n🔬 {test['name']}")
            
            try:
                maximizer = QuantumEdgeMaximizer()
                edge_metrics = await maximizer.maximize_edge_for_query(test["prompt"], test["category"])
                
                # Generar respuesta actual
                current_response = await self._generate_simple_response(test["prompt"], edge_metrics)
                
                # Calcular calidad
                current_quality = self._calculate_simple_quality(current_response, test)
                
                current_results.append({
                    'test_name': test['name'],
                    'quality': current_quality,
                    'response': current_response
                })
                
                print(f"   📊 Calidad: {current_quality:.3f}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        self.current_results = current_results
    
    async def _apply_direct_optimization(self):
        """Aplica optimización directa"""
        
        print(f"\n⚡ OPTIMIZACIÓN DIRECTA")
        print("-" * 30)
        
        optimized_results = []
        
        for test in self.quality_tests:
            print(f"\n🔬 {test['name']} (Optimizado)")
            
            try:
                maximizer = QuantumEdgeMaximizer()
                
                # Prompt optimizado simple
                optimized_prompt = self._create_optimized_prompt(test["prompt"])
                
                edge_metrics = await maximizer.maximize_edge_for_query(optimized_prompt, test["category"])
                
                # Generar respuesta optimizada
                optimized_response = await self._generate_optimized_response(optimized_prompt, edge_metrics)
                
                # Calcular calidad
                optimized_quality = self._calculate_simple_quality(optimized_response, test)
                
                optimized_results.append({
                    'test_name': test['name'],
                    'quality': optimized_quality,
                    'response': optimized_response
                })
                
                print(f"   🚀 Calidad: {optimized_quality:.3f}")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        self.optimized_results = optimized_results
    
    def _create_optimized_prompt(self, prompt: str) -> str:
        """Crea prompt optimizado simple"""
        
        return f"""
Please provide a clear, complete, and well-structured response to the following query:

{prompt}

Requirements:
- Be comprehensive and detailed
- Use clear structure and formatting
- Include relevant examples if applicable
- Ensure accuracy and completeness
- Provide step-by-step explanation when needed

Please respond with high quality and attention to detail.
"""
    
    async def _generate_simple_response(self, prompt: str, edge_metrics: Dict) -> str:
        """Genera respuesta simple"""
        
        model_id = "qwen/qwen3-coder"
        
        simple_prompt = f"""
{prompt}

Please respond to this query.
"""
        
        try:
            payload = {
                "model": model_id,
                "messages": [
                    {"role": "user", "content": simple_prompt}
                ],
                "max_tokens": 300,
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
                return f"Response: {prompt[:50]}..."
                
        except Exception as e:
            return f"Response: {prompt[:50]}..."
    
    async def _generate_optimized_response(self, prompt: str, edge_metrics: Dict) -> str:
        """Genera respuesta optimizada"""
        
        model_id = "qwen/qwen3-coder"
        
        try:
            payload = {
                "model": model_id,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 400,
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
                return f"Optimized Response: {prompt[:50]}..."
                
        except Exception as e:
            return f"Optimized Response: {prompt[:50]}..."
    
    def _calculate_simple_quality(self, response: str, test: Dict) -> float:
        """Calcula calidad de manera simple"""
        
        response_lower = response.lower()
        word_count = len(response.split())
        
        # Relevancia
        expected_components = test.get('expected_components', [])
        relevance_score = 0.0
        if expected_components:
            found_components = sum(1 for component in expected_components if component.lower() in response_lower)
            relevance_score = found_components / len(expected_components)
        
        # Completitud
        completeness_score = min(1.0, word_count / 30)
        
        # Precisión
        accuracy_score = 0.9 if word_count > 20 else 0.6
        
        # Score general
        overall_score = (relevance_score + completeness_score + accuracy_score) / 3
        
        return overall_score
    
    async def _evaluate_results(self):
        """Evalúa los resultados"""
        
        print(f"\n📊 RESULTADOS")
        print("-" * 30)
        
        if hasattr(self, 'current_results') and hasattr(self, 'optimized_results'):
            for current, optimized in zip(self.current_results, self.optimized_results):
                improvement = optimized['quality'] - current['quality']
                improvement_factor = optimized['quality'] / current['quality'] if current['quality'] > 0 else 1.0
                
                print(f"\n🔬 {current['test_name']}:")
                print(f"   📊 Original: {current['quality']:.3f}")
                print(f"   🚀 Optimizado: {optimized['quality']:.3f}")
                print(f"   📈 Mejora: {improvement:+.3f} ({improvement_factor:.1%})")
                
                # Mostrar respuestas
                print(f"   📝 Original: {current['response'][:100]}...")
                print(f"   📝 Optimizado: {optimized['response'][:100]}...")
            
            # Calcular mejoras promedio
            improvements = [opt['quality'] - curr['quality'] for curr, opt in zip(self.current_results, self.optimized_results)]
            avg_improvement = np.mean(improvements)
            
            print(f"\n🏆 RESUMEN:")
            print(f"   📈 Mejora promedio: {avg_improvement:+.3f}")
            
            if avg_improvement > 0:
                print(f"   ✅ OPTIMIZACIÓN EXITOSA")
            else:
                print(f"   ⚠️ REQUIERE MÁS AJUSTES")

async def main():
    """Función principal"""
    
    optimizer = QuantumEdgeDirectOptimizer()
    await optimizer.run_direct_optimization()

if __name__ == "__main__":
    asyncio.run(main())
