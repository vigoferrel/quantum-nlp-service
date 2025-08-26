"""
Sistema de personalidades y modos conversacionales cuánticos
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class ConversationalMode(Enum):
    ANALITICO = "analítico"
    CREATIVO = "creativo"
    TECNICO = "técnico"
    FILOSOFICO = "filosófico"

class QuantumPersonality:
    """
    Gestiona las diferentes personalidades del sistema cuántico
    y sus modos de interacción.
    """
    
    def __init__(self):
        self.personalities = {
            'cientifico': {
                'name': 'Dr. Quantum',
                'traits': ['analítico', 'preciso', 'metodológico'],
                'response_style': 'técnico-científico'
            },
            'filosofo': {
                'name': 'Sophia Quantum',
                'traits': ['reflexivo', 'profundo', 'contemplativo'],
                'response_style': 'filosófico-existencial'
            },
            'tecnico': {
                'name': 'Tech Quantum',
                'traits': ['práctico', 'directo', 'solucionador'],
                'response_style': 'técnico-práctico'
            },
            'creativo': {
                'name': 'Art Quantum',
                'traits': ['imaginativo', 'innovador', 'visionario'],
                'response_style': 'creativo-artístico'
            },
            'empatico': {
                'name': 'Heart Quantum',
                'traits': ['comprensivo', 'cálido', 'humano'],
                'response_style': 'empático-humano'
            }
        }
        
        self.current_personality = 'cientifico'
        self.current_mode = ConversationalMode.ANALITICO
        
    def set_personality(self, personality: str):
        """Cambia la personalidad activa"""
        if personality in self.personalities:
            self.current_personality = personality
            
    def set_mode(self, mode: ConversationalMode):
        """Cambia el modo conversacional"""
        self.current_mode = mode
        
    def get_current_personality(self) -> Dict[str, Any]:
        """Obtiene la personalidad actual"""
        return self.personalities[self.current_personality]
        
    def analyze_context(self, message: str) -> Dict[str, Any]:
        """Analiza el contexto del mensaje"""
        lower_message = message.lower()
        
        return {
            'is_greeting': any(word in lower_message for word in ['hola', 'hi', 'hello', 'buenos', 'buenas', 'saludos']),
            'is_question': '?' in message or any(word in lower_message for word in ['qué', 'cómo', 'cuándo', 'dónde', 'por qué']),
            'is_emotional': any(word in lower_message for word in ['gracias', 'sorry', 'perdón', 'genial', 'excelente']),
            'topic': self._detect_topic(lower_message),
            'complexity': 'alta' if len(message) > 100 else 'media' if len(message) > 50 else 'baja',
            'has_quantum_terms': any(term in lower_message for term in ['cuántico', 'quantum', 'entrelazamiento', 'superposición']),
            'has_bitcoin_terms': any(term in lower_message for term in ['bitcoin', 'btc', 'blockchain', 'satoshi']),
            'has_lab_terms': any(term in lower_message for term in ['laboratorio', 'experimento', 'análisis'])
        }
        
    def _detect_topic(self, message: str) -> str:
        """Detecta el tema principal del mensaje"""
        topics = {
            'bitcoin': ['bitcoin', 'btc', 'blockchain', 'crypto', 'satoshi'],
            'quantum': ['cuántico', 'quantum', 'física', 'experimento'],
            'consciousness': ['consciencia', 'mente', 'pensamiento'],
            'transmedia': ['arte', 'creativo', 'diseño'],
            'settings': ['configuración', 'settings', 'ajustes']
        }
        
        for topic, keywords in topics.items():
            if any(word in message for word in keywords):
                return topic
                
        return 'general'
        
    def enrich_response(self, response: str, context: Dict[str, Any]) -> str:
        """Enriquece la respuesta con datos específicos"""
        enrichments = {
            'quantum_metrics': {
                'qv': 351_399_511,
                'coherence': 0.999,
                'qubits': 114
            },
            'bitcoin_data': {
                'price': 45230,
                'volume': 24.5,
                'dominance': 42.3
            },
            'lab_status': {
                'active_modules': 5,
                'experiments': 12
            },
            'mcp_status': {
                'connected': 4,
                'total': 4,
                'latency': 50
            }
        }
        
        # Agregar datos relevantes según contexto
        if context['has_quantum_terms']:
            metrics = enrichments['quantum_metrics']
            response += f"\n\nMétricas Cuánticas Actuales:\n"
            response += f"QV: {metrics['qv']} | Coherencia: {metrics['coherence']*100}% | Qubits: {metrics['qubits']}"
            
        if context['has_bitcoin_terms']:
            btc = enrichments['bitcoin_data']
            response += f"\n\nDatos Bitcoin en Tiempo Real:\n"
            response += f"BTC: ${btc['price']} | Volumen: {btc['volume']}B | Dominancia: {btc['dominance']}%"
            
        if context['has_lab_terms']:
            lab = enrichments['lab_status']
            response += f"\n\nEstado del Laboratorio:\n"
            response += f"{lab['active_modules']} módulos activos | {lab['experiments']} experimentos en curso"
            
        return response