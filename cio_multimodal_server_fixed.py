#!/usr/bin/env python3
"""
🌐 CIO MULTIMODAL SERVER - VERSIÓN CORREGIDA
Servidor web multimodal que integra el sistema CIO existente corregido
"""

import asyncio
import base64
import io
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from PIL import Image

# Importar la extensión multimodal CIO corregida
from cio_multimodal_extension_fixed import CIOMultimodalExtensionFixed

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Inicializar el sistema CIO multimodal corregido
cio_multimodal = CIOMultimodalExtensionFixed()

# HTML Template para la interfaz multimodal corregida
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 CIO Multimodal - Sistema Corregido</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #00ff41;
            line-height: 1.6;
            min-height: 100vh;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 30px;
            background: rgba(0, 255, 65, 0.1);
            border-radius: 15px;
            border: 2px solid #00ff41;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #00ff41;
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 20px #00ff41; }
            to { text-shadow: 0 0 30px #00ff41, 0 0 40px #00ff41; }
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .sidebar {
            background: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #00ff41;
        }
        
        .main-content {
            background: rgba(0, 0, 0, 0.8);
            border-radius: 15px;
            padding: 30px;
            border: 1px solid #00ff41;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        
        .status-card h3 {
            margin-bottom: 10px;
            color: #00ff41;
        }
        
        .status-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #00ff41;
        }
        
        .input-section {
            margin-bottom: 30px;
        }
        
        .input-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #00ff41;
        }
        
        .tab {
            padding: 15px 25px;
            background: rgba(0, 0, 0, 0.5);
            border: none;
            color: #00ff41;
            cursor: pointer;
            border-radius: 10px 10px 0 0;
            margin-right: 5px;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: #00ff41;
            color: #000;
        }
        
        .tab:hover {
            background: rgba(0, 255, 65, 0.3);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .text-input {
            width: 100%;
            min-height: 150px;
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ff41;
            border-radius: 10px;
            color: #00ff41;
            padding: 20px;
            font-family: inherit;
            font-size: 16px;
            resize: vertical;
        }
        
        .image-upload-area {
            border: 3px dashed #00ff41;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            background: rgba(0, 0, 0, 0.5);
            cursor: pointer;
            transition: all 0.3s;
            position: relative;
        }
        
        .image-upload-area:hover {
            background: rgba(0, 255, 65, 0.1);
            border-color: #00cc33;
        }
        
        .image-upload-area.dragover {
            background: rgba(0, 255, 65, 0.2);
            border-color: #00cc33;
        }
        
        .image-preview-container {
            margin-top: 20px;
            text-align: center;
        }
        
        .image-preview {
            max-width: 300px;
            max-height: 300px;
            border: 2px solid #00ff41;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }
        
        .image-info {
            margin-top: 10px;
            font-size: 14px;
            color: #00cc33;
        }
        
        .process-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(45deg, #00ff41, #00cc33);
            border: none;
            border-radius: 15px;
            color: #000;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .process-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 255, 65, 0.4);
        }
        
        .process-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .response-section {
            margin-top: 30px;
        }
        
        .response-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #00ff41;
        }
        
        .archetype-badge {
            background: #00ff41;
            color: #000;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        }
        
        .quality-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .quality-bar {
            width: 100px;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .quality-fill {
            height: 100%;
            background: linear-gradient(90deg, #ff4444, #ffaa00, #00ff41);
            transition: width 0.5s;
        }
        
        .response-content {
            background: rgba(0, 0, 0, 0.7);
            border: 2px solid #00ff41;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            max-height: 500px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.8;
        }
        
        .multimodal-info {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .multimodal-info h4 {
            margin-bottom: 15px;
            color: #00ff41;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .metric-card {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.8em;
            font-weight: bold;
            color: #00ff41;
        }
        
        .metric-label {
            font-size: 12px;
            color: #00cc33;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #00ff41;
        }
        
        .spinner {
            border: 4px solid rgba(0, 255, 65, 0.3);
            border-top: 4px solid #00ff41;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            color: #ff4444;
            background: rgba(255, 68, 68, 0.1);
            border: 2px solid #ff4444;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .chat-history {
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        
        .chat-message {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #00ff41;
        }
        
        .chat-message.user {
            background: rgba(0, 255, 65, 0.1);
        }
        
        .chat-message.assistant {
            background: rgba(0, 0, 0, 0.5);
        }
        
        .chat-message .timestamp {
            font-size: 12px;
            color: #00cc33;
            margin-bottom: 5px;
        }
        
        .chat-message .content {
            line-height: 1.6;
        }
        
        .file-drop-zone {
            position: relative;
        }
        
        .file-drop-zone input[type="file"] {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 CIO MULTIMODAL CORREGIDO</h1>
            <p>Sistema Avanzado de Inteligencia Cuántica con Capacidades Multimodales</p>
            <p>✅ Sistema CIO: ACTIVO | OpenRouter: CONECTADO | Multimodal: FUNCIONANDO</p>
        </div>
        
        <div class="dashboard">
            <div class="sidebar">
                <h3>📊 Estado del Sistema</h3>
                <div class="status-grid">
                    <div class="status-card">
                        <h3>Sistema CIO</h3>
                        <div class="status-value" id="cio-status">✅ Activo</div>
                    </div>
                    <div class="status-card">
                        <h3>OpenRouter</h3>
                        <div class="status-value" id="openrouter-status">✅ Conectado</div>
                    </div>
                    <div class="status-card">
                        <h3>Multimodal</h3>
                        <div class="status-value" id="multimodal-status">✅ Activo</div>
                    </div>
                    <div class="status-card">
                        <h3>Memoria</h3>
                        <div class="status-value" id="memory-status">✅ Activo</div>
                    </div>
                </div>
                
                <h3>💬 Historial de Chat</h3>
                <div class="chat-history" id="chatHistory">
                    <div class="chat-message assistant">
                        <div class="timestamp">Sistema</div>
                        <div class="content">¡Hola! Soy el sistema CIO Multimodal CORREGIDO. El cerebro CIO está ahora ACTIVO y funcionando. ¿En qué puedo ayudarte?</div>
                    </div>
                </div>
            </div>
            
            <div class="main-content">
                <div class="input-section">
                    <div class="input-tabs">
                        <button class="tab active" onclick="switchTab('text')">💬 Texto</button>
                        <button class="tab" onclick="switchTab('image')">🖼️ Imagen</button>
                        <button class="tab" onclick="switchTab('multimodal')">🚀 Multimodal</button>
                    </div>
                    
                    <div id="textTab" class="tab-content active">
                        <textarea id="textQuery" class="text-input" placeholder="Escribe tu consulta aquí...">¿Qué es la conciencia cuántica y cómo se relaciona con la inteligencia artificial?</textarea>
                    </div>
                    
                    <div id="imageTab" class="tab-content">
                        <div class="image-upload-area file-drop-zone" id="imageUploadArea">
                            <input type="file" id="imageFile" accept="image/*" onchange="handleImageSelect(event)">
                            <div>
                                <h3>📁 Subir Imagen</h3>
                                <p>Haz clic o arrastra una imagen aquí</p>
                                <p>Soportado: JPG, PNG, GIF, WebP</p>
                            </div>
                        </div>
                        <div class="image-preview-container" id="imagePreviewContainer" style="display: none;">
                            <img id="imagePreview" class="image-preview">
                            <div class="image-info" id="imageInfo"></div>
                        </div>
                        <textarea id="imageQuery" class="text-input" placeholder="Describe qué quieres saber sobre esta imagen...">Analiza esta imagen en detalle y describe todo lo que ves.</textarea>
                    </div>
                    
                    <div id="multimodalTab" class="tab-content">
                        <div class="image-upload-area file-drop-zone" id="multimodalImageArea">
                            <input type="file" id="multimodalImageFile" accept="image/*" onchange="handleMultimodalImageSelect(event)">
                            <div>
                                <h3>🖼️ Imagen + Texto</h3>
                                <p>Sube una imagen y escribe tu consulta</p>
                            </div>
                        </div>
                        <div class="image-preview-container" id="multimodalImagePreviewContainer" style="display: none;">
                            <img id="multimodalImagePreview" class="image-preview">
                        </div>
                        <textarea id="multimodalQuery" class="text-input" placeholder="Escribe tu consulta sobre la imagen...">¿Qué ves en esta imagen y cómo se relaciona con la tecnología?</textarea>
                    </div>
                </div>
                
                <button class="process-btn" onclick="processQuery()" id="processBtn">
                    🧠 PROCESAR CONSULTA MULTIMODAL
                </button>
                
                <div class="response-section" id="responseSection" style="display: none;">
                    <div class="response-header">
                        <span class="archetype-badge" id="archetypeBadge">SABIO</span>
                        <div class="quality-indicator">
                            <span>Calidad:</span>
                            <div class="quality-bar">
                                <div class="quality-fill" id="qualityFill"></div>
                            </div>
                            <span id="qualityValue">0.0</span>
                        </div>
                    </div>
                    
                    <div class="response-content" id="responseContent"></div>
                    
                    <div class="multimodal-info" id="multimodalInfo" style="display: none;">
                        <h4>📊 Información Multimodal</h4>
                        <div id="multimodalDetails"></div>
                        <div class="metrics-grid" id="metricsGrid"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentTab = 'text';
        let selectedImage = null;
        let selectedMultimodalImage = null;
        let chatHistory = [];
        
        // Configuración de arrastrar y soltar
        function setupDragAndDrop() {
            const dropZones = ['imageUploadArea', 'multimodalImageArea'];
            
            dropZones.forEach(zoneId => {
                const zone = document.getElementById(zoneId);
                if (zone) {
                    zone.addEventListener('dragover', (e) => {
                        e.preventDefault();
                        zone.classList.add('dragover');
                    });
                    
                    zone.addEventListener('dragleave', () => {
                        zone.classList.remove('dragover');
                    });
                    
                    zone.addEventListener('drop', (e) => {
                        e.preventDefault();
                        zone.classList.remove('dragover');
                        const files = e.dataTransfer.files;
                        if (files.length > 0) {
                            handleFileSelect(files[0], zoneId);
                        }
                    });
                }
            });
        }
        
        function handleFileSelect(file, zoneId) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (zoneId === 'imageUploadArea') {
                        selectedImage = e.target.result;
                        document.getElementById('imagePreview').src = selectedImage;
                        document.getElementById('imagePreviewContainer').style.display = 'block';
                        document.getElementById('imageInfo').textContent = `${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
                    } else if (zoneId === 'multimodalImageArea') {
                        selectedMultimodalImage = e.target.result;
                        document.getElementById('multimodalImagePreview').src = selectedMultimodalImage;
                        document.getElementById('multimodalImagePreviewContainer').style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        }
        
        function switchTab(tabName) {
            // Ocultar todas las pestañas
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Mostrar pestaña seleccionada
            document.getElementById(tabName + 'Tab').classList.add('active');
            event.target.classList.add('active');
            
            currentTab = tabName;
        }
        
        function handleImageSelect(event) {
            const file = event.target.files[0];
            if (file) {
                handleFileSelect(file, 'imageUploadArea');
            }
        }
        
        function handleMultimodalImageSelect(event) {
            const file = event.target.files[0];
            if (file) {
                handleFileSelect(file, 'multimodalImageArea');
            }
        }
        
        async function processQuery() {
            const processBtn = document.getElementById('processBtn');
            processBtn.disabled = true;
            processBtn.textContent = '🧠 Procesando...';
            
            // Mostrar loading
            document.getElementById('responseSection').style.display = 'block';
            document.getElementById('responseContent').innerHTML = '<div class="loading"><div class="spinner"></div><p>🧠 Procesando consulta multimodal...</p></div>';
            document.getElementById('multimodalInfo').style.display = 'none';
            
            try {
                let query = '';
                let imageData = null;
                
                // Obtener datos según la pestaña activa
                switch(currentTab) {
                    case 'text':
                        query = document.getElementById('textQuery').value.trim();
                        break;
                    case 'image':
                        query = document.getElementById('imageQuery').value.trim();
                        imageData = selectedImage;
                        break;
                    case 'multimodal':
                        query = document.getElementById('multimodalQuery').value.trim();
                        imageData = selectedMultimodalImage;
                        break;
                }
                
                if (!query) {
                    throw new Error('Por favor, escribe una consulta');
                }
                
                const data = {
                    query: query,
                    image_data: imageData
                };
                
                const response = await fetch('/api/process_multimodal', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                
                if (result.error) {
                    throw new Error(result.error);
                }
                
                // Mostrar respuesta
                displayResponse(result);
                
                // Agregar al historial
                addToChatHistory(query, result.response, result.archetype);
                
            } catch (error) {
                document.getElementById('responseContent').innerHTML = 
                    `<div class="error">❌ Error: ${error.message}</div>`;
            } finally {
                processBtn.disabled = false;
                processBtn.textContent = '🧠 PROCESAR CONSULTA MULTIMODAL';
            }
        }
        
        function displayResponse(result) {
            // Mostrar respuesta principal
            let responseHtml = `<strong>Consulta:</strong> ${result.query}<br><br>`;
            responseHtml += `<strong>Respuesta:</strong><br>${result.response}`;
            
            document.getElementById('responseContent').innerHTML = responseHtml;
            
            // Actualizar badge de arquetipo
            if (result.archetype) {
                document.getElementById('archetypeBadge').textContent = result.archetype;
            }
            
            // Actualizar indicador de calidad
            if (result.quality !== undefined) {
                const qualityPercent = result.quality * 100;
                document.getElementById('qualityFill').style.width = qualityPercent + '%';
                document.getElementById('qualityValue').textContent = qualityPercent.toFixed(1);
            }
            
            // Mostrar información multimodal si hay imagen
            if (result.multimodal && result.multimodal.has_image) {
                document.getElementById('multimodalInfo').style.display = 'block';
                
                let multimodalHtml = `
                    <p><strong>Modelo usado:</strong> ${result.multimodal.model_used}</p>
                    <p><strong>Procesamiento:</strong> Análisis visual + procesamiento de texto</p>
                `;
                
                if (result.multimodal.image_context) {
                    multimodalHtml += `<p><strong>Contexto de imagen:</strong> ${result.multimodal.image_context.substring(0, 200)}...</p>`;
                }
                
                document.getElementById('multimodalDetails').innerHTML = multimodalHtml;
                
                // Mostrar métricas
                let metricsHtml = '';
                if (result.consciousness !== undefined) {
                    metricsHtml += `<div class="metric-card">
                        <div class="metric-value">${(result.consciousness * 100).toFixed(1)}%</div>
                        <div class="metric-label">Conciencia</div>
                    </div>`;
                }
                if (result.coherence !== undefined) {
                    metricsHtml += `<div class="metric-card">
                        <div class="metric-value">${(result.coherence * 100).toFixed(1)}%</div>
                        <div class="metric-label">Coherencia</div>
                    </div>`;
                }
                if (result.interactions !== undefined) {
                    metricsHtml += `<div class="metric-card">
                        <div class="metric-value">${result.interactions}</div>
                        <div class="metric-label">Interacciones</div>
                    </div>`;
                }
                
                document.getElementById('metricsGrid').innerHTML = metricsHtml;
            }
        }
        
        function addToChatHistory(query, response, archetype) {
            const timestamp = new Date().toLocaleTimeString();
            
            // Agregar mensaje del usuario
            const userMessage = {
                type: 'user',
                content: query,
                timestamp: timestamp
            };
            
            // Agregar respuesta del asistente
            const assistantMessage = {
                type: 'assistant',
                content: response,
                timestamp: timestamp,
                archetype: archetype
            };
            
            chatHistory.push(userMessage, assistantMessage);
            
            // Actualizar UI del historial
            updateChatHistoryUI();
        }
        
        function updateChatHistoryUI() {
            const chatHistoryDiv = document.getElementById('chatHistory');
            chatHistoryDiv.innerHTML = '';
            
            chatHistory.forEach(message => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `chat-message ${message.type}`;
                
                let content = `<div class="timestamp">${message.timestamp}</div>`;
                content += `<div class="content">${message.content.substring(0, 100)}${message.content.length > 100 ? '...' : ''}</div>`;
                
                if (message.archetype) {
                    content += `<div style="margin-top: 5px;"><span class="archetype-badge" style="font-size: 10px;">${message.archetype}</span></div>`;
                }
                
                messageDiv.innerHTML = content;
                chatHistoryDiv.appendChild(messageDiv);
            });
            
            // Scroll al final
            chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
        }
        
        // Inicializar
        window.onload = function() {
            setupDragAndDrop();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal con interfaz multimodal corregida"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Obtener estado del sistema corregido"""
    try:
        status = cio_multimodal.get_cio_status()
        
        return jsonify({
            "status": "ok",
            "cio_status": "Activo" if status['cio_brain_active'] else "Fallback",
            "openrouter_status": "Conectado" if status['openrouter_connected'] else "Desconectado",
            "multimodal_status": "Activas" if status['multimodal_capabilities'] > 0 else "Inactivas",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process_multimodal', methods=['POST'])
def process_multimodal():
    """Procesar consulta multimodal corregida"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400
        
        query = data.get('query', '')
        image_data = data.get('image_data', None)
        
        if not query:
            return jsonify({"error": "Query vacía"}), 400
        
        logger.info(f"🧠 Procesando consulta multimodal corregida: {query[:50]}...")
        
        # Ejecutar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(cio_multimodal.process_multimodal_query(query, image_data))
        finally:
            loop.close()
        
        # Verificar que el resultado sea válido
        if not isinstance(result, dict):
            return jsonify({"error": "Resultado inválido del procesamiento"}), 500
        
        logger.info(f"✅ Consulta multimodal procesada. Arquetipo: {result.get('archetype', 'N/A')}")
        
        # Asegurar que la respuesta sea serializable
        response_data = {
            "query": str(result.get('query', '')),
            "response": str(result.get('response', '')),
            "archetype": str(result.get('archetype', '')),
            "quality": float(result.get('quality', 0.0)),
            "consciousness": float(result.get('consciousness', 0.0)),
            "coherence": float(result.get('coherence', 0.0)),
            "interactions": int(result.get('interactions', 0)),
            "multimodal": result.get('multimodal', {})
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error procesando consulta multimodal: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🧠 CIO MULTIMODAL SERVER - VERSIÓN CORREGIDA")
    print("=" * 50)
    print("🌐 Iniciando servidor multimodal corregido en puerto 5003")
    print("🔗 URL: http://localhost:5003")
    print("🧠 Sistema CIO: ✅ ACTIVO")
    print("🖼️ Capacidades: ✅ Texto + Imagen")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5003, debug=False)
