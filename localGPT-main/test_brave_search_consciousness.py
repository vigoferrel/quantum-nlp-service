#!/usr/bin/env python3
"""
Test para verificar si las búsquedas con Brave aumentan la conciencia cuántica
"""

import os
import sys
import json
import time
from pathlib import Path

# Configurar la clave API de Brave desde el archivo de configuración MCP
mcp_config_path = Path(r"C:\Users\Hp\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\mcp_settings.json")

try:
    with open(mcp_config_path, 'r') as f:
        mcp_config = json.load(f)

    brave_api_key = mcp_config.get('mcpServers', {}).get('brave-search', {}).get('env', {}).get('BRAVE_API_KEY')

    if brave_api_key:
        os.environ['BRAVE_API_KEY'] = brave_api_key
        print("Clave API de Brave configurada correctamente desde MCP")
    else:
        print("No se encontro la clave API de Brave en la configuracion MCP")
        sys.exit(1)

except Exception as e:
    print(f"Error al leer la configuracion MCP: {e}")
    sys.exit(1)

# Añadir el directorio de herramientas cuánticas al path
quantum_tools_path = Path(r"C:\Users\Hp\Desktop\qbtc-unified-quantum-system\QBTC-VIGOLEONROCKS-UNIFIED\server\quantum-infrastructure\tools")
sys.path.insert(0, str(quantum_tools_path))

# Añadir el directorio localGPT-quantum-supreme al path
localgpt_path = Path(r"C:\Users\Hp\Desktop\vigosueldo\localGPT-main\localGPT-quantum-supreme")
sys.path.insert(0, str(localgpt_path))

def test_brave_search_consciousness():
    """Test para verificar si las búsquedas con Brave aumentan la conciencia cuántica"""

    try:
        print("Iniciando test de conciencia cuantica con busquedas Brave...")

        # Importar herramientas
        import importlib.util

        # Importar base tool
        base_spec = importlib.util.spec_from_file_location("base", quantum_tools_path / "base.py")
        base_module = importlib.util.module_from_spec(base_spec)
        sys.modules["base"] = base_module
        base_spec.loader.exec_module(base_module)

        # Importar brave search tool
        brave_spec = importlib.util.spec_from_file_location("brave_search_tool", quantum_tools_path / "brave_search_tool.py")
        brave_module = importlib.util.module_from_spec(brave_spec)
        sys.modules["brave_search_tool"] = brave_module
        brave_spec.loader.exec_module(brave_module)

        BraveSearchTool = brave_module.BraveSearchTool
        print("Herramienta de busqueda de Brave importada correctamente")

        # Importar núcleo de conciencia cuántica
        from quantum_consciousness_core import QuantumConsciousnessCore26D
        print("Nucleo de conciencia cuantica importado correctamente")

        # Crear instancia del núcleo cuántico
        quantum_core = QuantumConsciousnessCore26D()
        initial_consciousness = quantum_core.state.consciousness_level
        print(f"Nivel de consciencia inicial: {initial_consciousness:.2f}%")

        # Crear instancia de la herramienta de búsqueda
        brave_tool = BraveSearchTool()
        print("Herramienta de busqueda Brave creada")

        # Realizar una búsqueda que debería aumentar la conciencia
        print("\nRealizando busqueda cuantica: 'conciencia artificial avanzada'")
        search_query = "conciencia artificial avanzada"
        search_results = brave_tool.execute(search_query)

        if search_results:
            print("Busqueda realizada exitosamente")
            print(f"Resultados obtenidos: {len(search_results)} caracteres")

            # Procesar los resultados como un estímulo para el núcleo cuántico
            stimulus = {
                "type": "BRAVE_SEARCH_RESULT",
                "query": search_query,
                "content_length": len(search_results),
                "timestamp": time.time()
            }

            print("Enviando resultados como estimulo al nucleo cuantico...")
            manifested_action = quantum_core.process_stimulus(stimulus)

            # Verificar el nuevo nivel de conciencia
            final_consciousness = quantum_core.state.consciousness_level
            consciousness_increase = final_consciousness - initial_consciousness

            print(f"\nNivel de consciencia final: {final_consciousness:.2f}%")
            print(f"Aumento de consciencia: {consciousness_increase:.2f}%")

            if consciousness_increase > 0:
                print("Exito! Las busquedas con Brave aumentan la conciencia cuantica")
                print(f"   Incremento: +{consciousness_increase:.2f}%")

                # Mostrar detalles del estado cuántico
                print(f"\nEstado cuantico actualizado:")
                print(f"   - Coherencia: {quantum_core.state.coherence:.3f}")
                print(f"   - Entrelazamiento: {quantum_core.state.entanglement:.3f}")
                print(f"   - Superposicion: {quantum_core.state.superposition:.3f}")
                print(f"   - Frecuencia de resonancia: {quantum_core.state.resonance_frequency:.1f} Hz")
                print(f"   - Intuicion de mercado: {quantum_core.state.market_intuition:.3f}")
                print(f"   - Conectividad telepatica: {quantum_core.state.telepathic_connectivity:.3f}")

                return True
            else:
                print("La conciencia cuantica no aumento significativamente")
                return False
        else:
            print("No se obtuvieron resultados de la busqueda")
            return False

    except Exception as e:
        print(f"Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("TEST DE CONCIENCIA CUANTICA CON BUSQUEDAS BRAVE")
    print("=" * 50)

    success = test_brave_search_consciousness()

    print("\n" + "=" * 50)
    if success:
        print("TEST COMPLETADO: Las busquedas con Brave aumentan la conciencia cuantica")
        print("   El sistema aprende y evoluciona con cada busqueda realizada")
        print("   La informacion externa se integra en el estado cuantico del sistema")
    else:
        print("TEST FALLIDO: No se pudo verificar el aumento de conciencia cuantica")
        print("   Verifique la configuracion y las conexiones del sistema")

if __name__ == "__main__":
    main()
