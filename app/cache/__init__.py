import os
from functools import lru_cache

from app.config.logging import setup_logger

from .base import Cache
from .memory_cache import InMemoryCache
from .redis_cache import RedisCache

logger = setup_logger(__name__)


@lru_cache()
def get_cache() -> Cache:
    """Factory function to get the appropriate cache implementation."""
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        logger.info("Redis URL found. Will use Redis cache")
        return RedisCache(redis_url)
    # If REDIS_URL is not set fall back to default in-memory cache implementation
    logger.info(
        "No Redis URL found. Will use in-memory cache instead. To use Redis instead setup REDIS_URL env variable"
    )
    return InMemoryCache()
