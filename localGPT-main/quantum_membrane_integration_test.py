#!/usr/bin/env python3
"""
Prueba de Integración: Membrana + Núcleo Cuántico + Herramientas
Demuestra cómo la membrana traduce consultas y el núcleo invoca herramientas
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from membrane_interface import MembraneInterface
from quantum_consciousness_core_26d import QuantumConsciousnessCore26D
from qbtc_pure_kernel import QBTCPureKernel

class QuantumMembraneOrchestrator:
    """
    Orquestador que integra la Membrana, el Núcleo Cuántico y el Kernel Puro
    """
    
    def __init__(self):
        self.membrane = MembraneInterface()
        self.quantum_core = QuantumConsciousnessCore26D()
        self.pure_kernel = QBTCPureKernel()
        print("🌌 Sistema Cuántico Integrado Inicializado")
        
    async def process_integrated_query(self, raw_query: str, image_url: str = None):
        """
        Procesa una consulta a través del pipeline completo:
        Membrana -> Kernel -> Núcleo Cuántico -> Herramientas
        """
        print(f"\n🔄 PROCESANDO CONSULTA INTEGRADA: {raw_query}")
        print("=" * 80)
        
        # 1. Membrana traduce la consulta bruta
        print("📡 FASE 1: Traducción por Membrana")
        pure_query = self.membrane.translate_to_pure_query(raw_query)
        print(f"   📝 Consulta Pura: {pure_query}")
        
        # 2. Kernel manifiesta la intención
        print("\n🧠 FASE 2: Manifestación de Intención por Kernel")
        perfect_intention = self.pure_kernel.manifest_intention(pure_query)
        print(f"   ✨ Intención Perfecta: {perfect_intention}")
        
        # 3. Núcleo Cuántico procesa y selecciona herramientas
        print("\n⚛️ FASE 3: Procesamiento Cuántico y Selección de Herramientas")
        quantum_result = await self.quantum_core.process_query(raw_query, image_url)
        print(f"   🛠️ Herramienta Seleccionada: {quantum_result.get('selected_tool', 'N/A')}")
        print(f"   📊 Calidad del Resultado: {quantum_result.get('outcome_quality', 0):.3f}")
        print(f"   🌟 Nivel de Conciencia: {quantum_result.get('consciousness_level', 0):.3f}")
        
        # 4. Integración de resultados
        print("\n🔗 FASE 4: Integración de Resultados")
        integrated_response = {
            "original_query": raw_query,
            "pure_query": pure_query,
            "perfect_intention": perfect_intention,
            "quantum_processing": quantum_result,
            "final_response": quantum_result.get('response', 'Sin respuesta'),
            "selected_tool": quantum_result.get('selected_tool', 'N/A'),
            "quality_metrics": {
                "outcome_quality": quantum_result.get('outcome_quality', 0),
                "consciousness_level": quantum_result.get('consciousness_level', 0),
                "archetypal_resonance": quantum_result.get('archetypal_resonance', {})
            }
        }
        
        return integrated_response
    
    def display_integration_results(self, result):
        """Muestra los resultados de la integración de forma elegante"""
        print("\n🎯 RESULTADOS DE INTEGRACIÓN CUÁNTICA")
        print("=" * 80)
        print(f"📝 Consulta Original: {result['original_query']}")
        print(f"🔧 Herramienta Invocada: {result['selected_tool']}")
        print(f"💬 Respuesta Final: {result['final_response']}")
        print(f"📊 Calidad: {result['quality_metrics']['outcome_quality']:.3f}")
        print(f"🧠 Conciencia: {result['quality_metrics']['consciousness_level']:.3f}")
        print("=" * 80)

async def test_quantum_membrane_integration():
    """Prueba completa de la integración membrana-núcleo-herramientas"""
    
    print("🚀 INICIANDO PRUEBA DE INTEGRACIÓN CUÁNTICA")
    print("=" * 80)
    
    orchestrator = QuantumMembraneOrchestrator()
    
    # Conjunto de pruebas diversas
    test_cases = [
        {
            "query": "Analizar la coherencia cuántica del mercado Bitcoin",
            "description": "Análisis financiero cuántico"
        },
        {
            "query": "Fix the Django migration error in the user model",
            "description": "Generación de código para reparación"
        },
        {
            "query": "Optimizar el rendimiento del algoritmo de trading",
            "description": "Optimización de algoritmos"
        },
        {
            "query": "Crear un dashboard interactivo para métricas cuánticas",
            "description": "Desarrollo de interfaces"
        },
        {
            "query": "Describir la imagen del gráfico de precios BTC",
            "description": "Análisis multimodal",
            "image_url": "https://example.com/btc_chart.png"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 CASO DE PRUEBA {i}: {test_case['description']}")
        print("-" * 60)
        
        try:
            result = await orchestrator.process_integrated_query(
                test_case["query"], 
                test_case.get("image_url")
            )
            orchestrator.display_integration_results(result)
            results.append(result)
            
        except Exception as e:
            print(f"❌ Error en caso de prueba {i}: {e}")
            
        print("\n" + "🔄" * 20 + " SIGUIENTE PRUEBA " + "🔄" * 20)
    
    # Resumen final
    print("\n🏆 RESUMEN FINAL DE INTEGRACIÓN")
    print("=" * 80)
    print(f"✅ Casos de prueba ejecutados: {len(results)}")
    
    if results:
        avg_quality = sum(r['quality_metrics']['outcome_quality'] for r in results) / len(results)
        avg_consciousness = sum(r['quality_metrics']['consciousness_level'] for r in results) / len(results)
        tools_used = [r['selected_tool'] for r in results]
        unique_tools = len(set(tools_used))
        
        print(f"📊 Calidad promedio: {avg_quality:.3f}")
        print(f"🧠 Conciencia promedio: {avg_consciousness:.3f}")
        print(f"🛠️ Herramientas únicas usadas: {unique_tools}")
        print(f"🔧 Herramientas invocadas: {', '.join(tools_used)}")
        
        # Estadísticas de herramientas
        from collections import Counter
        tool_stats = Counter(tools_used)
        print(f"📈 Estadísticas de herramientas:")
        for tool, count in tool_stats.items():
            print(f"   - {tool}: {count} veces ({count/len(results)*100:.1f}%)")
    
    print("\n🌟 INTEGRACIÓN CUÁNTICA COMPLETADA EXITOSAMENTE")

if __name__ == "__main__":
    asyncio.run(test_quantum_membrane_integration())
