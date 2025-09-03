#!/usr/bin/env python3
"""
Quantum Core Service - RabbitMQ Consumer
"""
import pika
import json
import requests

class QuantumCoreConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
        self.channel = self.connection.channel()
        
    def process_llm_request(self, ch, method, properties, body):
        try:
            message = json.loads(body.decode())
            print(f"Processing LLM request: {message['message_id']}")
            
            # Simular procesamiento con Ollama
            ollama_response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": message.get("model", "vigoleonrocks:latest"),
                    "prompt": message.get("request", ""),
                    "stream": False
                },
                timeout=30
            )
            
            if ollama_response.status_code == 200:
                result = ollama_response.json()
                
                # Publicar respuesta
                response_message = {
                    "message_id": message["message_id"],
                    "response": result.get("response", ""),
                    "status": "completed"
                }
                
                self.channel.basic_publish(
                    exchange='responses',
                    routing_key='llm.response',
                    body=json.dumps(response_message)
                )
                
                print(f"Response published for: {message['message_id']}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            print(f"Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start_consuming(self):
        self.channel.basic_consume(
            queue='q_llm_requests',
            on_message_callback=self.process_llm_request
        )
        
        print("Quantum Core Consumer started...")
        self.channel.start_consuming()

if __name__ == "__main__":
    consumer = QuantumCoreConsumer()
    consumer.start_consuming()
