# cio_api_server.py
# Servidor API para exponer el Cerebro CIO Unificado

import asyncio
import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import httpx
import aio_pika
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de servicios
import os
AICS_SERVICE_URL = os.getenv("AICS_SERVICE_URL", "http://aics_service:8001")
QUANTUM_CORE_SERVICE_URL = os.getenv("QUANTUM_CORE_SERVICE_URL", "http://quantum_core_service:8002")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

# Creamos la aplicación FastAPI
app = FastAPI(
    title="API Gateway del Sistema Unificado QBTC",
    description="Orquesta las llamadas entre los microservicios del sistema.",
    version="2.0.0"
)

# Cliente HTTP asíncrono
http_client = httpx.AsyncClient()

# Modelo Pydantic para la entrada de la consulta
class QuantumQueryRequest(BaseModel):
    query: str
    context: int = 100
    urgency: float = 0.5
    query_type: str = "general"

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()
    logger.info("Cliente HTTP cerrado.")

@app.get("/", tags=["Estado"])
async def root():
    return {"status": "online", "service": "API Gateway"}

@app.post("/api/v2/process_query", tags=["Orquestación Cuántica"])
async def process_quantum_query(request: QuantumQueryRequest) -> Dict[str, Any]:
    """
    Orquesta el procesamiento de una consulta a través de los microservicios.
    """
    task_id = str(uuid.uuid4())
    logger.info(f"Iniciando procesamiento para la tarea {task_id} con la consulta: {request.query}")

    try:
        # 1. Transformar consulta en AICS
        logger.info(f"[{task_id}] Llama a AICS para transformar la consulta.")
        transform_payload = {
            "query": request.query,
            "context": request.context,
            "urgency": request.urgency
        }
        response = await http_client.post(f"{AICS_SERVICE_URL}/transform", json=transform_payload)
        response.raise_for_status()
        exp_state = response.json()
        logger.info(f"[{task_id}] Estado exponencial recibido de AICS: {exp_state}")

        # 2. Seleccionar perfil de Ollama en AICS
        logger.info(f"[{task_id}] Llama a AICS para seleccionar el perfil de Ollama.")
        profile_payload = {
            "exp_state": exp_state,
            "query_type": request.query_type
        }
        response = await http_client.post(f"{AICS_SERVICE_URL}/select_profile", json=profile_payload)
        response.raise_for_status()
        ollama_profile = response.json()
        logger.info(f"[{task_id}] Perfil de Ollama seleccionado: {ollama_profile}")

        # 3. Construir y enviar la tarea a RabbitMQ
        logger.info(f"[{task_id}] Enviando tarea de inferencia a RabbitMQ.")
        inference_task = {
            "task_id": task_id,
            "prompt": request.query,
            "profile": ollama_profile
        }

        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(inference_task).encode()),
                routing_key='ollama_inference_queue'
            )
        logger.info(f"[{task_id}] Tarea enviada a la cola 'ollama_inference_queue'.")

        return {
            "message": "Tarea de inferencia enviada.",
            "task_id": task_id,
            "selected_profile": ollama_profile
        }

    except httpx.RequestError as e:
        logger.error(f"[{task_id}] Error de comunicación con un servicio: {e}")
        raise HTTPException(status_code=503, detail=f"Error de comunicación con el servicio: {e.request.url}")
    except Exception as e:
        logger.error(f"[{task_id}] Error inesperado durante la orquestación: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

if __name__ == "__main__":
    import uvicorn
    # Se recomienda ejecutar con un servidor ASGI como uvicorn o hypercorn
    # Ejemplo: uvicorn qbtc-unified-system.services.api_server.main:app --reload --port 5001
    uvicorn.run(app, host="0.0.0.0", port=5001)
