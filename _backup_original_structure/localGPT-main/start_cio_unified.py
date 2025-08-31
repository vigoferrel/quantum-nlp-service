# start_cio_unified.py
# Punto de Entrada y Demostración del Sistema CIO Verdaderamente Unificado

import asyncio
from orquestador_ionico import OrquestadorIonico

async def demonstrate_fully_unified_cio():
    """
    Inicializa y demuestra el funcionamiento del sistema CIO final,
    ahora con el Orquestador actuando como el cuerpo y el Cerebro Unificado
    manejando toda la lógica interna.
    """
    print("=" * 60)
    print("INICIALIZANDO ARQUITECTURA CIO FINALMENTE UNIFICADA")
    print("=" * 60)

    # 1. La inicialización ahora es mucho más simple.
    #    Solo creamos el Orquestador; él se encarga de despertar al cerebro.
    print("\n--- Paso 1: Creando el Orquestador (Cuerpo) ---")
    cuerpo = OrquestadorIonico()
    print("[OK] Orquestador y Cerebro Unificado inicializados.")

    print("\n--- Paso 2: Simulación de Misiones Estratégicas ---")

    # 2. Definición de misiones de ejemplo para probar la inteligencia del cerebro.
    misiones = [
        {"query": "Analizar y optimizar el sistema de caché cuántico."},
        {"query": "Crear una nueva herramienta para calcular la resonancia iónica."},
        {"query": "Buscar en la web los últimos avances en computación neuromórfica."}
    ]

    # 3. El Orquestador maneja las misiones de forma asíncrona
    for i, mision in enumerate(misiones):
        print(f"\n--- Procesando Misión {i+1}/{len(misiones)} ---")
        resultado = await cuerpo.handle_mission_async(mision)

        print("\n--- Resultado de la Misión ---")
        if "error" in resultado:
            print(f"[ERROR] La misión ha fallado: {resultado['error']}")
        else:
            print(f"Mundo Arquetípico        : {resultado.get('archetypal_world', 'N/A')}")
            print(f"Herramienta Elegida (AICS) : {resultado.get('chosen_tool', 'N/A')}")
            print(f"Output Simulado            : {resultado.get('tool_output', '')[:100]}...")
            print(f"Calidad del Resultado      : {resultado.get('outcome_quality', 0):.2f}")
            print(f"Coherencia del Cerebro     : {resultado.get('coherence', 0):.3f}")

    print("\n=" * 60)
    print("DEMOSTRACIÓN DE LA ARQUITECTURA CIO UNIFICADA COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demonstrate_fully_unified_cio())
