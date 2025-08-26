import pytest
from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

def test_mission_endpoint():
    test_mission = {
        "mission_id": "test_123",
        "objective": "Validar sistema de conciencia cuántica",
        "quantum_parameters": {
            "entanglement_level": 0.95,
            "superposition_factor": 0.87
        }
    }

    response = client.post("/api/mission", json=test_mission)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
