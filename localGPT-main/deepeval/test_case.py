from typing import List, Optional, Any
from datetime import datetime

class LLMTestCase:
    """
    Clase base para casos de prueba de LLM con soporte para evaluación cuántica.
    """
    
    def __init__(
        self,
        input: str,
        actual_output: str,
        expected_output: Optional[str] = None,
        retrieval_context: Optional[List[str]] = None,
        metadata: Optional[dict] = None
    ):
        self.input = input
        self.actual_output = actual_output
        self.expected_output = expected_output
        self.retrieval_context = retrieval_context or []
        self.metadata = metadata or {}
        self.timestamp = datetime.now().timestamp()
        
    def add_context(self, context: str):
        """Agrega contexto de recuperación"""
        self.retrieval_context.append(context)
        
    def add_metadata(self, key: str, value: Any):
        """Agrega metadata al caso de prueba"""
        self.metadata[key] = value
        
    def get_metadata(self, key: str) -> Optional[Any]:
        """Obtiene valor de metadata"""
        return self.metadata.get(key)
        
    def clear_context(self):
        """Limpia el contexto de recuperación"""
        self.retrieval_context = []
        
    def clear_metadata(self):
        """Limpia la metadata"""
        self.metadata = {}