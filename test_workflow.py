from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_research_workflow():
    response = client.post("/api/research", json={
        "disease": "Alzheimer disease",
        "focus": "neuroinflammation",
        "max_records": 5
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["research_id"]
    assert payload["literature"]
    assert payload["hypothesis"]["supporting_record_ids"]

def test_graph_endpoint():
    response = client.get("/api/knowledge-graph/Alzheimer%20disease")
    assert response.status_code == 200
    assert response.json()["nodes"]
