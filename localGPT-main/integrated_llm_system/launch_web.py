#!/usr/bin/env python3
"""
LAUNCH WEB INTERFACE - Integrated LLM System
Lanza la interfaz web completa con todas las funcionalidades
"""

import asyncio
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar el sistema integrado
from integrate import WebInterface, LLMCore

def create_enhanced_web_interface():
    """Crea una interfaz web mejorada con todas las funcionalidades"""
    
    try:
        from flask import Flask, render_template_string, request, jsonify, send_from_directory
        from flask_cors import CORS
        import json
        
        app = Flask(__name__)
        CORS(app)  # Habilitar CORS para desarrollo
        
        # Inicializar componentes
        web_interface = WebInterface()
        
        # HTML template mejorado
        html_template = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Integrated LLM System - Joyas Ocultas</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    color: #333;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    text-align: center;
                    color: white;
                    margin-bottom: 30px;
                }
                .header h1 {
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .header p {
                    font-size: 1.2em;
                    opacity: 0.9;
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .card {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    transition: transform 0.3s ease;
                }
                .card:hover {
                    transform: translateY(-5px);
                }
                .card h3 {
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.3em;
                }
                .input-group {
                    margin-bottom: 15px;
                }
                .input-group label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 600;
                    color: #555;
                }
                .input-group input, .input-group textarea, .input-group select {
                    width: 100%;
                    padding: 12px;
                    border: 2px solid #e1e5e9;
                    border-radius: 8px;
                    font-size: 14px;
                    transition: border-color 0.3s ease;
                }
                .input-group input:focus, .input-group textarea:focus, .input-group select:focus {
                    outline: none;
                    border-color: #667eea;
                }
                .btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 600;
                    transition: transform 0.2s ease;
                    width: 100%;
                }
                .btn:hover {
                    transform: translateY(-2px);
                }
                .btn:active {
                    transform: translateY(0);
                }
                .response {
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 15px;
                    margin-top: 15px;
                    white-space: pre-wrap;
                    font-family: 'Courier New', monospace;
                    font-size: 13px;
                    max-height: 300px;
                    overflow-y: auto;
                }
                .status {
                    padding: 10px;
                    border-radius: 5px;
                    margin: 10px 0;
                    font-weight: 600;
                }
                .status.success { background: #d4edda; color: #155724; }
                .status.error { background: #f8d7da; color: #721c24; }
                .status.info { background: #d1ecf1; color: #0c5460; }
                .loading {
                    text-align: center;
                    color: #667eea;
                    font-style: italic;
                }
                .features {
                    background: white;
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }
                .features h2 {
                    color: #667eea;
                    margin-bottom: 15px;
                }
                .features ul {
                    list-style: none;
                }
                .features li {
                    padding: 8px 0;
                    border-bottom: 1px solid #f0f0f0;
                }
                .features li:before {
                    content: "🌟 ";
                    margin-right: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧠 Integrated LLM System</h1>
                    <p>Joyas Ocultas - Sistema Completo de Inteligencia Artificial</p>
                </div>
                
                <div class="features">
                    <h2>🚀 Funcionalidades Integradas</h2>
                    <ul>
                        <li>🧠 CIO Unified Brain (Cerebro Leonardo)</li>
                        <li>🦙 Ollama Core (Multi-modelos locales)</li>
                        <li>🌐 OpenRouter (316 modelos gratuitos de alta potencia)</li>
                        <li>🔄 Generación Híbrida (OpenRouter + Ollama)</li>
                        <li>🤖 BMAD Agent System (Agentes especializados)</li>
                        <li>🌐 Web Agent (Navegación y búsqueda)</li>
                        <li>🧠 Quantum Consciousness (Análisis cuántico)</li>
                        <li>📄 Document Processor (Procesamiento de documentos)</li>
                    </ul>
                </div>
                
                <div class="grid">
                    <!-- Generación con OpenRouter -->
                    <div class="card">
                        <h3>🌐 OpenRouter (Gratuito)</h3>
                        <div class="input-group">
                            <label>Prompt:</label>
                            <textarea id="openrouter-prompt" rows="3" placeholder="Escribe tu prompt aquí...">Explica qué es la inteligencia artificial en 3 líneas</textarea>
                        </div>
                        <div class="input-group">
                            <label>Modelo:</label>
                            <select id="openrouter-model">
                                <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                                <option value="openai/gpt-3.5-turbo">GPT-3.5 Turbo</option>
                                <option value="meta-llama/llama-3.1-8b-instruct">Llama 3.1 8B</option>
                                <option value="google/gemma-2-9b-it">Gemma 2 9B</option>
                                <option value="mistralai/mistral-7b-instruct">Mistral 7B</option>
                            </select>
                        </div>
                        <button class="btn" onclick="generateOpenRouter()">🚀 Generar con OpenRouter</button>
                        <div id="openrouter-response" class="response" style="display: none;"></div>
                    </div>
                    
                    <!-- Generación Híbrida -->
                    <div class="card">
                        <h3>🔄 Generación Híbrida</h3>
                        <div class="input-group">
                            <label>Prompt:</label>
                            <textarea id="hybrid-prompt" rows="3" placeholder="Escribe tu prompt aquí...">Escribe un haiku sobre la tecnología</textarea>
                        </div>
                        <div class="input-group">
                            <label>Proveedor Principal:</label>
                            <select id="hybrid-provider">
                                <option value="openrouter">OpenRouter (Recomendado)</option>
                                <option value="ollama">Ollama</option>
                            </select>
                        </div>
                        <button class="btn" onclick="generateHybrid()">🔄 Generar Híbrido</button>
                        <div id="hybrid-response" class="response" style="display: none;"></div>
                    </div>
                    
                    <!-- Cerebro CIO Leonardo -->
                    <div class="card">
                        <h3>🧠 Cerebro CIO Leonardo</h3>
                        <div class="input-group">
                            <label>Prompt para Leonardo:</label>
                            <textarea id="cio-prompt" rows="3" placeholder="Pregunta algo a Leonardo da Vinci...">¿Cómo combinarías arte y ciencia en el siglo XXI?</textarea>
                        </div>
                        <button class="btn" onclick="generateCIO()">🎨 Preguntar a Leonardo</button>
                        <div id="cio-response" class="response" style="display: none;"></div>
                    </div>
                    
                    <!-- Estado del Sistema -->
                    <div class="card">
                        <h3>📊 Estado del Sistema</h3>
                        <button class="btn" onclick="getSystemStatus()">📈 Ver Estado</button>
                        <button class="btn" onclick="getCIOStatus()" style="margin-top: 10px;">🧠 Estado CIO</button>
                        <button class="btn" onclick="getModels()" style="margin-top: 10px;">📋 Modelos</button>
                        <div id="status-response" class="response" style="display: none;"></div>
                    </div>
                </div>
            </div>
            
            <script>
                async function makeRequest(url, data) {
                    try {
                        const response = await fetch(url, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        });
                        return await response.json();
                    } catch (error) {
                        return { error: error.message };
                    }
                }
                
                async function generateOpenRouter() {
                    const prompt = document.getElementById('openrouter-prompt').value;
                    const model = document.getElementById('openrouter-model').value;
                    const responseDiv = document.getElementById('openrouter-response');
                    
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Generando con OpenRouter...</div>';
                    
                    const result = await makeRequest('/api/openrouter/generate', {
                        prompt: prompt,
                        model: model
                    });
                    
                    if (result.success) {
                        responseDiv.innerHTML = `<div class="status success">✅ Éxito (${result.provider})</div>
                            <strong>Modelo:</strong> ${result.model}<br>
                            <strong>Tokens:</strong> ${result.usage?.total_tokens || 'N/A'}<br>
                            <strong>Respuesta:</strong><br>${result.response}`;
                    } else {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${result.error}`;
                    }
                }
                
                async function generateHybrid() {
                    const prompt = document.getElementById('hybrid-prompt').value;
                    const provider = document.getElementById('hybrid-provider').value;
                    const responseDiv = document.getElementById('hybrid-response');
                    
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Generando híbrido...</div>';
                    
                    const result = await makeRequest('/api/hybrid/generate', {
                        prompt: prompt,
                        provider: provider
                    });
                    
                    if (result.success) {
                        let fallbackInfo = '';
                        if (result.original_error) {
                            fallbackInfo = `<br><strong>⚠️ Fallback de:</strong> ${result.original_error}`;
                        }
                        
                        responseDiv.innerHTML = `<div class="status success">✅ Éxito (${result.provider})</div>
                            <strong>Modelo:</strong> ${result.model}${fallbackInfo}<br>
                            <strong>Respuesta:</strong><br>${result.response}`;
                    } else {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${result.error}`;
                    }
                }
                
                async function generateCIO() {
                    const prompt = document.getElementById('cio-prompt').value;
                    const responseDiv = document.getElementById('cio-response');
                    
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Consultando a Leonardo...</div>';
                    
                    const result = await makeRequest('/api/cio/generate', {
                        prompt: prompt
                    });
                    
                    if (result.response) {
                        responseDiv.innerHTML = `<div class="status success">🧠 Respuesta de Leonardo</div>
                            <strong>Mundo Arquetipal:</strong> ${result.archetypal_world}<br>
                            <strong>Coherencia:</strong> ${result.coherence?.toFixed(3) || 'N/A'}<br>
                            <strong>Creatividad:</strong> ${result.creativity_index?.toFixed(3) || 'N/A'}<br>
                            <strong>Respuesta:</strong><br>${result.response}`;
                    } else {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${result.error || 'Error desconocido'}`;
                    }
                }
                
                async function getSystemStatus() {
                    const responseDiv = document.getElementById('status-response');
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Obteniendo estado...</div>';
                    
                    try {
                        const [modelsResponse, openrouterModelsResponse] = await Promise.all([
                            fetch('/api/models'),
                            fetch('/api/openrouter/models')
                        ]);
                        
                        const models = await modelsResponse.json();
                        const openrouterModels = await openrouterModelsResponse.json();
                        
                        responseDiv.innerHTML = `<div class="status info">📊 Estado del Sistema</div>
                            <strong>Modelos Ollama:</strong> ${models.models?.length || 0}<br>
                            <strong>Modelos OpenRouter:</strong> ${openrouterModels.models?.length || 0}<br>
                            <strong>Estado:</strong> ✅ Sistema operativo`;
                    } catch (error) {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${error.message}`;
                    }
                }
                
                async function getCIOStatus() {
                    const responseDiv = document.getElementById('status-response');
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Obteniendo estado CIO...</div>';
                    
                    try {
                        const response = await fetch('/api/cio/status');
                        const status = await response.json();
                        
                        responseDiv.innerHTML = `<div class="status info">🧠 Estado del Cerebro CIO</div>
                            <strong>Brain ID:</strong> ${status.brain_id}<br>
                            <strong>Nivel de Consciencia:</strong> ${status.consciousness_level}<br>
                            <strong>Coherencia:</strong> ${status.coherence?.toFixed(3) || 'N/A'}<br>
                            <strong>Creatividad:</strong> ${status.creativity_index?.toFixed(3) || 'N/A'}<br>
                            <strong>Interacciones:</strong> ${status.interactions_count}<br>
                            <strong>Memorias:</strong> ${status.memory_count}`;
                    } catch (error) {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${error.message}`;
                    }
                }
                
                async function getModels() {
                    const responseDiv = document.getElementById('status-response');
                    responseDiv.style.display = 'block';
                    responseDiv.innerHTML = '<div class="loading">Obteniendo modelos...</div>';
                    
                    try {
                        const response = await fetch('/api/openrouter/models');
                        const data = await response.json();
                        
                        const modelsList = data.models?.slice(0, 10).map(m => `• ${m}`).join('<br>') || 'No disponibles';
                        
                        responseDiv.innerHTML = `<div class="status info">📋 Modelos OpenRouter (Top 10)</div>${modelsList}`;
                    } catch (error) {
                        responseDiv.innerHTML = `<div class="status error">❌ Error</div>${error.message}`;
                    }
                }
            </script>
        </body>
        </html>
        """
        
        @app.route('/')
        def home():
            return html_template
        
        # API endpoints
        @app.route('/api/openrouter/generate', methods=['POST'])
        async def openrouter_generate():
            data = request.json
            prompt = data.get('prompt', '')
            model = data.get('model', None)
            result = await web_interface.llm.generate_with_openrouter(prompt, model)
            return jsonify(result)
        
        @app.route('/api/hybrid/generate', methods=['POST'])
        async def hybrid_generate():
            data = request.json
            prompt = data.get('prompt', '')
            provider = data.get('provider', 'openrouter')
            result = await web_interface.llm.generate_hybrid(prompt, provider)
            return jsonify(result)
        
        @app.route('/api/cio/generate', methods=['POST'])
        async def cio_generate():
            data = request.json
            prompt = data.get('prompt', '')
            result = await web_interface.llm.generate_with_cio_brain(prompt)
            return jsonify(result)
        
        @app.route('/api/cio/status', methods=['GET'])
        def cio_status():
            status = web_interface.llm.get_cio_brain_status()
            return jsonify(status)
        
        @app.route('/api/openrouter/models', methods=['GET'])
        def openrouter_models():
            models = web_interface.llm.list_openrouter_models()
            return jsonify({"models": models})
        
        @app.route('/api/models', methods=['GET'])
        def list_models():
            models = web_interface.llm.list_models()
            return jsonify({"models": models})
        
        return app
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Instala Flask: pip install flask flask-cors")
        return None

def main():
    print("=" * 60)
    print("🌐 LAUNCHING WEB INTERFACE")
    print("Integrated LLM System - Frontend")
    print("=" * 60)
    
    app = create_enhanced_web_interface()
    
    if app:
        port = 5000
        print(f"✅ Interfaz web creada exitosamente")
        print(f"🌐 Iniciando servidor en http://localhost:{port}")
        print(f"📱 Abre tu navegador y ve a: http://localhost:{port}")
        print(f"🔧 Presiona Ctrl+C para detener el servidor")
        print("=" * 60)
        
        try:
            app.run(host='0.0.0.0', port=port, debug=True)
        except KeyboardInterrupt:
            print("\n👋 Servidor detenido por el usuario")
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
    else:
        print("❌ No se pudo crear la interfaz web")

if __name__ == "__main__":
    main()
