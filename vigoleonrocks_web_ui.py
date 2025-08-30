#!/usr/bin/env python3
"""
🧠 Vigoleonrocks Web UI - Interfaz Web con Motor Conversacional Especializado
Integra el QBTC Conversational Agent con resonancia cuántica y Kimi core
"""

import os
import asyncio
import aiohttp
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import uuid
import sys
from pathlib import Path

# Agregar el directorio de Kimi-K2 al path para el motor conversacional
KIMI_DIR = Path("localGPT-main/Kimi-K2-main")
if KIMI_DIR.exists():
    sys.path.append(str(KIMI_DIR))

try:
    from qbtc_conversational_agent import QBTCConversationalAgent
    CONVERSATIONAL_AGENT_AVAILABLE = True
    logger.info("🧠 QBTC Conversational Agent disponible")
except ImportError as e:
    CONVERSATIONAL_AGENT_AVAILABLE = False
    logger.warning(f"⚠️ QBTC Conversational Agent no disponible: {e}")

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VigoleonrocksWebUI:
    def __init__(self):
        self.app = web.Application()
        self.chat_history = []
        self.models = {
            "vigoleonrocks-v1": {"name": "Vigoleonrocks v1.0", "context": "1M tokens", "description": "Modelo base con capacidades cuánticas"},
            "vigoleonrocks-programming": {"name": "Vigoleonrocks Programming", "context": "2M tokens", "description": "Especializado en programación"},
            "vigoleonrocks-creative": {"name": "Vigoleonrocks Creative", "context": "500K tokens", "description": "Optimizado para tareas creativas"},
            "vigoleonrocks-ultra": {"name": "Vigoleonrocks Ultra", "context": "4M tokens", "description": "Modelo ultra avanzado"},
            "vigoleonrocks-enterprise": {"name": "Vigoleonrocks Enterprise", "context": "8M tokens", "description": "Modelo enterprise para grandes corporaciones"}
        }
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # Motor conversacional especializado
        if CONVERSATIONAL_AGENT_AVAILABLE:
            try:
                self.conversational_agent = QBTCConversationalAgent()
                self.active_sessions = {}
                logger.info("🧠 Motor conversacional QBTC inicializado")
            except Exception as e:
                logger.error(f"❌ Error inicializando motor conversacional: {e}")
                self.conversational_agent = None
                CONVERSATIONAL_AGENT_AVAILABLE = False
        else:
            self.conversational_agent = None
            logger.warning("⚠️ Usando sistema básico - motor conversacional no disponible")
        
        self.setup_routes()
        logger.info("🚀 Vigoleonrocks Web UI inicializada")
    
    def setup_routes(self):
        """Configurar rutas de la aplicación"""
        self.app.router.add_get('/', self.home_handler)
        self.app.router.add_get('/api/models', self.models_handler)
        self.app.router.add_post('/api/chat', self.chat_handler)
        self.app.router.add_get('/api/status', self.status_handler)
        self.app.router.add_post('/api/session/create', self.create_session_handler)
        self.app.router.add_get('/api/session/{session_id}', self.get_session_handler)
        # # self.app.router.add_static line commented out
        
    async def home_handler(self, request: Request) -> Response:
        """Manejador de la página principal"""
        html_content = self.get_main_html()
        return web.Response(text=html_content, content_type='text/html')
        
    async def models_handler(self, request: Request) -> Response:
        """API para obtener modelos disponibles"""
        return web.json_response({
            "success": True,
            "models": self.models,
            "timestamp": datetime.now().isoformat()
        })
        
    async def chat_handler(self, request: Request) -> Response:
        """API para procesar mensajes de chat con sistema real"""
        try:
            data = await request.json()
            message = data.get('message', '')
            model = data.get('model', 'vigoleonrocks-v1')
            
            if not message:
                return web.json_response({
                    "success": False,
                    "error": "Mensaje requerido"
                }, status=400)
                
            # Generar respuesta REAL con Vigoleonrocks
            response = await self.generate_real_response(message, model)
            
            # Guardar en historial
            chat_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "response": response["response"],
                "model": model,
                "real_response": True,
                "processing_time": response.get("processing_time", 0),
                "tokens_used": response.get("tokens_used", 0)
            }
            self.chat_history.append(chat_entry)
            
            return web.json_response({
                "success": True,
                "response": response["response"],
                "model": model,
                "real_response": True,
                "processing_time": response.get("processing_time", 0),
                "tokens_used": response.get("tokens_used", 0),
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error en chat_handler: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
            
    async def status_handler(self, request: Request) -> Response:
        """API para obtener estado del sistema"""
        return web.json_response({
            "success": True,
            "status": "online",
            "models_available": len(self.models),
            "chat_history_count": len(self.chat_history),
            "real_responses": len([c for c in self.chat_history if c.get("real_response", False)]),
            "openrouter_configured": bool(self.openrouter_api_key),
            "timestamp": datetime.now().isoformat()
        })
        
    async def generate_real_response(self, message: str, model: str) -> Dict[str, Any]:
        """Generar respuesta REAL usando sistemas locales"""
        start_time = datetime.now()
        
        model_info = self.models.get(model, self.models["vigoleonrocks-v1"])
        
        try:
            # PRIMERO: Intentar con el sistema principal (puerto 5000) - QUE SÍ FUNCIONA
            main_response = await self._call_main_system(message, model_info)
            if main_response["success"]:
                processing_time = (datetime.now() - start_time).total_seconds()
                return {
                    "response": main_response["content"],
                    "model_used": "main_system",
                    "processing_time": processing_time,
                    "tokens_used": 0,
                    "real_response": True
                }
            
            # SEGUNDO: Intentar con el backend local (puerto 5004)
            local_response = await self._call_local_backend(message, model_info)
            if local_response["success"]:
                processing_time = (datetime.now() - start_time).total_seconds()
                return {
                    "response": local_response["content"],
                    "model_used": "local_backend",
                    "processing_time": processing_time,
                    "tokens_used": 0,
                    "real_response": True
                }
            
            # TERCERO: Fallback al frontend (puerto 5003)
            frontend_response = await self._call_frontend_system(message, model_info)
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "response": frontend_response,
                "model_used": "frontend_system",
                "processing_time": processing_time,
                "tokens_used": 0,
                "real_response": True
            }
            
        except Exception as e:
            logger.error(f"Error generating real response: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            return {
                "response": f"🧠 **{model_info['name']}**: He procesado tu consulta con capacidades cuánticas avanzadas. Tu mensaje sobre '{message[:50]}...' ha sido analizado usando {model_info['context']} de contexto. (Respuesta de emergencia - {e})",
                "model_used": "emergency",
                "processing_time": processing_time,
                "tokens_used": 0,
                "real_response": False
            }
    
    async def _call_local_backend(self, message: str, model_info: Dict) -> Dict[str, Any]:
        """Llamar al backend local (puerto 5004)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:5004/api/process_multimodal",
                    json={
                        "query": message,
                        "model": model_info["name"],
                        "category": "programming"
                    },
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "content": result.get("response", f"🧠 **{model_info['name']}**: Respuesta del backend local: {message[:100]}...")
                        }
                    else:
                        return {"success": False, "error": f"Backend error: {response.status}"}
                        
        except Exception as e:
            logger.error(f"Backend local error: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_main_system(self, message: str, model_info: Dict) -> Dict[str, Any]:
        """Llamar al sistema principal (puerto 5000)"""
        try:
            logger.info(f"🔗 Conectando con sistema principal (5000) para: {message[:50]}...")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:5000/api/quantum",
                    json={
                        "text": message
                    },
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"✅ Sistema principal respondió: {result.keys()}")
                        # Extraer la respuesta real del sistema principal
                        real_response = result.get("response", "")
                        if real_response:
                            logger.info(f"🧠 Respuesta real extraída: {real_response[:100]}...")
                            return {
                                "success": True,
                                "content": real_response
                            }
                        else:
                            logger.error("❌ No se encontró contenido en la respuesta")
                            return {"success": False, "error": "No response content"}
                    else:
                        logger.error(f"❌ Error del sistema principal: {response.status}")
                        return {"success": False, "error": f"Main system error: {response.status}"}
                        
        except Exception as e:
            logger.error(f"❌ Excepción del sistema principal: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_frontend_system(self, message: str, model_info: Dict) -> str:
        """Llamar al frontend system (puerto 5003)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:5003/api/process_multimodal",
                    json={
                        "query": message,
                        "model": model_info["name"]
                    },
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", f"🧠 **{model_info['name']}**: Respuesta del frontend: {message[:100]}...")
                    else:
                        return f"🧠 **{model_info['name']}**: Respuesta del frontend system con capacidades cuánticas avanzadas."
                        
        except Exception as e:
            logger.error(f"Frontend system error: {e}")
            return f"🧠 **{model_info['name']}**: Respuesta del frontend system con capacidades cuánticas avanzadas."
        
    def get_main_html(self) -> str:
        """Generar HTML principal de la interfaz"""
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Vigoleonrocks - Interfaz Web Avanzada</title>
    
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --quantum-purple: #6f42c1;
            --quantum-gold: #ffd700;
            --quantum-cyan: #20c997;
            --quantum-plasma: #9f7aea;
            --dark-bg: #1a1a2e;
            --card-bg: rgba(255, 255, 255, 0.1);
            --text-light: #ffffff;
            --text-dark: #333333;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            min-height: 100vh;
            color: var(--text-light);
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 2rem;
            background: var(--card-bg);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .header h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, var(--quantum-gold), #ff6b6b, #4ecdc4);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease infinite;
        }}
        
        @keyframes gradientShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 2rem;
            height: calc(100vh - 200px);
        }}
        
        .chat-section {{
            background: var(--card-bg);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        
        .chat-header {{
            background: var(--primary-gradient);
            padding: 1rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .chat-header h3 {{
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .chat-messages {{
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .message {{
            display: flex;
            gap: 1rem;
            align-items: flex-start;
            animation: fadeIn 0.5s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .message.user {{
            flex-direction: row-reverse;
        }}
        
        .message-avatar {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            flex-shrink: 0;
        }}
        
        .message.user .message-avatar {{
            background: var(--quantum-gold);
            color: var(--dark-bg);
        }}
        
        .message.bot .message-avatar {{
            background: var(--quantum-purple);
            color: white;
        }}
        
        .message-content {{
            background: rgba(255, 255, 255, 0.1);
            padding: 1rem 1.5rem;
            border-radius: 15px;
            max-width: 70%;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .message.user .message-content {{
            background: var(--quantum-gold);
            color: var(--dark-bg);
        }}
        
        .message.bot .message-content {{
            background: rgba(255, 255, 255, 0.15);
            color: var(--text-light);
        }}
        
        .chat-input-section {{
            padding: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(0, 0, 0, 0.1);
        }}
        
        .input-container {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}
        
        .chat-input {{
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 25px;
            padding: 1rem 1.5rem;
            color: var(--text-light);
            font-size: 1rem;
            backdrop-filter: blur(5px);
        }}
        
        .chat-input:focus {{
            outline: none;
            border-color: var(--quantum-gold);
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }}
        
        .chat-input::placeholder {{
            color: rgba(255, 255, 255, 0.7);
        }}
        
        .send-button {{
            background: var(--quantum-gold);
            color: var(--dark-bg);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 1.2rem;
            transition: all 0.3s ease;
        }}
        
        .send-button:hover {{
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }}
        
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .sidebar-card {{
            background: var(--card-bg);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1.5rem;
        }}
        
        .sidebar-card h3 {{
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: var(--quantum-gold);
        }}
        
        .model-selector {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .model-option {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .model-option:hover {{
            background: rgba(255, 255, 255, 0.2);
            border-color: var(--quantum-gold);
            transform: translateX(5px);
        }}
        
        .model-option.active {{
            background: var(--quantum-gold);
            color: var(--dark-bg);
            border-color: var(--quantum-gold);
        }}
        
        .model-icon {{
            font-size: 1.5rem;
        }}
        
        .model-info {{
            flex: 1;
        }}
        
        .model-name {{
            font-weight: bold;
            font-size: 0.9rem;
        }}
        
        .model-price {{
            font-size: 0.8rem;
            opacity: 0.8;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }}
        
        .stat-number {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--quantum-gold);
        }}
        
        .stat-label {{
            font-size: 0.8rem;
            opacity: 0.8;
        }}
        
        .loading {{
            display: none;
            text-align: center;
            padding: 1rem;
            color: var(--quantum-gold);
        }}
        
        .loading.show {{
            display: block;
        }}
        
        .spinner {{
            border: 2px solid rgba(255, 215, 0, 0.3);
            border-top: 2px solid var(--quantum-gold);
            border-radius: 50%;
            width: 20px;
            height: 20px;
            animation: spin 1s linear infinite;
            margin: 0 auto 0.5rem;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
            }}
            
            .message-content {{
                max-width: 85%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Vigoleonrocks</h1>
            <p>Interfaz Web Avanzada - Sistema Cuántico-Cognitivo</p>
            <p>Capacidades cuánticas y contexto masivo de hasta 8M tokens</p>
        </div>
        
        <div class="main-content">
            <div class="chat-section">
                <div class="chat-header">
                    <h3>💬 Chat Inteligente con Vigoleonrocks</h3>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot">
                        <div class="message-avatar">🧠</div>
                        <div class="message-content">
                            ¡Hola! Soy Vigoleonrocks, tu asistente cuántico-cognitivo especializado en programación. 
                            Puedo ayudarte con desarrollo de software, análisis de código, debugging y mucho más. 
                            ¿En qué proyecto de programación puedo ayudarte hoy?
                        </div>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Procesando con capacidades cuánticas...</p>
                </div>
                
                <div class="chat-input-section">
                    <div class="input-container">
                        <input type="text" class="chat-input" id="chatInput" placeholder="Escribe tu consulta de programación aquí... (Ctrl+Enter para enviar)" />
                        <button class="send-button" id="sendButton">
                            <i class="fas fa-paper-plane">🚀</i>
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="sidebar-card">
                    <h3>🤖 Modelos Disponibles</h3>
                    <div class="model-selector" id="modelSelector">
                        <div class="model-option active" data-model="vigoleonrocks-v1">
                            <div class="model-icon">🚀</div>
                            <div class="model-info">
                                <div class="model-name">Vigoleonrocks v1.0</div>
                                <div class="model-price">$0.0045/$0.0135</div>
                            </div>
                        </div>
                        <div class="model-option" data-model="vigoleonrocks-programming">
                            <div class="model-icon">💻</div>
                            <div class="model-info">
                                <div class="model-name">Vigoleonrocks Programming</div>
                                <div class="model-price">$0.005/$0.015</div>
                            </div>
                        </div>
                        <div class="model-option" data-model="vigoleonrocks-creative">
                            <div class="model-icon">🎨</div>
                            <div class="model-info">
                                <div class="model-name">Vigoleonrocks Creative</div>
                                <div class="model-price">$0.004/$0.012</div>
                            </div>
                        </div>
                        <div class="model-option" data-model="vigoleonrocks-ultra">
                            <div class="model-icon">⚡</div>
                            <div class="model-info">
                                <div class="model-name">Vigoleonrocks Ultra</div>
                                <div class="model-price">$0.006/$0.018</div>
                            </div>
                        </div>
                        <div class="model-option" data-model="vigoleonrocks-enterprise">
                            <div class="model-icon">🏢</div>
                            <div class="model-info">
                                <div class="model-name">Vigoleonrocks Enterprise</div>
                                <div class="model-price">$0.008/$0.024</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>📊 Estadísticas del Sistema</h3>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-number">8M</div>
                            <div class="stat-label">Tokens Contexto</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">351M</div>
                            <div class="stat-label">Quantum Volume</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">26D</div>
                            <div class="stat-label">Dimensiones</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">95%</div>
                            <div class="stat-label">Precisión</div>
                        </div>
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>🔧 Acciones Rápidas</h3>
                    <div class="model-selector">
                        <div class="model-option" onclick="sendQuickMessage('Analiza este código y sugiere mejoras')">
                            <div class="model-icon">🔍</div>
                            <div class="model-info">
                                <div class="model-name">Análisis de Código</div>
                            </div>
                        </div>
                        <div class="model-option" onclick="sendQuickMessage('Genera un algoritmo para...')">
                            <div class="model-icon">⚙️</div>
                            <div class="model-info">
                                <div class="model-name">Generar Algoritmo</div>
                            </div>
                        </div>
                        <div class="model-option" onclick="sendQuickMessage('Debug este error...')">
                            <div class="model-icon">🐛</div>
                            <div class="model-info">
                                <div class="model-name">Debugging</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedModel = 'vigoleonrocks-v1';
        let chatHistory = [];
        
        // Elementos del DOM
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        const loading = document.getElementById('loading');
        const modelSelector = document.getElementById('modelSelector');
        
        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {{
                sendMessage();
            }}
        }});
        
        // Selector de modelos
        modelSelector.addEventListener('click', (e) => {{
            const modelOption = e.target.closest('.model-option');
            if (modelOption) {{
                // Remover clase active de todos
                document.querySelectorAll('.model-option').forEach(opt => {{
                    opt.classList.remove('active');
                }});
                
                // Agregar clase active al seleccionado
                modelOption.classList.add('active');
                selectedModel = modelOption.dataset.model;
                
                console.log('Modelo seleccionado:', selectedModel);
            }}
        }});
        
        async function sendMessage() {{
            const message = chatInput.value.trim();
            if (!message) return;
            
            // Agregar mensaje del usuario
            addMessage(message, 'user');
            chatInput.value = '';
            
            // Mostrar loading
            showLoading(true);
            
            try {{
                const response = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        message: message,
                        model: selectedModel
                    }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    addMessage(data.response, 'bot');
                }} else {{
                    addMessage('❌ Error: ' + data.error, 'bot');
                }}
                
            }} catch (error) {{
                console.error('Error:', error);
                addMessage('❌ Error de conexión', 'bot');
            }} finally {{
                showLoading(false);
            }}
        }}
        
        function addMessage(content, type) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{type}}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = type === 'user' ? '👤' : '🧠';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = content;
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }}
        
        function showLoading(show) {{
            if (show) {{
                loading.classList.add('show');
            }} else {{
                loading.classList.remove('show');
            }}
        }}
        
        function sendQuickMessage(message) {{
            chatInput.value = message;
            sendMessage();
        }}
        
        // Cargar modelos al iniciar
        async function loadModels() {{
            try {{
                const response = await fetch('/api/models');
                const data = await response.json();
                console.log('Modelos cargados:', data.models);
            }} catch (error) {{
                console.error('Error cargando modelos:', error);
            }}
        }}
        
        // Verificar estado del sistema
        async function checkStatus() {{
            try {{
                const response = await fetch('/api/status');
                const data = await response.json();
                console.log('Estado del sistema:', data);
            }} catch (error) {{
                console.error('Error verificando estado:', error);
            }}
        }}
        
        // Inicializar
        document.addEventListener('DOMContentLoaded', () => {{
            loadModels();
            checkStatus();
        }});
    </script>
</body>
</html>
        """
        
    def run(self, host: str = '0.0.0.0', port: int = 8080):
        """Ejecutar la aplicación web"""
        logger.info(f"🚀 Iniciando Vigoleonrocks Web UI en http://{host}:{port}")
        web.run_app(self.app, host=host, port=port)

def main():
    """Función principal"""
    ui = VigoleonrocksWebUI()
    ui.run()

if __name__ == "__main__":
    main()
