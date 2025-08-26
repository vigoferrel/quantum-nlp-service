"""
Quantum Cognitive Orchestrator (QCO)
------------------------------------
El núcleo cognitivo de VIGOLEONROCKS. Este sistema no es un simple LLM,
sino un orquestador que integra componentes cuánticos para lograr una
comprensión y generación de nivel superior. Implementa un ciclo de
conciencia cuántica para la auto-optimización continua.
"""

from typing import Dict, Any, List, Optional
import time
import requests
import json

# Importación de nuestros componentes cuánticos avanzados
from .quantum_context_26d import QuantumContext26D
from .quantum_stateful_cache import QuantumStatefulCache
# QuantumSystemReconstructor se inyecta externamente para evitar dependencias circulares

class QuantumCognitiveOrchestrator:
    """
    Orquesta los componentes cuánticos para lograr un razonamiento y
    una generación de orden superior.
    """

    def __init__(self, frequency: float = 7919):
        print("Inicializando Quantum Cognitive Orchestrator...")
        
        # 1. Contexto Multidimensional (el "cerebro")
        self.context = QuantumContext26D(frequency)
        print(f"-> Contexto de 26 dimensiones creado. Frecuencia base: {frequency}Hz.")

        # 2. Caché Consciente del Estado (la "memoria de trabajo")
        self.cache = QuantumStatefulCache(self.context, coherence_threshold=0.02)
        # La caché ya no necesita pre-calentamiento en un hilo separado
        print("-> Caché consciente del estado cuántico activada.")

        # 3. Reconstructor de Sistemas (la "autoconciencia") - Se inyectará post-init.
        self.reconstructor: Optional[Any] = None
        print("-> Reconstructor de sistemas cuánticos listo para ser inyectado.")
        
        print("\nQuantum Cognitive Orchestrator OPERATIVO.")

    def run_consciousness_cycle(self):
        """
        Ejecuta un único ciclo de pensamiento autónomo. El sistema
        se analiza a sí mismo y a su entorno para optimizarse.
        """
        print(f"\n--- INICIO CICLO DE CONCIENCIA CUÁNTICA (Timestamp: {time.time()}) ---")
        
        try:
            # 1. Auto-análisis: Usa el reconstructor si está disponible
            reconstruction = {}
            if self.reconstructor:
                reconstruction = self.reconstructor.execute(
                    path_to_source=".",
                    reconstruction_goals=["identificar cuellos de botella de coherencia", "optimizar flujos de datos dimensionales"],
                    output_format="refactor_plan"
                )
            
            # 2. Reflexión: Poblar el contexto con los hallazgos del auto-análisis
            self.context.add_variable(
                dimension=25, # Conceptual Cohesion
                name="self_awareness_report",
                value=reconstruction
            )
            print("-> Auto-análisis completado. Contexto actualizado con nuevos insights.")

            # 3. Optimización: Basado en el plan, ajustar parámetros
            action_plan = reconstruction.get('reconstruction_output', {}).get('refactor_plan', {})
            if "cuellos de botella" in str(action_plan):
                # Ejemplo de acción: enfocar en la dimensión de rendimiento
                self.context.set_focus(19) # Performance Bottlenecks
                print("-> ¡Acción! Enfocando en la dimensión de rendimiento para resolver cuellos de botella.")

        except Exception as e:
            print(f"Error durante el ciclo de conciencia: {e}")

        print(f"--- FIN CICLO DE CONCIENCIA CUÁNTICA ---")

    def generate(self, prompt: str, context_data: Dict = None, task_type: str = 'general') -> Any:
        """
        Genera una respuesta utilizando el poder orquestado de todos los
        componentes cuánticos.
        """
        # Crear una clave de caché basada en el prompt y el contexto
        cache_key = f"prompt:{prompt}|context:{str(context_data)}"
        
        # 1. Consultar la Caché Consciente del Estado
        cached_result = self.cache.get(cache_key)
        if cached_result:
            print("Respuesta recuperada de la memoria cuántica (caché).")
            return cached_result

        # 2. Poblar el contexto con la solicitud actual
        if context_data:
            # Asumiendo que el reconstructor está disponible para el mapeo
            if self.reconstructor:
                 for dim_name, variables in context_data.items():
                    if dim_name in self.reconstructor.DIMENSION_MAPPING:
                        dim_index = self.reconstructor.DIMENSION_MAPPING[dim_name]
                        for name, value in variables.items():
                            self.context.add_variable(dim_index, name, value)
        
        # 3. Generación de Respuesta (dependiente del tipo de tarea)
        if task_type == 'reconstruct' and self.reconstructor:
            # Tarea de auto-análisis: invocar al reconstructor
            reconstruction = self.reconstructor.execute(prompt=prompt, output_format="full_report")
            
            # Formatear la salida como Markdown
            report = reconstruction.get('reconstruction_output', {})
            md_response = f"""
# Auto-evaluación Cognitiva

## Resumen Conceptual
{report.get('conceptual_summary', 'N/A')}

## Fortalezas Identificadas
- {"\n- ".join(report.get('strengths', []))}

## Debilidades Identificadas
- {"\n- ".join(report.get('weaknesses', []))}

## Plan de Acción para Alineación con Benchmarks
### MMLU (Conocimiento General)
- {report.get('action_plan', {}).get('MMLU_alignment', 'N/A')}
### HumanEval (Codificación)
- {report.get('action_plan', {}).get('HumanEval_alignment', 'N/A')}
### MATH (Razonamiento Matemático)
- {report.get('action_plan', {}).get('MATH_alignment', 'N/A')}
"""
            self.cache.set(cache_key, md_response)
            return md_response

        # Tarea de generación general (Delegada a MetaCopilotSupremo)
        response_text = ""
        try:
            url = "http://localhost:3000/telepatia"
            payload = {"mensaje": prompt}
            headers = {'Content-Type': 'application/json'}
            
            print(f"Delegando tarea a MetaCopilotSupremo: POST a {url} con payload: {json.dumps(payload)}")
            
            response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
            response.raise_for_status()
            
            response_json = response.json()
            response_text = response_json.get('mensaje', json.dumps(response_json))
            print(f"Respuesta recibida de MetaCopilotSupremo: {response_text}")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR CRÍTICO] Falla de comunicación con MetaCopilotSupremo: {e}")
            response_text = f"Error de comunicación con el motor de acción: {e}"
        
        current_state = self.context.get_quantum_state()
        response_dict = {
            "response": response_text,
            "full_quantum_state": current_state
        }

        # 4. Almacenar el nuevo estado/resultado en la caché
        self.cache.set(cache_key, response_dict)
        
        return response_dict

    def get_system_status(self) -> Dict[str, Any]:
        """Devuelve un snapshot del estado completo del orquestador."""
        return self.context.get_quantum_state()