from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_tool():
    tool_data = {
        "name": "Test Tool",
        "description": "A test tool for testing",
        "tags": ["test", "demo"],
        "metadata": {"category": "testing"}
    }
    response = client.post("/tools/", json=tool_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Tool"


def test_get_tools():
    response = client.get("/tools/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"