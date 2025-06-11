# tests/unit/test_rewrite_service.py
from unittest.mock import AsyncMock

import pytest

from app.cache.base import Cache
from app.llm_adapter.base import LLMAdapter
from app.model.models import RewriteResponse, StyleEnum
from app.service.rewrite_service import RewriteService


@pytest.fixture
def mock_llm_adapter():
    """Create a mock LLM adapter."""
    adapter = AsyncMock(spec=LLMAdapter)
    adapter.rewrite.return_value = "Rewritten text"
    return adapter


@pytest.fixture
def mock_cache():
    """Create a mock cache."""
    cache = AsyncMock(spec=Cache)
    cache.generate_key.return_value = "test_cache_key"
    return cache


@pytest.fixture
def rewrite_service(mock_llm_adapter, mock_cache):
    """Create a RewriteService instance with mocked dependencies."""
    return RewriteService(mock_llm_adapter, mock_cache)


@pytest.mark.asyncio
async def test_rewrite_cache_hit(rewrite_service, mock_cache, mock_llm_adapter):
    """Test rewrite when value is found in cache."""

    text = "Hello world"
    style = StyleEnum.PIRATE
    cached_text = "Ahoy, world!"
    mock_cache.get.return_value = cached_text

    result = await rewrite_service.rewrite(text, style)

    assert isinstance(result, RewriteResponse)
    assert result.original_text == text
    assert result.rewritten_text == cached_text
    assert result.style == style

    mock_cache.generate_key.assert_called_once_with(text, style)
    mock_cache.get.assert_called_once_with("test_cache_key")

    mock_llm_adapter.rewrite.assert_not_called()


@pytest.mark.asyncio
async def test_rewrite_cache_miss(rewrite_service, mock_cache, mock_llm_adapter):
    """Test rewrite when value is not in cache."""

    text = "Hello world"
    style = StyleEnum.PIRATE
    rewritten_text = "Ahoy, world!"
    mock_cache.get.return_value = None
    mock_llm_adapter.rewrite.return_value = rewritten_text

    result = await rewrite_service.rewrite(text, style)

    assert isinstance(result, RewriteResponse)
    assert result.original_text == text
    assert result.rewritten_text == rewritten_text
    assert result.style == style

    mock_cache.generate_key.assert_called_once_with(text, style)
    mock_cache.get.assert_called_once_with("test_cache_key")
    mock_cache.set.assert_called_once_with("test_cache_key", rewritten_text)

    mock_llm_adapter.rewrite.assert_called_once_with(text, style)
