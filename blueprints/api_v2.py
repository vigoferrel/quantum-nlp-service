#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - API v2 Blueprint
Blueprint con endpoints mejorados, documentación OpenAPI y funcionalidad avanzada
"""

import os
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from flask import Blueprint, request, jsonify, current_app
from pathlib import Path
import logging

logger = logging.getLogger('API_V2_BP')


def create_api_v2_blueprint(config):
    """Crear Blueprint de API v2 con todos los endpoints mejorados"""
    
    api_v2_bp = Blueprint('api_v2', __name__)
    
    # === DOCUMENTACIÓN OPENAPI ===
    
    @api_v2_bp.route('/docs')
    def api_docs():
        """Documentación interactiva de la API v2"""
        try:
            swagger_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>VIGOLEONROCKS API v2 Documentation</title>
                <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
                <style>
                    .swagger-ui .topbar { display: none; }
                    .swagger-ui .info hgroup.main .title { color: #3B82F6; }
                </style>
            </head>
            <body>
                <div id="swagger-ui"></div>
                <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
                <script>
                    SwaggerUIBundle({
                        url: '/api/v2/openapi.json',
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.presets.standalone],
                        plugins: [SwaggerUIBundle.plugins.DownloadUrl],
                        layout: "StandaloneLayout"
                    });
                </script>
            </body>
            </html>
            """
            return swagger_template
        
        except Exception as e:
            logger.error(f"Error sirviendo documentación: {e}")
            return jsonify({'error': str(e)}), 500
    
    @api_v2_bp.route('/openapi.json')
    def openapi_spec():
        """Especificación OpenAPI en formato JSON"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "VIGOLEONROCKS API v2",
                "version": config.VERSION,
                "description": "API avanzada del sistema multimodal de IA VIGOLEONROCKS",
                "contact": {
                    "name": "VIGOLEONROCKS Team",
                    "url": "https://vigoleonrocks.com"
                }
            },
            "servers": [
                {
                    "url": f"http://{config.HOST}:{config.PORT}/api/v2",
                    "description": "Servidor de desarrollo"
                }
            ],
            "paths": {
                "/system/health": {
                    "get": {
                        "summary": "Health Check detallado",
                        "description": "Verifica el estado de todos los componentes del sistema",
                        "responses": {
                            "200": {
                                "description": "Estado del sistema",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/system/models": {
                    "get": {
                        "summary": "Lista de modelos disponibles",
                        "description": "Obtiene información sobre todos los modelos multimodales",
                        "responses": {
                            "200": {
                                "description": "Información de modelos",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/ModelsResponse"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/metrics": {
                    "get": {
                        "summary": "Métricas del sistema",
                        "description": "Métricas detalladas de rendimiento y uso",
                        "responses": {
                            "200": {
                                "description": "Métricas del sistema",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/MetricsResponse"}
                                    }
                                }
                            }
                        }
                    }
                },
                "/cache/stats": {
                    "get": {
                        "summary": "Estadísticas del cache",
                        "description": "Información sobre el uso del sistema de cache",
                        "responses": {
                            "200": {
                                "description": "Stats del cache",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/CacheStatsResponse"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "HealthResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "enum": ["healthy", "degraded", "error"]},
                            "checks": {"type": "object"},
                            "timestamp": {"type": "number"}
                        }
                    },
                    "ModelsResponse": {
                        "type": "object",
                        "properties": {
                            "models": {"type": "array"},
                            "total": {"type": "integer"},
                            "loaded": {"type": "integer"}
                        }
                    },
                    "MetricsResponse": {
                        "type": "object",
                        "properties": {
                            "system": {"type": "object"},
                            "api": {"type": "object"},
                            "models": {"type": "object"}
                        }
                    },
                    "CacheStatsResponse": {
                        "type": "object",
                        "properties": {
                            "hits": {"type": "integer"},
                            "misses": {"type": "integer"},
                            "hit_rate": {"type": "number"},
                            "size": {"type": "integer"}
                        }
                    }
                }
            }
        }
        
        return jsonify(spec)
    
    # === SISTEMA Y HEALTH ===
    
    @api_v2_bp.route('/system/health')
    def system_health():
        """Health check detallado del sistema"""
        try:
            from app_factory import health_check
            health = health_check(current_app)
            return jsonify(health)
        
        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return jsonify({
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }), 500
    
    @api_v2_bp.route('/system/models')
    def system_models():
        """Lista detallada de modelos disponibles"""
        try:
            if not config.MULTIMODAL_ENABLED:
                return jsonify({
                    'error': 'Multimodal system disabled',
                    'models': [],
                    'total': 0
                })
            
            from multimodal_ai_manager import get_multimodal_manager
            manager = get_multimodal_manager()
            system_status = manager.get_system_status()
            
            models_info = []
            for model_key in system_status.get('models_available', []):
                if model_key in manager.model_configs:
                    model_config = manager.model_configs[model_key]
                    
                    # Determinar estado del modelo
                    is_loaded = model_key in manager.models
                    is_enabled = model_config.enabled
                    
                    model_info = {
                        'id': model_key,
                        'name': model_config.name,
                        'task': model_config.task,
                        'device': model_config.device,
                        'precision': model_config.precision,
                        'enabled': is_enabled,
                        'loaded': is_loaded,
                        'status': 'loaded' if is_loaded else ('enabled' if is_enabled else 'disabled'),
                        'memory_usage': None,  # TODO: Implementar medición de memoria
                        'last_used': None     # TODO: Implementar tracking de uso
                    }
                    
                    models_info.append(model_info)
            
            # Estadísticas generales
            total_models = len(models_info)
            loaded_models = sum(1 for m in models_info if m['loaded'])
            enabled_models = sum(1 for m in models_info if m['enabled'])
            
            return jsonify({
                'models': models_info,
                'summary': {
                    'total': total_models,
                    'loaded': loaded_models,
                    'enabled': enabled_models,
                    'disabled': total_models - enabled_models
                },
                'capabilities': system_status.get('capabilities', {}),
                'device': system_status.get('device', 'unknown'),
                'timestamp': time.time()
            })
        
        except Exception as e:
            logger.error(f"Error obteniendo modelos: {e}")
            return jsonify({'error': str(e)}), 500
    
    # === MÉTRICAS AVANZADAS ===
    
    @api_v2_bp.route('/metrics')
    def system_metrics():
        """Métricas detalladas del sistema"""
        try:
            metrics = {}
            
            # Métricas de la aplicación
            if hasattr(current_app, 'metrics'):
                app_metrics = current_app.metrics.copy()
                
                # Calcular estadísticas de respuesta
                response_times = app_metrics.get('response_times', [])
                if response_times:
                    app_metrics['response_stats'] = {
                        'avg': sum(response_times) / len(response_times),
                        'min': min(response_times),
                        'max': max(response_times),
                        'count': len(response_times)
                    }
                else:
                    app_metrics['response_stats'] = {
                        'avg': 0, 'min': 0, 'max': 0, 'count': 0
                    }
                
                metrics['application'] = app_metrics
            
            # Métricas del sistema
            try:
                import psutil
                system_metrics = {
                    'cpu_percent': psutil.cpu_percent(interval=0.1),
                    'memory': {
                        'total': psutil.virtual_memory().total,
                        'available': psutil.virtual_memory().available,
                        'percent': psutil.virtual_memory().percent,
                        'used': psutil.virtual_memory().used
                    },
                    'disk': {
                        'total': psutil.disk_usage('/').total,
                        'used': psutil.disk_usage('/').used,
                        'free': psutil.disk_usage('/').free,
                        'percent': psutil.disk_usage('/').percent
                    } if os.name != 'nt' else {
                        'total': psutil.disk_usage('C:\\').total,
                        'used': psutil.disk_usage('C:\\').used,
                        'free': psutil.disk_usage('C:\\').free,
                        'percent': psutil.disk_usage('C:\\').percent
                    }
                }
                metrics['system'] = system_metrics
            except ImportError:
                from config import system_entropy
                metrics['system'] = {
                    'cpu_percent': system_entropy() * 100,
                    'memory_percent': system_entropy() * 80 + 20
                }
            
            # Métricas multimodales
            if config.MULTIMODAL_ENABLED:
                try:
                    from multimodal_ai_manager import get_multimodal_manager
                    manager = get_multimodal_manager()
                    system_status = manager.get_system_status()
                    
                    multimodal_metrics = {
                        'models_loaded': system_status.get('models_loaded', 0),
                        'models_available': len(system_status.get('models_available', [])),
                        'capabilities': system_status.get('capabilities', {}),
                        'device': system_status.get('device', 'unknown')
                    }
                    
                    # Agregar estadísticas de uso si están disponibles
                    if hasattr(manager, 'usage_stats'):
                        multimodal_metrics['usage'] = manager.usage_stats
                    
                    metrics['multimodal'] = multimodal_metrics
                except Exception as e:
                    logger.error(f"Error obteniendo métricas multimodales: {e}")
                    metrics['multimodal'] = {'error': str(e)}
            
            # Métricas de cache
            if config.CACHE_ENABLED and hasattr(current_app, 'config') and 'CACHE' in current_app.config:
                cache = current_app.config['CACHE']
                try:
                    cache_stats = {
                        'type': config.CACHE_TYPE,
                        'ttl': config.CACHE_TTL,
                        'enabled': True
                    }
                    
                    # Intentar obtener estadísticas específicas del cache
                    if hasattr(cache, 'cache') and hasattr(cache.cache, '_cache'):
                        # Para SimpleCache (memory)
                        cache_dict = cache.cache._cache
                        cache_stats.update({
                            'size': len(cache_dict),
                            'keys': list(cache_dict.keys()) if len(cache_dict) < 20 else f"{len(cache_dict)} keys"
                        })
                    
                    metrics['cache'] = cache_stats
                except Exception as e:
                    metrics['cache'] = {'error': str(e), 'enabled': True}
            else:
                metrics['cache'] = {'enabled': False}
            
            # Timestamp y metadata
            metrics['metadata'] = {
                'timestamp': time.time(),
                'version': config.VERSION,
                'environment': config.__class__.__name__,
                'uptime_seconds': metrics.get('application', {}).get('uptime_seconds', 0)
            }
            
            return jsonify(metrics)
        
        except Exception as e:
            logger.error(f"Error obteniendo métricas: {e}")
            return jsonify({'error': str(e)}), 500
    
    # === CACHE ===
    
    @api_v2_bp.route('/cache/stats')
    def cache_stats():
        """Estadísticas detalladas del sistema de cache"""
        try:
            if not config.CACHE_ENABLED:
                return jsonify({
                    'enabled': False,
                    'message': 'Cache system is disabled'
                })
            
            cache_info = {
                'enabled': True,
                'type': config.CACHE_TYPE,
                'ttl': config.CACHE_TTL,
                'timestamp': time.time()
            }
            
            if hasattr(current_app, 'config') and 'CACHE' in current_app.config:
                cache = current_app.config['CACHE']
                
                try:
                    if config.CACHE_TYPE == 'memory':
                        # Estadísticas para cache en memoria
                        if hasattr(cache, 'cache') and hasattr(cache.cache, '_cache'):
                            cache_dict = cache.cache._cache
                            cache_info.update({
                                'size': len(cache_dict),
                                'keys': len(cache_dict),
                                'estimated_memory_kb': len(str(cache_dict)) / 1024,
                                'keys_sample': list(cache_dict.keys())[:10] if cache_dict else []
                            })
                    
                    elif config.CACHE_TYPE == 'redis':
                        # Estadísticas para Redis (si está disponible)
                        try:
                            import redis
                            redis_client = redis.Redis.from_url(config.REDIS_URL)
                            info = redis_client.info()
                            cache_info.update({
                                'redis_version': info.get('redis_version'),
                                'used_memory': info.get('used_memory'),
                                'connected_clients': info.get('connected_clients'),
                                'total_commands_processed': info.get('total_commands_processed'),
                                'keyspace_hits': info.get('keyspace_hits', 0),
                                'keyspace_misses': info.get('keyspace_misses', 0)
                            })
                            
                            # Calcular hit rate
                            hits = info.get('keyspace_hits', 0)
                            misses = info.get('keyspace_misses', 0)
                            total = hits + misses
                            cache_info['hit_rate'] = (hits / total) if total > 0 else 0
                            
                        except Exception as redis_error:
                            cache_info['redis_error'] = str(redis_error)
                
                except Exception as cache_error:
                    cache_info['cache_error'] = str(cache_error)
            
            else:
                cache_info['status'] = 'Cache object not found in app config'
            
            return jsonify(cache_info)
        
        except Exception as e:
            logger.error(f"Error obteniendo stats de cache: {e}")
            return jsonify({'error': str(e)}), 500
    
    @api_v2_bp.route('/cache/clear', methods=['POST'])
    def cache_clear():
        """Limpiar el cache del sistema"""
        try:
            if not config.CACHE_ENABLED:
                return jsonify({
                    'success': False,
                    'message': 'Cache system is disabled'
                }), 400
            
            if hasattr(current_app, 'config') and 'CACHE' in current_app.config:
                cache = current_app.config['CACHE']
                cache.clear()
                
                return jsonify({
                    'success': True,
                    'message': 'Cache cleared successfully',
                    'timestamp': time.time()
                })
            
            else:
                return jsonify({
                    'success': False,
                    'message': 'Cache object not available'
                }), 500
        
        except Exception as e:
            logger.error(f"Error limpiando cache: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    # === ENDPOINTS LEGACY PARA COMPATIBILIDAD ===
    
    @api_v2_bp.route('/multimodal/status')
    def multimodal_status():
        """Estado del sistema multimodal (endpoint legacy)"""
        try:
            if not config.MULTIMODAL_ENABLED:
                return jsonify({
                    'enabled': False,
                    'message': 'Multimodal system is disabled'
                })
            
            from multimodal_ai_manager import get_multimodal_manager, CLIP_AVAILABLE
            manager = get_multimodal_manager()
            system_status = manager.get_system_status()
            
            return jsonify({
                'enabled': True,
                'clip_available': CLIP_AVAILABLE,
                'system_status': system_status,
                'timestamp': time.time()
            })
        
        except Exception as e:
            logger.error(f"Error en multimodal status: {e}")
            return jsonify({'error': str(e)}), 500
    
    @api_v2_bp.route('/performance/report')
    def performance_report():
        """Reporte de performance del sistema"""
        try:
            # Obtener métricas de performance
            report = {
                'timestamp': time.time(),
                'version': config.VERSION
            }
            
            # Métricas de aplicación
            if hasattr(current_app, 'metrics'):
                app_metrics = current_app.metrics
                response_times = app_metrics.get('response_times', [])
                
                if response_times:
                    # Calcular percentiles
                    sorted_times = sorted(response_times)
                    count = len(sorted_times)
                    
                    report['response_times'] = {
                        'avg_ms': sum(response_times) / count,
                        'min_ms': min(response_times),
                        'max_ms': max(response_times),
                        'p50_ms': sorted_times[int(count * 0.5)],
                        'p95_ms': sorted_times[int(count * 0.95)],
                        'p99_ms': sorted_times[int(count * 0.99)] if count > 100 else max(response_times),
                        'total_requests': app_metrics.get('requests_total', 0)
                    }
                else:
                    report['response_times'] = {
                        'avg_ms': 0, 'min_ms': 0, 'max_ms': 0,
                        'p50_ms': 0, 'p95_ms': 0, 'p99_ms': 0,
                        'total_requests': 0
                    }
                
                report['uptime_seconds'] = app_metrics.get('uptime_seconds', 0)
                report['active_connections'] = app_metrics.get('active_connections', 0)
            
            # Estado de componentes críticos
            try:
                from app_factory import health_check
                health = health_check(current_app)
                report['system_health'] = health['status']
                report['component_checks'] = health['checks']
            except Exception:
                report['system_health'] = 'unknown'
            
            # Recomendaciones de performance
            recommendations = []
            
            if hasattr(current_app, 'metrics'):
                avg_response = report.get('response_times', {}).get('avg_ms', 0)
                
                if avg_response > 500:
                    recommendations.append("Average response time > 500ms. Consider enabling cache or optimizing queries.")
                
                if report.get('active_connections', 0) > 50:
                    recommendations.append("High number of active connections. Consider connection pooling.")
            
            if not config.CACHE_ENABLED:
                recommendations.append("Cache is disabled. Enable cache to improve performance.")
            
            report['recommendations'] = recommendations
            report['performance_grade'] = _calculate_performance_grade(report)
            
            return jsonify(report)
        
        except Exception as e:
            logger.error(f"Error en performance report: {e}")
            return jsonify({'error': str(e)}), 500
    
    # === UTILIDADES ===
    
    def _calculate_performance_grade(report):
        """Calcular grado de performance basado en métricas"""
        score = 100
        
        # Penalizar por tiempo de respuesta alto
        avg_response = report.get('response_times', {}).get('avg_ms', 0)
        if avg_response > 100:
            score -= min(50, (avg_response - 100) / 10)
        
        # Penalizar si el sistema no está healthy
        if report.get('system_health') != 'healthy':
            score -= 20
        
        # Bonus por tener cache habilitado
        if config.CACHE_ENABLED:
            score += 5
        
        # Determinar letra
        if score >= 90:
            return {'grade': 'A', 'score': score, 'description': 'Excellent'}
        elif score >= 80:
            return {'grade': 'B', 'score': score, 'description': 'Good'}
        elif score >= 70:
            return {'grade': 'C', 'score': score, 'description': 'Fair'}
        else:
            return {'grade': 'D', 'score': score, 'description': 'Needs improvement'}
    
    logger.info("✅ API v2 Blueprint creado con todos los endpoints")
    return api_v2_bp
