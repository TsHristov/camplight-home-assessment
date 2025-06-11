import pytest

from app.cache.memory_cache import InMemoryCache


@pytest.mark.asyncio
async def test_memory_cache_lru():
    """Test the LRU (Least Recently Used) functionality of the in-memory cache."""
    # Create a small cache to test LRU behavior
    cache = InMemoryCache(maxsize=2)

    # Add two items
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")

    # Verify both items are in cache
    assert await cache.get("key1") == "value1"
    assert await cache.get("key2") == "value2"

    # Add a third item, which should evict the least recently used item (key1)
    await cache.set("key3", "value3")

    # key1 should be evicted
    assert await cache.get("key1") is None
    # key2 and key3 should still be in cache
    assert await cache.get("key2") == "value2"
    assert await cache.get("key3") == "value3"

    # Access key2 to make it most recently used
    await cache.get("key2")

    # Add a fourth item, which should evict key3 (least recently used)
    await cache.set("key4", "value4")

    # key3 should be evicted
    assert await cache.get("key3") is None
    # key2 and key4 should still be in cache
    assert await cache.get("key2") == "value2"
    assert await cache.get("key4") == "value4"
