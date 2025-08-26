# ==============================================================================
# || QBTC UNIFIED SYSTEM - MAIN: Trading HFT Service                          ||
# ==============================================================================
#
# Este servicio simula un bot de High-Frequency Trading.
#   - Productor: Periódicamente, envía solicitudes de análisis de mercado
#     al servicio del núcleo cuántico.
#   - Consumidor: Escucha las señales de trading generadas por el núcleo y
#     actúa sobre ellas (actualmente, solo las registra en el log).
#

import os
import pika
import uuid
import json
import logging
import time
import threading

# --- Configuración de Logging -----------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [TradingHFT] - %(levelname)s - %(message)s')

# --- Constantes de RabbitMQ -------------------------------------------------
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', 'quantum_vhost')

REQUESTS_EXCHANGE = 'requests_exchange'
RESPONSES_EXCHANGE = 'responses_exchange'

TRADING_REQUEST_ROUTING_KEY = 'trading.request'

# --- Lógica del Consumidor de Señales ------------------------------------------

def on_signal_message_callback(ch, method, properties, body):
    """Callback que se ejecuta al recibir una señal de trading."""
    correlation_id = properties.correlation_id
    logging.info(f"Señal de trading recibida (Corr ID: {correlation_id}): {body.decode()}")
    
    # Aquí iría la lógica para ejecutar la orden (ej. comprar/vender)
    # Ejemplo: trade_executor.execute(json.loads(body))
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_signal_consumer():
    """Inicia un consumidor para las señales de trading del núcleo."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, virtual_host=RABBITMQ_VHOST, credentials=credentials)
    )
    channel = connection.channel()

    # Cola para recibir las señales de trading.
    # El nombre de la cola puede ser específico para esta instancia del servicio.
    result = channel.queue_declare(queue='q_trading_signals', exclusive=False, durable=True, arguments={'x-queue-type': 'quorum'})
    queue_name = result.method.queue

    # Nos enlazamos al exchange de respuestas con una routing key genérica para todas las señales
    # Asumimos que el core publica con una routing key del tipo 'trading.signal.<correlation_id>'
    channel.queue_bind(exchange=RESPONSES_EXCHANGE, queue=queue_name, routing_key='trading.signal.*')

    logging.info("Consumidor de señales de trading esperando mensajes.")
    channel.basic_consume(queue=queue_name, on_message_callback=on_signal_message_callback)
    channel.start_consuming()

# --- Lógica del Productor de Solicitudes ---------------------------------------

def start_request_producer():
    """Inicia un productor que envía solicitudes de análisis periódicamente."""
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, virtual_host=RABBITMQ_VHOST, credentials=credentials)
    )
    channel = connection.channel()

    while True:
        try:
            # Simular una solicitud de análisis de mercado
            request_id = str(uuid.uuid4())
            market_data = {
                "request_id": request_id,
                "market": "BTC/USD",
                "indicators": ["RSI", "MACD", "BollingerBands"],
                "timestamp": time.time()
            }
            
            # El core sabrá a qué routing key responder basado en el correlation_id
            channel.basic_publish(
                exchange=REQUESTS_EXCHANGE,
                routing_key=TRADING_REQUEST_ROUTING_KEY,
                properties=pika.BasicProperties(correlation_id=request_id),
                body=json.dumps(market_data)
            )
            logging.info(f"Solicitud de análisis de mercado enviada (ID: {request_id})")
            
            # Esperar antes de enviar la siguiente solicitud
            time.sleep(15) 
        except pika.exceptions.AMQPConnectionError:
            logging.error("Se perdió la conexión con RabbitMQ. Reconectando...")
            time.sleep(5)
            # El bucle intentará reconectar en la siguiente iteración.
            # Se necesita un manejo más robusto en producción.
            start_request_producer() # Simplificación para reconectar
        except KeyboardInterrupt:
            break

    connection.close()

# --- Punto de Entrada ----------------------------------------------------------

if __name__ == "__main__":
    # Iniciar el consumidor en un hilo separado para que no bloquee al productor
    consumer_thread = threading.Thread(target=start_signal_consumer, daemon=True)
    consumer_thread.start()
    
    # Iniciar el productor en el hilo principal
    start_request_producer()

    logging.info("Servicio de Trading HFT detenido.")
