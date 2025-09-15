#!/usr/bin/env python3
"""
🏠 VIGOLEONROCKS - Main Blueprint
Blueprint para páginas principales del sistema
"""

from flask import Blueprint, render_template_string, jsonify, current_app
import time
import logging

logger = logging.getLogger('MAIN_BP')


def create_main_blueprint(config):
    """Crear Blueprint principal con páginas básicas"""
    
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def home():
        """Página principal del sistema"""
        return render_template_string(HOME_TEMPLATE, config=config)
    
    @main_bp.route('/corporate')
    def corporate():
        """Página corporativa"""
        return render_template_string(CORPORATE_TEMPLATE, config=config)
    
    @main_bp.route('/ui')
    def ui():
        """Interfaz de chat/usuario"""
        return render_template_string(UI_TEMPLATE, config=config)
    
    @main_bp.route('/status')
    def status():
        """Página de estado del sistema"""
        try:
            # Obtener métricas básicas
            status_info = {
                'status': 'operational',
                'version': config.VERSION,
                'timestamp': time.time()
            }
            
            if hasattr(current_app, 'metrics'):
                metrics = current_app.metrics
                status_info.update({
                    'uptime_seconds': metrics.get('uptime_seconds', 0),
                    'requests_total': metrics.get('requests_total', 0),
                    'active_connections': metrics.get('active_connections', 0)
                })
            
            return jsonify(status_info)
        
        except Exception as e:
            logger.error(f"Error en status: {e}")
            return jsonify({'status': 'error', 'error': str(e)}), 500
    
    logger.info("✅ Main Blueprint creado")
    return main_bp


# === TEMPLATES ===

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 VIGOLEONROCKS - Sistema Multimodal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0A0B0D, #1C1D21, #2A2D37);
            color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .container { max-width: 900px; text-align: center; padding: 2rem; }
        h1 { font-size: 3rem; margin-bottom: 1rem; 
             background: linear-gradient(135deg, #3B82F6, #8B5CF6);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 1rem; margin-top: 2rem; }
        .card { background: rgba(28, 29, 33, 0.8); border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 12px; padding: 1.5rem; transition: all 0.3s ease; }
        .card:hover { border-color: #3B82F6; transform: translateY(-2px); 
                      box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2); }
        .card h3 { color: #3B82F6; margin-bottom: 0.5rem; }
        .card a { color: white; text-decoration: none; }
        .status { margin-top: 2rem; display: flex; justify-content: space-around; flex-wrap: wrap; }
        .status-item { margin: 0.5rem; text-align: center; }
        .status-value { font-size: 1.5rem; color: #10B981; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 VIGOLEONROCKS</h1>
        <p style="font-size: 1.2rem; opacity: 0.8; margin-bottom: 2rem;">
            Sistema Multimodal de IA Avanzada - v{{ config.VERSION }}
        </p>
        
        <div class="grid">
            <div class="card">
                <h3>📊 Dashboard</h3>
                <p>Monitoreo en tiempo real</p>
                <a href="/dashboard">Ver Dashboard →</a>
            </div>
            <div class="card">
                <h3>💬 Chat IA</h3>
                <p>Interfaz conversacional</p>
                <a href="/ui">Abrir Chat →</a>
            </div>
            <div class="card">
                <h3>🏢 Corporate</h3>
                <p>Información empresarial</p>
                <a href="/corporate">Ver Info →</a>
            </div>
            <div class="card">
                <h3>📚 API v2</h3>
                <p>Documentación técnica</p>
                <a href="/api/v2/docs">Ver Docs →</a>
            </div>
            <div class="card">
                <h3>💚 Sistema</h3>
                <p>Estado del sistema</p>
                <a href="/api/v2/system/health">Ver Estado →</a>
            </div>
            <div class="card">
                <h3>🧠 Modelos</h3>
                <p>Modelos disponibles</p>
                <a href="/api/v2/system/models">Ver Modelos →</a>
            </div>
        </div>
        
        <div class="status">
            <div class="status-item">
                <div class="status-value">{{ config.VERSION }}</div>
                <div style="opacity: 0.7;">Versión</div>
            </div>
            <div class="status-item">
                <div class="status-value">{% if config.MULTIMODAL_ENABLED %}✅{% else %}❌{% endif %}</div>
                <div style="opacity: 0.7;">Multimodal</div>
            </div>
            <div class="status-item">
                <div class="status-value">{% if config.CACHE_ENABLED %}✅{% else %}❌{% endif %}</div>
                <div style="opacity: 0.7;">Cache</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

CORPORATE_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏢 VIGOLEONROCKS - Corporate</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0A0B0D, #1C1D21, #2A2D37);
            color: white; min-height: 100vh; padding: 2rem;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 3rem; }
        h1 { 
            font-size: 2.5rem; margin-bottom: 1rem; 
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        }
        .section { 
            background: rgba(28, 29, 33, 0.8); 
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 12px; 
            padding: 2rem; 
            margin-bottom: 2rem; 
        }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .feature { padding: 1rem; border-left: 3px solid #3B82F6; }
        .stats { display: flex; justify-content: space-around; flex-wrap: wrap; }
        .stat { text-align: center; margin: 1rem; }
        .stat-value { font-size: 2rem; color: #10B981; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏢 VIGOLEONROCKS Corporate</h1>
            <p>Sistema Multimodal de IA Avanzada - Tecnología 2025</p>
        </div>
        
        <div class="section">
            <h2>🚀 Acerca de VIGOLEONROCKS</h2>
            <p>VIGOLEONROCKS es un sistema avanzado de inteligencia artificial multimodal que combina procesamiento de texto, imágenes y audio para ofrecer análisis comprehensivo y soluciones inteligentes. Desarrollado con tecnologías de vanguardia, proporciona capacidades de análisis en tiempo real con alta precisión y eficiencia.</p>
        </div>
        
        <div class="section">
            <h2>✨ Características Principales</h2>
            <div class="features">
                <div class="feature">
                    <h3>🧠 IA Multimodal</h3>
                    <p>Procesamiento simultáneo de texto, imágenes y audio con modelos avanzados como CLIP, Florence2 y Whisper.</p>
                </div>
                <div class="feature">
                    <h3>⚡ Rendimiento Optimizado</h3>
                    <p>Sistema de cache inteligente y optimizaciones de performance para respuestas ultra-rápidas.</p>
                </div>
                <div class="feature">
                    <h3>📊 Monitoreo Avanzado</h3>
                    <p>Dashboard en tiempo real con métricas detalladas y análisis de performance.</p>
                </div>
                <div class="feature">
                    <h3>🔒 Seguridad Empresarial</h3>
                    <p>Implementación con mejores prácticas de seguridad y conformidad con estándares industriales.</p>
                </div>
                <div class="feature">
                    <h3>🌐 API Robusta</h3>
                    <p>API v2 completamente documentada con OpenAPI/Swagger para fácil integración.</p>
                </div>
                <div class="feature">
                    <h3>🔄 Escalabilidad</h3>
                    <p>Arquitectura modular diseñada para escalar horizontalmente según las necesidades.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Estadísticas del Sistema</h2>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{{ config.VERSION }}</div>
                    <div>Versión Actual</div>
                </div>
                <div class="stat">
                    <div class="stat-value">7</div>
                    <div>Modelos IA</div>
                </div>
                <div class="stat">
                    <div class="stat-value">12+</div>
                    <div>Idiomas Soportados</div>
                </div>
                <div class="stat">
                    <div class="stat-value">99.9%</div>
                    <div>Uptime SLA</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🛠️ Configuración Técnica</h2>
            <ul style="list-style: none; padding: 0;">
                <li>💾 <strong>Sistema Multimodal:</strong> {% if config.MULTIMODAL_ENABLED %}✅ Habilitado{% else %}❌ Deshabilitado{% endif %}</li>
                <li>🗄️ <strong>Sistema de Cache:</strong> {% if config.CACHE_ENABLED %}✅ Activo ({{ config.CACHE_TYPE }}){% else %}❌ Deshabilitado{% endif %}</li>
                <li>📊 <strong>Métricas Prometheus:</strong> {% if config.PROMETHEUS_ENABLED %}✅ Habilitadas{% else %}❌ Deshabilitadas{% endif %}</li>
                <li>🔒 <strong>CORS:</strong> {% if config.CORS_ENABLED %}✅ Configurado{% else %}❌ Deshabilitado{% endif %}</li>
                <li>⚡ <strong>Ejecución en Background:</strong> {% if config.BACKGROUND_EXECUTION %}✅ Activa{% else %}❌ Deshabilitada{% endif %}</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 2rem;">
            <a href="/" style="color: #3B82F6; text-decoration: none; font-weight: bold;">← Volver al Inicio</a>
        </div>
    </div>
</body>
</html>
"""

UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>💬 VIGOLEONROCKS - Chat IA</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0A0B0D, #1C1D21, #2A2D37);
            color: white; height: 100vh; display: flex; flex-direction: column;
        }
        .header { 
            background: rgba(28, 29, 33, 0.9); 
            padding: 1rem 2rem; 
            border-bottom: 1px solid rgba(59, 130, 246, 0.3); 
        }
        .chat-container { 
            flex: 1; display: flex; flex-direction: column; 
            max-width: 800px; margin: 0 auto; width: 100%; padding: 1rem; 
        }
        .messages { 
            flex: 1; overflow-y: auto; padding: 1rem; 
            background: rgba(28, 29, 33, 0.5); border-radius: 12px; margin-bottom: 1rem; 
        }
        .message { 
            margin-bottom: 1rem; padding: 0.75rem 1rem; border-radius: 8px; 
            background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3B82F6; 
        }
        .message.system { border-left-color: #10B981; background: rgba(16, 185, 129, 0.1); }
        .input-container { display: flex; gap: 1rem; }
        .message-input { 
            flex: 1; padding: 0.75rem; border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 8px; background: rgba(28, 29, 33, 0.8); color: white;
        }
        .send-btn { 
            padding: 0.75rem 1.5rem; background: #3B82F6; color: white; 
            border: none; border-radius: 8px; cursor: pointer; 
        }
        .send-btn:hover { background: #2563EB; }
        .info-panel { 
            background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 8px; padding: 1rem; margin-bottom: 1rem; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>💬 VIGOLEONROCKS Chat IA</h1>
        <p>Interfaz de conversación con el sistema multimodal</p>
    </div>
    
    <div class="chat-container">
        <div class="info-panel">
            <h3>ℹ️ Información de la Interfaz</h3>
            <p>Esta es una interfaz básica para interactuar con VIGOLEONROCKS. El sistema completo de chat requiere la integración de endpoints de procesamiento multimodal.</p>
            <p><strong>Estado actual:</strong> Interfaz demo - Funcionalidad completa disponible vía API v2</p>
        </div>
        
        <div class="messages" id="messages">
            <div class="message system">
                <strong>Sistema:</strong> ¡Hola! Soy VIGOLEONROCKS, tu asistente de IA multimodal. Actualmente esta es una interfaz de demostración.
            </div>
            <div class="message system">
                <strong>Sistema:</strong> Para funcionalidad completa, usa los endpoints de la API v2: <a href="/api/v2/docs" style="color: #3B82F6;">/api/v2/docs</a>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" class="message-input" placeholder="Escribe tu mensaje aquí..." disabled>
            <button class="send-btn" onclick="sendMessage()" disabled>Enviar</button>
        </div>
    </div>
    
    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const messages = document.getElementById('messages');
            
            if (input.value.trim()) {
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.innerHTML = `<strong>Usuario:</strong> ${input.value}`;
                messages.appendChild(messageDiv);
                
                // Respuesta automática demo
                setTimeout(() => {
                    const responseDiv = document.createElement('div');
                    responseDiv.className = 'message system';
                    responseDiv.innerHTML = '<strong>Sistema:</strong> Esta es una interfaz de demostración. Para procesamiento real, integra con los endpoints de API v2.';
                    messages.appendChild(responseDiv);
                    messages.scrollTop = messages.scrollHeight;
                }, 500);
                
                input.value = '';
                messages.scrollTop = messages.scrollHeight;
            }
        }
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Mostrar advertencia
        setTimeout(() => {
            const messages = document.getElementById('messages');
            const infoDiv = document.createElement('div');
            infoDiv.className = 'message system';
            infoDiv.innerHTML = '<strong>Información:</strong> Para habilitar el chat completo, configura los endpoints de procesamiento multimodal en /api/v2/';
            messages.appendChild(infoDiv);
            messages.scrollTop = messages.scrollHeight;
        }, 2000);
    </script>
</body>
</html>
"""
