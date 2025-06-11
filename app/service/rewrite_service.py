from app.cache.base import Cache
from app.config.logging import setup_logger
from app.llm_adapter.base import LLMAdapter
from app.metrics.prometheus_metrics import CACHE_HITS, CACHE_MISSES
from app.model.models import RewriteResponse, StyleEnum

logger = setup_logger(__name__)


class RewriteService:
    def __init__(self, llm_adapter: LLMAdapter, cache: Cache):
        self.llm_adapter = llm_adapter
        self.cache = cache

    async def rewrite(self, text: str, style: StyleEnum) -> RewriteResponse:
        """Rewrite text in the specified style with caching."""
        cache_key = self.cache.generate_key(text, style)

        # Try to get from cache
        cached_result = await self.cache.get(cache_key)

        if cached_result:
            logger.debug("Value found in cache, skip calling LLM adapter")

            # Record cache hit metric
            CACHE_HITS.inc()

            return RewriteResponse(
                original_text=text, rewritten_text=cached_result, style=style
            )

        # Record cache miss metric
        CACHE_MISSES.inc()

        logger.debug("Value not found in cache, calling LLM adapter")
        rewritten_text = await self.llm_adapter.rewrite(text, style)

        await self.cache.set(cache_key, rewritten_text)

        return RewriteResponse(
            original_text=text, rewritten_text=rewritten_text, style=style
        )
