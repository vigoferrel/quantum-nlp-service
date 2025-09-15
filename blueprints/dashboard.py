#!/usr/bin/env python3
"""
📊 VIGOLEONROCKS - Dashboard Blueprint
Blueprint para servir el dashboard de monitoreo y métricas
"""

import os
import time
from pathlib import Path
from flask import Blueprint, render_template_string, jsonify, current_app, send_from_directory
import logging

logger = logging.getLogger('DASHBOARD_BP')


def create_dashboard_blueprint(config):
    """Crear Blueprint del dashboard"""
    
    dashboard_bp = Blueprint('dashboard', __name__)
    
    @dashboard_bp.route('/dashboard')
    def dashboard_main():
        """Dashboard principal de monitoreo"""
        try:
            # Intentar leer el archivo HTML del dashboard
            dashboard_file = Path(__file__).parent.parent / 'dashboard_monitoring.html'
            
            if dashboard_file.exists():
                with open(dashboard_file, 'r', encoding='utf-8') as f:
                    dashboard_html = f.read()
                
                # Inyectar datos dinámicos si la app tiene métricas
                if hasattr(current_app, 'metrics'):
                    metrics = current_app.metrics
                    
                    # Reemplazar placeholders con datos reales
                    dashboard_html = dashboard_html.replace('{{uptime}}', str(int(metrics.get('uptime_seconds', 0))))
                    dashboard_html = dashboard_html.replace('{{requests_total}}', str(metrics.get('requests_total', 0)))
                    dashboard_html = dashboard_html.replace('{{active_connections}}', str(metrics.get('active_connections', 0)))
                    
                    # Tiempo promedio de respuesta
                    response_times = metrics.get('response_times', [])
                    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
                    dashboard_html = dashboard_html.replace('{{avg_response_time}}', f"{avg_response_time:.2f}ms")
                
                return dashboard_html
            
            else:
                # Dashboard básico embebido si no existe el archivo
                return render_template_string(DASHBOARD_BASIC_TEMPLATE)
        
        except Exception as e:
            logger.error(f"Error sirviendo dashboard: {e}")
            return jsonify({
                'error': 'Dashboard Error',
                'message': str(e),
                'fallback_available': True
            }), 500
    
    @dashboard_bp.route('/dashboard/api/metrics')
    def dashboard_metrics():
        """API endpoint para métricas del dashboard"""
        try:
            if hasattr(current_app, 'metrics'):
                metrics = current_app.metrics.copy()
                
                # Calcular estadísticas adicionales
                response_times = metrics.get('response_times', [])
                if response_times:
                    metrics['avg_response_time'] = sum(response_times) / len(response_times)
                    metrics['max_response_time'] = max(response_times)
                    metrics['min_response_time'] = min(response_times)
                else:
                    metrics['avg_response_time'] = 0
                    metrics['max_response_time'] = 0  
                    metrics['min_response_time'] = 0
                
                # Agregar información del sistema multimodal
                try:
                    from multimodal_ai_manager import get_multimodal_manager, CLIP_AVAILABLE
                    manager = get_multimodal_manager()
                    system_status = manager.get_system_status()
                    
                    metrics['multimodal'] = {
                        'available': True,
                        'clip_available': CLIP_AVAILABLE,
                        'models_loaded': system_status.get('models_loaded', 0),
                        'models_available': len(system_status.get('models_available', [])),
                        'device': system_status.get('device', 'unknown')
                    }
                except Exception:
                    metrics['multimodal'] = {'available': False}
                
                return jsonify(metrics)
            
            else:
                return jsonify({
                    'error': 'No metrics available',
                    'timestamp': time.time()
                })
        
        except Exception as e:
            logger.error(f"Error obteniendo métricas: {e}")
            return jsonify({'error': str(e)}), 500
    
    @dashboard_bp.route('/dashboard/api/system-status')
    def dashboard_system_status():
        """Estado detallado del sistema para el dashboard"""
        try:
            from app_factory import health_check
            health = health_check(current_app)
            
            return jsonify(health)
        
        except Exception as e:
            logger.error(f"Error obteniendo estado del sistema: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    logger.info("✅ Dashboard Blueprint creado")
    return dashboard_bp


# Template básico embebido como fallback
DASHBOARD_BASIC_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 VIGOLEONROCKS - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0A0B0D 0%, #1C1D21 50%, #2A2D37 100%);
            color: white;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        .header {
            background: rgba(28, 29, 33, 0.9);
            backdrop-filter: blur(20px);
            padding: 1rem 2rem;
            border-bottom: 1px solid rgba(59, 130, 246, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10B981;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .metric-card {
            background: rgba(28, 29, 33, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.15);
            transform: translateY(-2px);
        }
        
        .metric-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
            color: #94A3B8;
            font-weight: 500;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #3B82F6;
            margin-bottom: 0.5rem;
        }
        
        .metric-subtitle {
            color: #64748B;
            font-size: 0.9rem;
        }
        
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 2rem;
            color: #FCA5A5;
        }
        
        .actions {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
            transition: all 0.2s ease;
        }
        
        .btn-primary {
            background: #3B82F6;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2563EB;
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #3B82F6;
        }
        
        .btn-secondary:hover {
            background: rgba(59, 130, 246, 0.2);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">🚀 VIGOLEONROCKS Dashboard</div>
            <div class="status-indicator">
                <div class="status-dot"></div>
                <span>Sistema Operativo</span>
            </div>
        </div>
    </div>
    
    <div class="dashboard-container">
        <div class="error-message">
            <h3>⚠️ Dashboard en Modo Básico</h3>
            <p>El archivo dashboard_monitoring.html no está disponible. Mostrando interfaz básica.</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">
                    📊 Requests Totales
                </div>
                <div class="metric-value" id="requests-total">--</div>
                <div class="metric-subtitle">Requests procesados desde inicio</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">
                    🔗 Conexiones Activas
                </div>
                <div class="metric-value" id="active-connections">--</div>
                <div class="metric-subtitle">Conexiones simultáneas actuales</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">
                    ⏱️ Tiempo de Respuesta
                </div>
                <div class="metric-value" id="avg-response-time">--</div>
                <div class="metric-subtitle">Promedio en milisegundos</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">
                    ⏰ Uptime
                </div>
                <div class="metric-value" id="uptime">--</div>
                <div class="metric-subtitle">Tiempo desde inicio</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">
                    🧠 Sistema Multimodal
                </div>
                <div class="metric-value" id="multimodal-status">--</div>
                <div class="metric-subtitle">Estado de modelos AI</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">
                    💾 Memoria del Sistema
                </div>
                <div class="metric-value" id="system-memory">--</div>
                <div class="metric-subtitle">Porcentaje de memoria usada</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/dashboard/api/metrics" class="btn btn-primary">Ver Métricas JSON</a>
            <a href="/dashboard/api/system-status" class="btn btn-secondary">Estado del Sistema</a>
            <a href="/api/v2/system/health" class="btn btn-secondary">Health Check</a>
            <a href="/" class="btn btn-secondary">Volver al Inicio</a>
        </div>
    </div>
    
    <script>
        // Actualizar métricas cada 5 segundos
        function updateMetrics() {
            fetch('/dashboard/api/metrics')
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error('Error obteniendo métricas:', data.error);
                        return;
                    }
                    
                    document.getElementById('requests-total').textContent = data.requests_total || '--';
                    document.getElementById('active-connections').textContent = data.active_connections || '--';
                    
                    const avgResponseTime = data.avg_response_time || 0;
                    document.getElementById('avg-response-time').textContent = avgResponseTime.toFixed(2) + 'ms';
                    
                    const uptime = data.uptime_seconds || 0;
                    const uptimeFormatted = Math.floor(uptime / 60) + 'm ' + Math.floor(uptime % 60) + 's';
                    document.getElementById('uptime').textContent = uptimeFormatted;
                    
                    if (data.multimodal) {
                        const status = data.multimodal.available ? '✅ Activo' : '❌ Inactivo';
                        document.getElementById('multimodal-status').textContent = status;
                    } else {
                        document.getElementById('multimodal-status').textContent = '❌ No disponible';
                    }
                    
                    const memoryUsage = data.system_memory || 0;
                    document.getElementById('system-memory').textContent = memoryUsage.toFixed(1) + '%';
                })
                .catch(error => {
                    console.error('Error actualizando métricas:', error);
                });
        }
        
        // Actualizar inmediatamente y luego cada 5 segundos
        updateMetrics();
        setInterval(updateMetrics, 5000);
    </script>
</body>
</html>
"""
