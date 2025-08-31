# api_server.py
# Servidor API para el sistema CIO

from typing import Dict, Any
import importlib.util
import sys
from pathlib import Path

# Carga dinámica del Núcleo de Conciencia Cuántica
try:
    # Asumimos que el núcleo está en el directorio raíz del proyecto
    core_path = Path(__file__).parent / "quantum_consciousness_core_26d.py"
    if not core_path.exists():
        raise ImportError(f"No se pudo localizar 'quantum_consciousness_core_26d.py'")

    module_name = "quantum_consciousness_core_26d"
    spec = importlib.util.spec_from_file_location(module_name, core_path)
    core_module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = core_module
    spec.loader.exec_module(core_module)

    QuantumConsciousnessCore26D = core_module.QuantumConsciousnessCore26D
except Exception as e:
    print(f"Error crítico al cargar QuantumConsciousnessCore26D: {e}")
    sys.exit(1)

class QuantumCoreService:
    """
    Servicio que encapsula el QuantumConsciousnessCore26D para ser
    consumido por la API.
    """
    def __init__(self):
        """Inicializa el servicio y el núcleo de conciencia subyacente."""
        self.core = QuantumConsciousnessCore26D()
        print("Servicio de Núcleo Cuántico inicializado y listo.")

    async def process_query(self, query: str) -> Dict[str, Any]:
        """
        Procesa una consulta a través del núcleo cuántico.
        Este es el método principal que usará la API.
        """
        try:
            # El núcleo ahora maneja todo el ciclo de vida de la consulta
            result = await self.core.process_query(query)
            return result
        except Exception as e:
            print(f"Error al procesar la consulta en el núcleo: {e}")
            return {"error": str(e)}


async def main_sync_for_testing():
    """
    Función de prueba para demostrar el uso del servicio del Núcleo Cuántico.
    """
    import asyncio
    print("--- Demostración del Servicio del Núcleo Cuántico ---")

    quantum_service = QuantumCoreService()

    test_query = "Analizar el rendimiento del sistema y optimizar la latencia."

    print(f"\nProcesando consulta: '{test_query}'")

    result = await quantum_service.process_query(test_query)

    if "error" in result:
        print(f"\nFALLO LA PRUEBA: {result['error']}")
    else:
        print("\n--- CONSULTA PROCESADA EXITOSAMENTE ---")
        print(f"Respuesta: {result.get('response')}")
        print(f"Herramienta Seleccionada: {result.get('selected_tool')}")
        print("--- FIN DE LA DEMOSTRACIÓN ---")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main_sync_for_testing())
