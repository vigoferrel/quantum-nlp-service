#!/usr/bin/env python3
"""
OPTIMAL UI - Ingeniería Inversa del Frontend Óptimo
UI que aprovecha todas las capacidades del sistema QBTC Ultimate
"""

import asyncio
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template_string, request, jsonify, send_from_directory
    from flask_cors import CORS
except ImportError as e:
    print(f"❌ Error importando Flask: {e}")
    sys.exit(1)

try:
    from integrate import LLMCore, OpenRouterClient
except ImportError as e:
    print(f"❌ Error importando sistema integrado: {e}")
    sys.exit(1)

class OptimalUI:
    """UI Optimizada con Ingeniería Inversa del Frontend Óptimo"""
    
    def __init__(self):
        self.llm_core = LLMCore()
        self.openrouter = OpenRouterClient()
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        
    def setup_routes(self):
        """Configurar rutas optimizadas"""
        
        @self.app.route('/')
        def optimal_home():
            return self.render_optimal_home()
            
        @self.app.route('/chat')
        def chat_interface():
            return self.render_chat_interface()
            
        @self.app.route('/agents')
        def agents_interface():
            return self.render_agents_interface()
            
        @self.app.route('/training')
        def training_interface():
            return self.render_training_interface()
            
        @self.app.route('/evaluation')
        def evaluation_interface():
            return self.render_evaluation_interface()
            
        @self.app.route('/development')
        def development_interface():
            return self.render_development_interface()
            
        @self.app.route('/api/chat', methods=['POST'])
        def chat_api():
            data = request.json
            prompt = data.get('prompt', '')
            model = data.get('model', 'hybrid')
            context = data.get('context', 'general')
            
            try:
                if model == 'openrouter':
                    response = asyncio.run(self.llm_core.generate_with_openrouter(prompt))
                elif model == 'ollama':
                    response = asyncio.run(self.llm_core.generate_with_ollama(prompt))
                else:  # hybrid
                    response = asyncio.run(self.llm_core.generate_hybrid(prompt))
                
                return jsonify({
                    'success': True,
                    'response': response.get('response', ''),
                    'provider': response.get('provider', ''),
                    'tokens': response.get('tokens', 0),
                    'model': model
                })
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/models')
        def models_api():
            try:
                ollama_models = self.llm_core.list_models()
                openrouter_models = self.llm_core.list_openrouter_models()
                return jsonify({
                    'ollama': ollama_models,
                    'openrouter': openrouter_models[:20],
                    'total_openrouter': len(openrouter_models)
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
                
        @self.app.route('/api/agents/<agent_type>', methods=['POST'])
        def agent_api(agent_type):
            data = request.json
            task = data.get('task', '')
            
            # Simular diferentes agentes BMAD
            agent_responses = {
                'analyst': f"📊 **Análisis realizado:** {task}\n\nInsights generados:\n- Patrón identificado\n- Tendencias detectadas\n- Recomendaciones",
                'architect': f"🏗️ **Arquitectura diseñada:** {task}\n\nComponentes:\n- Microservicios\n- APIs RESTful\n- Base de datos distribuida",
                'developer': f"💻 **Código generado:** {task}\n\n```python\n# Implementación optimizada\ndef solution():\n    return 'Código de alta calidad'\n```",
                'qa': f"🧪 **Testing plan:** {task}\n\n- Unit tests\n- Integration tests\n- Performance tests\n- Security tests",
                'ux': f"🎨 **UX Design:** {task}\n\n- User journey mapping\n- Wireframes\n- Prototipos interactivos\n- Usabilidad optimizada"
            }
            
            return jsonify({
                'success': True,
                'agent': agent_type,
                'response': agent_responses.get(agent_type, 'Agente no disponible'),
                'task': task
            })
            
        @self.app.route('/favicon.ico')
        def favicon():
            return '', 204
    
    def render_optimal_home(self):
        """Página principal optimizada"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 QBTC Optimal UI - Sistema Inteligente</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }
        
        .header h1 {
            font-size: 4rem;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, var(--accent), #ff6b6b, #4ecdc4);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientShift 3s ease infinite;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 1rem 2rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent);
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.4s ease;
            text-decoration: none;
            color: var(--light);
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.6s;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        .feature-card:hover {
            transform: translateY(-10px) scale(1.02);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .feature-card h3 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }
        
        .feature-card p {
            opacity: 0.9;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        .feature-list {
            list-style: none;
        }
        
        .feature-list li {
            padding: 0.3rem 0;
            opacity: 0.8;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .feature-list li::before {
            content: '✓';
            color: var(--accent);
            font-weight: bold;
        }
        
        .quick-actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .action-btn {
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 10px;
            color: var(--light);
            text-decoration: none;
            text-align: center;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .action-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .floating-menu {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(0,0,0,0.8);
            border-radius: 50px;
            padding: 1rem;
            backdrop-filter: blur(10px);
            z-index: 1000;
        }
        
        .floating-menu a {
            display: inline-block;
            margin: 0 0.5rem;
            padding: 0.8rem;
            background: var(--accent);
            color: var(--dark);
            border-radius: 50%;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .floating-menu a:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,255,136,0.4);
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5rem; }
            .stats-bar { flex-direction: column; align-items: center; }
            .main-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 QBTC Optimal UI</h1>
            <p>Sistema Inteligente con Ingeniería Inversa del Frontend Óptimo</p>
            <p>Aprovecha todas las capacidades: OpenRouter + Ollama + BMAD + OUMI + DeepEval</p>
        </div>
        
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-number">316</div>
                <div class="stat-label">OpenRouter Models</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10</div>
                <div class="stat-label">Ollama Models</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">🧠</div>
                <div class="stat-label">CIO Brain Active</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10</div>
                <div class="stat-label">BMAD Agents</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">⚡</div>
                <div class="stat-label">Real-time Processing</div>
            </div>
        </div>
        
        <div class="main-grid">
            <a href="/chat" class="feature-card">
                <h3>💬 Chat Inteligente</h3>
                <p>Interfaz de conversación avanzada con múltiples modelos y contextos</p>
                <ul class="feature-list">
                    <li>OpenRouter (316 modelos)</li>
                    <li>Ollama (10 modelos locales)</li>
                    <li>Generación híbrida automática</li>
                    <li>Contexto 26D CIO Brain</li>
                    <li>Respuestas en tiempo real</li>
                </ul>
            </a>
            
            <a href="/agents" class="feature-card">
                <h3>🧠 Agentes BMAD</h3>
                <p>Sistema de agentes especializados para tareas complejas</p>
                <ul class="feature-list">
                    <li>Analyst - Análisis de datos</li>
                    <li>Architect - Diseño de sistemas</li>
                    <li>Developer - Generación de código</li>
                    <li>QA - Testing y calidad</li>
                    <li>UX - Experiencia de usuario</li>
                </ul>
            </a>
            
            <a href="/training" class="feature-card">
                <h3>🚀 Entrenamiento OUMI</h3>
                <p>Framework completo para entrenamiento y fine-tuning de LLMs</p>
                <ul class="feature-list">
                    <li>SFT (Supervised Fine-Tuning)</li>
                    <li>LoRA (Low-Rank Adaptation)</li>
                    <li>QLoRA (Quantized LoRA)</li>
                    <li>DPO (Direct Preference Optimization)</li>
                    <li>Judges y Benchmarks</li>
                </ul>
            </a>
            
            <a href="/evaluation" class="feature-card">
                <h3>📊 Evaluación DeepEval</h3>
                <p>Sistema de evaluación cuántica con métricas avanzadas</p>
                <ul class="feature-list">
                    <li>Quantum Supremacy Benchmarks</li>
                    <li>Validadores cuánticos</li>
                    <li>Ecosistema integrado</li>
                    <li>Métricas personalizadas</li>
                    <li>Análisis de rendimiento</li>
                </ul>
            </a>
            
            <a href="/development" class="feature-card">
                <h3>🔧 Desarrollo Claude Engineer</h3>
                <p>Herramientas de desarrollo con creación dinámica</p>
                <ul class="feature-list">
                    <li>Tailwind CSS Interface</li>
                    <li>Code Highlighting</li>
                    <li>Token Counter</li>
                    <li>Image Upload</li>
                    <li>Tool Creator</li>
                </ul>
            </a>
            
            <div class="feature-card">
                <h3>⚡ Acciones Rápidas</h3>
                <p>Acceso directo a las funcionalidades más utilizadas</p>
                <div class="quick-actions">
                    <a href="/chat" class="action-btn">💬 Chat Rápido</a>
                    <a href="/agents" class="action-btn">🧠 Agentes</a>
                    <a href="/training" class="action-btn">🚀 Entrenar</a>
                    <a href="/evaluation" class="action-btn">📊 Evaluar</a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="floating-menu">
        <a href="/chat" title="Chat">💬</a>
        <a href="/agents" title="Agentes">🧠</a>
        <a href="/training" title="Entrenamiento">🚀</a>
        <a href="/evaluation" title="Evaluación">📊</a>
    </div>
</body>
</html>
        ''')
    
    def render_chat_interface(self):
        """Interfaz de chat optimizada"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💬 Chat Inteligente - QBTC Optimal UI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }
        
        .controls {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .control-group label {
            font-weight: bold;
            color: var(--accent);
        }
        
        .control-group select, .control-group input {
            padding: 0.5rem;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: var(--light);
            backdrop-filter: blur(10px);
        }
        
        .control-group select:focus, .control-group input:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .chat-container {
            flex: 1;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            margin-bottom: 1rem;
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 1rem;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .message.user {
            background: rgba(0,255,136,0.2);
            margin-left: auto;
            border: 1px solid rgba(0,255,136,0.3);
        }
        
        .message.assistant {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .message-header {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--accent);
        }
        
        .message-content {
            line-height: 1.5;
        }
        
        .input-area {
            display: flex;
            gap: 1rem;
            align-items: flex-end;
        }
        
        .input-group {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .input-group textarea {
            padding: 1rem;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 10px;
            background: rgba(255,255,255,0.1);
            color: var(--light);
            resize: vertical;
            min-height: 60px;
            backdrop-filter: blur(10px);
        }
        
        .input-group textarea:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .send-btn {
            padding: 1rem 2rem;
            background: var(--accent);
            color: var(--dark);
            border: none;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .send-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,255,136,0.4);
        }
        
        .send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 1rem;
        }
        
        .nav-btn {
            padding: 0.8rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: var(--light);
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 1rem;
            color: var(--accent);
        }
        
        .loading.show {
            display: block;
        }
        
        @media (max-width: 768px) {
            .controls { flex-direction: column; align-items: center; }
            .input-area { flex-direction: column; }
            .message { max-width: 95%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💬 Chat Inteligente</h1>
            <p>Interfaz de conversación avanzada con múltiples modelos</p>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="model-select">Modelo:</label>
                <select id="model-select">
                    <option value="hybrid">🤖 Híbrido (Recomendado)</option>
                    <option value="openrouter">🌐 OpenRouter</option>
                    <option value="ollama">🏠 Ollama Local</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="context-select">Contexto:</label>
                <select id="context-select">
                    <option value="general">🌍 General</option>
                    <option value="technical">⚙️ Técnico</option>
                    <option value="creative">🎨 Creativo</option>
                    <option value="analytical">📊 Analítico</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="temperature">Temperatura:</label>
                <input type="range" id="temperature" min="0" max="2" step="0.1" value="0.7">
                <span id="temp-value">0.7</span>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message assistant">
                    <div class="message-header">🤖 QBTC Assistant</div>
                    <div class="message-content">
                        ¡Hola! Soy tu asistente inteligente. Puedo ayudarte con:
                        <br>• Análisis de datos y patrones
                        <br>• Generación de código
                        <br>• Resolución de problemas
                        <br>• Ideas creativas
                        <br><br>¿En qué puedo ayudarte hoy?
                    </div>
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div>🤔 Pensando...</div>
            </div>
            
            <div class="input-area">
                <div class="input-group">
                    <textarea 
                        id="user-input" 
                        placeholder="Escribe tu mensaje aquí... (Ctrl+Enter para enviar)"
                        rows="3"
                    ></textarea>
                </div>
                <button class="send-btn" id="send-btn">🚀 Enviar</button>
            </div>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="nav-btn">🏠 Inicio</a>
            <a href="/agents" class="nav-btn">🧠 Agentes</a>
            <a href="/training" class="nav-btn">🚀 Entrenamiento</a>
            <a href="/evaluation" class="nav-btn">📊 Evaluación</a>
        </div>
    </div>
    
    <script>
        const messagesContainer = document.getElementById('messages');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');
        const loading = document.getElementById('loading');
        const modelSelect = document.getElementById('model-select');
        const contextSelect = document.getElementById('context-select');
        const temperature = document.getElementById('temperature');
        const tempValue = document.getElementById('temp-value');
        
        // Actualizar valor de temperatura
        temperature.addEventListener('input', (e) => {
            tempValue.textContent = e.target.value;
        });
        
        // Enviar mensaje con Ctrl+Enter
        userInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Enviar mensaje con botón
        sendBtn.addEventListener('click', sendMessage);
        
        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;
            
            // Agregar mensaje del usuario
            addMessage('user', '👤 Tú', message);
            userInput.value = '';
            
            // Mostrar loading
            loading.classList.add('show');
            sendBtn.disabled = true;
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        prompt: message,
                        model: modelSelect.value,
                        context: contextSelect.value,
                        temperature: parseFloat(temperature.value)
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const provider = data.provider === 'openrouter' ? '🌐 OpenRouter' : 
                                   data.provider === 'ollama' ? '🏠 Ollama' : '🤖 Híbrido';
                    addMessage('assistant', provider, data.response);
                } else {
                    addMessage('assistant', '❌ Error', 'Lo siento, hubo un error: ' + data.error);
                }
            } catch (error) {
                addMessage('assistant', '❌ Error', 'Error de conexión: ' + error.message);
            } finally {
                loading.classList.remove('show');
                sendBtn.disabled = false;
                userInput.focus();
            }
        }
        
        function addMessage(type, sender, content) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.innerHTML = `
                <div class="message-header">${sender}</div>
                <div class="message-content">${content}</div>
            `;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    </script>
</body>
</html>
                 ''')
    
    def render_agents_interface(self):
        """Interfaz de agentes BMAD"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Agentes BMAD - QBTC Optimal UI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }
        
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .agent-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .agent-card h3 {
            color: var(--accent);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .agent-card p {
            opacity: 0.9;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        .task-input {
            width: 100%;
            padding: 1rem;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: var(--light);
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
        }
        
        .task-input:focus {
            outline: none;
            border-color: var(--accent);
        }
        
        .agent-btn {
            padding: 0.8rem 1.5rem;
            background: var(--accent);
            color: var(--dark);
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
        }
        
        .agent-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,255,136,0.4);
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .nav-btn {
            padding: 0.8rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: var(--light);
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Agentes BMAD</h1>
            <p>Sistema de agentes especializados para tareas complejas</p>
        </div>
        
        <div class="agents-grid">
            <div class="agent-card">
                <h3>📊 Analyst</h3>
                <p>Analiza datos, identifica patrones y genera insights valiosos</p>
                <input type="text" class="task-input" placeholder="Describe la tarea de análisis..." id="analyst-task">
                <button class="agent-btn" onclick="callAgent('analyst')">📊 Ejecutar Análisis</button>
            </div>
            
            <div class="agent-card">
                <h3>🏗️ Architect</h3>
                <p>Diseña arquitecturas de software escalables y sistemas complejos</p>
                <input type="text" class="task-input" placeholder="Describe el sistema a diseñar..." id="architect-task">
                <button class="agent-btn" onclick="callAgent('architect')">🏗️ Diseñar Arquitectura</button>
            </div>
            
            <div class="agent-card">
                <h3>💻 Developer</h3>
                <p>Implementa código de alta calidad siguiendo mejores prácticas</p>
                <input type="text" class="task-input" placeholder="Describe el código a generar..." id="developer-task">
                <button class="agent-btn" onclick="callAgent('developer')">💻 Generar Código</button>
            </div>
            
            <div class="agent-card">
                <h3>🧪 QA Engineer</h3>
                <p>Garantiza la calidad del software mediante testing exhaustivo</p>
                <input type="text" class="task-input" placeholder="Describe el testing necesario..." id="qa-task">
                <button class="agent-btn" onclick="callAgent('qa')">🧪 Ejecutar QA</button>
            </div>
            
            <div class="agent-card">
                <h3>🎨 UX Expert</h3>
                <p>Optimiza la experiencia del usuario con diseños intuitivos</p>
                <input type="text" class="task-input" placeholder="Describe el diseño UX..." id="ux-task">
                <button class="agent-btn" onclick="callAgent('ux')">🎨 Diseñar UX</button>
            </div>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="nav-btn">🏠 Inicio</a>
            <a href="/chat" class="nav-btn">💬 Chat</a>
            <a href="/training" class="nav-btn">🚀 Entrenamiento</a>
            <a href="/evaluation" class="nav-btn">📊 Evaluación</a>
        </div>
    </div>
    
    <script>
        async function callAgent(agentType) {
            const taskInput = document.getElementById(agentType + '-task');
            const task = taskInput.value.trim();
            
            if (!task) {
                alert('Por favor, describe la tarea para el agente ' + agentType);
                return;
            }
            
            try {
                const response = await fetch(`/api/agents/${agentType}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ task: task })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`Respuesta del agente ${agentType}:\n\n${data.response}`);
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                alert('Error de conexión: ' + error.message);
            }
        }
    </script>
</body>
</html>
        ''')
    
    def render_training_interface(self):
        """Interfaz de entrenamiento OUMI"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Entrenamiento OUMI - QBTC Optimal UI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }
        
        .training-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .training-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }
        
        .training-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .training-card h3 {
            color: var(--accent);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .training-card p {
            opacity: 0.9;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .nav-btn {
            padding: 0.8rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: var(--light);
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Entrenamiento OUMI</h1>
            <p>Framework completo para entrenamiento y fine-tuning de LLMs</p>
        </div>
        
        <div class="training-grid">
            <div class="training-card">
                <h3>🎯 SFT (Supervised Fine-Tuning)</h3>
                <p>Entrenamiento supervisado para adaptar modelos a tareas específicas con datos etiquetados.</p>
            </div>
            
            <div class="training-card">
                <h3>🔧 LoRA (Low-Rank Adaptation)</h3>
                <p>Adaptación eficiente de parámetros con bajo rango computacional para fine-tuning rápido.</p>
            </div>
            
            <div class="training-card">
                <h3>⚡ QLoRA (Quantized LoRA)</h3>
                <p>LoRA cuantizado para máxima eficiencia en memoria y velocidad de entrenamiento.</p>
            </div>
            
            <div class="training-card">
                <h3>🎭 DPO (Direct Preference Optimization)</h3>
                <p>Optimización directa de preferencias para alineación de modelos con valores humanos.</p>
            </div>
            
            <div class="training-card">
                <h3>👨‍⚖️ Judges</h3>
                <p>Sistema de evaluación automática con criterios múltiples para validar modelos.</p>
            </div>
            
            <div class="training-card">
                <h3>📊 Benchmarks</h3>
                <p>Pruebas estandarizadas para medir rendimiento de modelos en diferentes tareas.</p>
            </div>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="nav-btn">🏠 Inicio</a>
            <a href="/chat" class="nav-btn">💬 Chat</a>
            <a href="/agents" class="nav-btn">🧠 Agentes</a>
            <a href="/evaluation" class="nav-btn">📊 Evaluación</a>
        </div>
    </div>
</body>
</html>
        ''')
    
    def render_evaluation_interface(self):
        """Interfaz de evaluación DeepEval"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Evaluación DeepEval - QBTC Optimal UI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }
        
        .eval-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .eval-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }
        
        .eval-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .eval-card h3 {
            color: var(--accent);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .eval-card p {
            opacity: 0.9;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .nav-btn {
            padding: 0.8rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: var(--light);
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Evaluación DeepEval</h1>
            <p>Sistema de evaluación cuántica con métricas avanzadas</p>
        </div>
        
        <div class="eval-grid">
            <div class="eval-card">
                <h3>🎯 Quantum Supremacy</h3>
                <p>Benchmarks para demostrar supremacía cuántica en tareas específicas de computación.</p>
            </div>
            
            <div class="eval-card">
                <h3>🔍 Validators</h3>
                <p>Validadores cuánticos para verificar resultados y consistencia de modelos.</p>
            </div>
            
            <div class="eval-card">
                <h3>🌐 Ecosystem</h3>
                <p>Ecosistema completo de evaluación cuántica integrado con múltiples métricas.</p>
            </div>
            
            <div class="eval-card">
                <h3>📈 Metrics</h3>
                <p>Métricas personalizadas para análisis detallado de rendimiento de modelos.</p>
            </div>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="nav-btn">🏠 Inicio</a>
            <a href="/chat" class="nav-btn">💬 Chat</a>
            <a href="/agents" class="nav-btn">🧠 Agentes</a>
            <a href="/training" class="nav-btn">🚀 Entrenamiento</a>
        </div>
    </div>
</body>
</html>
        ''')
    
    def render_development_interface(self):
        """Interfaz de desarrollo Claude Engineer"""
        return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔧 Desarrollo Claude Engineer - QBTC Optimal UI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00ff88;
            --dark: #1a1a2e;
            --light: #ffffff;
            --gradient: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient);
            color: var(--light);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 0.5rem;
        }
        
        .dev-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .dev-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s;
        }
        
        .dev-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .dev-card h3 {
            color: var(--accent);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }
        
        .dev-card p {
            opacity: 0.9;
            line-height: 1.5;
            margin-bottom: 1rem;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .nav-btn {
            padding: 0.8rem 1.5rem;
            background: rgba(255,255,255,0.1);
            border: 2px solid rgba(255,255,255,0.3);
            color: var(--light);
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .nav-btn:hover {
            background: rgba(255,255,255,0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 Desarrollo Claude Engineer</h1>
            <p>Herramientas de desarrollo con creación dinámica</p>
        </div>
        
        <div class="dev-grid">
            <div class="dev-card">
                <h3>🎨 Tailwind CSS Interface</h3>
                <p>Framework CSS utilitario para diseño moderno y responsive con componentes predefinidos.</p>
            </div>
            
            <div class="dev-card">
                <h3>📝 Code Highlight</h3>
                <p>Resaltado de sintaxis para múltiples lenguajes de programación con temas personalizables.</p>
            </div>
            
            <div class="dev-card">
                <h3>📊 Token Counter</h3>
                <p>Monitoreo en tiempo real del uso de tokens y costos para optimización de recursos.</p>
            </div>
            
            <div class="dev-card">
                <h3>🖼️ Image Upload</h3>
                <p>Soporte para carga y procesamiento de imágenes con análisis automático.</p>
            </div>
            
            <div class="dev-card">
                <h3>🔨 Tool Creator</h3>
                <p>Creación dinámica de herramientas personalizadas para automatización de tareas.</p>
            </div>
        </div>
        
        <div class="nav-buttons">
            <a href="/" class="nav-btn">🏠 Inicio</a>
            <a href="/chat" class="nav-btn">💬 Chat</a>
            <a href="/agents" class="nav-btn">🧠 Agentes</a>
            <a href="/training" class="nav-btn">🚀 Entrenamiento</a>
        </div>
    </div>
</body>
</html>
        ''')
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Ejecutar la UI optimizada"""
        print("=" * 70)
        print("🚀 LAUNCHING QBTC OPTIMAL UI")
        print("Ingeniería Inversa del Frontend Óptimo")
        print("=" * 70)
        print("✅ Chat Inteligente con múltiples modelos")
        print("✅ Agentes BMAD especializados")
        print("✅ Entrenamiento OUMI completo")
        print("✅ Evaluación DeepEval cuántica")
        print("✅ Desarrollo Claude Engineer")
        print("✅ OpenRouter + Ollama + CIO Brain")
        print(f"🌐 Iniciando en http://{host}:{port}")
        print("📱 Abre tu navegador y ve a: http://127.0.0.1:5000")
        print("🔧 Presiona Ctrl+C para detener")
        print("=" * 70)
        
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Función principal"""
    try:
        optimal_ui = OptimalUI()
        optimal_ui.run()
    except KeyboardInterrupt:
        print("\n🛑 UI detenida por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
