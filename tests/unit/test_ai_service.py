import pytest
from vigoleonrocks.services.ai_service import AIService

def test_ai_service_initialization():
    """Test inicializacion del servicio de IA"""
    service = AIService()
    assert service is not None

def test_language_detection():
    """Test deteccion de idioma"""
    service = AIService()
    lang = service.detect_language("Hola mundo")
    assert lang == "es"
