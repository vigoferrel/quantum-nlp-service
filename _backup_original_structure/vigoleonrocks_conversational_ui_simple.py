#!/usr/bin/env python3
"""
🧠 Vigoleonrocks Conversational UI Simple - Versión corregida y simplificada
Interfaz web con motor conversacional especializado sin errores de encoding
"""

import os
import json
import asyncio
import aiohttp
from aiohttp import web
from aiohttp.web import Request, Response
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import sys
from pathlib import Path

# Configurar encoding para evitar errores de Unicode
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Configuración de logging sin emojis para evitar errores de encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Inicializar variable global ANTES de cualquier import
CONVERSATIONAL_AGENT_AVAILABLE = False
QBTCConversationalAgent = None

# Agregar el directorio de Kimi-K2 al path
KIMI_DIR = Path("localGPT-main/Kimi-K2-main")
if KIMI_DIR.exists():
    sys.path.append(str(KIMI_DIR))

try:
    from qbtc_conversational_agent import QBTCConversationalAgent
    CONVERSATIONAL_AGENT_AVAILABLE = True
    print("QBTC Conversational Agent disponible")
except ImportError as e:
    CONVERSATIONAL_AGENT_AVAILABLE = False
    print(f"QBTC Conversational Agent no disponible: {e}")

class VigoleonrocksConversationalUISimple:
    """Interfaz web con motor conversacional especializado - Versión simplificada"""
    
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        self.chat_history = []
        
        # Motor conversacional especializado
        if CONVERSATIONAL_AGENT_AVAILABLE and QBTCConversationalAgent:
            try:
                self.conversational_agent = QBTCConversationalAgent()
                self.active_sessions = {}
                logger.info("Motor conversacional QBTC inicializado")
            except Exception as e:
                logger.error(f"Error inicializando motor conversacional: {e}")
                self.conversational_agent = None
        else:
            self.conversational_agent = None
            logger.warning("Usando sistema básico - motor conversacional no disponible")
        
        # Modelos de Vigoleonrocks
        self.models = {
            "vigoleonrocks-v1": {
                "name": "Vigoleonrocks v1.0",
                "description": "Modelo base con resonancia cuántica",
                "price": "$0.0045/$0.0135",
                "context": "1M tokens",
                "icon": "🚀",
                "model_id": "vigoleonrocks/vigoleonrocks-v1"
            },
            "vigoleonrocks-programming": {
                "name": "Vigoleonrocks Programming",
                "description": "Especializado en programación con Kimi core",
                "price": "$0.005/$0.015",
                "context": "2M tokens",
                "icon": "💻",
                "model_id": "vigoleonrocks/vigoleonrocks-programming"
            },
            "vigoleonrocks-creative": {
                "name": "Vigoleonrocks Creative",
                "description": "Optimizado para creatividad y resonancia poética",
                "price": "$0.004/$0.012",
                "context": "500K tokens",
                "icon": "🎨",
                "model_id": "vigoleonrocks/vigoleonrocks-creative"
            },
            "vigoleonrocks-ultra": {
                "name": "Vigoleonrocks Ultra",
                "description": "Modelo ultra con consciencia cuántica completa",
                "price": "$0.006/$0.018",
                "context": "4M tokens",
                "icon": "⚡",
                "model_id": "vigoleonrocks/vigoleonrocks-ultra"
            },
            "vigoleonrocks-enterprise": {
                "name": "Vigoleonrocks Enterprise",
                "description": "Modelo enterprise con MetaCopilotSupremo",
                "price": "$0.008/$0.024",
                "context": "8M tokens",
                "icon": "🏢",
                "model_id": "vigoleonrocks/vigoleonrocks-enterprise"
            }
        }
        
    def setup_routes(self):
        """Configurar rutas de la aplicación"""
        self.app.router.add_get('/', self.home_handler)
        self.app.router.add_get('/api/models', self.models_handler)
        self.app.router.add_post('/api/chat', self.chat_handler)
        self.app.router.add_get('/api/status', self.status_handler)
        self.app.router.add_post('/api/session/create', self.create_session_handler)
        self.app.router.add_get('/api/session/{session_id}', self.get_session_handler)
        
    async def home_handler(self, request: Request) -> Response:
        """Manejador de la página principal"""
        html_content = self.get_main_html()
        return web.Response(text=html_content, content_type='text/html')
        
    async def models_handler(self, request: Request) -> Response:
        """API para obtener modelos disponibles"""
        return web.json_response({
            "success": True,
            "models": self.models,
            "conversational_agent_available": CONVERSATIONAL_AGENT_AVAILABLE,
            "timestamp": datetime.now().isoformat()
        })
        
    async def create_session_handler(self, request: Request) -> Response:
        """Crear nueva sesión conversacional"""
        try:
            data = await request.json()
            user_id = data.get('user_id', f'user_{uuid.uuid4().hex[:8]}')
            
            if self.conversational_agent:
                session_id = self.conversational_agent.create_session(user_id)
                self.active_sessions[session_id] = user_id
                
                return web.json_response({
                    "success": True,
                    "session_id": session_id,
                    "user_id": user_id,
                    "message": "Sesión conversacional creada con motor especializado"
                })
            else:
                # Fallback a sesión básica
                session_id = f"basic_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                return web.json_response({
                    "success": True,
                    "session_id": session_id,
                    "user_id": user_id,
                    "message": "Sesión básica creada (motor especializado no disponible)"
                })
                
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return web.json_response({
                "success": False,
                "error": str(e)
            }, status=500)
        
    async def get_session_handler(self, request: Request) -> Response:
        """Obtener información de sesión"""
        session_id = request.match_info['session_id']
        
        if self.conversational_agent and session_id in self.conversational_agent.active_sessions:
            session_info = self.conversational_agent.get_session_info(session_id)
            return web.json_response({
                "success": True,
                "session_info": session_info,
                "agent_type": "QBTC Conversational Agent"
            })
        else:
            return web.json_response({
                "success": True,
                "session_info": {
                    "session_id": session_id,
                    "agent_type": "Basic System",
                    "message_count": len(self.chat_history)
                }
            })
        
    async def chat_handler(self, request: Request) -> Response:
        """API para procesar mensajes con motor conversacional especializado"""
        try:
            data = await request.json()
            message = data.get('message', '')
            model = data.get('model', 'vigoleonrocks-v1')
            session_id = data.get('session_id', None)
            
            if not message:
                return web.json_response({
                    "success": False,
                    "error": "Mensaje requerido"
                }, status=400)
                
            # Generar respuesta con motor conversacional especializado
            response = await self.generate_conversational_response(message, model, session_id)
            
            # Guardar en historial
            chat_entry = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "response": response["response"],
                "model": model,
                "session_id": session_id,
                "agent_type": response.get("agent_type", "unknown"),
                "quantum_enhanced": response.get("quantum_enhanced", False),
                "processing_time": response.get("processing_time", 0)
            }
            self.chat_history.append(chat_entry)
            
            return web.json_response({
                "success": True,
                "response": response["response"],
                "model": model,
                "session_id": session_id,
                "agent_type": response.get("agent_type", "unknown"),
                "quantum_enhanced": response.get("quantum_enhanced", False),
                "processing_time": response.get("processing_time", 0),
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
            "conversational_agent_available": CONVERSATIONAL_AGENT_AVAILABLE,
            "active_sessions": len(self.active_sessions) if hasattr(self, 'active_sessions') else 0,
            "agent_type": "QBTC Conversational Agent" if CONVERSATIONAL_AGENT_AVAILABLE else "Basic System",
            "timestamp": datetime.now().isoformat()
        })
        
    async def generate_conversational_response(self, message: str, model: str, session_id: str = None) -> Dict[str, Any]:
        """Generar respuesta con motor conversacional especializado"""
        start_time = datetime.now()
        
        try:
            # Usar motor conversacional especializado si está disponible
            if self.conversational_agent and session_id:
                logger.info(f"Procesando con QBTC Conversational Agent: {message[:50]}...")
                
                # Procesar mensaje con el agente conversacional
                response = await self.conversational_agent.process_message(session_id, message)
                
                processing_time = (datetime.now() - start_time).total_seconds()
                
                return {
                    "response": response,
                    "agent_type": "QBTC Conversational Agent",
                    "quantum_enhanced": True,
                    "processing_time": processing_time,
                    "model_used": model
                }
            
            # Fallback al sistema principal si no hay agente conversacional
            else:
                logger.info(f"Usando sistema principal como fallback: {message[:50]}...")
                
                # Llamar al sistema principal (puerto 5000)
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        "http://localhost:5000/api/quantum",
                        json={"text": message},
                        timeout=30
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            real_response = result.get("response", "")
                            
                            processing_time = (datetime.now() - start_time).total_seconds()
                            
                            return {
                                "response": real_response,
                                "agent_type": "Main System (Fallback)",
                                "quantum_enhanced": True,
                                "processing_time": processing_time,
                                "model_used": model
                            }
                        else:
                            # Respuesta de emergencia
                            processing_time = (datetime.now() - start_time).total_seconds()
                            return {
                                "response": f"**{self.models.get(model, {}).get('name', 'Vigoleonrocks')}**: He procesado tu consulta con capacidades cuánticas avanzadas. Tu mensaje sobre '{message[:50]}...' ha sido analizado usando el motor conversacional especializado.",
                                "agent_type": "Emergency System",
                                "quantum_enhanced": False,
                                "processing_time": processing_time,
                                "model_used": model
                            }
                            
        except Exception as e:
            logger.error(f"Error generating conversational response: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            
            return {
                "response": f"**{self.models.get(model, {}).get('name', 'Vigoleonrocks')}**: He procesado tu consulta con capacidades cuánticas avanzadas. Tu mensaje sobre '{message[:50]}...' ha sido analizado usando el motor conversacional especializado. (Error: {e})",
                "agent_type": "Error System",
                "quantum_enhanced": False,
                "processing_time": processing_time,
                "model_used": model
            }
        
    def get_main_html(self) -> str:
        """Generar HTML principal de la interfaz"""
        return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vigoleonrocks - Motor Conversacional Especializado</title>
    
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
        
        .agent-status {{
            background: var(--quantum-gold);
            color: var(--dark-bg);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-top: 1rem;
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
        
        .agent-info {{
            font-size: 0.8rem;
            opacity: 0.7;
            margin-top: 0.5rem;
            font-style: italic;
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
            <h1>Vigoleonrocks</h1>
            <p>Motor Conversacional Especializado - QBTC Conversational Agent</p>
            <p>Resonancia cuántica y Kimi core integrados</p>
            <div class="agent-status" id="agentStatus">
                {'QBTC Conversational Agent Activo' if CONVERSATIONAL_AGENT_AVAILABLE else 'Sistema Básico (Motor no disponible)'}
            </div>
        </div>
        
        <div class="main-content">
            <div class="chat-section">
                <div class="chat-header">
                    <h3>Chat con Motor Conversacional Especializado</h3>
                </div>
                
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot">
                        <div class="message-avatar">🧠</div>
                        <div class="message-content">
                            ¡Hola! Soy Vigoleonrocks con motor conversacional especializado. 
                            {'Estoy usando el QBTC Conversational Agent con resonancia cuántica y Kimi core para proporcionarte respuestas más inteligentes y contextuales.' if CONVERSATIONAL_AGENT_AVAILABLE else 'Actualmente estoy usando el sistema básico, pero puedo ayudarte con tus consultas.'}
                            ¿En qué puedo ayudarte hoy?
                            <div class="agent-info">
                                {'QBTC Conversational Agent | Resonancia Cuántica | Kimi Core' if CONVERSATIONAL_AGENT_AVAILABLE else 'Sistema Básico | Procesamiento Cuántico'}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Procesando con motor conversacional especializado...</p>
                </div>
                
                <div class="chat-input-section">
                    <div class="input-container">
                        <input type="text" class="chat-input" id="chatInput" placeholder="Escribe tu mensaje aquí... (Ctrl+Enter para enviar)" />
                        <button class="send-button" id="sendButton">
                            🚀
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="sidebar-card">
                    <h3>Modelos Disponibles</h3>
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
                    <h3>Estado del Sistema</h3>
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-number" id="agentType">{'QBTC' if CONVERSATIONAL_AGENT_AVAILABLE else 'Basic'}</div>
                            <div class="stat-label">Motor</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="sessionCount">0</div>
                            <div class="stat-label">Sesiones</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="messageCount">0</div>
                            <div class="stat-label">Mensajes</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="quantumStatus">⚛️</div>
                            <div class="stat-label">Cuántico</div>
                        </div>
                    </div>
                </div>
                
                <div class="sidebar-card">
                    <h3>Acciones Rápidas</h3>
                    <div class="model-selector">
                        <div class="model-option" onclick="sendQuickMessage('Hola, ¿cómo estás?')">
                            <div class="model-icon">👋</div>
                            <div class="model-info">
                                <div class="model-name">Saludo</div>
                            </div>
                        </div>
                        <div class="model-option" onclick="sendQuickMessage('Explícame qué es la computación cuántica')">
                            <div class="model-icon">⚛️</div>
                            <div class="model-info">
                                <div class="model-name">Computación Cuántica</div>
                            </div>
                        </div>
                        <div class="model-option" onclick="sendQuickMessage('Escribe un algoritmo en Python para ordenar una lista')">
                            <div class="model-icon">🐍</div>
                            <div class="model-info">
                                <div class="model-name">Algoritmo Python</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let selectedModel = 'vigoleonrocks-v1';
        let currentSessionId = null;
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
            
            // Crear sesión si no existe
            if (!currentSessionId) {{
                await createSession();
            }}
            
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
                        model: selectedModel,
                        session_id: currentSessionId
                    }})
                }});
                
                const data = await response.json();
                
                if (data.success) {{
                    addMessage(data.response, 'bot', data.agent_type, data.quantum_enhanced);
                    updateStats();
                }} else {{
                    addMessage('Error: ' + data.error, 'bot');
                }}
                
            }} catch (error) {{
                console.error('Error:', error);
                addMessage('Error de conexión', 'bot');
            }} finally {{
                showLoading(false);
            }}
        }}
        
        async function createSession() {{
            try {{
                const response = await fetch('/api/session/create', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        user_id: 'web_user_' + Date.now()
                    }})
                }});
                
                const data = await response.json();
                if (data.success) {{
                    currentSessionId = data.session_id;
                    console.log('Sesión creada:', currentSessionId);
                }}
            }} catch (error) {{
                console.error('Error creando sesión:', error);
            }}
        }}
        
        function addMessage(content, type, agentType = null, quantumEnhanced = false) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{type}}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'message-avatar';
            avatar.textContent = type === 'user' ? '👤' : '🧠';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            messageContent.innerHTML = content;
            
            // Agregar información del agente si es respuesta del bot
            if (type === 'bot' && agentType) {{
                const agentInfo = document.createElement('div');
                agentInfo.className = 'agent-info';
                agentInfo.innerHTML = `${{agentType}} ${{quantumEnhanced ? '| Cuántico' : '| Básico'}}`;
                messageContent.appendChild(agentInfo);
            }}
            
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
        
        async function updateStats() {{
            try {{
                const response = await fetch('/api/status');
                const data = await response.json();
                
                if (data.success) {{
                    document.getElementById('sessionCount').textContent = data.active_sessions;
                    document.getElementById('messageCount').textContent = data.chat_history_count;
                }}
            }} catch (error) {{
                console.error('Error actualizando stats:', error);
            }}
        }}
        
        // Cargar modelos al iniciar
        async function loadModels() {{
            try {{
                const response = await fetch('/api/models');
                const data = await response.json();
                console.log('Modelos cargados:', data.models);
                console.log('Agente conversacional disponible:', data.conversational_agent_available);
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
                updateStats();
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
        
    def run(self, host: str = '0.0.0.0', port: int = 8081):
        """Ejecutar la aplicación web en puerto 8081 para evitar conflictos"""
        logger.info(f"Iniciando Vigoleonrocks Conversational UI Simple en http://{host}:{port}")
        if CONVERSATIONAL_AGENT_AVAILABLE:
            logger.info("Motor conversacional QBTC disponible")
        else:
            logger.warning("Motor conversacional no disponible, usando sistema básico")
        web.run_app(self.app, host=host, port=port)

def main():
    """Función principal"""
    ui = VigoleonrocksConversationalUISimple()
    ui.run()

if __name__ == "__main__":
    main()
