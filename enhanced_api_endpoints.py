#!/usr/bin/env python3
"""
🌐 Sistema de APIs Expandidas para VIGOLEONROCKS
Endpoints específicos, WebSocket, y documentación automática
"""

from flask import Flask, request, jsonify
import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import json
import base64
from io import BytesIO
from PIL import Image

logger = logging.getLogger(__name__)

class EnhancedAPIEndpoints:
    """Endpoints API mejorados y especializados"""
    
    def __init__(self, flask_app: Flask):
        self.app = flask_app
        self.register_enhanced_endpoints()
        
        # Métricas de API
        self.api_metrics = {
            'total_requests': 0,
            'endpoints_usage': {},
            'error_count': 0,
            'start_time': time.time()
        }
        
        logger.info("🌐 Enhanced API Endpoints inicializados")
    
    def register_enhanced_endpoints(self):
        """Registra todos los endpoints mejorados"""
        
        # === ANÁLISIS DE IMÁGENES ESPECÍFICOS ===
        
        @self.app.route('/api/v2/image/analyze', methods=['POST'])
        async def analyze_image_v2():
            """Análisis avanzado de imagen con opciones específicas"""
            try:
                self._track_endpoint_usage('image_analyze_v2')
                
                # Obtener datos de la imagen
                if 'image' not in request.files and 'image_data' not in request.json:
                    return jsonify({'error': 'No image provided'}), 400
                
                # Procesar imagen
                if 'image' in request.files:
                    image_file = request.files['image']
                    image = Image.open(image_file.stream)
                else:
                    # Imagen en base64
                    image_data = request.json['image_data']
                    if 'data:image' in image_data:
                        image_data = image_data.split(',')[1]
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(BytesIO(image_bytes))
                
                # Opciones de análisis
                options = request.json.get('options', {}) if request.is_json else {}
                analysis_type = options.get('type', 'comprehensive')
                include_embeddings = options.get('embeddings', False)
                include_objects = options.get('objects', False)
                include_text = options.get('text', False)
                
                # Realizar análisis multimodal
                from multimodal_ai_manager import get_multimodal_manager
                manager = get_multimodal_manager()
                
                start_time = time.time()
                result = await manager.analyze_image(image, analysis_type=analysis_type)
                processing_time = time.time() - start_time
                
                # Construir respuesta estructurada
                response = {
                    'success': True,
                    'analysis': {
                        'description': result.content,
                        'confidence': result.confidence,
                        'model_used': result.model_used,
                        'processing_time': processing_time,
                        'timestamp': result.timestamp
                    },
                    'metadata': {
                        'image_size': list(image.size),
                        'image_format': image.format or 'Unknown',
                        'analysis_type': analysis_type,
                        'options_requested': options
                    }
                }
                
                # Agregar embeddings si se solicitaron
                if include_embeddings and 'embeddings' in result.metadata:
                    response['embeddings'] = result.metadata['embeddings']
                
                return jsonify(response)
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error en /api/v2/image/analyze: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'error_type': 'analysis_error'
                }), 500
        
        @self.app.route('/api/v2/image/quick', methods=['POST'])
        async def quick_image_analysis():
            """Análisis rápido de imagen optimizado para velocidad"""
            try:
                self._track_endpoint_usage('image_quick')
                
                if 'image' not in request.files:
                    return jsonify({'error': 'No image provided'}), 400
                
                image_file = request.files['image']
                image = Image.open(image_file.stream)
                
                # Análisis rápido usando cache inteligente
                from performance_optimizer import performance_optimizer
                from multimodal_ai_manager import get_multimodal_manager
                
                manager = get_multimodal_manager()
                
                @performance_optimizer.cached_model_inference(cache_ttl=3600)
                async def cached_quick_analysis(img):
                    return await manager.analyze_image(img, analysis_type="fast")
                
                start_time = time.time()
                result = await cached_quick_analysis(image)
                processing_time = time.time() - start_time
                
                return jsonify({
                    'success': True,
                    'description': result.content,
                    'confidence': result.confidence,
                    'processing_time': processing_time,
                    'cached': processing_time < 0.1  # Indica si vino del cache
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error en /api/v2/image/quick: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # === ENDPOINTS DE SISTEMA ===
        
        @self.app.route('/api/v2/system/health', methods=['GET'])
        def system_health_detailed():
            """Health check detallado del sistema"""
            try:
                self._track_endpoint_usage('system_health')
                
                # Verificar componentes del sistema
                components = {
                    'multimodal_manager': self._check_multimodal_manager(),
                    'performance_optimizer': self._check_performance_optimizer(),
                    'clip_availability': self._check_clip_status(),
                    'cache_system': self._check_cache_system()
                }
                
                # Determinar estado general
                all_healthy = all(comp['healthy'] for comp in components.values())
                
                return jsonify({
                    'status': 'healthy' if all_healthy else 'degraded',
                    'timestamp': datetime.now().isoformat(),
                    'uptime_seconds': time.time() - self.api_metrics['start_time'],
                    'components': components,
                    'api_metrics': self._get_api_metrics()
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error en system health: {e}")
                return jsonify({
                    'status': 'error',
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/v2/system/models', methods=['GET'])
        def list_available_models():
            """Lista todos los modelos disponibles con detalles"""
            try:
                self._track_endpoint_usage('system_models')
                
                from multimodal_ai_manager import get_multimodal_manager
                manager = get_multimodal_manager()
                
                status = manager.get_system_status()
                
                models_info = []
                for model_key in status.get('models_available', []):
                    if model_key in manager.model_configs:
                        config = manager.model_configs[model_key]
                        models_info.append({
                            'key': model_key,
                            'name': config.name,
                            'task': config.task,
                            'enabled': config.enabled,
                            'loaded': model_key in manager.models,
                            'device': config.device,
                            'precision': config.precision
                        })
                
                return jsonify({
                    'success': True,
                    'total_models': len(models_info),
                    'loaded_models': len(manager.models),
                    'models': models_info,
                    'capabilities': status.get('capabilities', {}),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error listando modelos: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # === ENDPOINTS DE CACHE Y RENDIMIENTO ===
        
        @self.app.route('/api/v2/cache/stats', methods=['GET'])
        def cache_statistics():
            """Estadísticas detalladas del cache"""
            try:
                self._track_endpoint_usage('cache_stats')
                
                from performance_optimizer import performance_optimizer
                
                cache_stats = performance_optimizer.cache.get_stats()
                perf_report = performance_optimizer.get_performance_report()
                
                return jsonify({
                    'success': True,
                    'cache': cache_stats,
                    'performance': perf_report['cache_performance'],
                    'recommendations': [
                        rec for rec in perf_report['recommendations'] 
                        if 'cache' in rec.lower()
                    ],
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error obteniendo stats de cache: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/v2/cache/clear', methods=['POST'])
        def clear_cache():
            """Limpiar cache manualmente"""
            try:
                self._track_endpoint_usage('cache_clear')
                
                from performance_optimizer import performance_optimizer
                
                # Limpiar cache expirado
                expired_count = performance_optimizer.cache.cleanup_expired()
                
                # Si se solicita, hacer limpieza LRU
                force_clear = request.json.get('force', False) if request.is_json else False
                lru_count = 0
                
                if force_clear:
                    performance_optimizer.cache._evict_lru()
                    lru_count = 1
                
                return jsonify({
                    'success': True,
                    'expired_removed': expired_count,
                    'lru_evicted': lru_count,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error limpiando cache: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # === DOCUMENTACIÓN AUTOMÁTICA ===
        
        @self.app.route('/api/v2/docs', methods=['GET'])
        def api_documentation():
            """Documentación automática de todos los endpoints"""
            try:
                self._track_endpoint_usage('api_docs')
                
                endpoints_info = []
                
                # Iterar sobre todas las rutas registradas
                for rule in self.app.url_map.iter_rules():
                    if rule.endpoint.startswith('api_v2') or '/api/v2/' in rule.rule:
                        endpoint_info = {
                            'path': rule.rule,
                            'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                            'description': self._get_endpoint_description(rule.endpoint),
                            'parameters': self._get_endpoint_parameters(rule.endpoint),
                            'examples': self._get_endpoint_examples(rule.endpoint)
                        }
                        endpoints_info.append(endpoint_info)
                
                return jsonify({
                    'api_version': '2.0',
                    'title': 'VIGOLEONROCKS Enhanced API',
                    'description': 'APIs avanzadas para análisis multimodal con IA',
                    'total_endpoints': len(endpoints_info),
                    'endpoints': endpoints_info,
                    'generated_at': datetime.now().isoformat()
                })
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error generando documentación: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        # === ENDPOINT DE MÉTRICAS ===
        
        @self.app.route('/api/v2/metrics', methods=['GET'])
        def enhanced_metrics():
            """Métricas completas del sistema API"""
            try:
                self._track_endpoint_usage('enhanced_metrics')
                
                metrics = self._get_api_metrics()
                
                # Agregar métricas de rendimiento si están disponibles
                try:
                    from performance_optimizer import performance_optimizer
                    perf_report = performance_optimizer.get_performance_report()
                    metrics['performance'] = perf_report
                except ImportError:
                    metrics['performance'] = 'Performance optimizer not available'
                
                return jsonify(metrics)
                
            except Exception as e:
                self._track_error()
                logger.error(f"Error obteniendo métricas: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def _track_endpoint_usage(self, endpoint_name: str):
        """Trackea el uso de endpoints"""
        self.api_metrics['total_requests'] += 1
        
        if endpoint_name not in self.api_metrics['endpoints_usage']:
            self.api_metrics['endpoints_usage'][endpoint_name] = {
                'count': 0,
                'first_used': datetime.now().isoformat(),
                'last_used': None
            }
        
        self.api_metrics['endpoints_usage'][endpoint_name]['count'] += 1
        self.api_metrics['endpoints_usage'][endpoint_name]['last_used'] = datetime.now().isoformat()
    
    def _track_error(self):
        """Trackea errores de API"""
        self.api_metrics['error_count'] += 1
    
    def _get_api_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas completas de la API"""
        uptime = time.time() - self.api_metrics['start_time']
        
        return {
            'total_requests': self.api_metrics['total_requests'],
            'error_count': self.api_metrics['error_count'],
            'success_rate': (
                (self.api_metrics['total_requests'] - self.api_metrics['error_count']) 
                / max(1, self.api_metrics['total_requests'])
            ) * 100,
            'uptime_seconds': uptime,
            'uptime_hours': uptime / 3600,
            'requests_per_hour': (self.api_metrics['total_requests'] / (uptime / 3600)) if uptime > 0 else 0,
            'endpoints_usage': self.api_metrics['endpoints_usage'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _check_multimodal_manager(self) -> Dict[str, Any]:
        """Verifica estado del multimodal manager"""
        try:
            from multimodal_ai_manager import get_multimodal_manager
            manager = get_multimodal_manager()
            status = manager.get_system_status()
            
            return {
                'healthy': True,
                'models_loaded': status.get('models_loaded', 0),
                'models_enabled': len(status.get('models_enabled', [])),
                'clip_available': status.get('capabilities', {}).get('clip_embeddings', False)
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_performance_optimizer(self) -> Dict[str, Any]:
        """Verifica estado del optimizador de rendimiento"""
        try:
            from performance_optimizer import performance_optimizer
            stats = performance_optimizer.cache.get_stats()
            
            return {
                'healthy': True,
                'cache_entries': stats['entries'],
                'cache_hit_rate': stats['hit_rate'],
                'memory_usage_mb': stats['size_mb']
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_clip_status(self) -> Dict[str, Any]:
        """Verifica estado específico de CLIP"""
        try:
            from multimodal_ai_manager import CLIP_AVAILABLE
            
            status = {'healthy': CLIP_AVAILABLE, 'available': CLIP_AVAILABLE}
            
            if not CLIP_AVAILABLE:
                status['message'] = 'CLIP not available - install with: pip install clip-by-openai'
            
            return status
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _check_cache_system(self) -> Dict[str, Any]:
        """Verifica estado del sistema de cache"""
        try:
            from performance_optimizer import performance_optimizer
            stats = performance_optimizer.cache.get_stats()
            
            # Considerar saludable si el cache no está lleno y tiene hit rate razonable
            healthy = (
                stats['memory_usage_percent'] < 90 and 
                (stats['hit_rate'] > 0.3 or stats['hits'] + stats['misses'] < 10)
            )
            
            return {
                'healthy': healthy,
                'hit_rate': stats['hit_rate'],
                'memory_usage_percent': stats['memory_usage_percent'],
                'total_requests': stats['hits'] + stats['misses']
            }
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e)
            }
    
    def _get_endpoint_description(self, endpoint: str) -> str:
        """Obtiene descripción de un endpoint"""
        descriptions = {
            'analyze_image_v2': 'Análisis avanzado de imagen con opciones específicas',
            'quick_image_analysis': 'Análisis rápido optimizado para velocidad',
            'system_health_detailed': 'Health check detallado del sistema',
            'list_available_models': 'Lista modelos disponibles con detalles',
            'cache_statistics': 'Estadísticas detalladas del cache',
            'clear_cache': 'Limpiar cache manualmente',
            'api_documentation': 'Documentación automática de endpoints',
            'enhanced_metrics': 'Métricas completas del sistema API'
        }
        return descriptions.get(endpoint, 'Sin descripción disponible')
    
    def _get_endpoint_parameters(self, endpoint: str) -> Dict[str, Any]:
        """Obtiene parámetros de un endpoint"""
        # Definir parámetros por endpoint
        parameters = {
            'analyze_image_v2': {
                'image': 'File upload o image_data en base64',
                'options': {
                    'type': 'comprehensive|fast|detailed',
                    'embeddings': 'boolean - incluir embeddings',
                    'objects': 'boolean - detectar objetos',
                    'text': 'boolean - extraer texto'
                }
            },
            'quick_image_analysis': {
                'image': 'File upload requerido'
            },
            'clear_cache': {
                'force': 'boolean - forzar limpieza LRU'
            }
        }
        return parameters.get(endpoint, {})
    
    def _get_endpoint_examples(self, endpoint: str) -> List[Dict[str, Any]]:
        """Obtiene ejemplos de uso de un endpoint"""
        examples = {
            'analyze_image_v2': [
                {
                    'method': 'POST',
                    'content_type': 'multipart/form-data',
                    'body': 'image=<file>&options={"type":"comprehensive","embeddings":true}'
                }
            ],
            'quick_image_analysis': [
                {
                    'method': 'POST',
                    'content_type': 'multipart/form-data',
                    'body': 'image=<file>'
                }
            ]
        }
        return examples.get(endpoint, [])

def initialize_enhanced_api(flask_app: Flask) -> EnhancedAPIEndpoints:
    """Inicializa los endpoints mejorados en una app Flask"""
    enhanced_api = EnhancedAPIEndpoints(flask_app)
    logger.info("🌐 Enhanced API Endpoints registrados exitosamente")
    return enhanced_api

if __name__ == "__main__":
    # Test de la API mejorada
    from flask import Flask
    
    app = Flask(__name__)
    enhanced_api = initialize_enhanced_api(app)
    
    print("🧪 Testing Enhanced API Endpoints...")
    with app.test_client() as client:
        # Test documentación
        response = client.get('/api/v2/docs')
        print(f"📚 Docs endpoint: {response.status_code}")
        
        # Test métricas
        response = client.get('/api/v2/metrics')
        print(f"📊 Metrics endpoint: {response.status_code}")
        
        # Test health
        response = client.get('/api/v2/system/health')
        print(f"💚 Health endpoint: {response.status_code}")
    
    print("✅ Enhanced API Endpoints listos para integración!")
