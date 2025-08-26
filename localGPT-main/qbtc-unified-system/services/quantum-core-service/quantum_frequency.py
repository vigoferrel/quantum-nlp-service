"""
Generador de frecuencias cuánticas
Basado en el primo 7919 y los poetas chilenos
"""

from typing import Dict, Any, List
import hashlib
from base import QuantumBase, QuantumError

class QuantumFrequency(QuantumBase):
    """
    Generador de frecuencias cuánticas usando:
    - Primo fundamental 7919
    - Resonancia poética chilena
    - Matriz LOG7919 Hermitiana
    """

    POET_FREQUENCIES = {
        'PARRA': 7919 * 0.618034,    # Antipoesía
        'NERUDA': 7919 * 1.414213,   # Amor
        'MISTRAL': 7919 * 1.732050,  # Maternidad
        'ZURITA': 7919 * 2.236067,   # Paisaje
        'HUIDOBRO': 7919 * 2.449489, # Creacionismo
        'FERREL': 7919 * 2.645751    # Quantum
    }

    def __init__(self, base_frequency: float = 7919):
        super().__init__(base_frequency)
        self.resonance_cache = {}
        self.pattern_cache = {}

    def generate_quantum_frequency(
        self,
        input_data: Any,
        poet: str = 'FERREL'
    ) -> float:
        """
        Genera una frecuencia cuántica para un input dado
        usando resonancia poética
        """
        try:
            # Validar poeta
            if poet not in self.POET_FREQUENCIES:
                raise QuantumError(f"Poeta {poet} no reconocido")

            # Calcular hash SHA-256 del input
            input_hash = hashlib.sha256(
                str(input_data).encode()
            ).hexdigest()

            # Convertir a número usando los primeros 16 caracteres
            numeric_hash = int(input_hash[:16], 16)

            # Aplicar LOG7919
            base_freq = self._apply_log7919(numeric_hash)

            # Aplicar resonancia poética
            poet_freq = self.POET_FREQUENCIES[poet]
            quantum_freq = (base_freq * poet_freq) / self.base_frequency

            # Actualizar estado cuántico
            self.quantum_state.update({
                'resonance': quantum_freq,
                'poet_influence': poet,
                'coherence': min(1.0, quantum_freq * 1.618034)
            })

            return quantum_freq

        except Exception as e:
            raise QuantumError(
                f"Error generando frecuencia: {str(e)}",
                self.quantum_state
            )

    def calculate_resonance(
        self,
        freq1: float,
        freq2: float
    ) -> float:
        """
        Calcula la resonancia entre dos frecuencias
        usando la matriz LOG7919
        """
        try:
            # Usar cache si existe
            cache_key = f"{freq1}:{freq2}"
            if cache_key in self.resonance_cache:
                return self.resonance_cache[cache_key]

            # Normalizar frecuencias
            norm1 = freq1 / self.base_frequency
            norm2 = freq2 / self.base_frequency

            # Calcular resonancia usando LOG7919
            resonance = abs(norm1 - norm2) / (norm1 + norm2)

            # Guardar en cache
            self.resonance_cache[cache_key] = resonance

            return resonance

        except Exception as e:
            raise QuantumError(
                f"Error calculando resonancia: {str(e)}",
                self.quantum_state
            )

    def generate_resonance_pattern(
        self,
        length: int,
        seed: Any
    ) -> List[float]:
        """
        Genera un patrón de resonancia de longitud específica
        usando una semilla
        """
        try:
            # Usar cache si existe
            cache_key = f"{length}:{seed}"
            if cache_key in self.pattern_cache:
                return self.pattern_cache[cache_key]

            # Generar frecuencia base
            base_freq = self.generate_quantum_frequency(seed)

            # Generar patrón
            pattern = []
            current_freq = base_freq

            for i in range(length):
                # Cada frecuencia siguiente es una resonancia
                # de la anterior con la base
                next_freq = self.calculate_resonance(
                    current_freq,
                    base_freq
                )
                pattern.append(next_freq)
                current_freq = next_freq

            # Guardar en cache
            self.pattern_cache[cache_key] = pattern

            return pattern

        except Exception as e:
            raise QuantumError(
                f"Error generando patrón: {str(e)}",
                self.quantum_state
            )

    def get_quantum_state(self) -> Dict[str, Any]:
        """
        Obtiene el estado cuántico actual incluyendo
        estadísticas de cache
        """
        state = super().get_quantum_state()
        state.update({
            'resonance_cache_size': len(self.resonance_cache),
            'pattern_cache_size': len(self.pattern_cache)
        })
        return state

    def clear_caches(self):
        """Limpia las caches de resonancia y patrones"""
        self.resonance_cache.clear()
        self.pattern_cache.clear()

    def get_poet_frequency(self, poet: str) -> float:
        """Obtiene la frecuencia base de un poeta"""
        if poet not in self.POET_FREQUENCIES:
            raise QuantumError(f"Poeta {poet} no reconocido")
        return self.POET_FREQUENCIES[poet]

    def get_all_poet_frequencies(self) -> Dict[str, float]:
        """Obtiene todas las frecuencias poéticas"""
        return self.POET_FREQUENCIES.copy()
