import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rewrite_endpoint_default_style(client):
    """Test that missing style defaults to formal."""
    payload = {"text": "Hello world"}

    response = client.post("/v1/rewrite", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["style"] == "formal"


def test_rewrite_endpoint_empty_text(client):
    """Test that empty text returns 400."""
    payload = {"text": "", "style": "formal"}

    response = client.post("/v1/rewrite", json=payload)

    assert response.status_code == 400
    error_response = response.json()
    assert error_response["error"]["message"] == "Text cannot be empty"


def test_rewrite_endpoint_text_too_long(client):
    """Test that text over 5000 characters returns 422."""
    payload = {"text": "x" * 5001, "style": "formal"}

    response = client.post("/v1/rewrite", json=payload)

    assert response.status_code == 400
    error_response = response.json()
    assert (
        error_response["error"]["message"]
        == "Text exceeds the maximum threshold of 5000 symbols"
    )


def test_rewrite_endpoint_invalid_style(client):
    """Test that empty text returns 400."""
    payload = {"text": "Sample text", "style": "invalid"}

    response = client.post("/v1/rewrite", json=payload)

    assert response.status_code == 400
    error_response = response.json()
    assert "Style must be one of: " in error_response["error"]["message"]
