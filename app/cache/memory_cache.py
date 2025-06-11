from typing import Optional

from cachetools import LRUCache

from .base import Cache


class InMemoryCache(Cache):
    """In-memory cache implementation using cachetools LRUCache."""

    def __init__(self, maxsize: int = 1000):
        self._cache = LRUCache(maxsize=maxsize)

    async def get(self, key: str) -> Optional[str]:
        """Get a value from the in-memory cache."""
        return self._cache.get(key)

    async def set(self, key: str, value: str) -> None:
        """Set a value in the in-memory cache."""
        self._cache[key] = value
