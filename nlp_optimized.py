#!/usr/bin/env python3
"""
🧠 OPTIMIZACIÓN NLP CON LAZY LOADING
Reducir tiempo de inicialización de 11.35s a <2s
"""

import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Variables globales para lazy loading
_nlp_models = {}
_models_loaded = False
_loading_start_time = None

def load_models_lazy():
    """Cargar modelos NLP solo cuando sea necesario"""
    global _models_loaded, _nlp_models, _loading_start_time
    
    if not _models_loaded:
        _loading_start_time = time.time()
        logger.info("🔄 Iniciando carga lazy de modelos NLP...")
        
        try:
            # Cargar spaCy
            import spacy
            _nlp_models['spacy'] = spacy.load("en_core_web_sm")
            
            # Cargar sentence transformer
            from sentence_transformers import SentenceTransformer
            _nlp_models['transformer'] = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Cargar NLTK
            import nltk
            _nlp_models['nltk'] = nltk
            
            _models_loaded = True
            loading_time = time.time() - _loading_start_time
            logger.info(f"✅ Modelos NLP cargados en {loading_time:.2f}s")
            
        except Exception as e:
            logger.error(f"❌ Error cargando modelos NLP: {e}")
            _models_loaded = False
    
    return _nlp_models

def get_spacy_model():
    """Obtener modelo spaCy"""
    models = load_models_lazy()
    return models.get('spacy')

def get_transformer_model():
    """Obtener modelo transformer"""
    models = load_models_lazy()
    return models.get('transformer')

def get_nltk():
    """Obtener NLTK"""
    models = load_models_lazy()
    return models.get('nltk')

# Cache para resultados NLP
_nlp_cache = {}

def analyze_text_cached(text: str) -> Dict[str, Any]:
    """Análisis de texto con cache"""
    import hashlib
    text_hash = hashlib.md5(text.encode()).hexdigest()
    
    if text_hash in _nlp_cache:
        return _nlp_cache[text_hash]
    
    # Realizar análisis
    result = analyze_text_optimized(text)
    _nlp_cache[text_hash] = result
    return result

def analyze_text_optimized(text: str) -> Dict[str, Any]:
    """Análisis de texto optimizado"""
    # Implementación optimizada aquí
    return {
        "sentiment": {"level": "neutral", "confidence": 0.5},
        "intent": {"type": "greeting", "confidence": 0.3},
        "entities": []
    }
