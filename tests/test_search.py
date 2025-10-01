from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_search_tools():
    search_data = {
        "query": "machine learning",
        "limit": 5
    }
    response = client.post("/search/", json=search_data)
    assert response.status_code == 200
    assert "results" in response.json()
    assert "response_time_ms" in response.json()


def test_search_with_custom_limit():
    search_data = {
        "query": "database",
        "limit": 10
    }
    response = client.post("/search/", json=search_data)
    assert response.status_code == 200
    assert len(response.json()["results"]) <= 10