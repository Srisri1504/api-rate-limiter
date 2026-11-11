from fastapi.testclient import TestClient
from main import app, limiter

client = TestClient(app)

def test_rate_limiting_flow():
    limiter.reset()
    
    for _ in range(5):
        response = client.get("/api/data")
        assert response.status_code == 200

    blocked_response = client.get("/api/data")
    assert blocked_response.status_code == 429
    assert "Retry-After" in blocked_response.headers

    stats = client.get("/api/stats").json()
    assert stats["metrics"]["allowed"] == 5
    assert stats["metrics"]["blocked"] == 1
