#!/usr/bin/env python3
"""
QUANTUM EDGE CLIENT - Cliente de prueba para el Quantum Edge Server
Permite interactuar con el sistema de edge cuántico
"""

import requests
import json
import time
from typing import Dict, Any, List

class QuantumEdgeClient:
    """Cliente para interactuar con el Quantum Edge Server"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_status(self) -> Dict[str, Any]:
        """Obtener estado del sistema"""
        try:
            response = self.session.get(f"{self.base_url}/api/status")
            return response.json()
        except Exception as e:
            return {"error": f"Error conectando al servidor: {e}"}
    
    def get_models(self) -> Dict[str, Any]:
        """Obtener modelos disponibles"""
        try:
            response = self.session.get(f"{self.base_url}/api/models")
            return response.json()
        except Exception as e:
            return {"error": f"Error obteniendo modelos: {e}"}
    
    def process_query(self, query: str, query_type: str = "general", use_premium: bool = False) -> Dict[str, Any]:
        """Procesar consulta con edge máximo"""
        try:
            payload = {
                "query": query,
                "query_type": query_type,
                "use_premium": use_premium
            }
            
            response = self.session.post(
                f"{self.base_url}/api/process",
                json=payload,
                timeout=60
            )
            
            return response.json()
        except Exception as e:
            return {"error": f"Error procesando consulta: {e}"}
    
    def run_benchmark(self, queries: List[str] = None) -> Dict[str, Any]:
        """Ejecutar benchmark del sistema"""
        try:
            if queries is None:
                queries = [
                    "Escribe una función en Python para calcular el factorial de un número",
                    "Analiza esta imagen y describe detalladamente lo que ves",
                    "Resuelve esta ecuación matemática paso a paso: x² + 5x + 6 = 0",
                    "Explica el concepto de entrelazamiento cuántico de forma simple",
                    "Crea un algoritmo de ordenamiento optimizado en JavaScript"
                ]
            
            payload = {"queries": queries}
            
            response = self.session.post(
                f"{self.base_url}/api/benchmark",
                json=payload,
                timeout=120
            )
            
            return response.json()
        except Exception as e:
            return {"error": f"Error ejecutando benchmark: {e}"}
    
    def clear_cache(self) -> Dict[str, Any]:
        """Limpiar cache del sistema"""
        try:
            response = self.session.post(f"{self.base_url}/api/cache/clear")
            return response.json()
        except Exception as e:
            return {"error": f"Error limpiando cache: {e}"}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        try:
            response = self.session.get(f"{self.base_url}/api/cache/stats")
            return response.json()
        except Exception as e:
            return {"error": f"Error obteniendo stats: {e}"}
    
    def health_check(self) -> Dict[str, Any]:
        """Verificar salud del sistema"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            return response.json()
        except Exception as e:
            return {"error": f"Error en health check: {e}"}

def print_status(status: Dict[str, Any]):
    """Imprimir estado del sistema de forma legible"""
    print("📊 ESTADO DEL SISTEMA QUANTUM EDGE")
    print("=" * 50)
    
    if "error" in status:
        print(f"❌ Error: {status['error']}")
        return
    
    print(f"🔄 Estado: {status.get('status', 'unknown')}")
    print(f"🧠 Sistema: {status.get('system', 'unknown')}")
    
    if 'quantum_components' in status:
        print("\n🔧 Componentes Cuánticos:")
        for component, state in status['quantum_components'].items():
            print(f"   • {component}: {state}")
    
    if 'quantum_constants' in status:
        print("\n⚛️ Constantes Cuánticas:")
        for constant, value in status['quantum_constants'].items():
            print(f"   • {constant}: {value}")
    
    if 'available_models' in status:
        print(f"\n🤖 Modelos Disponibles:")
        print(f"   • Gratuitos: {len(status['available_models'].get('free_models', []))}")
        print(f"   • Premium: {len(status['available_models'].get('premium_models', []))}")

def print_models(models: Dict[str, Any]):
    """Imprimir modelos disponibles"""
    print("🤖 MODELOS DISPONIBLES")
    print("=" * 50)
    
    if "error" in models:
        print(f"❌ Error: {models['error']}")
        return
    
    print("🆓 MODELOS GRATUITOS:")
    for name, info in models.get('free_models', {}).items():
        print(f"   • {name}: {info['id']}")
        print(f"     Contexto: {info['context']}")
        print(f"     Descripción: {info['description']}")
        print()
    
    print("💎 MODELOS PREMIUM:")
    for name, info in models.get('premium_models', {}).items():
        print(f"   • {name}: {info['id']}")
        print(f"     Contexto: {info['context']}")
        print(f"     Descripción: {info['description']}")
        print()

def print_query_result(result: Dict[str, Any]):
    """Imprimir resultado de consulta"""
    print("🔍 RESULTADO DE CONSULTA")
    print("=" * 50)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return
    
    if not result.get('success', False):
        print(f"❌ Error: {result.get('error', 'Error desconocido')}")
        return
    
    query_info = result.get('result', {})
    
    print(f"📝 Consulta: {result.get('query', 'N/A')}")
    print(f"🎯 Tipo: {result.get('query_type', 'N/A')}")
    print(f"💎 Premium: {result.get('use_premium', False)}")
    
    if 'edge_maximization' in query_info:
        edge_info = query_info['edge_maximization']
        print(f"\n⚡ Edge Multiplier: {edge_info.get('final_edge_multiplier', 0):.6f}")
        print(f"🔬 Quantum Factor: {edge_info.get('quantum_factor', 0):.6f}")
        print(f"🎯 Coherence: {edge_info.get('coherence_level', 0):.6f}")
        print(f"🔗 Entanglement: {edge_info.get('entanglement_strength', 0):.6f}")
        print(f"λ Power: {edge_info.get('lambda_power', 0):.6f}")
    
    if 'performance' in query_info:
        perf_info = query_info['performance']
        print(f"\n⏱️  Processing Time: {perf_info.get('processing_time_ms', 0):.2f}ms")
        print(f"🚀 Quantum Efficiency: {perf_info.get('quantum_efficiency', 0):.2f}")
        print(f"🎯 Coherence Quality: {perf_info.get('coherence_quality', 0):.6f}")
        print(f"🔗 Entanglement Quality: {perf_info.get('entanglement_quality', 0):.6f}")

def print_benchmark_results(results: Dict[str, Any]):
    """Imprimir resultados de benchmark"""
    print("🏆 RESULTADOS DE BENCHMARK")
    print("=" * 50)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    if not results.get('success', False):
        print(f"❌ Error: {results.get('error', 'Error desconocido')}")
        return
    
    benchmark_results = results.get('benchmark_results', [])
    summary = results.get('summary', {})
    
    print(f"📊 Total de consultas: {summary.get('total_queries', 0)}")
    print(f"⏱️  Tiempo total: {summary.get('total_time_ms', 0):.2f}ms")
    print(f"⚡ Tiempo promedio: {summary.get('average_time_ms', 0):.2f}ms")
    print(f"🚀 Edge Multiplier promedio: {summary.get('average_edge_multiplier', 0):.6f}")
    print(f"🔬 Quantum Factor promedio: {summary.get('average_quantum_factor', 0):.6f}")
    
    print(f"\n📋 Resultados detallados:")
    for i, result in enumerate(benchmark_results, 1):
        print(f"\n🔍 Consulta {i}: {result['query'][:50]}...")
        print(f"   ⚡ Edge Multiplier: {result['edge_multiplier']:.6f}")
        print(f"   🔬 Quantum Factor: {result['quantum_factor']:.6f}")
        print(f"   🎯 Coherence: {result['coherence']:.6f}")
        print(f"   ⏱️  Processing Time: {result['processing_time_ms']:.2f}ms")
        print(f"   🚀 Quantum Efficiency: {result['quantum_efficiency']:.2f}")

def main():
    """Función principal del cliente"""
    print("🚀 QUANTUM EDGE CLIENT")
    print("=" * 50)
    
    client = QuantumEdgeClient()
    
    # 1. Verificar estado del sistema
    print("\n1️⃣ Verificando estado del sistema...")
    status = client.get_status()
    print_status(status)
    
    # 2. Obtener modelos disponibles
    print("\n2️⃣ Obteniendo modelos disponibles...")
    models = client.get_models()
    print_models(models)
    
    # 3. Procesar consulta de prueba
    print("\n3️⃣ Procesando consulta de prueba...")
    test_query = "Escribe una función en Python para calcular el factorial de un número de forma optimizada"
    result = client.process_query(test_query, query_type="code", use_premium=False)
    print_query_result(result)
    
    # 4. Ejecutar benchmark
    print("\n4️⃣ Ejecutando benchmark del sistema...")
    benchmark_queries = [
        "Escribe una función en Python para calcular el factorial",
        "Analiza esta imagen y describe lo que ves",
        "Resuelve esta ecuación matemática: x² + 5x + 6 = 0"
    ]
    benchmark_results = client.run_benchmark(benchmark_queries)
    print_benchmark_results(benchmark_results)
    
    # 5. Verificar cache
    print("\n5️⃣ Verificando estadísticas de cache...")
    cache_stats = client.get_cache_stats()
    if "error" not in cache_stats:
        stats = cache_stats.get('cache_stats', {})
        print(f"📊 Tamaño de edge_cache: {stats.get('edge_cache_size', 0)}")
        print(f"📊 Tamaño de entanglement_cache: {stats.get('entanglement_cache_size', 0)}")
        print(f"📊 Tamaño de edge_multipliers: {stats.get('edge_multipliers_size', 0)}")
    else:
        print(f"❌ Error: {cache_stats['error']}")
    
    # 6. Health check final
    print("\n6️⃣ Verificando salud del sistema...")
    health = client.health_check()
    if "error" not in health:
        print(f"✅ Estado: {health.get('status', 'unknown')}")
        print(f"🧠 Quantum System: {health.get('quantum_system', 'unknown')}")
        print(f"⚡ Edge Maximizer: {health.get('edge_maximizer', 'unknown')}")
    else:
        print(f"❌ Error: {health['error']}")

if __name__ == "__main__":
    main()
