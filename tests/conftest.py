"""
Configuración global de testing para quantum-nlp-service
VIGOLEONROCKS Testing Framework
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch
from flask import Flask

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuración de entorno de testing
os.environ['TESTING'] = 'true'
os.environ['FLASK_ENV'] = 'testing'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

@pytest.fixture(scope="session")
def app():
    """Fixture de la aplicación Flask para testing"""
    from vigoleonrocks.interfaces.rest_api import app
    
    # Configuración específica para testing
    app.config.update({
        'TESTING': True,
        'DEBUG': False,
        'SECRET_KEY': 'test-key-quantum-nlp',
        'WTF_CSRF_ENABLED': False
    })
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Cliente de pruebas Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de comandos CLI"""
    return app.test_cli_runner()

@pytest.fixture
def vigoleonrocks_server():
    """Mock del servidor VIGOLEONROCKS"""
    with patch('vigoleonrocks.interfaces.rest_api.VIGOLEONROCKSServer') as mock:
        server_instance = MagicMock()
        server_instance.start_time = 1234567890.0
        server_instance.request_count = 0
        server_instance.current_profile = 'human'
        server_instance.quantum_states = 26
        server_instance.interaction_history = []
        
        # Mock de métodos críticos
        server_instance.process_query.return_value = {
            'response': 'Test response',
            'language': 'es',
            'processing_time': 10.0,
            'profile': 'human',
            'quantum_states': 26
        }
        
        server_instance.detect_language.return_value = 'es'
        server_instance.generate_human_response.return_value = 'Test human response'
        
        mock.return_value = server_instance
        yield server_instance

@pytest.fixture
def metrics_based_rng():
    """Mock del RNG basado en métricas (CRÍTICO para política de aleatoriedad)"""
    class MetricsBasedRNG:
        def __init__(self):
            self.seed = 12345  # Seed determinística para testing
        
        def integers(self, low, high, size=None):
            """Mock de generación de enteros basado en métricas"""
            if size:
                return [42] * size  # Valores determinísticos para testing
            return 42
        
        def choice(self, choices):
            """Mock de selección basada en métricas"""
            return choices[0] if choices else None
        
        def uniform(self, low=0.0, high=1.0, size=None):
            """Mock de números uniformes basado en métricas"""
            if size:
                return [0.5] * size
            return 0.5
    
    return MetricsBasedRNG()

@pytest.fixture
def multilingual_responses():
    """Fixture con respuestas multilingües para testing"""
    return {
        'es': {
            'greeting': 'Hola! ¿En qué puedo ayudarte?',
            'goodbye': 'Hasta luego!',
            'error': 'Ocurrió un error'
        },
        'en': {
            'greeting': 'Hello! How can I help you?',
            'goodbye': 'Goodbye!',
            'error': 'An error occurred'
        },
        'pt': {
            'greeting': 'Olá! Como posso te ajudar?',
            'goodbye': 'Até logo!',
            'error': 'Ocorreu um erro'
        }
    }
