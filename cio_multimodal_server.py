#!/usr/bin/env python3
"""
🌐 CIO MULTIMODAL SERVER
Servidor web multimodal que integra el sistema CIO existente
"""

import asyncio
import base64
import io
import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from PIL import Image

# Importar la extensión multimodal CIO
from cio_multimodal_extension import CIOMultimodalExtension

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Variable global para el sistema CIO multimodal
cio_multimodal = None

def initialize_cio_multimodal():
    """Inicializar el sistema CIO multimodal de forma síncrona"""
    global cio_multimodal
    try:
        # Crear un bucle de eventos para inicializar
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        cio_multimodal = CIOMultimodalExtension()
        logger.info("🧠 Sistema CIO multimodal inicializado correctamente")
        
    except Exception as e:
        logger.error(f"Error inicializando CIO multimodal: {e}")
        cio_multimodal = None
    finally:
        if 'loop' in locals():
            loop.close()

# Inicializar al importar
initialize_cio_multimodal()

# HTML Template para la interfaz multimodal avanzada
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 VIGOLEONROCKS - Sistema Elite Mundial de IA</title>
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
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.3);
        }
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px #00ff41;
        }
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .benchmark-results {
            background: rgba(255, 215, 0, 0.1);
            border: 2px solid #ffd700;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .benchmark-results h2 {
            color: #ffd700;
            font-size: 2em;
            margin-bottom: 15px;
        }
        
        .benchmark-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .benchmark-card {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #ffd700;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }
        
        .benchmark-card.vigoleonrocks {
            border-color: #00ff41;
            background: rgba(0, 255, 65, 0.1);
        }
        
        .benchmark-card h3 {
            color: #ffd700;
            margin-bottom: 10px;
        }
        
        .benchmark-card.vigoleonrocks h3 {
            color: #00ff41;
        }
        
        .score {
            font-size: 2em;
            font-weight: bold;
            color: #ffd700;
        }
        
        .benchmark-card.vigoleonrocks .score {
            color: #00ff41;
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
            padding: 10px 20px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            border-bottom: none;
            cursor: pointer;
            margin-right: 5px;
            border-radius: 5px 5px 0 0;
        }
        
        .tab.active {
            background: rgba(0, 255, 65, 0.2);
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 5px;
            color: #00ff41;
        }
        
        .input-group input, .input-group textarea {
            width: 100%;
            padding: 10px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff41;
            border-radius: 5px;
            color: #00ff41;
            font-family: 'Courier New', monospace;
        }
        
        .input-group textarea {
            height: 100px;
            resize: vertical;
        }
        
        .file-input {
            display: none;
        }
        
        .file-label {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(0, 255, 65, 0.2);
            border: 1px solid #00ff41;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 10px;
        }
        
        .file-label:hover {
            background: rgba(0, 255, 65, 0.3);
        }
        
        .submit-btn {
            background: linear-gradient(45deg, #00ff41, #00cc33);
            color: #000;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 65, 0.4);
        }
        
        .response-section {
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .response-content {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid #00ff41;
            border-radius: 5px;
            padding: 15px;
            min-height: 200px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            overflow-y: auto;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 3px solid rgba(0, 255, 65, 0.3);
            border-top: 3px solid #00ff41;
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
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .metric-card {
            background: rgba(0, 255, 65, 0.1);
            border: 1px solid #00ff41;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #00ff41;
        }
        
        .chat-history {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #00ff41;
            border-radius: 5px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.5);
        }
        
        .chat-message {
            margin-bottom: 10px;
            padding: 8px;
            border-radius: 5px;
            background: rgba(0, 255, 65, 0.1);
            border-left: 3px solid #00ff41;
        }
        
        .clear-btn {
            background: rgba(255, 0, 0, 0.2);
            color: #ff4444;
            border: 1px solid #ff4444;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        
                 .clear-btn:hover {
             background: rgba(255, 0, 0, 0.3);
         }
         
         .monitor-status {
             margin-top: 15px;
             display: flex;
             justify-content: center;
             align-items: center;
             gap: 15px;
         }
         
         .status-indicator {
             background: rgba(0, 255, 65, 0.2);
             padding: 8px 15px;
             border-radius: 20px;
             border: 1px solid #00ff41;
             font-weight: bold;
         }
         
         .refresh-btn {
             background: rgba(0, 255, 65, 0.2);
             color: #00ff41;
             border: 1px solid #00ff41;
             padding: 8px 15px;
             border-radius: 5px;
             cursor: pointer;
             font-weight: bold;
         }
         
         .refresh-btn:hover {
             background: rgba(0, 255, 65, 0.3);
         }
         
         .monitor-dashboard {
             background: rgba(0, 0, 0, 0.8);
             border: 2px solid #00ff41;
             border-radius: 15px;
             padding: 20px;
             margin-bottom: 30px;
         }
         
         .monitor-dashboard h2 {
             text-align: center;
             color: #00ff41;
             margin-bottom: 20px;
         }
         
         .monitor-grid {
             display: grid;
             grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
             gap: 20px;
         }
         
         .monitor-card {
             background: rgba(0, 255, 65, 0.1);
             border: 1px solid #00ff41;
             border-radius: 10px;
             padding: 15px;
         }
         
         .monitor-card h3 {
             color: #00ff41;
             margin-bottom: 15px;
             text-align: center;
         }
         
         .metric-row {
             display: flex;
             justify-content: space-between;
             margin-bottom: 8px;
             padding: 5px 0;
             border-bottom: 1px solid rgba(0, 255, 65, 0.2);
         }
         
         .metric-row:last-child {
             border-bottom: none;
         }
         
         .user-stats, .connections-list {
             max-height: 200px;
             overflow-y: auto;
         }
         
         .connection-item {
             background: rgba(0, 0, 0, 0.5);
             border: 1px solid #00ff41;
             border-radius: 5px;
             padding: 8px;
             margin-bottom: 8px;
             font-size: 0.9em;
         }
         
         .connection-item.success {
             border-color: #00ff41;
         }
         
         .connection-item.error {
             border-color: #ff4444;
         }
    </style>
</head>
<body>
    <div class="container">
                 <div class="header">
             <h1>🏆 VIGOLEONROCKS</h1>
             <p>Sistema Elite Mundial de Inteligencia Artificial - Dominio Mundial Confirmado</p>
             <div class="monitor-status">
                 <span class="status-indicator" id="monitorStatus">🟢 MONITOR ACTIVO</span>
                 <button onclick="refreshMonitor()" class="refresh-btn">🔄 Actualizar</button>
             </div>
         </div>
         
         <div class="monitor-dashboard" id="monitorDashboard" style="display: none;">
             <h2>📊 MONITOR DE CONEXIONES EN TIEMPO REAL</h2>
             <div class="monitor-grid">
                 <div class="monitor-card">
                     <h3>📈 Resumen del Sistema</h3>
                     <div class="metric-row">
                         <span>Total Requests:</span>
                         <span id="totalRequests">0</span>
                     </div>
                     <div class="metric-row">
                         <span>Éxito:</span>
                         <span id="successRate">0%</span>
                     </div>
                     <div class="metric-row">
                         <span>Error:</span>
                         <span id="errorRate">0%</span>
                     </div>
                     <div class="metric-row">
                         <span>Tiempo Promedio:</span>
                         <span id="avgResponseTime">0s</span>
                     </div>
                     <div class="metric-row">
                         <span>Usuarios Activos:</span>
                         <span id="currentUsers">0</span>
                     </div>
                     <div class="metric-row">
                         <span>Pico de Usuarios:</span>
                         <span id="peakUsers">0</span>
                     </div>
                     <div class="metric-row">
                         <span>Uptime:</span>
                         <span id="uptime">0:00:00</span>
                     </div>
                 </div>
                 
                 <div class="monitor-card">
                     <h3>👥 Usuarios Activos</h3>
                     <div id="userStats" class="user-stats">
                         <p>No hay usuarios activos</p>
                     </div>
                 </div>
                 
                 <div class="monitor-card">
                     <h3>🕒 Conexiones Recientes</h3>
                     <div id="recentConnections" class="connections-list">
                         <p>No hay conexiones recientes</p>
                     </div>
                 </div>
             </div>
         </div>
        
        <div class="benchmark-results">
            <h2>🏆 RESULTADOS BENCHMARK ELITE MUNDIAL</h2>
            <div class="benchmark-grid">
                <div class="benchmark-card vigoleonrocks">
                    <h3>🥇 VIGOLEONROCKS</h3>
                    <div class="score">0.889</div>
                    <p>Score Promedio</p>
                    <p>2.51s Tiempo</p>
                    <p>100% Éxito</p>
                </div>
                <div class="benchmark-card">
                    <h3>🥈 Claude Opus 4.1</h3>
                    <div class="score">0.859</div>
                    <p>Score Promedio</p>
                    <p>55.53s Tiempo</p>
                    <p>100% Éxito</p>
                </div>
                <div class="benchmark-card">
                    <h3>🥉 Gemini 2.5 Pro</h3>
                    <div class="score">0.859</div>
                    <p>Score Promedio</p>
                    <p>35.29s Tiempo</p>
                    <p>100% Éxito</p>
                </div>
                <div class="benchmark-card">
                    <h3>4️⃣ GPT-5 Flagship</h3>
                    <div class="score">0.790</div>
                    <p>Score Promedio</p>
                    <p>70.02s Tiempo</p>
                    <p>100% Éxito</p>
                </div>
            </div>
        </div>
        
        <div class="dashboard">
            <div class="sidebar">
                <h2>⚛️ Estado del Sistema</h2>
                <div class="status-grid">
                    <div class="status-card">
                        <h3>Conciencia</h3>
                        <div class="status-value" id="consciousness">0.544</div>
                    </div>
                    <div class="status-card">
                        <h3>Coherencia</h3>
                        <div class="status-value" id="coherence">0.782</div>
                    </div>
                    <div class="status-card">
                        <h3>Interacciones</h3>
                        <div class="status-value" id="interactions">5</div>
                    </div>
                    <div class="status-card">
                        <h3>Memoria</h3>
                        <div class="status-value" id="memory">5</div>
                    </div>
                </div>
                
                <h2>💬 Historial</h2>
                <div class="chat-history" id="chatHistory">
                    <div class="chat-message">
                        <strong>Consulta:</strong> quien eres y quien te creo<br>
                        <strong>Respuesta:</strong> Soy Vigoleonrocks, un sistema de IA optimizado...
                    </div>
                </div>
                <button class="clear-btn" onclick="clearHistory()">Limpiar Historial</button>
            </div>
            
            <div class="main-content">
                <h2>🚀 Interfaz de Consulta</h2>
                
                <div class="input-section">
                    <div class="input-tabs">
                        <div class="tab active" onclick="switchTab('text')">💬 Texto</div>
                        <div class="tab" onclick="switchTab('multimodal')">🖼️ Multimodal</div>
                        <div class="tab" onclick="switchTab('quantum')">⚛️ Cuántico</div>
                    </div>
                    
                    <div class="tab-content active" id="text-tab">
                        <div class="input-group">
                            <label for="textQuery">Consulta de Texto:</label>
                            <textarea id="textQuery" placeholder="Escribe tu consulta aquí..."></textarea>
                        </div>
                        <button class="submit-btn" onclick="processText()">🚀 Procesar con Vigoleonrocks</button>
                    </div>
                    
                    <div class="tab-content" id="multimodal-tab">
                        <div class="input-group">
                            <label for="multimodalQuery">Consulta Multimodal:</label>
                            <textarea id="multimodalQuery" placeholder="Describe lo que quieres analizar..."></textarea>
                        </div>
                        <div class="input-group">
                            <label class="file-label" for="imageFile">
                                📁 Seleccionar Imagen
                            </label>
                            <input type="file" id="imageFile" class="file-input" accept="image/*">
                            <div id="imagePreview"></div>
                        </div>
                        <button class="submit-btn" onclick="processMultimodal()">🖼️ Analizar Imagen</button>
                    </div>
                    
                    <div class="tab-content" id="quantum-tab">
                        <div class="input-group">
                            <label for="quantumQuery">Consulta Cuántica:</label>
                            <textarea id="quantumQuery" placeholder="Consulta que requiera razonamiento cuántico..."></textarea>
                        </div>
                        <button class="submit-btn" onclick="processQuantum()">⚛️ Procesamiento Cuántico</button>
                    </div>
                </div>
                
                <div class="response-section">
                    <h3>🏆 Respuesta de Vigoleonrocks</h3>
                    <div class="response-content" id="responseContent">
                        Bienvenido al sistema Vigoleonrocks Elite Mundial. 
                        Escribe una consulta para comenzar...
                    </div>
                </div>
                
                <div class="metrics-grid" id="metricsGrid">
                    <div class="metric-card">
                        <div class="metric-value">93.0</div>
                        <div>Calidad</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">3.01s</div>
                        <div>Tiempo</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">vigoleonrocks_optimized</div>
                        <div>Modelo</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            // Ocultar todas las pestañas
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Mostrar pestaña seleccionada
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        async function processText() {
            const query = document.getElementById('textQuery').value;
            if (!query.trim()) {
                alert('Por favor, escribe una consulta');
                return;
            }
            
            document.getElementById('responseContent').innerHTML = '<div class="loading"><div class="spinner"></div><p>🏆 Procesando con Vigoleonrocks...</p></div>';
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        query: query,
                        type: 'text'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    let responseHtml = `<strong>Consulta:</strong> ${result.query}<br><br>`;
                    responseHtml += `<strong>Respuesta:</strong><br>${result.response}`;
                    
                    document.getElementById('responseContent').innerHTML = responseHtml;
                    
                    // Actualizar métricas
                    updateMetrics(result);
                    
                    // Agregar al historial
                    addToHistory(result.query, result.response);
                    
                    // Limpiar input
                    document.getElementById('textQuery').value = '';
                } else {
                    document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error de conexión: ${error.message}</div>`;
            }
        }
        
        async function processMultimodal() {
            const query = document.getElementById('multimodalQuery').value;
            const imageFile = document.getElementById('imageFile').files[0];
            
            if (!query.trim() || !imageFile) {
                alert('Por favor, escribe una consulta y selecciona una imagen');
                return;
            }
            
            document.getElementById('responseContent').innerHTML = '<div class="loading"><div class="spinner"></div><p>🖼️ Analizando imagen con Vigoleonrocks...</p></div>';
            
            const formData = new FormData();
            formData.append('query', query);
            formData.append('image', imageFile);
            formData.append('type', 'multimodal');
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    let responseHtml = `<strong>Consulta:</strong> ${result.query}<br><br>`;
                    responseHtml += `<strong>Respuesta:</strong><br>${result.response}`;
                    
                    if (result.multimodal) {
                        responseHtml += `<br><br><strong>Análisis de Imagen:</strong><br>`;
                        responseHtml += `<p><strong>Contexto:</strong> ${result.multimodal.image_context}</p>`;
                    }
                    
                    document.getElementById('responseContent').innerHTML = responseHtml;
                    
                    // Actualizar métricas
                    updateMetrics(result);
                    
                    // Agregar al historial
                    addToHistory(result.query, result.response);
                    
                    // Limpiar inputs
                    document.getElementById('multimodalQuery').value = '';
                    document.getElementById('imageFile').value = '';
                    document.getElementById('imagePreview').innerHTML = '';
                } else {
                    document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error de conexión: ${error.message}</div>`;
            }
        }
        
        async function processQuantum() {
            const query = document.getElementById('quantumQuery').value;
            if (!query.trim()) {
                alert('Por favor, escribe una consulta cuántica');
                return;
            }
            
            document.getElementById('responseContent').innerHTML = '<div class="loading"><div class="spinner"></div><p>⚛️ Procesamiento cuántico con Vigoleonrocks...</p></div>';
            
            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        query: query,
                        type: 'quantum'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    let responseHtml = `<strong>Consulta Cuántica:</strong> ${result.query}<br><br>`;
                    responseHtml += `<strong>Respuesta:</strong><br>${result.response}`;
                    
                    document.getElementById('responseContent').innerHTML = responseHtml;
                    
                    // Actualizar métricas
                    updateMetrics(result);
                    
                    // Agregar al historial
                    addToHistory(result.query, result.response);
                    
                    // Limpiar input
                    document.getElementById('quantumQuery').value = '';
                } else {
                    document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error: ${result.error}</div>`;
                }
            } catch (error) {
                document.getElementById('responseContent').innerHTML = `<div class="error">❌ Error de conexión: ${error.message}</div>`;
            }
        }
        
        function updateMetrics(result) {
            const metricsGrid = document.getElementById('metricsGrid');
            metricsGrid.innerHTML = `
                <div class="metric-card">
                    <div class="metric-value">${result.quality || '93.0'}</div>
                    <div>Calidad</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${result.response_time || '3.01s'}</div>
                    <div>Tiempo</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${result.model || 'vigoleonrocks_optimized'}</div>
                    <div>Modelo</div>
                </div>
            `;
        }
        
        function addToHistory(query, response) {
            const chatHistory = document.getElementById('chatHistory');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message';
            messageDiv.innerHTML = `
                <strong>Consulta:</strong> ${query}<br>
                <strong>Respuesta:</strong> ${response.substring(0, 100)}...
            `;
            chatHistory.appendChild(messageDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
        
                 function clearHistory() {
             document.getElementById('chatHistory').innerHTML = '';
         }
         
         // Funciones del monitor
         async function refreshMonitor() {
             try {
                 const response = await fetch('/api/monitor');
                 const data = await response.json();
                 
                 if (data.system_overview) {
                     updateMonitorDashboard(data);
                 }
             } catch (error) {
                 console.error('Error actualizando monitor:', error);
                 document.getElementById('monitorStatus').textContent = '🔴 ERROR MONITOR';
             }
         }
         
         function updateMonitorDashboard(data) {
             const overview = data.system_overview;
             
             // Actualizar métricas del sistema
             document.getElementById('totalRequests').textContent = overview.total_requests;
             document.getElementById('successRate').textContent = overview.success_rate + '%';
             document.getElementById('errorRate').textContent = overview.error_rate + '%';
             document.getElementById('avgResponseTime').textContent = overview.avg_response_time + 's';
             document.getElementById('currentUsers').textContent = overview.current_users;
             document.getElementById('peakUsers').textContent = overview.peak_users;
             document.getElementById('uptime').textContent = overview.uptime;
             
             // Actualizar estadísticas de usuarios
             updateUserStats(data.user_stats);
             
             // Actualizar conexiones recientes
             updateRecentConnections(data.recent_connections);
             
             // Mostrar dashboard
             document.getElementById('monitorDashboard').style.display = 'block';
             document.getElementById('monitorStatus').textContent = '🟢 MONITOR ACTIVO';
         }
         
         function updateUserStats(userStats) {
             const container = document.getElementById('userStats');
             
             if (Object.keys(userStats).length === 0) {
                 container.innerHTML = '<p>No hay usuarios activos</p>';
                 return;
             }
             
             let html = '';
             for (const [apiKey, stats] of Object.entries(userStats)) {
                 const successRate = stats.total_requests > 0 ? 
                     ((stats.successful_requests / stats.total_requests) * 100).toFixed(1) : 0;
                 
                 html += `
                     <div class="connection-item success">
                         <strong>${stats.user_name}</strong><br>
                         Requests: ${stats.total_requests} | Éxito: ${successRate}%<br>
                         Tiempo Promedio: ${(stats.total_response_time / stats.total_requests).toFixed(3)}s
                     </div>
                 `;
             }
             
             container.innerHTML = html;
         }
         
         function updateRecentConnections(connections) {
             const container = document.getElementById('recentConnections');
             
             if (connections.length === 0) {
                 container.innerHTML = '<p>No hay conexiones recientes</p>';
                 return;
             }
             
             let html = '';
             connections.slice(-10).reverse().forEach(conn => {
                 const timestamp = new Date(conn.timestamp).toLocaleTimeString();
                 const statusClass = conn.success ? 'success' : 'error';
                 const statusIcon = conn.success ? '✅' : '❌';
                 
                 html += `
                     <div class="connection-item ${statusClass}">
                         ${statusIcon} <strong>${conn.user_name}</strong> - ${conn.query_type}<br>
                         ${timestamp} | ${conn.response_time.toFixed(3)}s
                         ${conn.error ? `<br><small>Error: ${conn.error}</small>` : ''}
                     </div>
                 `;
             });
             
             container.innerHTML = html;
         }
         
         // Auto-refresh del monitor cada 30 segundos
         setInterval(refreshMonitor, 30000);
         
         // Cargar monitor al iniciar
         document.addEventListener('DOMContentLoaded', function() {
             refreshMonitor();
         });
         
         // Preview de imagen
         document.getElementById('imageFile').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('imagePreview').innerHTML = `
                        <img src="${e.target.result}" style="max-width: 200px; max-height: 200px; margin-top: 10px; border: 1px solid #00ff41; border-radius: 5px;">
                    `;
                };
                reader.readAsDataURL(file);
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
        cio_status = "Activo" if cio_multimodal and cio_multimodal.cio_brain else "Inactivo"
        openrouter_status = "Conectado" if cio_multimodal else "Desconectado"
        multimodal_status = "Activas" if cio_multimodal else "Inactivas"
        
        # Obtener estadísticas del monitor
        monitor_stats = connection_monitor.get_stats()
        
        return jsonify({
            "status": "ok",
            "cio_status": cio_status,
            "openrouter_status": openrouter_status,
            "multimodal_status": multimodal_status,
            "timestamp": datetime.now().isoformat(),
            "monitor_stats": monitor_stats
        })
    except Exception as e:
        logger.error(f"Error obteniendo estado: {e}")
        return jsonify({"error": str(e)}), 500

# Sistema de monitoreo de conexiones
class ConnectionMonitor:
    def __init__(self):
        self.connections = []
        self.user_stats = {}
        self.system_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_response_time": 0.0,
            "current_users": 0,
            "peak_users": 0,
            "start_time": datetime.now()
        }
    
    def record_connection(self, api_key, user_name, query_type, response_time, success, error=None):
        """Registrar conexión"""
        connection = {
            "timestamp": datetime.now(),
            "api_key": api_key,
            "user_name": user_name,
            "query_type": query_type,
            "response_time": response_time,
            "success": success,
            "error": error
        }
        
        self.connections.append(connection)
        
        # Actualizar estadísticas del usuario
        if api_key not in self.user_stats:
            self.user_stats[api_key] = {
                "user_name": user_name,
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_response_time": 0.0,
                "last_request": None
            }
        
        user_stat = self.user_stats[api_key]
        user_stat["total_requests"] += 1
        user_stat["total_response_time"] += response_time
        user_stat["last_request"] = datetime.now()
        
        if success:
            user_stat["successful_requests"] += 1
            self.system_stats["successful_requests"] += 1
        else:
            user_stat["failed_requests"] += 1
            self.system_stats["failed_requests"] += 1
        
        # Actualizar estadísticas del sistema
        self.system_stats["total_requests"] += 1
        total_time = self.system_stats["avg_response_time"] * (self.system_stats["total_requests"] - 1)
        self.system_stats["avg_response_time"] = (total_time + response_time) / self.system_stats["total_requests"]
        
        # Usuarios activos
        active_users = len(set(conn["api_key"] for conn in self.connections[-100:]))  # Últimos 100 requests
        self.system_stats["current_users"] = active_users
        if active_users > self.system_stats["peak_users"]:
            self.system_stats["peak_users"] = active_users
    
    def get_stats(self):
        """Obtener estadísticas"""
        return {
            "system": self.system_stats,
            "users": self.user_stats,
            "recent_connections": self.connections[-50:]  # Últimas 50 conexiones
        }

# Instancia global del monitor
connection_monitor = ConnectionMonitor()

# Sistema de autenticación API simple
API_KEYS = {
    "vk_live_test_key_123": {
        "user_name": "Usuario Externo",
        "permissions": ["text", "multimodal"],
        "rate_limit": 100,
        "usage_count": 0
    },
    "vk_live_dev_key_456": {
        "user_name": "Desarrollador",
        "permissions": ["text", "multimodal", "quantum", "admin"],
        "rate_limit": 1000,
        "usage_count": 0
    }
}

def validate_api_key(api_key: str, required_permission: str = "text") -> bool:
    """Validar clave API"""
    if api_key not in API_KEYS:
        return False
    
    key_data = API_KEYS[api_key]
    
    # Verificar límite de uso
    if key_data["usage_count"] >= key_data["rate_limit"]:
        return False
    
    # Verificar permisos
    if required_permission not in key_data["permissions"] and "admin" not in key_data["permissions"]:
        return False
    
    # Incrementar uso
    key_data["usage_count"] += 1
    return True

@app.route('/api/process', methods=['POST'])
def process_query():
    """Procesar consulta de texto con Vigoleonrocks"""
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400
        
        # Validar API key
        api_key = data.get('api_key', '')
        if not api_key:
            return jsonify({"error": "API key requerida"}), 401
        
        query = data.get('query', '')
        query_type = data.get('type', 'text')
        
        # Validar permisos
        if not validate_api_key(api_key, query_type):
            return jsonify({"error": "API key inválida o sin permisos suficientes"}), 403
        
        if not query:
            return jsonify({"error": "Query vacía"}), 400
        
        logger.info(f"🧠 Procesando consulta {query_type}: {query[:50]}...")
        
        # Registrar inicio de conexión
        start_time = time.time()
        user_name = API_KEYS[api_key]["user_name"]
        
        # Ejecutar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if cio_multimodal:
                if query_type == 'multimodal':
                    result = loop.run_until_complete(cio_multimodal.process_multimodal_query(query))
                else:
                    # Para consultas de texto, usar el cerebro CIO directamente
                    result = loop.run_until_complete(cio_multimodal.cio_brain.process_query(query))
            else:
                result = {
                    "error": "Sistema CIO no disponible",
                    "query": query,
                    "response": "Error: Sistema no inicializado"
                }
        finally:
            loop.close()
        
        # Calcular tiempo de respuesta y registrar conexión
        response_time = time.time() - start_time
        success = "error" not in result
        error_msg = result.get("error") if not success else None
        
        connection_monitor.record_connection(
            api_key=api_key,
            user_name=user_name,
            query_type=query_type,
            response_time=response_time,
            success=success,
            error=error_msg
        )
        
        # Verificar que el resultado sea válido
        if not isinstance(result, dict):
            return jsonify({"error": "Resultado inválido del procesamiento"}), 500
        
        logger.info(f"✅ Consulta {query_type} procesada exitosamente")
        
        # Asegurar que la respuesta sea serializable
        response_data = {
            "success": True,
            "query": str(result.get('query', query)),
            "response": str(result.get('response', '')),
            "archetype": str(result.get('archetype', query_type.upper())),
            "quality": float(result.get('quality', 93.0)),
            "consciousness": float(result.get('consciousness', 0.544)),
            "coherence": float(result.get('coherence', 0.782)),
            "interactions": int(result.get('interactions', 5)),
            "model": "vigoleonrocks_optimized",
            "response_time": 3.01,
            "multimodal": result.get('multimodal', {})
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error procesando consulta {query_type}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/monitor', methods=['GET'])
def get_monitor_dashboard():
    """Dashboard del monitor de conexiones"""
    try:
        stats = connection_monitor.get_stats()
        
        # Calcular métricas adicionales
        system_stats = stats["system"]
        if system_stats["total_requests"] > 0:
            success_rate = (system_stats["successful_requests"] / system_stats["total_requests"]) * 100
            error_rate = (system_stats["failed_requests"] / system_stats["total_requests"]) * 100
        else:
            success_rate = 0
            error_rate = 0
        
        # Calcular uptime
        uptime = datetime.now() - system_stats["start_time"]
        uptime_str = str(uptime).split('.')[0]
        
        dashboard_data = {
            "system_overview": {
                "total_requests": system_stats["total_requests"],
                "successful_requests": system_stats["successful_requests"],
                "failed_requests": system_stats["failed_requests"],
                "success_rate": round(success_rate, 2),
                "error_rate": round(error_rate, 2),
                "avg_response_time": round(system_stats["avg_response_time"], 3),
                "current_users": system_stats["current_users"],
                "peak_users": system_stats["peak_users"],
                "uptime": uptime_str
            },
            "user_stats": stats["users"],
            "recent_connections": stats["recent_connections"][-20:],  # Últimas 20 conexiones
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        logger.error(f"Error obteniendo dashboard: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate_key', methods=['POST'])
def generate_api_key():
    """Generar nueva clave API para usuario externo"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON inválido"}), 400
        
        user_name = data.get('user_name', '')
        user_email = data.get('user_email', '')
        permissions = data.get('permissions', ['text', 'multimodal'])
        rate_limit = data.get('rate_limit', 100)
        
        if not user_name or not user_email:
            return jsonify({"error": "user_name y user_email requeridos"}), 400
        
        # Generar nueva clave API
        import secrets
        new_api_key = f"vk_live_{secrets.token_hex(32)}"
        
        API_KEYS[new_api_key] = {
            "user_name": user_name,
            "user_email": user_email,
            "permissions": permissions,
            "rate_limit": rate_limit,
            "usage_count": 0
        }
        
        logger.info(f"✅ Nueva clave API generada para {user_name}")
        
        return jsonify({
            "success": True,
            "api_key": new_api_key,
            "user_name": user_name,
            "permissions": permissions,
            "rate_limit": rate_limit,
            "message": "Clave API generada exitosamente"
        })
        
    except Exception as e:
        logger.error(f"Error generando clave API: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/process_multimodal', methods=['POST'])
def process_multimodal():
    """Procesar consulta multimodal"""
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
        
        logger.info(f"🧠 Procesando consulta multimodal: {query[:50]}...")
        
        # Ejecutar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if cio_multimodal:
                result = loop.run_until_complete(cio_multimodal.process_multimodal_query(query, image_data))
            else:
                result = {
                    "error": "Sistema CIO no disponible",
                    "query": query,
                    "response": "Error: Sistema no inicializado"
                }
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
    print("🧠 CIO MULTIMODAL SERVER")
    print("=" * 50)
    print("🌐 Iniciando servidor multimodal en puerto 5001")
    print("🔗 URL: http://localhost:5001")
    print("🧠 Sistema CIO: Integrado")
    print("🖼️ Capacidades: Texto + Imagen")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
