from app.model.models import StyleEnum

from .base import LLMAdapter


class MockLLMAdapter(LLMAdapter):
    """Mock LLM adapter for testing and when no API key is available."""

    async def rewrite(self, text: str, style: StyleEnum) -> str:
        """Mock rewrite implementation that wraps text with style indicators."""
        if style == StyleEnum.PIRATE:
            return f"[*pirate*] {text} [*pirate*]"
        elif style == StyleEnum.HAIKU:
            return f"[*haiku*] {text} [*haiku*]"
        elif style == StyleEnum.FORMAL:
            return f"[*formal*] {text} [*formal*]"
