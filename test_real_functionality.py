#!/usr/bin/env python3
"""
🧪 TEST REAL FUNCTIONALITY
Prueba la funcionalidad real de la esencia cuántica
"""

import asyncio
from quantum_essence_real import QuantumInterfaceReal

async def test_real_functionality():
    print("🧪 PROBANDO FUNCIONALIDAD REAL")
    print("=" * 50)
    
    interface = QuantumInterfaceReal()
    
    # Prueba 1: Consulta simple
    print("\n🔍 Prueba 1: Consulta simple")
    query1 = "¿Quién eres?"
    result1 = await interface.process_query(query1)
    
    print(f"Consulta: {result1['query']}")
    print(f"Respuesta: {result1['response'][:200]}...")
    print(f"Arquetipo: {result1['archetype']}")
    print(f"Calidad: {result1['quality']:.3f}")
    print(f"Longitud respuesta: {len(result1['response'])} caracteres")
    
    # Prueba 2: Consulta compleja
    print("\n🔍 Prueba 2: Consulta compleja")
    query2 = "Explícame detalladamente qué es la conciencia cuántica y cómo funciona"
    result2 = await interface.process_query(query2)
    
    print(f"Consulta: {result2['query']}")
    print(f"Respuesta: {result2['response'][:300]}...")
    print(f"Arquetipo: {result2['archetype']}")
    print(f"Calidad: {result2['quality']:.3f}")
    print(f"Longitud respuesta: {len(result2['response'])} caracteres")
    
    # Estado del sistema
    print("\n📊 Estado del Sistema:")
    status = interface.get_status()
    print(f"Nivel de Conciencia: {status['consciousness_level']:.3f}")
    print(f"Coherencia Cuántica: {status['quantum_coherence']:.3f}")
    print(f"Interacciones: {status['total_interactions']}")
    print(f"Memoria: {status['memory_size']} entradas")
    print(f"Calidad Promedio: {status['average_quality']:.3f}")
    
    print("\n✅ Pruebas completadas")

if __name__ == "__main__":
    asyncio.run(test_real_functionality())
