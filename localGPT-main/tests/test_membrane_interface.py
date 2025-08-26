import pytest
from membrane_interface import MembraneInterface

class TestMembraneInterface:
    @pytest.fixture
    def setup_membrane(self):
        return MembraneInterface()

    def test_inicializacion(self, setup_membrane):
        membrane = setup_membrane
        assert membrane is not None
        assert membrane.quantum_state is not None

    def test_manifestar_estado(self, setup_membrane):
        membrane = setup_membrane
        quantum_state = {
            "entanglement_level": 0.95,
            "superposition_factor": 0.87
        }

        result = membrane.manifestar_estado(quantum_state)
        assert "manifestation_id" in result
        assert result["status"] == "manifested"
        assert "manifestation_path" in result
