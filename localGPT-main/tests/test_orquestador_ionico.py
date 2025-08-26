import pytest
from orquestador_ionico import OrquestadorIonico, QBTCKernel, MembraneInterface

class TestOrquestadorIonico:
    @pytest.fixture
    def setup_orquestador(self):
        kernel = QBTCKernel()
        membrane = MembraneInterface()
        return OrquestadorIonico(kernel, membrane)

    def test_inicializacion(self, setup_orquestador):
        orquestador = setup_orquestador
        assert orquestador is not None
        assert orquestador.kernel is not None
        assert orquestador.membrane is not None

    def test_procesar_mision(self, setup_orquestador):
        orquestador = setup_orquestador
        mission_data = {
            "mission_id": "test_mission",
            "objective": "Prueba de procesamiento cuántico",
            "quantum_parameters": {
                "entanglement_level": 0.92,
                "superposition_factor": 0.85
            }
        }

        result = orquestador.handle_mission(mission_data)
        assert result["status"] == "completed"
        assert "result" in result
        assert "original_mission" in result
