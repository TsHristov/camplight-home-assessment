import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.main import app

PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env.tst")


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def api_key():
    """Fixture to provide OpenAI API key."""
    key = os.getenv("OPENAI_API_KEY")
    assert key is not None, "OPENAI_API_KEY environment variable is not set"
    assert key != "", "OPENAI_API_KEY environment variable is empty"
    return key


@pytest.mark.parametrize("style", ["pirate", "haiku", "formal"])
def test_rewrite_openai_integration(client, api_key, style):
    """Validates LLM integration with OpenAPI returns transformed content for valid styles."""

    response = client.post(
        "/v1/rewrite",
        json={"text": "Testing the integration with OpenAI.", "style": style},
    )

    assert response.status_code == 200, f"Unexpected response: {response.text}"
    data = response.json()

    assert data["original_text"] == "Testing the integration with OpenAI."
    assert data["style"] == style

    rewritten = data["rewritten_text"]
    assert isinstance(rewritten, str), "rewritten_text must be a string"
    assert len(rewritten.strip()) > 0, "rewritten_text should not be empty"
    assert (
        rewritten != data["original_text"]
    ), "rewritten_text should differ from original"
