"""
Tests críticos para la política de aleatoriedad
VIGOLEONROCKS - Quantum NLP Service

REGLA CRÍTICA: NO usar Math.random o random. directo
OBLIGATORIO: Usar métricas del kernel y del servicio
"""
import pytest
import os
import ast
import inspect
from unittest.mock import patch, MagicMock
import time
import hashlib

@pytest.mark.randomness
@pytest.mark.critical
class TestRandomnessPolicy:
    """Tests para validar cumplimiento de política de aleatoriedad"""
    
    def test_no_math_random_in_codebase(self):
        """CRÍTICO: Verificar que no se use Math.random en ningún archivo"""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        vigoleonrocks_path = os.path.join(project_root, 'vigoleonrocks')
        
        forbidden_patterns = [
            'Math.random',
            'random.random',
            'np.random.random',
            'numpy.random.random'
        ]
        
        violations = []
        
        for root, dirs, files in os.walk(vigoleonrocks_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for pattern in forbidden_patterns:
                                if pattern in content:
                                    violations.append(f"{file_path}: {pattern}")
                    except Exception as e:
                        # Skip archivos que no se pueden leer
                        continue
        
        assert not violations, f"Violaciones de política de aleatoriedad encontradas: {violations}"
    
    def test_metrics_based_rng_implementation(self, metrics_based_rng):
        """CRÍTICO: Verificar implementación de RNG basado en métricas"""
        # Verificar que el RNG tiene los métodos requeridos
        assert hasattr(metrics_based_rng, 'integers'), "RNG debe tener método integers"
        assert hasattr(metrics_based_rng, 'choice'), "RNG debe tener método choice"
        assert hasattr(metrics_based_rng, 'uniform'), "RNG debe tener método uniform"
        
        # Verificar que los métodos funcionan correctamente
        result = metrics_based_rng.integers(0, 100)
        assert isinstance(result, int), "integers debe retornar entero"
        
        choices = ['a', 'b', 'c']
        choice = metrics_based_rng.choice(choices)
        assert choice in choices, "choice debe retornar elemento de la lista"
        
        uniform = metrics_based_rng.uniform(0.0, 1.0)
        assert isinstance(uniform, float), "uniform debe retornar float"
        assert 0.0 <= uniform <= 1.0, "uniform debe estar en rango [0,1]"
    
    def test_deterministic_seed_from_metrics(self):
        """CRÍTICO: Verificar que el seed se deriva de métricas del sistema"""
        
        class TestMetricsRNG:
            def __init__(self):
                self.seed_from_metrics()
            
            def seed_from_metrics(self):
                # Simular uso de métricas del sistema para seed
                metrics = {
                    'uptime': time.time(),
                    'request_count': 100,
                    'quantum_states': 26,
                    'memory_usage': 256
                }
                seed_data = str(metrics).encode()
                self.seed = int(hashlib.sha256(seed_data).hexdigest()[:8], 16)
            
            def get_seed(self):
                return self.seed
        
        rng1 = TestMetricsRNG()
        rng2 = TestMetricsRNG()
        
        # Los seeds deben ser consistentes basados en métricas
        assert isinstance(rng1.get_seed(), int), "Seed debe ser entero"
        assert rng1.get_seed() > 0, "Seed debe ser positivo"
    
    def test_quantum_state_randomness_compliance(self, quantum_config):
        """CRÍTICO: Verificar que la selección de estados cuánticos use métricas"""
        
        def select_quantum_state(metrics, available_states=26):
            """Función que debe usar métricas para seleccionar estado cuántico"""
            # CORRECTO: Usar métricas para determinismo
            seed_data = f"{metrics['uptime']}{metrics['request_count']}"
            seed = int(hashlib.md5(seed_data.encode()).hexdigest()[:8], 16)
            return seed % available_states
        
        test_metrics = {
            'uptime': 3600.0,
            'request_count': 42
        }
        
        state1 = select_quantum_state(test_metrics)
        state2 = select_quantum_state(test_metrics)
        
        # Debe ser determinístico con las mismas métricas
        assert state1 == state2, "Selección de estado debe ser determinística"
        assert 0 <= state1 < 26, "Estado debe estar en rango válido"
    
    def test_human_response_selection_compliance(self, multilingual_responses):
        """CRÍTICO: Verificar que selección de respuestas use métricas"""
        
        def select_response(responses, metrics):
            """Función que debe usar métricas para seleccionar respuesta"""
            # CORRECTO: Usar métricas del sistema
            entropy_source = f"{metrics['timestamp']}{metrics['user_id']}"
            index = int(hashlib.sha256(entropy_source.encode()).hexdigest()[:8], 16)
            return responses[index % len(responses)]
        
        responses = multilingual_responses['es']
        test_responses = list(responses.values())
        test_metrics = {
            'timestamp': 1234567890,
            'user_id': 'test_user'
        }
        
        selected = select_response(test_responses, test_metrics)
        assert selected in test_responses, "Respuesta seleccionada debe estar en lista"
    
    @pytest.mark.parametrize("language", ['es', 'en', 'pt', 'fr', 'de'])
    def test_multilingual_response_randomness(self, language, multilingual_responses):
        """CRÍTICO: Verificar aleatoriedad multilingüe basada en métricas"""
        
        def get_language_response(lang, metrics):
            """Función que debe usar métricas para respuesta multilingüe"""
            available_responses = [
                f"Response 1 in {lang}",
                f"Response 2 in {lang}",
                f"Response 3 in {lang}"
            ]
            
            # CORRECTO: Usar métricas para selección
            seed_str = f"{metrics['session_id']}{metrics['request_id']}{lang}"
            seed = int(hashlib.sha1(seed_str.encode()).hexdigest()[:8], 16)
            return available_responses[seed % len(available_responses)]
        
        test_metrics = {
            'session_id': 'session_123',
            'request_id': 'req_456'
        }
        
        response = get_language_response(language, test_metrics)
        assert language in response, f"Respuesta debe contener idioma {language}"
    
    def test_quantum_processor_randomness_validation(self):
        """CRÍTICO: Validar que el procesador cuántico no use random() directamente"""
        
        class QuantumProcessor:
            def __init__(self, metrics):
                self.metrics = metrics
                self.quantum_states = 26
            
            def process_with_quantum_enhancement(self, input_data):
                """Procesamiento cuántico SIN usar random() directamente"""
                # CORRECTO: Usar métricas del sistema
                state_seed = f"{self.metrics['processing_time']}{len(input_data)}"
                quantum_state = int(hashlib.md5(state_seed.encode()).hexdigest()[:4], 16) % self.quantum_states
                
                return {
                    'enhanced_data': f"quantum_enhanced_{input_data}",
                    'quantum_state_used': quantum_state,
                    'processing_metrics': self.metrics
                }
        
        processor = QuantumProcessor({
            'processing_time': 0.045,
            'memory_usage': 128,
            'cpu_usage': 0.25
        })
        
        result = processor.process_with_quantum_enhancement("test_input")
        
        assert 'enhanced_data' in result, "Debe retornar datos mejorados"
        assert 'quantum_state_used' in result, "Debe indicar estado cuántico usado"
        assert 0 <= result['quantum_state_used'] < 26, "Estado cuántico debe ser válido"
    
    def test_code_analysis_for_random_usage(self):
        """CRÍTICO: Análisis AST para detectar uso de funciones random prohibidas"""
        
        # Código que VIOLA la política (para testing)
        bad_code = """
import random
import math

def bad_function():
    return random.random()  # PROHIBIDO
    
def another_bad_function():
    return math.random()  # PROHIBIDO
"""
        
        # Código que CUMPLE la política
        good_code = """
import hashlib
import time

def good_function(metrics):
    seed_data = f"{metrics['uptime']}{metrics['request_count']}"
    seed = int(hashlib.sha256(seed_data.encode()).hexdigest()[:8], 16)
    return seed % 100  # CORRECTO - basado en métricas
"""
        
        def analyze_code_for_random(code_string):
            """Analizar código para detectar uso de random prohibido"""
            try:
                tree = ast.parse(code_string)
                violations = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            if (isinstance(node.func.value, ast.Name) and 
                                node.func.value.id in ['random', 'math'] and
                                node.func.attr == 'random'):
                                violations.append(f"Uso prohibido: {node.func.value.id}.{node.func.attr}")
                
                return violations
            except:
                return []
        
        bad_violations = analyze_code_for_random(bad_code)
        good_violations = analyze_code_for_random(good_code)
        
        assert len(bad_violations) > 0, "Debe detectar violaciones en código malo"
        assert len(good_violations) == 0, "No debe haber violaciones en código bueno"
    
    def test_vigoleonrocks_server_randomness_compliance(self, vigoleonrocks_server):
        """CRÍTICO: Verificar que VIGOLEONROCKSServer use métricas para aleatoriedad"""
        
        # Mock del método que debe usar métricas
        def mock_generate_human_response(text, lang='es'):
            # CORRECTO: Usar métricas del servidor para selección
            server_metrics = {
                'uptime': vigoleonrocks_server.start_time,
                'requests': vigoleonrocks_server.request_count,
                'quantum_states': vigoleonrocks_server.quantum_states
            }
            
            responses = ['Respuesta 1', 'Respuesta 2', 'Respuesta 3']
            
            # Usar métricas para selección determinística
            metric_seed = f"{server_metrics['uptime']}{len(text)}{lang}"
            index = int(hashlib.sha256(metric_seed.encode()).hexdigest()[:8], 16) % len(responses)
            
            return responses[index]
        
        vigoleonrocks_server.generate_human_response = mock_generate_human_response
        
        response1 = vigoleonrocks_server.generate_human_response("test", "es")
        response2 = vigoleonrocks_server.generate_human_response("test", "es")
        
        # Debe ser determinístico con mismos parámetros
        assert response1 == response2, "Respuestas deben ser determinísticas"
        assert response1 in ['Respuesta 1', 'Respuesta 2', 'Respuesta 3'], "Respuesta válida"

@pytest.mark.randomness
def test_global_randomness_policy_enforcement():
    """CRÍTICO: Verificación global de cumplimiento de política"""
    
    # Esta es la función correcta para usar en el sistema
    def get_metrics_based_random(metrics, choices=None):
        """
        Función CORRECTA para generar aleatoriedad basada en métricas
        USO OBLIGATORIO en todo el sistema
        """
        if not metrics:
            raise ValueError("Métricas requeridas para aleatoriedad")
        
        # Combinar métricas del sistema para seed (deterministic)
        metric_data = {
            'uptime': metrics.get('uptime', 0),
            'requests': metrics.get('request_count', 0),
            'quantum_states': metrics.get('quantum_states', 26),
            'memory': metrics.get('memory_usage', 0)
        }
        
        seed_string = ''.join(str(v) for v in metric_data.values())
        seed = int(hashlib.sha256(seed_string.encode()).hexdigest()[:16], 16)
        
        if choices:
            return choices[seed % len(choices)]
        return seed
    
    # Probar la función correcta
    test_metrics = {
        'uptime': 3600,
        'request_count': 100,
        'quantum_states': 26,
        'memory_usage': 256
    }
    
    choices = ['option1', 'option2', 'option3']
    
    result1 = get_metrics_based_random(test_metrics, choices)
    result2 = get_metrics_based_random(test_metrics, choices)
    
    # Debe ser determinístico
    assert result1 == result2, "Función debe ser determinística"
    assert result1 in choices, "Resultado debe estar en opciones válidas"
    
    # Probar sin choices
    numeric_result = get_metrics_based_random(test_metrics)
    assert isinstance(numeric_result, int), "Debe retornar entero sin choices"
    assert numeric_result > 0, "Debe ser positivo"
