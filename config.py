#!/usr/bin/env python3
"""
🔧 VIGOLEONROCKS - Configuración Simplificada
Sistema multimodal de IA - Configuración enfocada sin características irrelevantes
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

class BaseConfig:
    """Configuración base del sistema multimodal VIGOLEONROCKS"""
    
    # === INFORMACIÓN DEL SISTEMA ===
    VERSION = "2.1.0"
    NAME = "VIGOLEONROCKS"
    DESCRIPTION = "Sistema Multimodal de IA Avanzada"
    
    # === CONFIGURACIÓN FLASK ===
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DEBUG = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    TESTING = False
    
    # === RED Y SERVIDOR ===
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    WORKERS = int(os.environ.get('WORKERS', 4))
    
    # === DIRECTORIOS ===
    BASE_DIR = Path(__file__).parent.absolute()
    TEMPLATES_DIR = BASE_DIR / 'templates'
    STATIC_DIR = BASE_DIR / 'static'
    LOGS_DIR = BASE_DIR / 'logs'
    DIAGNOSTICS_DIR = BASE_DIR / 'diagnostics'
    
    # === SISTEMA DE ENTROPÍA (POLÍTICA: NO Math.random) ===
    USE_SYSTEM_ENTROPY = True
    ENTROPY_SOURCE = 'system'
    
    # === EJECUCIÓN EN BACKGROUND (POLÍTICA REQUERIDA) ===
    BACKGROUND_EXECUTION = os.environ.get('BACKGROUND_EXECUTION', 'true').lower() == 'true'
    DAEMON_THREADS = True
    METRICS_UPDATE_INTERVAL = int(os.environ.get('METRICS_UPDATE_INTERVAL', 5))
    
    # === MULTIMODAL (PROPÓSITO PRINCIPAL) ===
    MULTIMODAL_ENABLED = os.environ.get('MULTIMODAL_ENABLED', 'true').lower() == 'true'
    DEVICE = os.environ.get('DEVICE', 'auto')
    MODEL_CACHE_DIR = os.environ.get('MODEL_CACHE_DIR', str(BASE_DIR / 'models'))
    CLIP_ENABLED = os.environ.get('CLIP_ENABLED', 'true').lower() == 'true'
    
    # === MODELOS DE IA DISPONIBLES ===
    ENABLED_MODELS = {
        'moondream2': os.environ.get('ENABLE_MOONDREAM2', 'true').lower() == 'true',
        'florence2': os.environ.get('ENABLE_FLORENCE2', 'true').lower() == 'true', 
        'qwen2_vl': os.environ.get('ENABLE_QWEN2_VL', 'true').lower() == 'true',
        'whisper_large': os.environ.get('ENABLE_WHISPER_LARGE', 'false').lower() == 'true',
        'whisper_medium': os.environ.get('ENABLE_WHISPER_MEDIUM', 'true').lower() == 'true',
        'clip_vit': os.environ.get('ENABLE_CLIP_VIT', 'true').lower() == 'true',
        'blip2': os.environ.get('ENABLE_BLIP2', 'true').lower() == 'true'
    }
    
    # === PROCESAMIENTO MULTIMODAL ===
    AUDIO_PROCESSING_ENABLED = os.environ.get('AUDIO_PROCESSING', 'auto').lower()
    VIDEO_PROCESSING_ENABLED = os.environ.get('VIDEO_PROCESSING', 'auto').lower()
    
    # === CACHE Y PERFORMANCE ===
    CACHE_ENABLED = os.environ.get('CACHE_ENABLED', 'true').lower() == 'true'
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'memory')
    CACHE_TTL = int(os.environ.get('CACHE_TTL', 3600))
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # === MÉTRICAS Y MONITOREO ===
    PROMETHEUS_ENABLED = os.environ.get('PROMETHEUS_ENABLED', 'true').lower() == 'true'
    METRICS_ENABLED = True
    HEALTHCHECK_ENABLED = True
    
    # === LOGGING ===
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.environ.get('LOG_FORMAT', 'structured')
    LOG_TO_FILE = os.environ.get('LOG_TO_FILE', 'true').lower() == 'true'
    
    # === SEGURIDAD ===
    CORS_ENABLED = os.environ.get('CORS_ENABLED', 'true').lower() == 'true'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    RATE_LIMITING_ENABLED = os.environ.get('RATE_LIMITING', 'true').lower() == 'true'
    MAX_REQUESTS_PER_MINUTE = int(os.environ.get('MAX_REQUESTS_PER_MINUTE', 60))
    
    # === API v2 ===
    API_V2_ENABLED = True
    API_V2_PREFIX = '/api/v2'
    OPENAPI_ENABLED = os.environ.get('OPENAPI_ENABLED', 'true').lower() == 'true'
    SWAGGER_UI_ENABLED = os.environ.get('SWAGGER_UI_ENABLED', 'true').lower() == 'true'
    
    @classmethod
    def init_directories(cls):
        """Crear directorios necesarios"""
        directories = [
            cls.LOGS_DIR,
            cls.DIAGNOSTICS_DIR, 
            cls.TEMPLATES_DIR,
            cls.STATIC_DIR,
            cls.STATIC_DIR / 'css',
            cls.STATIC_DIR / 'js',
        ]
        
        if cls.MODEL_CACHE_DIR:
            directories.append(Path(cls.MODEL_CACHE_DIR))
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validar configuración del sistema multimodal"""
        issues = []
        
        if not cls.BASE_DIR.exists():
            issues.append("BASE_DIR no existe")
        
        if not cls.USE_SYSTEM_ENTROPY:
            issues.append("Sistema debe usar entropía del sistema (política)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'config_summary': {
                'version': cls.VERSION,
                'debug': cls.DEBUG,
                'multimodal_enabled': cls.MULTIMODAL_ENABLED,
                'cache_enabled': cls.CACHE_ENABLED,
                'background_execution': cls.BACKGROUND_EXECUTION
            }
        }


class DevelopmentConfig(BaseConfig):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(BaseConfig):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    MAX_REQUESTS_PER_MINUTE = 30


class TestingConfig(BaseConfig):
    """Configuración para pruebas"""
    DEBUG = True
    TESTING = True
    CACHE_TYPE = 'memory'


# === FACTORY DE CONFIGURACIÓN ===
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(environment: Optional[str] = None) -> BaseConfig:
    """Obtener configuración según el entorno"""
    if environment is None:
        environment = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(environment.lower(), DevelopmentConfig)


def print_config_summary(config: BaseConfig):
    """Imprimir resumen enfocado"""
    print(f"\n🔧 {config.NAME} v{config.VERSION} - Sistema Multimodal")
    print("=" * 60)
    print(f"Entorno: {config.__class__.__name__}")
    print(f"Debug: {config.DEBUG}")
    print(f"Host: {config.HOST}:{config.PORT}")
    print(f"Multimodal: {config.MULTIMODAL_ENABLED}")
    print(f"CLIP: {config.CLIP_ENABLED}")
    print(f"Cache: {config.CACHE_ENABLED} ({config.CACHE_TYPE})")
    print(f"Background: {config.BACKGROUND_EXECUTION}")
    print(f"Prometheus: {config.PROMETHEUS_ENABLED}")
    print("=" * 60)

def setup_system_entropy():
    """Configurar generación de entropía del sistema (cumple política)"""
    import secrets
    import time
    
    def get_system_entropy():
        """Generar entropía usando fuentes del sistema (NO Math.random)"""
        entropy_sources = [
            secrets.randbits(64),
            time.time_ns(),
            hash(str(os.getpid())),
            os.urandom(8)
        ]
        
        combined = 0
        for source in entropy_sources:
            if isinstance(source, bytes):
                source = int.from_bytes(source, 'big')
            combined ^= source
        
        return abs(combined % 100) / 100.0
    
    return get_system_entropy

# Configurar entropía del sistema
system_entropy = setup_system_entropy()

if __name__ == "__main__":
    config = get_config()
    validation = config.validate_config()
    
    print_config_summary(config)
    print(f"\nValidación: {'✅' if validation['valid'] else '❌'}")
    
    if validation['issues']:
        print("Issues encontrados:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    
    print(f"\nEntropía del sistema: {system_entropy():.4f}")
    print("\n✅ Configuración enfocada en sistema multimodal")
