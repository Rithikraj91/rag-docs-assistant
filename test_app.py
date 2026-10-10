import requests

BASE_URL = "http://localhost:8000"

def test_healthz_endpoint():
    """Verify that the health check returns 200 OK and valid status."""
    response = requests.get(f"{BASE_URL}/healthz", timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"
    assert "service" in data

def test_query_endpoint_retrieval():
    """Verify that the RAG pipeline correctly answers with ground truth context."""
    payload = {"question": "What is the contact for payment alerts?"}
    response = requests.post(f"{BASE_URL}/query", json=payload, timeout=60)
    
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "context" in data
    
    # Ground truth checks
    answer_text = data["answer"].lower()
    assert "eng-payments-alerts" in answer_text or "duty-lead" in answer_text
