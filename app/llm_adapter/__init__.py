import os
from functools import lru_cache

from app.config.logging import setup_logger

from .base import LLMAdapter
from .mock_adapter import MockLLMAdapter
from .openai_adapter import OpenAIAdapter

logger = setup_logger(__name__)


@lru_cache()
def get_llm_adapter() -> LLMAdapter:
    """Factory function to get the appropriate LLM adapter based on environment variables."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        logger.info("Found OpenAI API key. Will use OpenAI LLM adapter")
        return OpenAIAdapter(openai_api_key)
    # If OPENAI_API_KEY is not set fall back to default mocked LLM adapter
    logger.info(
        "No OpenAI API key found. Will use mock LLM adapter instead. To use OpenAI setup OPENAI_API_KEY env variable"
    )
    return MockLLMAdapter()
