from typing import Optional

from .base import Cache


class RedisCache(Cache):
    """Redis cache implementation."""

    def __init__(self, redis_url: str):
        pass

    async def get(self, key: str) -> Optional[str]:
        """Get a value from Redis cache."""
        pass

    async def set(self, key: str, value: str) -> None:
        """Set a value in Redis cache."""
        pass
