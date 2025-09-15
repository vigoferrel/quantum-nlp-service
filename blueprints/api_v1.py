#!/usr/bin/env python3
"""
🔗 VIGOLEONROCKS - API v1 Blueprint (Legacy)
Blueprint con endpoints legacy para compatibilidad hacia atrás
"""

import time
from flask import Blueprint, jsonify, current_app
import logging

logger = logging.getLogger('API_V1_BP')


def create_api_v1_blueprint(config):
    """Crear Blueprint de API v1 para compatibilidad"""
    
    api_v1_bp = Blueprint('api_v1', __name__)
    
    @api_v1_bp.route('/status')
    def api_status():
        """Status básico del sistema (legacy endpoint)"""
        try:
            status = {
                'status': 'operational',
                'version': f'VIGOLEONROCKS-Fast-v{config.VERSION}',
                'timestamp': time.time()
            }
            
            if hasattr(current_app, 'metrics'):
                metrics = current_app.metrics
                status.update({
                    'uptime': f"{int(metrics.get('uptime_seconds', 0))}s",
                    'requests': metrics.get('requests_total', 0),
                    'active_connections': metrics.get('active_connections', 0)
                })
            
            return jsonify(status)
        
        except Exception as e:
            logger.error(f"Error en api status: {e}")
            return jsonify({'status': 'error', 'error': str(e)}), 500
    
    @api_v1_bp.route('/quantum-metrics')
    def quantum_metrics():
        """Métricas cuánticas básicas (legacy endpoint)"""
        try:
            from config import system_entropy
            
            metrics = {
                'quantum_coherence': 98.9,
                'quantum_states': 26,
                'supremacy_score': 0.998,
                'system_entropy': system_entropy(),
                'timestamp': time.time()
            }
            
            # Agregar métricas de la app si están disponibles
            if hasattr(current_app, 'metrics'):
                app_metrics = current_app.metrics
                response_times = app_metrics.get('response_times', [])
                
                if response_times:
                    avg_response = sum(response_times) / len(response_times)
                    metrics['performance'] = {
                        'avg_response_time': avg_response,
                        'total_requests': app_metrics.get('requests_total', 0),
                        'uptime_seconds': app_metrics.get('uptime_seconds', 0)
                    }
            
            return jsonify(metrics)
        
        except Exception as e:
            logger.error(f"Error en quantum metrics: {e}")
            return jsonify({'error': str(e)}), 500
    
    # Redirecciones a API v2 para endpoints que migraron
    @api_v1_bp.route('/multimodal/status')
    def multimodal_status_redirect():
        """Redirigir a API v2"""
        return jsonify({
            'message': 'This endpoint has moved to API v2',
            'new_url': '/api/v2/multimodal/status',
            'api_v2_docs': '/api/v2/docs'
        }), 301
    
    @api_v1_bp.route('/performance/report')
    def performance_report_redirect():
        """Redirigir a API v2"""
        return jsonify({
            'message': 'This endpoint has moved to API v2',
            'new_url': '/api/v2/performance/report',
            'api_v2_docs': '/api/v2/docs'
        }), 301
    
    logger.info("✅ API v1 Blueprint creado (legacy)")
    return api_v1_bp
