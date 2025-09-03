#!/usr/bin/env python3
"""
LLM API Service - RabbitMQ Connector
"""
import pika
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

class LLMServiceConnector:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:5672/"))
        self.channel = self.connection.channel()
    
    def publish_llm_request(self, request_data):
        message = {
            "message_id": f"llm_{int(time.time())}",
            "request": request_data.get("prompt", ""),
            "model": request_data.get("model", "vigoleonrocks:latest"),
            "parameters": request_data.get("parameters", {})
        }
        
        self.channel.basic_publish(
            exchange='llm_requests',
            routing_key='llm.request',
            body=json.dumps(message)
        )
        
        return message["message_id"]

@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    connector = LLMServiceConnector()
    message_id = connector.publish_llm_request(request.json)
    
    return jsonify({
        "message_id": message_id,
        "status": "processing"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
