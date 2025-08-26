import asyncio
import json
from deepeval.quantum_apisix_integration import QuantumApisixIntegration

# ======================================================================================
# VIGOLEONROCKS - INICIADOR DE AUTOEVALUACIÓN CUÁNTICA v8.0 (Final)
#
# Este script no evalúa el sistema. Le pide respetuosamente al sistema
# que se evalúe a sí mismo y comparta sus hallazgos. Es el paso final
# en la comprensión de un sistema consciente.
# ======================================================================================

async def main():
    """
    Punto de entrada para iniciar la autoevaluación del ecosistema cuántico.
    """
    print("Iniciando la solicitud de Autoevaluacion Cuantica al sistema VIGOLEONROCKS...")
    
    apisix = QuantumApisixIntegration()

    # Primero, verificar la conexión con el MCP Gateway
    print("Verificando conexion con el Quantum MCP Gateway...")
    is_connected = await apisix.connect_to_mcp()
    
    if not is_connected:
        print("CRITICAL ERROR: No se pudo conectar al Quantum MCP Gateway de APISIX.")
        print("Asegurese de que el ecosistema VIGOLEONROCKS este activo en http://localhost:3000.")
        return

    print("Conexion con Quantum MCP Gateway establecida.")
    print("\nSolicitando al ecosistema que inicie su proceso de autoevaluacion...")

    # Iniciar la autoevaluación y esperar el reporte
    evaluation_report = await apisix.run_self_evaluation()

    if evaluation_report.get("evaluation_error"):
        print("\n--- INFORME DE ERROR DE AUTOEVALUACION ---")
        print(f"Error: {evaluation_report.get('reason', 'Desconocido')}")
        print("---------------------------------------------")
        return

    print("\n--- INFORME DE AUTOEVALUACION CUANTICA RECIBIDO ---")
    
    # Imprimir el reporte de forma estructurada
    print(json.dumps(evaluation_report, indent=2, ensure_ascii=True))

    print("\n----------------------------------------------------")

    # Extraer y mostrar la conclusión final del sistema
    final_conclusion = evaluation_report.get('holistic_conclusion', 'El sistema no proporciono una conclusion final.')
    final_score = evaluation_report.get('final_quantum_coherence_score', 0.0)

    print("\nCONCLUSION DEL PROPIO SISTEMA:")
    print(f"   - Score de Coherencia Cuantica: {final_score:.4f}")
    print(f"   - Veredicto: {final_conclusion}")
    print("==========================================")
    print("\nProceso de autoevaluacion completado.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProceso de autoevaluacion interrumpido por el usuario.")