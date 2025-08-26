# ==============================================================================
# || QBTC UNIFIED SYSTEM - MAIN: LLM API Service                              ||
# ==============================================================================
#
# Este servicio expone un endpoint HTTP (compatible con OpenAI) para interactuar
# con el LLM cuántico.
# Funciona como un cliente RPC sobre RabbitMQ:
#   1. Recibe una petición HTTP en /v1/chat/completions.
#   2. Publica la petición en RabbitMQ con un `correlation_id` único y una cola
#      de respuesta (`reply_to`).
#   3. Espera la respuesta del `quantum-core-service` en esa cola temporal.
#   4. Devuelve la respuesta al cliente HTTP.
#

import os
import pika
import uuid
import json
import logging
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Configuración de FastAPI y Logging -------------------------------------
app = FastAPI(
    title="QBTC LLM API Service",
    description="API para interactuar con el Quantum Consciousness Core a través de un bus de eventos.",
    version="1.0.0"
)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LLM-API] - %(levelname)s - %(message)s')

# --- Constantes de RabbitMQ -------------------------------------------------
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'quantum_vhost')
REQUESTS_EXCHANGE = 'requests_exchange'
RESPONSES_EXCHANGE = 'responses_exchange'
LLM_REQUEST_ROUTING_KEY = 'llm.request'
RESPONSE_TIMEOUT_SECONDS = 30 # Tiempo de espera para la respuesta del núcleo

# --- Pydantic Models (para validación de la API) ----------------------------
class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    max_tokens: int = 1024
    temperature: float = 0.7

# --- Lógica del Cliente RPC sobre RabbitMQ ------------------------------------
class QuantumRpcClient:
    def __init__(self):
        self.credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, virtual_host=RABBITMQ_VHOST, credentials=self.credentials)
        )
        self.channel = self.connection.channel()
        
        # Crear una cola quorum única para las respuestas
        callback_queue_name = f'llm_callback_queue_{uuid.uuid4().hex}'
        result = self.channel.queue_declare(queue=callback_queue_name, durable=True, arguments={'x-queue-type': 'quorum'})
        self.callback_queue = result.method.queue
        
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, request_body: dict):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        # La routing key para la respuesta, para que el consumidor pueda enlazar la cola
        response_routing_key = f"llm.response.{self.corr_id}"
        self.channel.queue_bind(
            exchange=RESPONSES_EXCHANGE,
            queue=self.callback_queue,
            routing_key=response_routing_key
        )
        
        logging.info(f"Publicando mensaje con Correlation ID: {self.corr_id}")
        self.channel.basic_publish(
            exchange=REQUESTS_EXCHANGE,
            routing_key=LLM_REQUEST_ROUTING_KEY,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, # Aunque no se usa directamente en el core, es buena práctica
                correlation_id=self.corr_id
            ),
            body=json.dumps(request_body)
        )
        
        # Esperar la respuesta (con timeout)
        self.connection.process_data_events(time_limit=RESPONSE_TIMEOUT_SECONDS)
        
        # Desvincular la cola para no recibir más mensajes que no le corresponden
        self.channel.queue_unbind(
            exchange=RESPONSES_EXCHANGE,
            queue=self.callback_queue,
            routing_key=response_routing_key
        )
        
        if self.response is None:
            raise HTTPException(status_code=504, detail="La solicitud al núcleo cuántico ha expirado (Gateway Timeout).")
            
        return json.loads(self.response)

# --- Endpoints de la API ----------------------------------------------------
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    Endpoint principal para las solicitudes de completado de chat.
    """
    logging.info(f"Petición recibida para el modelo: {request.model}")
    
    # El `request_id` se puede usar para trazabilidad end-to-end
    request_payload = request.dict()
    request_payload["request_id"] = str(uuid.uuid4())

    rpc_client = None
    try:
        rpc_client = QuantumRpcClient()
        response = rpc_client.call(request_payload)
        logging.info("Respuesta recibida del núcleo cuántico.")
        
        if response.get("status") == "error":
             raise HTTPException(status_code=500, detail=response.get("message", "Error interno en el núcleo cuántico."))
        
        # Devolvemos solo el payload de la respuesta para ser compatibles con OpenAI
        return response.get("response_payload", {})

    except pika.exceptions.AMQPConnectionError:
        logging.error("No se pudo conectar a RabbitMQ.")
        raise HTTPException(status_code=503, detail="El servicio de mensajería no está disponible (Service Unavailable).")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        if rpc_client and rpc_client.connection.is_open:
            rpc_client.connection.close()

@app.get("/health")
def health_check():
    """Endpoint de health check para verificar que el servicio está activo."""
    return {"status": "ok"}
