#!/usr/bin/env python3
"""
🧠 CIO MULTIMODAL SERVER - VERSIÓN CORREGIDA DEFINITIVA
Servidor multimodal con sistema CIO corregido
Estado real y funcional
"""

import asyncio
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
import requests

# Importar la extensión corregida
from cio_multimodal_extension_corrected import CIOMultimodalExtensionCorrected

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Inicializar el sistema CIO corregido
cio_multimodal = CIOMultimodalExtensionCorrected()

# Template HTML mejorado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 CIO Multimodal - Cache Inteligente Enrutadora</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }
        
        .status-card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }
        
        .status-card:hover {
            transform: translateY(-5px);
        }
        
        .status-card h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .status-indicator {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .status-active {
            background: #4CAF50;
            color: white;
        }
        
        .status-fallback {
            background: #FF9800;
            color: white;
        }
        
        .status-inactive {
            background: #f44336;
            color: white;
        }
        
        .chat-section {
            padding: 30px;
            background: #f8f9fa;
        }
        
        .chat-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }
        
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .input-group input:focus, .input-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .file-input {
            background: #f8f9fa;
            border: 2px dashed #667eea;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .file-input:hover {
            background: #e3f2fd;
            border-color: #2196F3;
        }
        
        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s ease;
            width: 100%;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        .response-container {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }
        
        .response-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .response-text {
            line-height: 1.6;
            color: #333;
            white-space: pre-wrap;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .metric {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #f44336;
        }
        
        .success {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            border-left: 5px solid #4caf50;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 CIO Multimodal</h1>
            <p>Cache Inteligente Enrutadora - Sistema Avanzado</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>Estado del Sistema</h3>
                <div id="cio-status" class="status-indicator status-active">Cargando...</div>
                <p style="margin-top: 10px; color: #666;">Estado del cerebro CIO</p>
            </div>
            
            <div class="status-card">
                <h3>OpenRouter</h3>
                <div id="openrouter-status" class="status-indicator status-active">Conectado</div>
                <p style="margin-top: 10px; color: #666;">API de modelos multimodales</p>
            </div>
            
            <div class="status-card">
                <h3>Capacidades</h3>
                <div id="multimodal-status" class="status-indicator status-active">Activas</div>
                <p style="margin-top: 10px; color: #666;">Procesamiento texto + imagen</p>
            </div>
            
            <div class="status-card">
                <h3>Última Actualización</h3>
                <div id="timestamp" style="font-weight: bold; color: #667eea;">Cargando...</div>
                <p style="margin-top: 10px; color: #666;">Estado en tiempo real</p>
            </div>
        </div>
        
        <div class="chat-section">
            <div class="chat-container">
                <h2 style="margin-bottom: 25px; color: #333;">💬 Consulta Multimodal</h2>
                
                <form id="query-form">
                    <div class="input-group">
                        <label for="query">Consulta:</label>
                        <textarea id="query" name="query" rows="4" placeholder="Escribe tu consulta aquí..." required></textarea>
                    </div>
                    
                    <div class="input-group">
                        <label for="image">Imagen (opcional):</label>
                        <div class="file-input" onclick="document.getElementById('image').click()">
                            <input type="file" id="image" name="image" accept="image/*" style="display: none;">
                            <p>📷 Haz clic para seleccionar una imagen</p>
                            <p style="font-size: 0.9em; color: #666;">Soporta: JPG, PNG, GIF</p>
                        </div>
                    </div>
                    
                    <button type="submit" class="submit-btn">🚀 Procesar Consulta</button>
                </form>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>🧠 Procesando con CIO...</p>
                </div>
                
                <div id="response-container" class="response-container" style="display: none;">
                    <div class="response-header">
                        <h3>📋 Respuesta del Sistema</h3>
                        <span id="archetype" style="background: #667eea; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.9em;"></span>
                    </div>
                    
                    <div class="response-text" id="response-text"></div>
                    
                    <div class="metrics">
                        <div class="metric">
                            <div class="metric-value" id="quality">0%</div>
                            <div class="metric-label">Calidad</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" id="consciousness">0%</div>
                            <div class="metric-label">Conciencia</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" id="coherence">0%</div>
                            <div class="metric-label">Coherencia</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value" id="interactions">0</div>
                            <div class="metric-label">Interacciones</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Actualizar estado
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                // Actualizar indicadores de estado
                const cioStatus = document.getElementById('cio-status');
                const openrouterStatus = document.getElementById('openrouter-status');
                const multimodalStatus = document.getElementById('multimodal-status');
                const timestamp = document.getElementById('timestamp');
                
                // Estado CIO
                if (data.cio_status === 'Activo') {
                    cioStatus.textContent = '✅ Activo';
                    cioStatus.className = 'status-indicator status-active';
                } else if (data.cio_status === 'Fallback') {
                    cioStatus.textContent = '🔄 Fallback';
                    cioStatus.className = 'status-indicator status-fallback';
                } else {
                    cioStatus.textContent = '❌ Inactivo';
                    cioStatus.className = 'status-indicator status-inactive';
                }
                
                // OpenRouter
                if (data.openrouter_status === 'Conectado') {
                    openrouterStatus.textContent = '✅ Conectado';
                    openrouterStatus.className = 'status-indicator status-active';
                } else {
                    openrouterStatus.textContent = '❌ Desconectado';
                    openrouterStatus.className = 'status-indicator status-inactive';
                }
                
                // Multimodal
                if (data.multimodal_status === 'Activas') {
                    multimodalStatus.textContent = '✅ Activas';
                    multimodalStatus.className = 'status-indicator status-active';
                } else {
                    multimodalStatus.textContent = '❌ Inactivas';
                    multimodalStatus.className = 'status-indicator status-inactive';
                }
                
                // Timestamp
                timestamp.textContent = new Date(data.timestamp).toLocaleString('es-ES');
                
            } catch (error) {
                console.error('Error actualizando estado:', error);
            }
        }
        
        // Procesar consulta
        document.getElementById('query-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const query = document.getElementById('query').value;
            const imageFile = document.getElementById('image').files[0];
            const loading = document.getElementById('loading');
            const responseContainer = document.getElementById('response-container');
            
            // Mostrar loading
            loading.style.display = 'block';
            responseContainer.style.display = 'none';
            
            try {
                const formData = new FormData();
                formData.append('query', query);
                
                if (imageFile) {
                    formData.append('image', imageFile);
                }
                
                const response = await fetch('/api/process_multimodal', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                // Ocultar loading
                loading.style.display = 'none';
                
                if (result.error) {
                    responseContainer.innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                    responseContainer.style.display = 'block';
                } else {
                    // Mostrar respuesta
                    document.getElementById('response-text').textContent = result.response;
                    document.getElementById('archetype').textContent = result.archetype || 'N/A';
                    document.getElementById('quality').textContent = Math.round((result.quality || 0) * 100) + '%';
                    document.getElementById('consciousness').textContent = Math.round((result.consciousness || 0) * 100) + '%';
                    document.getElementById('coherence').textContent = Math.round((result.coherence || 0) * 100) + '%';
                    document.getElementById('interactions').textContent = result.interactions || 0;
                    
                    responseContainer.style.display = 'block';
                }
                
                // Actualizar estado
                updateStatus();
                
            } catch (error) {
                loading.style.display = 'none';
                responseContainer.innerHTML = `<div class="error">❌ Error de conexión: ${error.message}</div>`;
                responseContainer.style.display = 'block';
            }
        });
        
        // Actualizar estado cada 5 segundos
        updateStatus();
        setInterval(updateStatus, 5000);
        
        // Mostrar nombre del archivo seleccionado
        document.getElementById('image').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const fileInput = document.querySelector('.file-input');
                fileInput.innerHTML = `<p>📷 Archivo seleccionado: ${file.name}</p>`;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Página principal con interfaz multimodal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Obtener estado del sistema"""
    try:
        # Obtener estado real del CIO
        cio_status_info = cio_multimodal.get_cio_status()
        
        # Determinar estado para mostrar
        if cio_status_info['cio_brain_active']:
            cio_status = "Activo"
        elif cio_status_info['status'] == 'fallback_mode':
            cio_status = "Fallback"
        else:
            cio_status = "Inactivo"
            
        openrouter_status = "Conectado" if cio_status_info['openrouter_connected'] else "Desconectado"
        multimodal_status = "Activas" if cio_status_info['multimodal_capabilities'] > 0 else "Inactivas"
        
        return jsonify({
            "status": "ok",
            "cio_status": cio_status,
            "openrouter_status": openrouter_status,
            "multimodal_status": multimodal_status,
            "cio_details": cio_status_info,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process_multimodal', methods=['POST'])
def process_multimodal():
    """Procesar consulta multimodal"""
    try:
        query = request.form.get('query', '')
        image_file = request.files.get('image')
        
        if not query:
            return jsonify({"error": "Query vacía"}), 400
        
        logger.info(f"🧠 Procesando consulta multimodal: {query[:50]}...")
        
        # Procesar imagen si existe
        image_data = None
        if image_file:
            import base64
            image_bytes = image_file.read()
            image_data = base64.b64encode(image_bytes).decode('utf-8')
        
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
    print("🧠 CIO MULTIMODAL SERVER - VERSIÓN CORREGIDA DEFINITIVA")
    print("=" * 60)
    print("🌐 Iniciando servidor multimodal corregido en puerto 5004")
    print("🔗 URL: http://localhost:5004")
    print("🧠 Sistema CIO: ✅ CORREGIDO Y FUNCIONAL")
    print("🖼️ Capacidades: ✅ Texto + Imagen + Fallback Inteligente")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5004, debug=False)
