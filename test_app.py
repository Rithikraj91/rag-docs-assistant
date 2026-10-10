import os
from dotenv import load_dotenv

# Load local .env credentials before instantiating the app
load_dotenv()

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_or_root():
    """Verify that the FastAPI service is reachable."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_query_validation():
    """Verify that an empty payload triggers a 422 Unprocessable Entity."""
    response = client.post("/query", json={})
    assert response.status_code == 422

def test_query_success():
    """Verify that asking a question returns an answer and context."""
    response = client.post(
        "/query",
        json={"question": "What is the database connection timeout?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "context" in data
