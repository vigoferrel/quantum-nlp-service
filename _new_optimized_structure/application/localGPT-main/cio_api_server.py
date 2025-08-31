# cio_api_server.py
# Servidor API para exponer el Cerebro CIO Unificado

import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Importamos nuestro cerebro unificado
from cio_unified_brain import QBTCQuantumBrainLeonardo

# Creamos la aplicación FastAPI
app = FastAPI(
    title="Servidor de API del Cerebro Cuántico CIO",
    description="Expone la inteligencia del QBTCQuantumBrainLeonardo, potenciado por AICS.",
    version="1.0.0"
)

# Inicializamos una única instancia de nuestro cerebro para toda la aplicación
# Esto asegura que el estado y el aprendizaje se mantengan entre llamadas.
try:
    cio_brain = QBTCQuantumBrainLeonardo(brain_id="api_server_brain")
except Exception as e:
    print(f"Error fatal al inicializar el cerebro CIO: {e}")
    cio_brain = None

# Modelo Pydantic para la entrada de la consulta
class QuantumQueryRequest(BaseModel):
    query: str
    context: str = "" # Contexto adicional, opcional
    mission_type: str = "general_query"

@app.on_event("startup")
async def startup_event():
    if cio_brain is None:
        # Esto previene que el servidor se inicie si el cerebro no pudo ser creado
        raise RuntimeError("No se pudo inicializar el QBTCQuantumBrainLeonardo. El servidor no puede iniciar.")
    print("Servidor API del Cerebro CIO iniciado y listo para recibir misiones.")

@app.on_event("shutdown")
def shutdown_event():
    if cio_brain:
        cio_brain.shutdown_gracefully()
    print("Servidor API del Cerebro CIO apagado correctamente.")


@app.get("/", tags=["Estado"])
async def root():
    """
    Endpoint raíz para una verificación rápida del estado del servidor.
    """
    return {"status": "online", "brain_id": cio_brain.brain_id if cio_brain else "offline"}

@app.post("/api/quantum_query", tags=["Inteligencia Cuántica"])
async def process_quantum_query(request: QuantumQueryRequest) -> Dict[str, Any]:
    """
    Procesa una consulta a través del cerebro cuántico unificado.

    Este es el endpoint principal que será consumido por herramientas de benchmark
    y otras aplicaciones cliente.
    """
    if cio_brain is None:
        raise HTTPException(status_code=503, detail="El cerebro CIO no está disponible.")

    try:
        # El cerebro maneja todo el flujo internamente
        result = await cio_brain.manifest_leonardo_intelligence(request.query)

        # Devolvemos una respuesta compatible con lo que espera el benchmark_arena
        return {
            "response": result.get("tool_output", "[SIN RESPUESTA]"),
            "full_analysis": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Se recomienda ejecutar con un servidor ASGI como uvicorn o hypercorn
    # Ejemplo: uvicorn cio_api_server:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8003)
