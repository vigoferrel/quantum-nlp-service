"""
Quantum Stateful Cache
----------------------
Una caché consciente del estado cuántico global del sistema.

A diferencia de una caché tradicional basada en TTL (Time-To-Live),
esta caché invalida sus entradas no por el tiempo, sino por cambios
significativos en la coherencia del contexto 26D al que está vinculada.
"""

import threading
import time
from typing import Dict, Any, Optional

# Dependencia del contexto para monitorear la coherencia
from .quantum_context_26d import QuantumContext26D

class QuantumStatefulCache:
    """
    Gestiona una caché que se invalida basada en la coherencia del estado cuántico.
    """

    def __init__(self, context: QuantumContext26D, coherence_threshold: float = 0.05, prewarm_interval: int = 60):
        self._cache: Dict[str, Any] = {}
        self._context = context
        self._coherence_threshold = coherence_threshold
        self._prewarm_interval = prewarm_interval
        
        # Almacena la coherencia global en el momento en que se guarda cada entrada
        self._coherence_map: Dict[str, float] = {}
        
        # Hilo para pre-calentamiento proactivo
        self._prewarmer_thread = threading.Thread(target=self._prewarm_cycle, daemon=True)
        self._stop_prewarmer = threading.Event()

    def start_prewarming(self):
        """Inicia el ciclo de pre-calentamiento de la caché."""
        if not self._prewarmer_thread.is_alive():
            self._prewarmer_thread.start()

    def stop_prewarming(self):
        """Detiene el ciclo de pre-calentamiento."""
        self._stop_prewarmer.set()

    def _prewarm_cycle(self):
        """
        Ciclo proactivo que intenta anticipar futuras necesidades
        y poblar la caché. (Lógica de simulación).
        """
        while not self._stop_prewarmer.is_set():
            time.sleep(self._prewarm_interval)
            # Simulación: pre-calienta una consulta común
            common_prompt = "Resume el estado actual del proyecto."
            cache_key = f"prewarm:{common_prompt}"
            if cache_key not in self._cache:
                # Simula una generación para esta clave
                self.set(cache_key, {"response": "Pre-warmed cache entry: Project status is nominal."})

    def set(self, key: str, value: Any):
        """
        Almacena un valor en la caché, asociándolo con la coherencia
        global actual del contexto.
        """
        current_coherence = self._context.get_quantum_state()['global_coherence']
        self._cache[key] = value
        self._coherence_map[key] = current_coherence

    def get(self, key: str) -> Optional[Any]:
        """
        Recupera un valor de la caché, pero solo si la coherencia
        del sistema no ha variado más allá de un umbral.
        """
        if key not in self._cache:
            return None

        # Comprobar la validez de la coherencia
        stored_coherence = self._coherence_map.get(key, 0)
        current_coherence = self._context.get_quantum_state()['global_coherence']
        
        coherence_drift = abs(current_coherence - stored_coherence)
        
        if coherence_drift > self._coherence_threshold:
            # La coherencia ha cambiado demasiado. La entrada es inválida.
            self.delete(key)
            return None
            
        return self._cache.get(key)

    def delete(self, key: str):
        """Elimina una entrada de la caché y de su mapa de coherencia."""
        if key in self._cache:
            del self._cache[key]
        if key in self._coherence_map:
            del self._coherence_map[key]

    def flush(self):
        """Limpia toda la caché."""
        self._cache.clear()
        self._coherence_map.clear()