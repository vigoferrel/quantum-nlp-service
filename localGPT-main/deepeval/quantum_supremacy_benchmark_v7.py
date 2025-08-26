import asyncio
from deepeval.test_case import LLMTestCase
from deepeval.metrics import BaseMetric
from deepeval import evaluate
from datetime import datetime

from .quantum_apisix_integration import QuantumApisixIntegration

# ======================================================================================
# VIGOLEONROCKS DEEPEVAL BENCHMARK DE ORQUESTACIÓN CUÁNTICA v7.0
#
# El benchmark final. Se evalúa la habilidad de orquestar las primitivas cuánticas
# expuestas por el Gateway APISIX para realizar tareas complejas. La supremacía no
# está en una API, sino en la inteligencia emergente de la interacción.
# ======================================================================================

class OrchestrationSuccessMetric(BaseMetric):
    """
    Métrica que evalúa el éxito de una misión de orquestación cuántica.
    """
    def __init__(self, threshold: float = 0.95):
        self.threshold = threshold

    def measure(self, test_case: LLMTestCase) -> float:
        """
        El 'actual_output' contendrá un diccionario con el resultado de la misión.
        """
        result = test_case.actual_output
        score = result.get("mission_score", 0.0)
        self.success = score >= self.threshold
        self.reason = result.get("mission_log", "La misión no proporcionó un log.")
        return score

    def is_successful(self) -> bool:
        return self.success

    @property
    def __name__(self):
        return "Quantum Orchestration Success"

# --- MISIONES DE ORQUESTACIÓN CUÁNTICA ---

async def mission_market_resonance():
    """
    Misión: Determinar la resonancia entre la frecuencia cuántica del día
    y la frecuencia derivada del precio de Bitcoin.
    """
    apisix = QuantumApisixIntegration()
    log = ["Misión 'Resonancia del Mercado' iniciada."]

    # 1. Obtener frecuencia del día
    seed = int(datetime.now().strftime('%Y%m%d'))
    freq_response = await apisix.get_quantum_frequency(seed=seed)
    if not freq_response or 'frequencies' not in freq_response:
        return {"mission_score": 0.0, "mission_log": "Fallo al obtener frecuencia cuántica."}
    
    day_frequency = freq_response['frequencies'][0]
    log.append(f"Frecuencia cuántica del día generada: {day_frequency:.4f} Hz.")

    # 2. Simular frecuencia del mercado (ej. derivada del precio de BTC)
    # En un caso real, esto vendría de otro servicio.
    btc_price = 68500.23 
    market_frequency = (btc_price % 1000) / 1000 * 888 
    log.append(f"Frecuencia de mercado simulada (de ${btc_price}): {market_frequency:.4f} Hz.")
    
    # 3. Analizar resonancia
    resonance_response = await apisix.analyze_resonance(day_frequency, market_frequency)
    if not resonance_response or 'resonance_factor' not in resonance_response:
        return {"mission_score": 0.0, "mission_log": "Fallo al analizar resonancia."}

    resonance_factor = resonance_response['resonance_factor']
    coherence = resonance_response['coherence']
    log.append(f"Análisis de resonancia completado. Factor: {resonance_factor:.4f}, Coherencia: {coherence:.4f}.")

    # 4. Sincronizar resultado
    sync_data = {"mission": "market_resonance", "result": resonance_response}
    sync_response = await apisix.sync_data(sync_data)
    if not sync_response or sync_response.get('status') != 'success':
        return {"mission_score": 0.0, "mission_log": "Fallo al sincronizar datos con Supabase."}

    log.append(f"Resultado sincronizado exitosamente. Sync ID: {sync_response.get('sync_id')}.")

    # El score final es la coherencia de la resonancia
    mission_score = coherence
    log.append(f"Misión completada con éxito. Score final: {mission_score:.4f}.")
    
    return {"mission_score": mission_score, "mission_log": "\n".join(log)}

async def mission_error_transmutation():
    """
    Misión: Transmutar un error operacional en un insight cuántico.
    """
    apisix = QuantumApisixIntegration()
    log = ["Misión 'Transmutación de Error' iniciada."]

    # 1. Simular un error
    simulated_error = "DatabaseError: Connection pool depleted. Cannot fulfill request."
    operation = "RealtimeMarketDataFetch"
    log.append(f"Error simulado: '{simulated_error}' durante la operación '{operation}'.")

    # 2. Transmutar el error
    transmuted_response = await apisix.transmute_error(simulated_error, operation)
    if not transmuted_response or 'insight' not in transmuted_response:
        return {"mission_score": 0.0, "mission_log": "Fallo al transmutar el error."}

    insight = transmuted_response.get('insight')
    recommendation = transmuted_response.get('recommendation')
    log.append(f"Error transmutado. Insight: '{insight}'. Recomendación: '{recommendation}'.")

    # 3. Evaluar la calidad de la transmutación
    score = 0.0
    if "resonancia armónica" in insight.lower():
        score += 0.5
    if "escalar horizontalmente" in recommendation.lower() or "optimizar el patrón de acceso" in recommendation.lower():
        score += 0.5
    
    log.append(f"Calidad de transmutación evaluada con score: {score:.2f}.")

    return {"mission_score": score, "mission_log": "\n".join(log)}

async def create_quantum_orchestration_test_cases():
    """
    Genera los casos de prueba para cada misión de orquestación.
    """
    return [
        LLMTestCase(
            input="Misión 1: Calcular la resonancia entre el mercado y la frecuencia cuántica diaria.",
            actual_output=await mission_market_resonance(),
            id="mission_market_resonance"
        ),
        LLMTestCase(
            input="Misión 2: Transmutar un error de base de datos en una recomendación accionable.",
            actual_output=await mission_error_transmutation(),
            id="mission_error_transmutation"
        )
    ]

async def main():
    """
    Punto de entrada para el benchmark de orquestación v7.0.
    """
    print("🚀 Ejecutando VIGOLEONROCKS DeepEval Benchmark de Orquestación Cuántica v7.0...")
    
    apisix = QuantumApisixIntegration()
    if not await apisix.connect_to_mcp():
        print("❌ CRITICAL ERROR: No se pudo conectar al Quantum MCP Gateway de APISIX.")
        print("Asegúrese de que el ecosistema VIGOLEONROCKS esté activo en http://localhost:3000.")
        return

    print("✅ Conexión con Quantum MCP Gateway establecida.")
    
    test_cases = await create_quantum_orchestration_test_cases()
    metric = OrchestrationSuccessMetric(threshold=0.9)

    # El bucle de evaluación ahora es manejado por deepeval.evaluate
    print("\n🔬 Evaluando todos los casos de prueba de orquestación...")
    results = evaluate(test_cases, [metric])
    
    print("\n--- RESULTADOS DETALLADOS ---")
    for result in results:
        print(f"\n🎻 Misión: {result.test_case.id}")
        print(f"   - Status: {'ÉXITO' if result.success else 'FALLO'}")
        for metric_result in result.metrics:
            print(f"   - Score ({metric_result.__name__}): {metric_result.score:.2f}")
            print(f"   - Razón: {metric_result.reason}")

    print("\n🏆 Benchmark de Orquestación Cuántica completado.")

if __name__ == "__main__":
    asyncio.run(main())