#!/usr/bin/env python3
"""
MULTIMODAL INTEGRATION - Unified Interface System
Integra todas las joyas ocultas de interfaces multimodales
"""

import asyncio
import sys
import os
from pathlib import Path
import json
import threading
import time

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template_string, request, jsonify, send_from_directory
    from flask_cors import CORS
    import streamlit as st
except ImportError as e:
    print(f"❌ Error importando dependencias: {e}")
    print("💡 Instala: pip install flask flask-cors streamlit")
    sys.exit(1)

# Importar el sistema integrado
try:
    from integrate import LLMCore, OpenRouterClient
except ImportError as e:
    print(f"❌ Error importando sistema integrado: {e}")
    sys.exit(1)

class MultimodalInterface:
    """Sistema unificado de interfaces multimodales"""
    
    def __init__(self):
        self.llm_core = LLMCore()
        self.openrouter = OpenRouterClient()
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        
    def setup_routes(self):
        """Configurar todas las rutas de interfaces"""
        
        @self.app.route('/')
        def home():
            return self.render_metacopilot_interface()
            
        @self.app.route('/telepathic')
        def telepathic():
            return self.render_metacopilot_interface()
            
        @self.app.route('/modern')
        def modern():
            return self.render_modern_interface()
            
        @self.app.route('/streamlit')
        def streamlit_redirect():
            return """
            <html>
            <head><title>Streamlit Interface</title></head>
            <body>
                <h1>🌐 Streamlit Interface</h1>
                <p>Ejecuta: <code>streamlit run webwalker_interface.py</code></p>
                <a href="/">← Volver al menú principal</a>
            </body>
            </html>
            """
            
        @self.app.route('/api/generate', methods=['POST'])
        def generate_response():
            data = request.json
            prompt = data.get('prompt', '')
            interface_type = data.get('interface', 'telepathic')
            
            try:
                # Generar respuesta usando el sistema integrado
                response = asyncio.run(self.llm_core.generate_hybrid(prompt))
                
                return jsonify({
                    'success': True,
                    'response': response.get('response', ''),
                    'provider': response.get('provider', ''),
                    'interface': interface_type
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
                
        @self.app.route('/api/models')
        def get_models():
            try:
                ollama_models = self.llm_core.list_models()
                openrouter_models = self.llm_core.list_openrouter_models()
                
                return jsonify({
                    'ollama': ollama_models,
                    'openrouter': openrouter_models[:10],  # Primeros 10
                    'total_openrouter': len(openrouter_models)
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def render_metacopilot_interface(self):
        """Renderizar la interfaz telepática de MetaCopilotSupremo"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌐 QBTC Multimodal - Interfaz Telepática</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0a0a0a, #1a1a2e, #16213e);
            color: #00ff88;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.1;
        }
        
        .container {
            position: relative;
            z-index: 2;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border: 2px solid #00ff88;
            padding: 20px;
            border-radius: 10px;
            background: rgba(0, 255, 136, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5em;
            text-shadow: 0 0 20px #00ff88;
            animation: glow 2s infinite alternate;
        }
        
        @keyframes glow {
            from { text-shadow: 0 0 20px #00ff88; }
            to { text-shadow: 0 0 30px #00ff88, 0 0 40px #00ff88; }
        }
        
        .interface-selector {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .interface-btn {
            padding: 12px 25px;
            border: 2px solid #00ff88;
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        
        .interface-btn:hover {
            background: rgba(0, 255, 136, 0.4);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
            transform: translateY(-2px);
        }
        
        .interface-btn.active {
            background: rgba(0, 255, 136, 0.6);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
        }
        
        .telepathic-interface {
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #00ff88;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .telepathic-input {
            width: 100%;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            color: #00ff88;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 16px;
            min-height: 120px;
            resize: vertical;
        }
        
        .telepathic-input:focus {
            outline: none;
            border-color: #ffff00;
            box-shadow: 0 0 15px rgba(255, 255, 0, 0.5);
        }
        
        .control-buttons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 25px;
            border: 2px solid #00ff88;
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            transition: all 0.3s;
            text-transform: uppercase;
        }
        
        .btn:hover {
            background: rgba(0, 255, 136, 0.4);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
            transform: translateY(-2px);
        }
        
        .btn.big-bang {
            border-color: #ff0088;
            color: #ff0088;
            background: rgba(255, 0, 136, 0.2);
        }
        
        .btn.big-bang:hover {
            background: rgba(255, 0, 136, 0.4);
            box-shadow: 0 0 20px rgba(255, 0, 136, 0.6);
        }
        
        .response-area {
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        
        .status-panel {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
            border-radius: 8px;
            padding: 15px;
            backdrop-filter: blur(5px);
        }
        
        .status-card h3 {
            color: #ffff00;
            margin-bottom: 10px;
            font-size: 1.2em;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #ffff00;
            font-size: 1.2em;
            margin: 20px 0;
        }
        
        .spinner {
            border: 2px solid #00ff88;
            border-top: 2px solid transparent;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="matrix-rain" id="matrixRain"></div>
    
    <div class="container">
        <div class="header">
            <h1>🌐 QBTC MULTIMODAL SYSTEM</h1>
            <p>Interfaz Telepática Unificada - OpenRouter + Ollama + CIO Brain</p>
        </div>
        
        <div class="interface-selector">
            <a href="/telepathic" class="interface-btn active">🧠 Telepática</a>
            <a href="/modern" class="interface-btn">💎 Moderna</a>
            <a href="/streamlit" class="interface-btn">📊 Streamlit</a>
            <a href="/api/models" class="interface-btn" target="_blank">🔧 API</a>
        </div>
        
        <div class="status-panel">
            <div class="status-card">
                <h3>🧠 CIO Brain</h3>
                <p>✅ Leonardo Active</p>
                <p>🌐 26D Context</p>
            </div>
            <div class="status-card">
                <h3>🚀 OpenRouter</h3>
                <p>✅ 316 Models</p>
                <p>🔑 API Connected</p>
            </div>
            <div class="status-card">
                <h3>🤖 Ollama</h3>
                <p>✅ 10 Models</p>
                <p>🔄 Fallback Ready</p>
            </div>
        </div>
        
        <div class="telepathic-interface">
            <div class="input-section">
                <label for="telepathicInput">🧠 PENSAMIENTO TELEPÁTICO:</label>
                <textarea 
                    id="telepathicInput" 
                    class="telepathic-input" 
                    placeholder="Expresa tu pensamiento telepático aquí... (El sistema usará OpenRouter + Ollama + CIO Brain)"
                ></textarea>
            </div>
            
            <div class="control-buttons">
                <button class="btn" onclick="generateResponse()">
                    🌟 GENERAR RESPUESTA
                </button>
                <button class="btn big-bang" onclick="generateWithCIO()">
                    🧠 BIG BANG (CIO Brain)
                </button>
                <button class="btn" onclick="clearResponse()">
                    🗑️ LIMPIAR
                </button>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>🔄 Procesando pensamiento telepático...</p>
            </div>
            
            <div class="response-area" id="responseArea">
                <p style="color: #666;">La respuesta aparecerá aquí...</p>
            </div>
        </div>
    </div>
    
    <script>
        // Matrix rain effect
        function createMatrixRain() {
            const canvas = document.createElement('canvas');
            canvas.id = 'matrixRain';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100%';
            canvas.style.height = '100%';
            canvas.style.pointerEvents = 'none';
            canvas.style.zIndex = '1';
            canvas.style.opacity = '0.1';
            
            document.body.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
            const matrixArray = matrix.split("");
            
            const fontSize = 10;
            const columns = canvas.width / fontSize;
            const drops = [];
            
            for (let x = 0; x < columns; x++) {
                drops[x] = 1;
            }
            
            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.fillStyle = '#0F0';
                ctx.font = fontSize + 'px monospace';
                
                for (let i = 0; i < drops.length; i++) {
                    const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }
            
            setInterval(draw, 35);
        }
        
        // Initialize matrix rain
        createMatrixRain();
        
        // API functions
        async function generateResponse() {
            const input = document.getElementById('telepathicInput').value;
            if (!input.trim()) {
                alert('Por favor, ingresa un pensamiento telepático');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: input,
                        interface: 'telepathic'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('responseArea').innerHTML = 
                        `<p style="color: #00ff88;"><strong>🤖 RESPUESTA:</strong></p>
                         <p style="color: #ffff00;">${data.response}</p>
                         <p style="color: #666; font-size: 0.8em;">Proveedor: ${data.provider}</p>`;
                } else {
                    document.getElementById('responseArea').innerHTML = 
                        `<p style="color: #ff0088;">❌ Error: ${data.error}</p>`;
                }
            } catch (error) {
                document.getElementById('responseArea').innerHTML = 
                    `<p style="color: #ff0088;">❌ Error de conexión: ${error.message}</p>`;
            }
            
            hideLoading();
        }
        
        async function generateWithCIO() {
            const input = document.getElementById('telepathicInput').value;
            if (!input.trim()) {
                alert('Por favor, ingresa un pensamiento telepático');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: `[CIO BRAIN MODE] ${input}`,
                        interface: 'cio'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('responseArea').innerHTML = 
                        `<p style="color: #ff0088;"><strong>🧠 CIO BRAIN RESPONSE:</strong></p>
                         <p style="color: #ffff00;">${data.response}</p>
                         <p style="color: #666; font-size: 0.8em;">Proveedor: ${data.provider}</p>`;
                } else {
                    document.getElementById('responseArea').innerHTML = 
                        `<p style="color: #ff0088;">❌ Error: ${data.error}</p>`;
                }
            } catch (error) {
                document.getElementById('responseArea').innerHTML = 
                    `<p style="color: #ff0088;">❌ Error de conexión: ${error.message}</p>`;
            }
            
            hideLoading();
        }
        
        function clearResponse() {
            document.getElementById('telepathicInput').value = '';
            document.getElementById('responseArea').innerHTML = 
                '<p style="color: #666;">La respuesta aparecerá aquí...</p>';
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        // Enter key support
        document.getElementById('telepathicInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                generateResponse();
            }
        });
    </script>
</body>
</html>
        ''')
    
    def render_modern_interface(self):
        """Renderizar la interfaz moderna de LocalGPTUI"""
        return render_template_string('''
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>💎 QBTC Modern Interface</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />
    
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
        }
        .chat-container { 
            max-width: 900px; 
            margin: 2rem auto; 
            background: rgba(255,255,255,0.95); 
            border-radius: 15px; 
            box-shadow: 0 8px 32px rgba(31,38,135,0.37); 
        }
        .chat-header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 1.5rem; 
            text-align: center; 
            border-radius: 15px 15px 0 0; 
        }
        .chat-body { padding: 2rem; }
        .btn-primary { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border: none; 
            border-radius: 10px; 
        }
        .form-control { border-radius: 10px; }
        .alert { border-radius: 10px; }
        .stats-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 1rem; 
            margin: 1rem 0; 
        }
        .stat-item { 
            text-align: center; 
            padding: 1rem; 
            background: rgba(102,126,234,0.1); 
            border-radius: 8px; 
        }
        .interface-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .interface-btn {
            padding: 8px 16px;
            border: 2px solid #667eea;
            background: rgba(102,126,234,0.1);
            color: #667eea;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        .interface-btn:hover {
            background: rgba(102,126,234,0.2);
            transform: translateY(-2px);
            text-decoration: none;
            color: #667eea;
        }
        .interface-btn.active {
            background: rgba(102,126,234,0.3);
            box-shadow: 0 0 10px rgba(102,126,234,0.5);
        }
        @media (max-width: 768px) { 
            .interface-selector { flex-direction: column; } 
        }
    </style>
</head>

<body>
    <div class="container-fluid">
        <div class="chat-container">
            <div class="chat-header">
                <h1><i class="fas fa-robot"></i> 💎 QBTC Modern Interface</h1>
                <p>OpenRouter + Ollama + CIO Brain Integration</p>
                <span class="badge bg-success">Online</span>
            </div>

            <div class="chat-body">
                <div class="interface-selector">
                    <a href="/telepathic" class="interface-btn">🧠 Telepática</a>
                    <a href="/modern" class="interface-btn active">💎 Moderna</a>
                    <a href="/streamlit" class="interface-btn">📊 Streamlit</a>
                    <a href="/api/models" class="interface-btn" target="_blank">🔧 API</a>
                </div>

                <div class="stats-grid">
                    <div class="stat-item">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">316</div>
                        <div>OpenRouter Models</div>
                    </div>
                    <div class="stat-item">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">10</div>
                        <div>Ollama Models</div>
                    </div>
                    <div class="stat-item">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">🧠</div>
                        <div>CIO Brain Active</div>
                    </div>
                </div>

                <form id="promptForm">
                    <div class="mb-3">
                        <label for="user_prompt" class="form-label">
                            <i class="fas fa-question-circle"></i> Pregunta al sistema integrado
                        </label>
                        <textarea class="form-control" id="user_prompt" rows="4" 
                                placeholder="Escribe tu pregunta aquí... (El sistema usará OpenRouter + Ollama + CIO Brain)" required></textarea>
                    </div>
                    
                    <div class="d-flex gap-2 justify-content-center">
                        <button type="button" class="btn btn-primary" onclick="generateResponse()">
                            <i class="fas fa-search"></i> Generar Respuesta
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="generateWithCIO()">
                            <i class="fas fa-brain"></i> CIO Brain
                        </button>
                        <button type="button" class="btn btn-outline-secondary" onclick="clearForm()">
                            <i class="fas fa-eraser"></i> Limpiar
                        </button>
                    </div>
                    
                    <div class="text-center mt-3" id="loadingSpinner" style="display: none;">
                        <div class="spinner-border text-primary"></div>
                        <p class="mt-2">Procesando...</p>
                    </div>
                </form>

                <hr class="my-4">

                <div class="response-area">
                    <h5><i class="fas fa-comments"></i> Respuesta del Sistema</h5>
                    <div id="responseContent" class="mt-3 p-3 bg-light rounded">
                        <p class="text-muted">La respuesta aparecerá aquí...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        async function generateResponse() {
            const input = document.getElementById('user_prompt').value;
            if (!input.trim()) {
                alert('Por favor, ingresa una pregunta');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: input,
                        interface: 'modern'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('responseContent').innerHTML = 
                        `<div class="alert alert-success">
                            <strong>🤖 Respuesta:</strong><br>
                            ${data.response.replace(/\\n/g, '<br>')}
                            <br><small class="text-muted">Proveedor: ${data.provider}</small>
                        </div>`;
                } else {
                    document.getElementById('responseContent').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Error:</strong> ${data.error}
                        </div>`;
                }
            } catch (error) {
                document.getElementById('responseContent').innerHTML = 
                    `<div class="alert alert-danger">
                        <strong>❌ Error de conexión:</strong> ${error.message}
                    </div>`;
            }
            
            hideLoading();
        }
        
        async function generateWithCIO() {
            const input = document.getElementById('user_prompt').value;
            if (!input.trim()) {
                alert('Por favor, ingresa una pregunta');
                return;
            }
            
            showLoading();
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: `[CIO BRAIN MODE] ${input}`,
                        interface: 'cio'
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('responseContent').innerHTML = 
                        `<div class="alert alert-info">
                            <strong>🧠 CIO Brain Response:</strong><br>
                            ${data.response.replace(/\\n/g, '<br>')}
                            <br><small class="text-muted">Proveedor: ${data.provider}</small>
                        </div>`;
                } else {
                    document.getElementById('responseContent').innerHTML = 
                        `<div class="alert alert-danger">
                            <strong>❌ Error:</strong> ${data.error}
                        </div>`;
                }
            } catch (error) {
                document.getElementById('responseContent').innerHTML = 
                    `<div class="alert alert-danger">
                        <strong>❌ Error de conexión:</strong> ${error.message}
                    </div>`;
            }
            
            hideLoading();
        }
        
        function clearForm() {
            document.getElementById('user_prompt').value = '';
            document.getElementById('responseContent').innerHTML = 
                '<p class="text-muted">La respuesta aparecerá aquí...</p>';
        }
        
        function showLoading() {
            document.getElementById('loadingSpinner').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loadingSpinner').style.display = 'none';
        }
        
        // Enter key support
        document.getElementById('user_prompt').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                generateResponse();
            }
        });
    </script>
</body>
</html>
        ''')
    
    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Ejecutar el servidor multimodal"""
        print("=" * 60)
        print("🌐 LAUNCHING MULTIMODAL INTERFACE SYSTEM")
        print("Integrated LLM System - Interfaces Unificadas")
        print("=" * 60)
        print("✅ Componentes LLM inicializados correctamente")
        print("✅ Servidor web multimodal creado exitosamente")
        print(f"🌐 Iniciando en http://localhost:{port}")
        print("📱 Interfaces disponibles:")
        print("   🧠 /telepathic - Interfaz telepática Matrix")
        print("   💎 /modern - Interfaz moderna Bootstrap")
        print("   📊 /streamlit - Interfaz Streamlit (redirección)")
        print("   🔧 /api/* - APIs del sistema")
        print("📱 Abre tu navegador y ve a: http://localhost:5000")
        print("🔧 Presiona Ctrl+C para detener")
        print("=" * 60)
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Función principal"""
    try:
        multimodal = MultimodalInterface()
        multimodal.run()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
