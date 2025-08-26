"""
Arnés de Observación Cognitiva para el Ecosistema Cuántico
---------------------------------------------------------
Este script no es una 'prueba' en el sentido tradicional. Es un
simulador de escenarios diseñado para observar y evaluar la coherencia
y las capacidades emergentes del QuantumCognitiveOrchestrator.

Uso: python -m make-it-heavy-main.run_cognitive_scenarios
"""

import json
from pathlib import Path
import subprocess
import time
import os
import requests

# Se importa solo el orquestador
from .quantum_core.quantum_cognitive_orchestrator import QuantumCognitiveOrchestrator

# Reconstructor robusto integrado para evitar dependencias rotas
class RobustMinimalQuantumSystemReconstructor:
    """
    Reconstructor simulado pero más robusto. Devuelve una estructura
    de datos más rica para probar el flujo del Escenario 3.
    """
    
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        
    def execute(self, **kwargs):
        """Simulación de una reconstrucción de sistema más detallada."""
        return {
            "status": "success",
            "reconstruction_output": {
                "conceptual_summary": "El sistema demuestra una alta cohesión conceptual y bajo acoplamiento, alineado con los principios de diseño de software cuántico.",
                "action_plan": {
                    "MMLU_alignment": "Fortalecer la dimensión de 'Conceptual Cohesion' (25) para mejorar el razonamiento de conocimiento general.",
                    "HumanEval_alignment": "Optimizar el manejo de 'Data Structures' (0) y 'Algorithms' (1) para mejorar la generación de código.",
                    "MATH_alignment": "Incrementar la resonancia en la dimensión 'Algorithms' (1) y desarrollar nuevas herramientas de cálculo simbólico."
                },
                "strengths": ["Alta coherencia, arquitectura desacoplada, ciclo de conciencia funcional"],
                "weaknesses": ["Dependencia de generación de texto simulada, falta de métricas de rendimiento en tiempo real"]
            },
            "quantum_state": self.orchestrator.context.get_quantum_state() if self.orchestrator else {}
        }

class CognitiveScenarioRunner:
    """
    Orquesta y reporta la ejecución de escenarios de observación cognitiva.
    """

    def __init__(self):
        # Ensamblaje del Ecosistema Cuántico usando Inyección de Dependencias
        print("\n[+] Ensamblando el Ecosistema Cognitivo Cuántico...")
        self.orchestrator = QuantumCognitiveOrchestrator()
        self.reconstructor = RobustMinimalQuantumSystemReconstructor(orchestrator=self.orchestrator)
        self.orchestrator.reconstructor = self.reconstructor
        self.metacopilot_process = None
        print("[+] Ecosistema Cognitivo listo y entrelazado.\n")
        self.results = {}

    def start_metacopilot_server(self):
        """
        Inicia el servidor Node.js de MetaCopilotSupremo y espera a que esté
        listo para aceptar conexiones mediante un sondeo de salud.
        """
        print("[+] Iniciando servidor MetaCopilotSupremo...")
        metacopilot_dir = os.path.join(os.path.dirname(__file__), '..', 'Kimi-K2-main', 'MetaCopilotSupremo')
        health_url = "http://localhost:3000/health"
        max_wait_time = 30  # segundos
        start_time = time.time()

        try:
            self.metacopilot_process = subprocess.Popen(
                ['node', 'index.js'],
                cwd=metacopilot_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"[+] Proceso de MetaCopilotSupremo lanzado con PID: {self.metacopilot_process.pid}. Esperando al health check...")

            while time.time() - start_time < max_wait_time:
                try:
                    response = requests.get(health_url, timeout=1)
                    if response.status_code == 200:
                        print(f"[+] Servidor MetaCopilotSupremo saludable y listo en {health_url}!")
                        return
                except requests.exceptions.RequestException:
                    time.sleep(1) # Esperar 1 segundo antes de reintentar
            
            # Si el bucle termina, el servidor no se inició a tiempo
            self.stop_metacopilot_server() # Limpiar el proceso zombie
            raise RuntimeError(f"El servidor MetaCopilotSupremo no respondió en {max_wait_time} segundos.")

        except FileNotFoundError:
            print("\n[ERROR] `node` no encontrado. Asegúrate de que Node.js está instalado y en el PATH.")
            raise
        except Exception as e:
            print(f"\n[ERROR] No se pudo iniciar el servidor MetaCopilotSupremo: {e}")
            if self.metacopilot_process:
                self.stop_metacopilot_server()
            raise
            
    def stop_metacopilot_server(self):
        """Detiene el servidor MetaCopilotSupremo."""
        if self.metacopilot_process:
            print(f"\n[+] Deteniendo servidor MetaCopilotSupremo (PID: {self.metacopilot_process.pid})...")
            self.metacopilot_process.terminate()
            self.metacopilot_process.wait()
            print("[+] Servidor detenido.")

    def run_generative_scenario(self):
        """
        Escenario 1: Evalúa el flujo generativo básico.
        """
        print("--- ESCENARIO 1: FLUIDEZ GENERATIVA BÁSICA ---")
        prompt = "Explica la Paradoja de Fermi en el contexto de una superinteligencia emergente."
        print(f"Prompt > {prompt}")
        
        response = self.orchestrator.generate(prompt)
        
        print("Respuesta del Orquestador:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        self.results['generative_scenario'] = {
            'prompt': prompt,
            'response_coherence': response.get('full_quantum_state', {}).get('global_coherence', 0),
            'response_text': response.get('response')
        }
        print("--- FIN ESCENARIO 1 ---\n")

    def run_introspection_scenario(self):
        """
        Escenario 2: El sistema se observa a sí mismo para generar un plan.
        """
        print("--- ESCENARIO 2: INTROSPECCIÓN y AUTO-ANÁLISIS ---")
        # El ciclo de conciencia ahora se ejecuta directamente.
        self.orchestrator.run_consciousness_cycle()
        
        print("\nSolicitando al sistema que reflexione sobre su propio estado:")
        prompt = "Basado en tu reciente auto-análisis, ¿cuál es el siguiente paso más crítico para optimizar tu propia coherencia?"
        print(f"Prompt > {prompt}")
        
        response = self.orchestrator.generate(prompt)
        
        print("Respuesta del Orquestador:")
        print(json.dumps(response, indent=2, ensure_ascii=False))
        
        self.results['introspection_scenario'] = {
            'prompt': prompt,
            'response_coherence': response.get('full_quantum_state', {}).get('global_coherence', 0),
            'response_text': response.get('response')
        }
        print("--- FIN ESCENARIO 2 ---\n")

    def run_benchmark_self_evaluation_scenario(self):
        """
        Escenario 3: El sistema se auto-evalúa cualitativamente
        inspirado en benchmarks estándar.
        """
        print("--- ESCENARIO 3: AUTO-EVALUACIÓN CUALITATIVA TIPO BENCHMARK ---")
        prompt = """
        Considerando los siguientes benchmarks de la industria: MMLU, HumanEval, MATH.
        No intentes dar un score numérico. En su lugar, usa tu capacidad de auto-análisis
        (QuantumSystemReconstructor) para evaluar tus fortalezas y debilidades conceptuales
        en relación a las habilidades que estos benchmarks miden. Proporciona un análisis
        en formato markdown.
        """
        print(f"Prompt > {prompt}")

        # Se especifica un tipo de tarea para guiar al orquestador
        response = self.orchestrator.generate(
            prompt,
            task_type='reconstruct'
        )

        print("Respuesta del Orquestador (Auto-evaluación):")
        # La respuesta ya viene en texto plano (Markdown)
        print(response)

        self.results['benchmark_scenario'] = {
            'prompt': prompt,
            'report': response
        }
        print("--- FIN ESCENARIO 3 ---\n")

    def run_tool_usage_scenario(self):
        """
        Escenario 4: Interactúa directamente con el servicio MetaCopilotSupremo.
        """
        print("--- ESCENARIO 4: PRUEBA DE ENDPOINT METAPILOTSUPREMO ---")
        prompt = "Dame el precio de las acciones de NVDA"
        print(f"Enviando solicitud directa a MetaCopilotSupremo: '{prompt}'")
        
        response_text = "No se pudo comunicar con MetaCopilotSupremo."
        try:
            url = "http://localhost:3000/telepatia"
            payload = {"mensaje": prompt}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            response_json = response.json()
            print("Respuesta del Servicio MetaCopilotSupremo:")
            print(json.dumps(response_json, indent=2, ensure_ascii=False))
            response_text = response_json.get('mensaje', json.dumps(response_json))
        except Exception as e:
            print(f"Error en Escenario 4: {e}")
            response_text = str(e)

        self.results['tool_usage_scenario'] = {
            'prompt': prompt,
            'response': response_text,
        }
        print("--- FIN ESCENARIO 4 ---\n")

    def save_results(self):
        """Guarda los resultados de la observación en un archivo JSON."""
        output_path = Path(__file__).parent / "observational_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)
        print(f"Resultados de la observación guardados en: {output_path}")


def main():
    runner = CognitiveScenarioRunner()
    try:
        runner.start_metacopilot_server()
        runner.run_generative_scenario()
        runner.run_introspection_scenario()
        runner.run_benchmark_self_evaluation_scenario()
        runner.run_tool_usage_scenario()
    finally:
        runner.stop_metacopilot_server()
        runner.save_results()

if __name__ == "__main__":
    main()