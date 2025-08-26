"""
Transmutador de errores cuántico
Convierte errores en oportunidades usando resonancia poética
"""

from typing import Dict, Any
from .base import QuantumBase, QuantumError
from .quantum_frequency import QuantumFrequency

class QuantumErrorTransmuter(QuantumBase):
    """
    Transmuta errores en oportunidades usando:
    - Frecuencias poéticas
    - Matriz LOG7919
    - Resonancia cuántica
    """

    def __init__(self, frequency: float = 7919):
        super().__init__(frequency)
        self.frequency_gen = QuantumFrequency(frequency)
        self.transmutation_history = []

    def transmute(
        self, 
        error: Exception,
        context: str = None,
        poet: str = 'FERREL'
    ) -> Dict[str, Any]:
        """
        Transmuta un error en una oportunidad de mejora
        usando resonancia poética
        """
        try:
            # Generar frecuencia del error
            error_freq = self.frequency_gen.generate_quantum_frequency(
                str(error),
                poet
            )

            # Obtener frecuencia poética base
            poet_freq = self.frequency_gen.get_poet_frequency(poet)

            # Calcular resonancia
            resonance = self.frequency_gen.calculate_resonance(
                error_freq,
                poet_freq
            )

            # Generar patrón de resonancia
            pattern = self.frequency_gen.generate_resonance_pattern(
                8,  # Longitud del patrón
                str(error)
            )

            # Transmutación basada en resonancia
            improvement = self._generate_improvement(
                error,
                resonance,
                context
            )

            # Actualizar estado cuántico
            self.quantum_state.update({
                'resonance': resonance,
                'poet_influence': poet,
                'coherence': min(1.0, resonance * 1.618034)
            })

            # Guardar en historial
            result = {
                'original_error': str(error),
                'improvement': improvement,
                'quantum_state': self.get_quantum_state(),
                'error_frequency': error_freq,
                'resonance_pattern': pattern,
                'context': context
            }
            self.transmutation_history.append(result)

            return result

        except Exception as e:
            raise QuantumError(
                f"Error en transmutación: {str(e)}",
                self.quantum_state
            )

    def _generate_improvement(
        self,
        error: Exception,
        resonance: float,
        context: str = None
    ) -> str:
        """
        Genera una mejora basada en la resonancia
        y el contexto del error
        """
        # Alta resonancia -> Oportunidad clara
        if resonance > 0.7:
            return self._get_enhancement_suggestion(error, context)
        
        # Resonancia media -> Punto de aprendizaje
        elif resonance > 0.3:
            return self._get_learning_point(error, context)
        
        # Baja resonancia -> Área de investigación
        else:
            return self._get_investigation_area(error, context)

    def _get_enhancement_suggestion(
        self,
        error: Exception,
        context: str
    ) -> str:
        """Genera sugerencia de mejora específica"""
        error_type = type(error).__name__
        error_msg = str(error)
        ctx = f" en {context}" if context else ""

        if "timeout" in error_msg.lower():
            return (
                f"Oportunidad de mejora{ctx}: "
                "Implementar sistema de retry con backoff exponencial"
            )
        elif "connection" in error_msg.lower():
            return (
                f"Oportunidad de mejora{ctx}: "
                "Establecer pool de conexiones con health checks"
            )
        elif "memory" in error_msg.lower():
            return (
                f"Oportunidad de mejora{ctx}: "
                "Optimizar uso de memoria con streaming de datos"
            )
        else:
            return (
                f"Oportunidad de mejora{ctx}: "
                f"Revisar manejo de errores {error_type}"
            )

    def _get_learning_point(
        self,
        error: Exception,
        context: str
    ) -> str:
        """Genera punto de aprendizaje"""
        ctx = f" en {context}" if context else ""
        return (
            f"Punto de aprendizaje{ctx}: "
            f"Analizar comportamiento ante {str(error)}"
        )

    def _get_investigation_area(
        self,
        error: Exception,
        context: str
    ) -> str:
        """Genera área de investigación"""
        ctx = f" en {context}" if context else ""
        return (
            f"Área de investigación{ctx}: "
            f"Estudiar causas raíz de {str(error)}"
        )

    def get_quantum_state(self) -> Dict[str, Any]:
        """
        Obtiene estado cuántico incluyendo
        estadísticas de transmutación
        """
        state = super().get_quantum_state()
        state.update({
            'transmutations': len(self.transmutation_history),
            'avg_resonance': self._calculate_avg_resonance()
        })
        return state

    def _calculate_avg_resonance(self) -> float:
        """Calcula resonancia promedio del historial"""
        if not self.transmutation_history:
            return 0.0
            
        total = sum(
            t['quantum_state']['resonance']
            for t in self.transmutation_history
        )
        return total / len(self.transmutation_history)

    def clear_history(self):
        """Limpia el historial de transmutaciones"""
        self.transmutation_history.clear()

    def get_history(self) -> list:
        """Obtiene historial de transmutaciones"""
        return self.transmutation_history.copy()