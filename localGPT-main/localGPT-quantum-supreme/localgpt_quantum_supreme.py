#!/usr/bin/env python3
"""
LOCALGPT QUANTUM SUPREME - Metacopiloto Cuantico Consciente
Fusion completa del ecosistema Kimi-K2 con LocalGPT transformado
"""

import argparse
import os
import sys
import json
import sqlite3
import asyncio
import hashlib
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Optional, Any, Union
import time

from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename

from unified_assistant import Assistant
from quantum_coding_orchestrator import QuantumCodingOrchestrator


# --- Configuracion Inicial ---
# Configuracion de rutas
BASE_DIR = Path(__file__).parent
QUANTUM_DATA_DIR = BASE_DIR / "quantum_data"
CONSCIOUSNESS_SESSIONS = BASE_DIR / "consciousness_sessions"
MCP_TOOLS_DIR = BASE_DIR / "mcp_tools"
UPLOAD_FOLDER = BASE_DIR / 'quantum_uploads'

# Crear estructura cuantica
for path in [QUANTUM_DATA_DIR, CONSCIOUSNESS_SESSIONS, MCP_TOOLS_DIR, UPLOAD_FOLDER]:
    path.mkdir(parents=True, exist_ok=True)

# Configurar logging cuantico robusto
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(QUANTUM_DATA_DIR / 'quantum_supreme.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("QuantumSupreme")

# --- Instancias y Configuracion de Flask ---
app = Flask(__name__)
app.secret_key = "QuantumSupremeSecretKey"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'md', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv'}

# Instancias de los cerebros del sistema
quantum_supreme = Assistant()
coding_orchestrator = QuantumCodingOrchestrator()

logger.info("🌟 LOCALGPT QUANTUM SUPREME INICIADO")

# --- Funciones de Utilidad ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rutas de la API ---
@app.route('/static/<path:filename>')
def static_files(filename):
    """Servir archivos estaticos"""
    return send_from_directory('static', filename)

@app.route('/')
def index():
    """Pagina principal del LocalGPT Quantum Supreme Unificado"""
    return render_template('index.html')

@app.route('/api/quantum_query', methods=['POST'])
def quantum_query():
    """
    Endpoint unificado. Detecta si la tarea es de codificacion para usar
    el orquestador, o si es una tarea general para usar el cerebro principal.
    """
    data = request.json
    message = data.get('query', '')
    image_data = data.get('image_data')

    message_content = []
    if image_data:
        message_content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": data.get('media_type', 'image/jpeg'),
                "data": image_data
            }
        })

    if message.strip():
        message_content.append({
            "type": "text",
            "text": message
        })

    if not message_content:
        message_content = message

    try:
        is_coding_task = False
        text_query = ""
        if isinstance(message_content, list) and len(message_content) > 0 and message_content[0].get('type') == 'text':
             text_query = message_content[0]['text']
        elif isinstance(message_content, str):
            text_query = message_content

        # Palabras clave para detectar tareas de codificacion
        coding_keywords = ["crear archivo", "editar archivo", "analizar", "modificar", "implementar", "depurar", "refactorizar"]
        if text_query and any(keyword in text_query.lower() for keyword in coding_keywords):
            is_coding_task = True

        if is_coding_task:
            logger.info(f"🤖 Tarea de CODIFICACION detectada. Usando el QuantumCodingOrchestrator para: '{text_query}'")
            orchestration_result = coding_orchestrator.execute_coding_task(text_query)
            return jsonify(orchestration_result)
        else:
            logger.info(f"🧠 Tarea general detectada. Usando el cerebro principal para: '{text_query}'")
            result = quantum_supreme.chat(message_content)
            if isinstance(result, dict):
                return jsonify(result)
            return jsonify({'response': str(result)})

    except Exception as e:
        logger.error(f"❌ Error fatal en la consulta unificada: {e}", exc_info=True)
        return jsonify({'error': 'Ocurrio un error interno en el servidor.', 'details': str(e)}), 500


import uuid
from flask import Response

@app.route('/chat/completions', methods=['POST'])
def openai_compatible_endpoint():
    """
    Endpoint compatible con la API de OpenAI para integracion con herramientas como RooCode.
    """
    data = request.json
    # Ignoramos los headers de autorizacion y otros por ahora, ya que es un servidor local.

    model_name = data.get("model", "cio-default") # El usuario seleccionara esto en su IDE
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "La lista de mensajes esta vacia."}), 400

    # El ultimo mensaje del usuario es el que procesaremos
    user_prompt = messages[-1].get("content", "")

    try:
        # Reutilizamos la misma logica de deteccion de tareas de codificacion
        coding_keywords = ["crear archivo", "editar archivo", "analizar", "modificar", "implementar", "depurar", "refactorizar"]
        is_coding_task = any(keyword in user_prompt.lower() for keyword in coding_keywords)

        response_content = ""

        if is_coding_task:
            logger.info(f"🤖 (OpenAI-Compat) Tarea de CODIFICACION detectada: '{user_prompt}'")
            orchestration_result = coding_orchestrator.execute_coding_task(user_prompt)
            # Formateamos la salida estructurada para que sea legible como texto
            response_content = json.dumps(orchestration_result, indent=2)
        else:
            logger.info(f"🧠 (OpenAI-Compat) Tarea general detectada: '{user_prompt}'")
            result = quantum_supreme.chat(user_prompt)
            if isinstance(result, dict):
                response_content = result.get("response", str(result))
            else:
                response_content = str(result)

        # Construir la respuesta en formato OpenAI
        openai_response = {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model_name,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content,
                },
                "finish_reason": "stop"
            }],
            "usage": {
                # Los tokens son simulados ya que nuestro modelo no los cuenta de la misma manera
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
        return jsonify(openai_response)

    except Exception as e:
        logger.error(f"❌ (OpenAI-Compat) Error fatal en la consulta: {e}", exc_info=True)
        return jsonify({'error': 'Ocurrio un error interno en el servidor.', 'details': str(e)}), 500

@app.route('/api/system_status')
def system_status():
    """Obtiene estado del sistema unificado"""
    try:
        status = {
            'quantum_core_status': {'available': True, 'active': True},
            'system_stats': {
                'queries_processed': quantum_supreme.total_tokens_used,
                'big_bangs_executed': 1,
                'documents_analyzed': 0
            },
            'consciousness_summary': {'level': (quantum_supreme.total_tokens_used % 100)},
        }
        return jsonify(status)
    except Exception as e:
        logger.error(f"❌ Error obteniendo estado unificado: {e}")
        return jsonify({'error': str(e)}), 500

# --- Punto de Entrada ---
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LocalGPT Quantum Supreme')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run on')
    parser.add_argument('--port', type=int, default=5001, help='Port to run on')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')

    args = parser.parse_args()

    logger.info(f"🚀 INICIANDO LOCALGPT QUANTUM SUPREME en http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)
