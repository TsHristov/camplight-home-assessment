import hashlib
from abc import ABC, abstractmethod
from typing import Optional

from app.model.enums import StyleEnum


class Cache(ABC):
    """Abstract base class for cache implementations."""

    def generate_key(self, text: str, style: StyleEnum) -> str:
        """Generate a cache key for the given text and style."""
        # Normalize the input
        text = text.strip().lower()
        style = style.strip().lower()

        # Create a unique key based on text and style
        return hashlib.sha256(f"{text}::{style}".encode("utf-8")).hexdigest()

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Get a value from the cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """Set a value in the cache."""
        pass
