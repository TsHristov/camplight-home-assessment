from abc import ABC, abstractmethod

from app.model.models import StyleEnum


class LLMAdapter(ABC):
    """Abstract base class for LLM adapters."""

    @abstractmethod
    async def rewrite(self, text: str, style: StyleEnum) -> str:
        """Rewrite the given text in the specified style."""
        pass
