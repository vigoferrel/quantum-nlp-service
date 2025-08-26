# updater.py - Servicio para procesar resultados y actualizar la memoria del cerebro.

import pika
import json
import time
import requests
import logging
import os

# --- Configuración ---
RABBITMQ_URL = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@localhost')
QUANTUM_CORE_URL = os.getenv('QUANTUM_CORE_SERVICE_URL', 'http://localhost:8002')
RESULTS_QUEUE = 'ollama_results_queue'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Lógica del Updater ---

def _calculate_outcome_quality(outcome: str, query: str, success: bool) -> float:
    """
    Calcula una métrica de calidad simple para el resultado de la inferencia.
    """
    if not success:
        return 0.0

    quality = 0.5
    if len(outcome) > 50: quality += 0.1
    if "error" not in outcome.lower(): quality += 0.1

    query_words = set(query.lower().split())
    outcome_words = set(outcome.lower().split())
    relevance = len(query_words.intersection(outcome_words)) / len(query_words) if query_words else 0
    quality += relevance * 0.3

    return min(1.0, quality)

def process_result(channel, method, properties, body):
    """
    Callback que se ejecuta con cada mensaje de la cola de resultados.
    """
    try:
        data = json.loads(body)
        task_id = data.get('task_id', 'unknown_task')
        logging.info(f"[{task_id}] Resultado de inferencia recibido.")

        # 1. Calcular la calidad del resultado
        quality = _calculate_outcome_quality(data['outcome'], data['prompt'], data['success'])
        logging.info(f"[{task_id}] Calidad del resultado calculada: {quality:.2f}")

        # 2. Preparar el payload para el Quantum Core Service
        memory_payload = {
            "query": data['prompt'],
            "archetypal_world": data.get('query_type', 'general'), # Usamos query_type como archetypal_world
            "ollama_profile": data['profile'],
            "outcome": data['outcome'],
            "outcome_quality": quality
        }

        # 3. Enviar la memoria para ser almacenada
        logging.info(f"[{task_id}] Enviando memoria al Quantum Core Service...")
        response = requests.post(
            f"{QUANTUM_CORE_URL}/api/store_memory",
            json=memory_payload,
            timeout=10 # 10 segundos de timeout
        )
        response.raise_for_status()

        logging.info(f"[{task_id}] Memoria almacenada exitosamente en el Quantum Core. Respuesta: {response.json()}")

        # 4. Confirmar que el mensaje fue procesado
        channel.basic_ack(delivery_tag=method.delivery_tag)

    except requests.RequestException as e:
        logging.error(f"[RequestException] Error comunicándose con el Quantum Core Service: {e}. El mensaje será re-encolado.")
        # No hacemos ack para que RabbitMQ reintente el mensaje más tarde
        channel.basic_nack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logging.error(f"[Exception] Error procesando el resultado: {e}")
        # Rechazar el mensaje sin re-encolar para evitar bucles de errores
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_updater():
    """
    Inicia el consumidor de RabbitMQ.
    """
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            channel = connection.channel()

            channel.queue_declare(queue=RESULTS_QUEUE, durable=True)
            logging.info(f"[*] Esperando resultados en la cola '{RESULTS_QUEUE}'.")

            channel.basic_consume(queue=RESULTS_QUEUE, on_message_callback=process_result)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Error de conexión con RabbitMQ: {e}. Reintentando en 10 segundos...")
            time.sleep(10)
        except Exception as e:
            logging.critical(f"Error fatal en el updater: {e}. Reiniciando en 15 segundos...")
            time.sleep(15)

if __name__ == '__main__':
    start_updater()
