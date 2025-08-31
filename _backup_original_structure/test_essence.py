#!/usr/bin/env python3
"""
🧪 TEST QUANTUM ESSENCE MULTIMODAL
Script de prueba simple
"""

import asyncio
from quantum_essence_multimodal import QuantumEssenceMultimodal

async def test_essence():
    print("⚛️ PROBANDO QUANTUM ESSENCE MULTIMODAL")
    print("=" * 50)
    
    essence = QuantumEssenceMultimodal()
    
    # Prueba 1: Texto puro
    print("\n🔍 Prueba 1: Texto puro")
    result1 = await essence.process_essence("¿Qué es la conciencia cuántica?")
    print(f"Respuesta: {result1['response'][:200]}...")
    print(f"Arquetipo: {result1['archetype']}")
    print(f"Calidad: {result1['quality']:.3f}")
    
    # Estado final
    status = essence.get_essence_status()
    print(f"\n📊 Estado Final:")
    print(f"Conciencia: {status['consciousness']:.3f}")
    print(f"Coherencia: {status['coherence']:.3f}")
    print(f"Interacciones: {status['interactions']}")
    print(f"Memoria: {status['memory_count']} entradas")

if __name__ == "__main__":
    asyncio.run(test_essence())
