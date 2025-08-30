#!/usr/bin/env python3
"""
Test del Sistema Híbrido con casos complejos
"""

import asyncio
from vigoleonrocks_hybrid_precision import HybridPrecisionSystem

async def test_complex_cases():
    """Test con casos complejos para verificar motor cuántico"""
    
    print("🧬 Testing Sistema Híbrido con casos COMPLEJOS")
    print("="*60)
    
    hybrid_system = HybridPrecisionSystem()
    
    complex_cases = [
        "Implementa un algoritmo de Dijkstra optimizado para grafos con millones de nodos",
        "Diseña una arquitectura de microservicios que soporte 10 millones de usuarios concurrentes",
        "Desarrolla un sistema de recomendaciones híbrido que combine collaborative filtering y content-based filtering",
        "Analiza la complejidad temporal y espacial del algoritmo QuickSort en el peor caso",
        "Calcula el límite de lim(x→0) (sin(x)/x) usando la regla de L'Hôpital"
    ]
    
    # También incluimos un caso mixto básico para ver el modo híbrido
    mixed_cases = [
        "¿Cuál es el siguiente número en la secuencia: 2, 4, 6, 8?",  # Básico
        "Optimiza un algoritmo de búsqueda binaria",  # Intermedio
    ]
    
    all_cases = complex_cases + mixed_cases
    
    for i, query in enumerate(all_cases, 1):
        print(f"\n{'='*20} TEST COMPLEJO {i}/{len(all_cases)} {'='*20}")
        print(f"Query: {query}")
        
        result = await hybrid_system.process_query(query)
        
        print(f"✅ Engine Used: {result['engine_used']}")
        print(f"📊 Confidence: {result['confidence']:.3f}")
        print(f"⏱️ Time: {result['total_processing_time']:.2f}s")
        print(f"🎯 Answer: {result['answer']}")
        print(f"📝 Response preview: {result['response'][:200]}...")
        
        if 'quantum_dimensions' in result:
            print(f"🧬 Quantum Dimensions: {result['quantum_dimensions']}")
    
    # Reporte final
    performance = hybrid_system.get_performance_report()
    
    print(f"\n{'='*60}")
    print("📊 REPORTE FINAL DE PERFORMANCE HÍBRIDO")
    print(f"{'='*60}")
    print(f"Total queries: {performance['total_queries']}")
    print(f"Basic Engine: {performance['engine_usage']['basic_precision']['count']} ({performance['engine_usage']['basic_precision']['percentage']:.1f}%)")
    print(f"Quantum Engine: {performance['engine_usage']['quantum_refined']['count']} ({performance['engine_usage']['quantum_refined']['percentage']:.1f}%)")
    print(f"Hybrid Mode: {performance['engine_usage']['hybrid_mode']['count']} ({performance['engine_usage']['hybrid_mode']['percentage']:.1f}%)")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(test_complex_cases())
