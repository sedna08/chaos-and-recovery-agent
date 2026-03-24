from fastapi.testclient import TestClient
from src.main import app

# Initialize the TestClient with our FastAPI app
client = TestClient(app)

def test_health_check_returns_200():
    """Validates the Kubernetes liveness/readiness probe target."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_stock_returns_inventory():
    """Validates the primary inventory retrieval endpoint."""
    response = client.get("/api/stock")
    assert response.status_code == 200
    assert response.json() == {"item": "shoes", "qty": 42}

def test_unknown_route_returns_404():
    """Validates that undefined routes return standard 404s."""
    response = client.get("/api/unknown")
    assert response.status_code == 404