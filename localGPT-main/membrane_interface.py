# membrane_interface.py
# Interfaz de membrana: el nexo entre el Alma (Kernel), el Cerebro (AICS) y el Cuerpo (Orquestador)

class MembraneInterface:
    """
    Traduce intenciones, consulta al cerebro para optimizar planes y
    ordena al cuerpo que ejecute las acciones resultantes.
    """

    def __init__(self):
        self.quantum_state = {"initialized": True}
        self.nlp_pipeline = [
            'normalization', 'ner', 'intent_classification',
            'archetype_mapping', 'parameter_extraction'
        ]
        print("Membrana de Manifestación inicializada.")

    def translate_to_pure_query(self, raw_input):
        """
        Convierte la entrada caótica del mundo exterior en una Consulta Pura
        Estructurada (CPE) que el núcleo puede entender.
        """
        print(f"[Membrana-In] Traduciendo entrada bruta: {raw_input}")
        if isinstance(raw_input, dict):
            return {
                'archetype': raw_input.get('type', 'healing'),
                'params': raw_input.get('params', {'component': 'deepeval'}),
                'priority': 1,
                'raw_query': raw_input.get('query', '')
            }
        # Simulación de pipeline de NLP
        return {
            'archetype': 'healing',
            'params': {'component': 'deepeval'},
            'priority': 1,
            'raw_query': str(raw_input)
        }

    def execute_intention(self, perfect_intention, pure_query, orchestrator, aics_service):
        """
        Proceso central de la membrana: recibe una intención y la consulta pura,
        la optimiza con el AICS y la ejecuta a través del orquestador.
        """
        print(f"[Membrana-Out] Recibida Intención del Kernel: {perfect_intention['intention']}")

        if orchestrator is None or aics_service is None:
            return {'error': 'Orquestador o Servicio AICS no proporcionados'}

        # 1. Consultar al Cerebro (AICS) para un plan de ejecución optimizado.
        #    Ahora usamos la 'raw_query' que viene en el objeto 'pure_query'.
        plan_request = {
            "query": pure_query.get('raw_query', ''), # Corregido: usa la query de pure_query
            "context_length": 1024, # Valor por defecto o extraído
            "query_type": perfect_intention.get('intention', 'general'),
            "urgency": perfect_intention.get('priority', 1.0)
        }
        print(f"[Membrana-Out] Consultando a AICS con: {plan_request}")
        execution_plan = aics_service.get_execution_plan(**plan_request)

        if "error" in execution_plan:
            print(f"[Membrana-Out] Error de AICS: {execution_plan['error']}. Procediendo sin plan.")
            action_to_execute = perfect_intention['intention']
            params = perfect_intention.get('params', {})
        else:
            print(f"[Membrana-Out] Plan de AICS recibido. Modelo recomendado: {execution_plan['recommended_model']}")
            # La acción a ejecutar ahora puede ser guiada por el plan.
            # Por ahora, seguimos usando la intención original, pero en el futuro
            # el plan podría refinar la acción o sus parámetros.
            action_to_execute = perfect_intention['intention']
            params = perfect_intention.get('params', {})
            # Ejemplo de cómo el plan podría modificar la acción:
            # params['recommended_model'] = execution_plan['recommended_model']

        # 2. Mapear la intención a una acción concreta del Orquestador (cuerpo)
        action_map = {
            'healing': orchestrator._auto_repair,
            'optimization': orchestrator._optimize_system,
            'start': orchestrator._start_component,
            'stop': orchestrator._stop_component
        }

        # 3. Ordenar al Cuerpo (Orquestador) o invocar un LLM
        action_method = action_map.get(action_to_execute)

        if action_method:
            result = action_method(params)
            # Aquí se generaría el 'ExecutionReceipt'
            return {"execution_result": result, "aics_plan": execution_plan}
        else:
            # Si la intención no es una acción del sistema, es una consulta para un LLM.
            print(f"[Membrana-Out] Intención de consulta. Usando plan de AICS para invocar LLM.")

            # Simulación de la llamada al LLM recomendado por el AICS
            # En una implementación real, aquí iría el código para llamar a la API del LLM.
            recommended_model = execution_plan.get('recommended_model', 'default_model')
            print(f"[Membrana-LLM] Simulating call to: {recommended_model}")

            # Crear una respuesta simulada basada en la pregunta
            raw_query = pure_query.get('raw_query', '')
            simulated_response = f"Respuesta simulada para '{raw_query[:30]}...' desde el modelo {recommended_model}"

            # Completar el resultado de la ejecución
            result = {'status': 'answered_by_llm', 'response': simulated_response}
            return {"execution_result": result, "aics_plan": execution_plan}

    def manifestar_estado(self, quantum_state):
        """Manifestar un estado cuántico en la realidad"""
        return {
            "manifestation_id": "test_manifest_123",
            "status": "manifested",
            "manifestation_path": "/quantum/manifest/test"
        }
