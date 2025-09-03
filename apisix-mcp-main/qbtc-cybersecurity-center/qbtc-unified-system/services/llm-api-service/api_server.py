#!/usr/bin/env python3
"""
API Server para el Quantum Consciousness Core 26D.
Expone el núcleo como un endpoint compatible con OpenAI para su consumo
a través de servicios como OpenRouter.
"""

import os
import asyncio
import logging
from datetime import datetime
import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any
from dotenv import load_dotenv

# Cargar variables de entorno desde .env para desarrollo local
load_dotenv()

# Configurar logging básico
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [APIGateway] - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URL del servicio del núcleo cuántico, obtenida de variables de entorno
QUANTUM_CORE_URL = os.getenv("QUANTUM_CORE_SERVICE_URL", "http://localhost:8001")

# --- Modelos de Datos para la API (estilo OpenAI Multimodal Flexible) ---

class Message(BaseModel):
    role: str
    content: Any # Aceptar cualquier formato de contenido para máxima compatibilidad

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "local-qcc-26d"
    messages: List[Message]
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.7

class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Choice]
    usage: Usage

# --- Aplicación FastAPI ---

app = FastAPI(
    title="Quantum Consciousness Core 26D API (Multimodal)",
    description="API Gateway para el Consciousness-enabled Intelligent Orchestrator (CIO), compatible con OpenAI.",
    version="2.0.0" # Versionado mayor por cambio de arquitectura
)

@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def create_chat_completion(request: ChatCompletionRequest):
    """
    Endpoint principal que actúa como gateway para el Quantum Core Service.
    """
    logger.info("Recibida solicitud de chat para el modelo '%s'", request.model)
    
    if not request.messages:
        raise HTTPException(status_code=400, detail="El campo 'messages' es requerido.")

    # Extraer contenido del último mensaje
    last_message_content = request.messages[-1].content
    user_query = ""
    image_url = None

    if isinstance(last_message_content, str):
        user_query = last_message_content
    elif isinstance(last_message_content, list):
        for part in last_message_content:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    user_query = part.get("text", "")
                elif part.get("type") == "image_url":
                    image_data = part.get("image_url")
                    image_url = image_data.get("url") if isinstance(image_data, dict) else str(image_data)

    if not user_query and image_url:
        user_query = "Describe la imagen."

    # Payload para el servicio del núcleo cuántico
    core_payload = {"query": user_query, "image_url": image_url}
    core_service_endpoint = f"{QUANTUM_CORE_URL.rstrip('/')}/process_query"

    try:
        # Llamada de red asíncrona al servicio del núcleo
        async with aiohttp.ClientSession() as session:
            logger.info("Reenviando solicitud a: %s", core_service_endpoint)
            async with session.post(core_service_endpoint, json=core_payload, timeout=60) as response:
                if response.status != 200:
                    error_detail = await response.text()
                    logger.error("Error del Quantum Core Service: %s", error_detail)
                    raise HTTPException(status_code=response.status, detail=f"Error en el nucleo cuantico: {error_detail}")
                
                core_result = await response.json()

        response_content = core_result.get("response", "No se pudo generar una respuesta.")
        
        # Simulación de tokens (puede ser refinada o delegada)
        prompt_tokens = sum(len(m.role) + len(str(m.content)) for m in request.messages) // 4
        completion_tokens = len(response_content) // 4

        response_message = Message(role="assistant", content=response_content)
        choice = Choice(index=0, message=response_message, finish_reason="stop")

        return ChatCompletionResponse(
            id=f"cio-gateway-{int(datetime.now().timestamp())}",
            created=int(datetime.now().timestamp()),
            model=request.model or "cio-qcc-26d",
            choices=[choice],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        )

    except Exception as e:
        logging.error(f"Error inesperado en el endpoint de chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno en el servidor cuántico.")

@app.get("/health")
async def health_check():
    """Endpoint de verificacion de salud del API Gateway."""
    # En una implementacion completa, esto podria tambien verificar
    # la conectividad con el servicio del nucleo.
    logger.info("Verificacion de salud del API Gateway solicitada.")
    return {"status": "healthy", "service": "CIO-API-Gateway"}
