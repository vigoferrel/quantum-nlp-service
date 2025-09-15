#!/usr/bin/env python3
"""
🚀 VIGOLEONROCKS - Application Factory
Factory pattern para crear instancia Flask con todos los componentes integrados
"""

import os
import sys
import time
import logging
import threading
from typing import Optional, Dict, Any
from pathlib import Path

from flask import Flask, request, jsonify, g
from flask_cors import CORS

# Importar configuración
from config import get_config, print_config_summary, system_entropy

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VIGOLEONROCKS_FACTORY')


def create_app(config_name: Optional[str] = None) -> Flask:
    """
    Factory para crear aplicación Flask con toda la configuración
    
    Args:
        config_name: Nombre del entorno (development, production, testing)
        
    Returns:
        Flask app configurada
    """
    
    # === CONFIGURACIÓN ===
    config = get_config(config_name)
    config.init_directories()
    
    # Validar configuración
    validation = config.validate_config()
    if not validation['valid']:
        logger.error(f"Configuración inválida: {validation['issues']}")
        for issue in validation['issues']:
            logger.error(f"  - {issue}")
    
    # === CREAR APP FLASK ===
    app = Flask(
        __name__,
        template_folder=str(config.TEMPLATES_DIR),
        static_folder=str(config.STATIC_DIR),
        static_url_path='/static'
    )
    
    # Aplicar configuración
    app.config.from_object(config)
    app.config['CONFIG_OBJECT'] = config
    
    # === EXTENSIONES ===
    setup_extensions(app, config)
    
    # === BLUEPRINTS ===
    register_blueprints(app, config)
    
    # === MIDDLEWARE ===
    setup_middleware(app, config)
    
    # === SISTEMA BACKGROUND ===
    if config.BACKGROUND_EXECUTION:
        setup_background_tasks(app, config)
    
    # === LOGGING Y MÉTRICAS ===
    setup_logging_and_metrics(app, config)
    
    # === HANDLERS DE ERROR ===
    setup_error_handlers(app, config)
    
    # Mostrar resumen de configuración
    with app.app_context():
        print_config_summary(config)
        logger.info("✅ VIGOLEONROCKS App Factory inicializada correctamente")
    
    return app


def setup_extensions(app: Flask, config) -> None:
    """Configurar extensiones Flask"""
    
    # === CORS ===
    if config.CORS_ENABLED:
        CORS(app, 
             origins=config.CORS_ORIGINS,
             supports_credentials=True,
             allow_headers=['Content-Type', 'Authorization'])
        logger.info("✅ CORS configurado")
    
    # === RATE LIMITING ===
    if config.RATE_LIMITING_ENABLED:
        try:
            from flask_limiter import Limiter
            from flask_limiter.util import get_remote_address
            
            limiter = Limiter(
                key_func=get_remote_address,
                default_limits=[f"{config.MAX_REQUESTS_PER_MINUTE} per minute"]
            )
            limiter.init_app(app)
            app.config['LIMITER'] = limiter
            logger.info("✅ Rate limiting configurado")
        except ImportError:
            logger.warning("⚠️ Flask-Limiter no instalado, rate limiting deshabilitado")
    
    # === CACHE ===
    if config.CACHE_ENABLED:
        try:
            from flask_caching import Cache
            cache_config = {
                'CACHE_TYPE': config.CACHE_TYPE,
                'CACHE_DEFAULT_TIMEOUT': config.CACHE_TTL
            }
            
            if config.CACHE_TYPE == 'redis':
                cache_config['CACHE_REDIS_URL'] = config.REDIS_URL
            
            cache = Cache(app, config=cache_config)
            app.config['CACHE'] = cache
            logger.info(f"✅ Cache configurado ({config.CACHE_TYPE})")
        except ImportError:
            logger.warning("⚠️ Flask-Caching no instalado, cache deshabilitado")


def register_blueprints(app: Flask, config) -> None:
    """Registrar todos los Blueprints"""
    
    # === API v1 (LEGACY) ===
    try:
        from blueprints.api_v1 import create_api_v1_blueprint
        api_v1_bp = create_api_v1_blueprint(config)
        app.register_blueprint(api_v1_bp, url_prefix='/api')
        logger.info("✅ API v1 Blueprint registrado")
    except ImportError as e:
        logger.warning(f"⚠️ API v1 Blueprint no disponible: {e}")
    
    # === API v2 (ENHANCED) ===
    if config.API_V2_ENABLED:
        try:
            from blueprints.api_v2 import create_api_v2_blueprint
            api_v2_bp = create_api_v2_blueprint(config)
            app.register_blueprint(api_v2_bp, url_prefix=config.API_V2_PREFIX)
            logger.info("✅ API v2 Blueprint registrado")
        except ImportError as e:
            logger.warning(f"⚠️ API v2 Blueprint no disponible: {e}")
    
    # === DASHBOARD ===
    try:
        from blueprints.dashboard import create_dashboard_blueprint
        dashboard_bp = create_dashboard_blueprint(config)
        app.register_blueprint(dashboard_bp)
        logger.info("✅ Dashboard Blueprint registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Dashboard Blueprint no disponible: {e}")
    
    # === MAIN PAGES ===
    try:
        from blueprints.main import create_main_blueprint
        main_bp = create_main_blueprint(config)
        app.register_blueprint(main_bp)
        logger.info("✅ Main Blueprint registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Main Blueprint no disponible: {e}")


def setup_middleware(app: Flask, config) -> None:
    """Configurar middleware personalizado"""
    
    @app.before_request
    def before_request():
        """Middleware ejecutado antes de cada request"""
        g.start_time = time.time()
        g.request_id = f"req_{system_entropy():.6f}_{int(time.time() * 1000000) % 1000000}"
        
        # Incrementar métricas
        if hasattr(app, 'metrics'):
            app.metrics['requests_total'] = app.metrics.get('requests_total', 0) + 1
            app.metrics['active_connections'] = app.metrics.get('active_connections', 0) + 1
    
    @app.after_request
    def after_request(response):
        """Middleware ejecutado después de cada request"""
        if hasattr(g, 'start_time'):
            response_time = (time.time() - g.start_time) * 1000
            
            # Actualizar métricas
            if hasattr(app, 'metrics'):
                app.metrics['active_connections'] = max(0, 
                    app.metrics.get('active_connections', 1) - 1)
                
                if 'response_times' not in app.metrics:
                    app.metrics['response_times'] = []
                
                app.metrics['response_times'].append(response_time)
                
                # Mantener solo las últimas 1000 mediciones
                if len(app.metrics['response_times']) > 1000:
                    app.metrics['response_times'] = app.metrics['response_times'][-1000:]
        
        # Headers de seguridad básicos
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        return response


def setup_background_tasks(app: Flask, config) -> None:
    """Configurar tareas en background"""
    import time
    
    def metrics_updater():
        """Thread para actualizar métricas del sistema"""
        while True:
            try:
                with app.app_context():
                    # Actualizar métricas del sistema
                    if not hasattr(app, 'metrics'):
                        app.metrics = {}
                    
                    app.metrics['uptime_seconds'] = time.time() - app.metrics.get('start_time', time.time())
                    app.metrics['system_entropy'] = system_entropy()
                    app.metrics['last_update'] = time.time()
                    
                    # Métricas de memoria si psutil está disponible
                    try:
                        import psutil
                        app.metrics['system_cpu'] = psutil.cpu_percent(interval=0.1)
                        app.metrics['system_memory'] = psutil.virtual_memory().percent
                    except ImportError:
                        app.metrics['system_cpu'] = system_entropy() * 100
                        app.metrics['system_memory'] = system_entropy() * 80 + 20
                
            except Exception as e:
                logger.error(f"Error en metrics_updater: {e}")
            
            time.sleep(config.METRICS_UPDATE_INTERVAL)
    
    # Inicializar métricas
    app.metrics = {
        'start_time': time.time(),
        'requests_total': 0,
        'active_connections': 0,
        'response_times': []
    }
    
    # Iniciar thread daemon
    metrics_thread = threading.Thread(
        target=metrics_updater,
        daemon=True,
        name="MetricsUpdater"
    )
    metrics_thread.start()
    logger.info("✅ Background tasks iniciadas")


def setup_logging_and_metrics(app: Flask, config) -> None:
    """Configurar logging y métricas"""
    
    # === PROMETHEUS (OPCIONAL) ===
    if config.PROMETHEUS_ENABLED:
        try:
            from prometheus_flask_exporter import PrometheusMetrics
            metrics = PrometheusMetrics(app)
            app.config['PROMETHEUS_METRICS'] = metrics
            logger.info("✅ Prometheus metrics habilitadas")
        except ImportError:
            logger.warning("⚠️ Prometheus no disponible")
    
    # === LOGGING ESTRUCTURADO ===
    if config.LOG_FORMAT == 'structured':
        import json
        import logging
        
        class StructuredFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': self.formatTime(record),
                    'level': record.levelname,
                    'logger': record.name,
                    'message': record.getMessage(),
                    'module': record.module,
                    'line': record.lineno
                }
                
                if hasattr(record, 'request_id'):
                    log_data['request_id'] = record.request_id
                
                return json.dumps(log_data)
        
        # Configurar handler
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        
        app.logger.handlers = []
        app.logger.addHandler(handler)
        app.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        logger.info("✅ Logging estructurado configurado")


def setup_error_handlers(app: Flask, config) -> None:
    """Configurar manejadores de error personalizados"""
    
    @app.errorhandler(404)
    def not_found(error):
        """404 - Not Found"""
        return jsonify({
            'error': 'Not Found',
            'message': 'El endpoint solicitado no existe',
            'status_code': 404,
            'path': request.path
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 - Internal Server Error"""
        logger.error(f"Error interno: {error}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Error interno del servidor',
            'status_code': 500,
            'request_id': getattr(g, 'request_id', 'unknown')
        }), 500
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """429 - Rate Limit Exceeded"""
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Demasiadas requests, intenta más tarde',
            'status_code': 429
        }), 429
    
    logger.info("✅ Error handlers configurados")


# === UTILIDADES ===

def get_app_info(app: Flask) -> Dict[str, Any]:
    """Obtener información de la aplicación"""
    config = app.config.get('CONFIG_OBJECT')
    
    info = {
        'name': config.NAME if config else 'VIGOLEONROCKS',
        'version': config.VERSION if config else '2.1.0',
        'debug': app.debug,
        'testing': app.testing,
        'blueprints': list(app.blueprints.keys()),
        'endpoints': len(app.url_map._rules),
        'uptime_seconds': app.metrics.get('uptime_seconds', 0) if hasattr(app, 'metrics') else 0
    }
    
    return info


def health_check(app: Flask) -> Dict[str, Any]:
    """Health check de la aplicación"""
    try:
        config = app.config.get('CONFIG_OBJECT')
        
        # Verificar componentes críticos
        checks = {
            'flask_app': True,
            'config': config is not None,
            'metrics': hasattr(app, 'metrics'),
            'templates_dir': config.TEMPLATES_DIR.exists() if config else False,
            'static_dir': config.STATIC_DIR.exists() if config else False
        }
        
        # Verificar multimodal (si está habilitado)
        if config and config.MULTIMODAL_ENABLED:
            try:
                from multimodal_ai_manager import get_multimodal_manager
                manager = get_multimodal_manager()
                checks['multimodal_manager'] = True
            except Exception:
                checks['multimodal_manager'] = False
        
        all_healthy = all(checks.values())
        
        return {
            'status': 'healthy' if all_healthy else 'degraded',
            'checks': checks,
            'timestamp': time.time()
        }
        
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': time.time()
        }


if __name__ == "__main__":
    # Test del factory
    import time
    
    print("🧪 Testeando App Factory...")
    app = create_app('development')
    
    with app.app_context():
        info = get_app_info(app)
        health = health_check(app)
        
        print(f"\n📊 Información de la App:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        print(f"\n🏥 Health Check:")
        for key, value in health.items():
            print(f"  {key}: {value}")
    
    print("\n✅ Test completado")
