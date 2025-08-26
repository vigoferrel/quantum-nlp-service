"""
Base del sistema cuántico
Define la estructura fundamental y los tipos base
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class QuantumBase(ABC):
    """Base para todos los componentes cuánticos"""
    
    def __init__(self, frequency: float = 7919):
        self.base_frequency = frequency
        self.quantum_state = {
            'coherence': 1.0,
            'resonance': frequency,
            'poet_influence': None,
            'context_depth': 10
        }

    @abstractmethod
    def get_quantum_state(self) -> Dict[str, Any]:
        """Retorna el estado cuántico actual"""
        pass

    @abstractmethod
    def calculate_resonance(self, input_data: Any) -> float:
        """Calcula la resonancia cuántica para un input"""
        pass

    def _apply_log7919(self, value: int) -> float:
        """Aplica la matriz LOG7919 a un valor"""
        return (value % self.base_frequency) / self.base_frequency

class BaseTool(QuantumBase):
    """Base para todas las herramientas cuánticas"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre de la herramienta"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descripción detallada"""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """Esquema de entrada en formato JSON"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Ejecuta la herramienta"""
        pass

    def get_quantum_state(self) -> Dict[str, Any]:
        """Implementación base del estado cuántico"""
        return self.quantum_state

    def calculate_resonance(self, input_data: Any) -> float:
        """Implementación base del cálculo de resonancia"""
        # Calcular hash del input
        input_hash = sum(ord(c) for c in str(input_data))
        
        # Aplicar LOG7919
        resonance = self._apply_log7919(input_hash)
        
        # Actualizar estado cuántico
        self.quantum_state['resonance'] = resonance
        self.quantum_state['coherence'] = min(1.0, resonance * 1.618034)
        
        return resonance

    def to_quantum_schema(self) -> Dict[str, Any]:
        """Convierte la herramienta a esquema cuántico"""
        return {
            "type": "quantum_function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
                "quantum_state": self.get_quantum_state()
            }
        }

class QuantumError(Exception):
    """Error cuántico base"""
    
    def __init__(
        self, 
        message: str, 
        quantum_state: Dict[str, Any] = None
    ):
        super().__init__(message)
        self.quantum_state = quantum_state or {
            'coherence': 0.0,
            'resonance': 0.0,
            'poet_influence': 'PARRA',
            'context_depth': 1
        }

class QuantumValidator:
    """Validador base para componentes cuánticos"""
    
    @staticmethod
    def validate_frequency(frequency: float) -> bool:
        """Valida que una frecuencia sea válida"""
        return 0 < frequency <= 7919

    @staticmethod
    def validate_coherence(coherence: float) -> bool:
        """Valida que una coherencia sea válida"""
        return 0 <= coherence <= 1.0

    @staticmethod
    def validate_quantum_state(state: Dict[str, Any]) -> bool:
        """Valida un estado cuántico completo"""
        required_keys = ['coherence', 'resonance', 'poet_influence', 'context_depth']
        return all(key in state for key in required_keys)

class QuantumRegistry:
    """Registro global de componentes cuánticos"""
    
    _instance = None
    _components = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(
        self, 
        name: str, 
        component: Any, 
        quantum_state: Dict[str, Any]
    ):
        """Registra un nuevo componente"""
        if not QuantumValidator.validate_quantum_state(quantum_state):
            raise QuantumError("Estado cuántico inválido")
            
        self._components[name] = {
            'component': component,
            'quantum_state': quantum_state
        }

    def get(self, name: str) -> Any:
        """Obtiene un componente registrado"""
        if name not in self._components:
            raise QuantumError(f"Componente {name} no encontrado")
        return self._components[name]

    def list_components(self) -> List[str]:
        """Lista todos los componentes registrados"""
        return list(self._components.keys())

    def get_quantum_state(self, name: str) -> Dict[str, Any]:
        """Obtiene el estado cuántico de un componente"""
        return self.get(name)['quantum_state']