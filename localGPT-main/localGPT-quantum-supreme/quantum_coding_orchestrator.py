import logging
from unified_quantum_consciousness import UnifiedQuantumOptimizer

# Configurar un logger especifico para el orquestador
logger = logging.getLogger(__name__)

class QuantumCodingOrchestrator:
    def __init__(self):
        """
        Inicializa el orquestador, creando una instancia del optimizador cuantico.
        """
        self.optimizer = UnifiedQuantumOptimizer()
        self.sub_task_prompts = self._load_sub_task_prompts()

    def _load_sub_task_prompts(self):
        return {
            "CREATE_FILE": "Tarea de Codigo: Crear un nuevo archivo llamado '{file_name}' con el siguiente contenido:\n---\n{content_spec}\n---",
            "EDIT_FILE": "Tarea de Codigo: Editar el archivo '{file_name}' para que cumpla con la siguiente especificacion:\n---\n{edit_spec}\n---",
            "ANALYZE_CODE": "Tarea de Analisis: Analiza el siguiente fragmento de codigo y describe su proposito, identifica posibles errores y sugiere mejoras:\n---\n{code_snippet}\n---",
        }

    def _decompose_task(self, main_prompt):
        """
        Descompone el prompt principal en una secuencia de sub-tareas.
        """
        steps = []
        prompt_lower = main_prompt.lower()

        # Logica mejorada para parsear el prompt
        if "crear archivo" in prompt_lower:
            try:
                parts = main_prompt.split(" con ", 1)
                file_name_part = parts[0].split("crear archivo", 1)[1].strip()
                content_spec = parts[1] if len(parts) > 1 else "Contenido vacio."
                steps.append({"action": "CREATE_FILE", "file_name": file_name_part, "spec": content_spec})
            except IndexError:
                logger.warning(f"No se pudo parsear la tarea CREATE_FILE del prompt: {main_prompt}")
                steps.append({"action": "ERROR", "details": "Formato de 'crear archivo' no reconocido. Use 'crear archivo [nombre] con [contenido]'."})

        elif "editar archivo" in prompt_lower:
            try:
                parts = main_prompt.split(" para que ", 1)
                file_name_part = parts[0].split("editar archivo", 1)[1].strip()
                edit_spec = parts[1] if len(parts) > 1 else "Sin especificacion."
                steps.append({"action": "EDIT_FILE", "file_name": file_name_part, "spec": edit_spec})
            except IndexError:
                logger.warning(f"No se pudo parsear la tarea EDIT_FILE del prompt: {main_prompt}")
                steps.append({"action": "ERROR", "details": "Formato de 'editar archivo' no reconocido. Use 'editar archivo [nombre] para que [especificacion]'."})
        else:
            steps.append({"action": "ANALYZE_CODE", "spec": main_prompt})

        return steps

    def execute_coding_task(self, prompt: str) -> dict:
        """
        Orquesta la ejecucion de una tarea de codificacion y devuelve un resultado estructurado.
        """
        logger.info(f"Orquestador: Recibida tarea de codificacion: '{prompt}'")
        steps = self._decompose_task(prompt)
        execution_summary = {
            "overall_status": "pending",
            "steps": []
        }

        logger.info(f"Orquestador: Tarea descompuesta en {len(steps)} pasos.")

        for i, step in enumerate(steps):
            step_number = i + 1
            action = step.get("action", "UNKNOWN")
            step_result = {
                "step": step_number,
                "action": action,
                "status": "pending",
                "output": None
            }
            logger.info(f"Orquestador: Ejecutando paso {step_number}/{len(steps)} - Accion: {action}")

            if action == "ERROR":
                step_result["status"] = "error"
                step_result["output"] = step.get("details")
                logger.error(f"Error en la descomposicion del paso {step_number}: {step.get('details')}")
                execution_summary["steps"].append(step_result)
                continue

            if action in self.sub_task_prompts:
                try:
                    sub_prompt_template = self.sub_task_prompts[action]

                    if action == "CREATE_FILE":
                        sub_prompt = sub_prompt_template.format(file_name=step.get('file_name', ''), content_spec=step.get('spec', ''))
                    elif action == "EDIT_FILE":
                        sub_prompt = sub_prompt_template.format(file_name=step.get('file_name', ''), edit_spec=step.get('spec', ''))
                    else: # ANALYZE_CODE
                        sub_prompt = sub_prompt_template.format(code_snippet=step.get('spec', ''))

                    # Invocacion al optimizador con manejo de errores
                    result = self.optimizer.quantum_optimize_all(sub_prompt)
                    step_result["status"] = "success"
                    step_result["output"] = result
                    logger.info(f"Orquestador: Paso {step_number} completado exitosamente.")

                except Exception as e:
                    error_message = f"Error en el optimizador cuantico durante el paso {step_number}: {str(e)}"
                    logger.error(error_message)
                    step_result["status"] = "error"
                    step_result["output"] = error_message
            else:
                error_message = f"Accion desconocida '{action}' en el paso {step_number}."
                logger.warning(error_message)
                step_result["status"] = "error"
                step_result["output"] = error_message

            execution_summary["steps"].append(step_result)

        # Determinar el estado general
        if any(s["status"] == "error" for s in execution_summary["steps"]):
            execution_summary["overall_status"] = "completed_with_errors"
        else:
            execution_summary["overall_status"] = "success"

        logger.info("Orquestador: Todos los pasos han sido ejecutados.")
        return execution_summary
