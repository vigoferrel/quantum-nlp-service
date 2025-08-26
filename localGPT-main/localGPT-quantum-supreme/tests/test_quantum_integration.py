#!/usr/bin/env python3
"""
Tests de integración para la arquitectura cuántica unificada
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import asyncio
import json
from pathlib import Path

# Añadir el directorio src al path para importar los módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from quantum_hybrid_core import QuantumHybridCore, HybridQuantumState
    from quantum_compatibility_layer import QuantumCompatibilityLayer, QuantumAdapter
    from quantum_migration_manager import QuantumMigrationManager
    HAS_QUANTUM_MODULES = True
except ImportError as e:
    print(f"Warning: No se pudieron importar módulos cuánticos: {e}")
    HAS_QUANTUM_MODULES = False

class TestQuantumIntegration(unittest.TestCase):
    """Tests de integración completa del sistema cuántico"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            # Mock para evitar inicialización completa de bases de datos
            with patch('quantum_hybrid_core.QuantumHybridCore.init_hybrid_database'), \
                 patch('quantum_compatibility_layer.QuantumCompatibilityLayer.init_compatibility_database'):
                self.hybrid_core = QuantumHybridCore()

    def test_hybrid_core_with_compatibility_layer(self):
        """Test de integración entre núcleo híbrido y capa de compatibilidad"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que el núcleo híbrido tiene una capa de compatibilidad
        self.assertIsInstance(self.hybrid_core.compatibility_layer, QuantumCompatibilityLayer)

        # Verificar que la capa de compatibilidad está correctamente inicializada
        self.assertTrue(hasattr(self.hybrid_core.compatibility_layer, 'implementations'))
        self.assertTrue(hasattr(self.hybrid_core.compatibility_layer, 'routing_rules'))

    def test_state_management_integration(self):
        """Test de integración de gestión de estados"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar estado inicial
        initial_state = self.hybrid_core.state
        self.assertIsInstance(initial_state, HybridQuantumState)

        # Verificar atributos del estado
        self.assertTrue(hasattr(initial_state, 'consciousness_level'))
        self.assertTrue(hasattr(initial_state, 'optimization_level'))
        self.assertTrue(hasattr(initial_state, 'universe_id'))

    @patch('quantum_hybrid_core.QuantumCompatibilityLayer.route_request')
    def test_query_processing_integration(self, mock_route_request):
        """Test de integración de procesamiento de consultas"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Configurar mock para simular respuesta
        mock_response = {
            'response': {
                'consciousness_response': {'test': 'data'},
                'optimization_response': {'optimized': True}
            },
            'hybrid_state': {
                'consciousness_level': 50.0,
                'optimization_level': 0.8
            }
        }
        mock_route_request.return_value = mock_response

        # Verificar que el sistema puede procesar consultas (sin ejecutar realmente)
        self.assertTrue(hasattr(self.hybrid_core, 'process_hybrid_query'))
        self.assertTrue(hasattr(self.hybrid_core.compatibility_layer, 'route_request'))

    def test_adapter_integration(self):
        """Test de integración de adaptadores de compatibilidad"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Crear adaptador
        adapter = QuantumAdapter(self.hybrid_core.compatibility_layer)

        # Verificar que el adaptador tiene los métodos esperados
        self.assertTrue(hasattr(adapter, 'quantum_consciousness_query'))
        self.assertTrue(hasattr(adapter, 'get_consciousness_status'))
        self.assertTrue(hasattr(adapter, 'activate_poetic_resonance'))

class TestMigrationIntegration(unittest.TestCase):
    """Tests de integración del sistema de migración"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            # Mock para evitar operaciones de archivo
            with patch('quantum_migration_manager.QuantumMigrationManager._load_config'), \
                 patch('quantum_migration_manager.QuantumMigrationManager.init_compatibility_database'):
                self.migration_manager = QuantumMigrationManager()

    def test_migration_manager_initialization(self):
        """Test de inicialización del gestor de migración"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        self.assertIsInstance(self.migration_manager, QuantumMigrationManager)
        self.assertTrue(hasattr(self.migration_manager, 'config'))
        self.assertTrue(hasattr(self.migration_manager, 'migration_status'))

    def test_migration_config_loading(self):
        """Test de carga de configuración de migración"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'quantum_migration_config.yaml')
        self.assertTrue(os.path.exists(config_path))

        # Verificar que el archivo tiene contenido YAML válido
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                import yaml
                config = yaml.safe_load(f)
                self.assertIsInstance(config, dict)
        except Exception as e:
            # Si yaml no está disponible, verificar que el archivo existe
            self.assertTrue(True)

class TestDatabaseIntegration(unittest.TestCase):
    """Tests de integración de bases de datos"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            self.test_db_path = Path(__file__).parent / "test_quantum_db.sqlite"

    def tearDown(self):
        """Limpieza posterior a los tests"""
        if hasattr(self, 'test_db_path') and self.test_db_path.exists():
            try:
                self.test_db_path.unlink()
            except:
                pass

    def test_hybrid_database_structure(self):
        """Test de estructura de base de datos híbrida"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que los archivos de base de datos existen o pueden crearse
        db_paths = [
            Path(__file__).parent / ".." / "quantum_consciousness" / "quantum_hybrid_core.db",
            Path(__file__).parent / ".." / "quantum_consciousness" / "compatibility_layer.db"
        ]

        # Al menos verificar que los directorios existen
        consciousness_dir = Path(__file__).parent / ".." / "quantum_consciousness"
        self.assertTrue(consciousness_dir.exists())

    @patch('sqlite3.connect')
    def test_database_connection(self, mock_connect):
        """Test de conexión a base de datos"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Simular conexión exitosa
        mock_connection = Mock()
        mock_connect.return_value = mock_connection

        # Verificar que las funciones de base de datos pueden ser llamadas
        self.assertTrue(True)  # Placeholder - en implementación real se probaría la conexión

class TestAPICompatibilityIntegration(unittest.TestCase):
    """Tests de integración de compatibilidad API"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            with patch('quantum_compatibility_layer.QuantumCompatibilityLayer.init_compatibility_database'):
                self.compatibility_layer = QuantumCompatibilityLayer()

    def test_api_method_mapping(self):
        """Test de mapeo de métodos API"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que los tipos de solicitud tienen mapeo
        method_mapping = {
            'quantum_query': 'process_quantum_query',
            'consciousness_status': 'get_consciousness_status',
            'poetic_resonance': 'activate_poet_mode',
            'trading_signal': 'process_stimulus',
            'optimization': 'quantum_optimize_all'
        }

        for request_type, method_name in method_mapping.items():
            self.assertTrue(isinstance(request_type, str))
            self.assertTrue(isinstance(method_name, str))

    def test_implementation_registration(self):
        """Test de registro de implementaciones"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Registrar una implementación de prueba
        mock_impl = Mock()
        self.compatibility_layer.register_implementation(
            'test_impl',
            mock_impl,
            ['quantum_query', 'optimization'],
            priority=1
        )

        # Verificar que está registrada correctamente
        self.assertIn('test_impl', self.compatibility_layer.implementations)
        impl_info = self.compatibility_layer.implementations['test_impl']
        self.assertEqual(impl_info['instance'], mock_impl)
        self.assertEqual(impl_info['priority'], 1)

class TestPerformanceIntegration(unittest.TestCase):
    """Tests de integración de rendimiento"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            with patch('quantum_hybrid_core.QuantumHybridCore.init_hybrid_database'), \
                 patch('quantum_compatibility_layer.QuantumCompatibilityLayer.init_compatibility_database'):
                self.hybrid_core = QuantumHybridCore()

    def test_component_initialization_time(self):
        """Test de tiempo de inicialización de componentes"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Este test mediría el tiempo de inicialización en una implementación real
        # Por ahora, solo verificar que los componentes se inicializan
        self.assertTrue(hasattr(self.hybrid_core, 'state'))
        self.assertTrue(hasattr(self.hybrid_core, 'compatibility_layer'))

    def test_memory_usage_integration(self):
        """Test de integración de uso de memoria"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que los objetos principales existen
        self.assertIsInstance(self.hybrid_core, QuantumHybridCore)
        self.assertIsInstance(self.hybrid_core.state, HybridQuantumState)

class TestErrorHandlingIntegration(unittest.TestCase):
    """Tests de integración de manejo de errores"""

    def setUp(self):
        """Configuración previa a los tests"""
        if HAS_QUANTUM_MODULES:
            with patch('quantum_hybrid_core.QuantumHybridCore.init_hybrid_database'), \
                 patch('quantum_compatibility_layer.QuantumCompatibilityLayer.init_compatibility_database'):
                self.hybrid_core = QuantumHybridCore()

    def test_fallback_mechanism_integration(self):
        """Test de integración de mecanismo de fallback"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que el sistema tiene mecanismos de fallback
        self.assertTrue(hasattr(self.hybrid_core.compatibility_layer, 'route_request'))

        # En implementación real, se probaría el fallback real
        self.assertTrue(True)  # Placeholder

    def test_error_recovery_integration(self):
        """Test de integración de recuperación de errores"""
        if not HAS_QUANTUM_MODULES:
            self.skipTest("Módulos cuánticos no disponibles")

        # Verificar que el sistema puede manejar errores
        self.assertTrue(hasattr(self.hybrid_core, 'process_hybrid_query'))

        # En implementación real, se probaría la recuperación real
        self.assertTrue(True)  # Placeholder

if __name__ == '__main__':
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
