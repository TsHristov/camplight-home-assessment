from prometheus_client import CollectorRegistry, Counter
from prometheus_client.openmetrics.exposition import generate_latest

cache_registry = CollectorRegistry()

CACHE_HITS = Counter(
    "rewrite_cache_hits_total", "Total number of cache hits", registry=cache_registry
)

CACHE_MISSES = Counter(
    "rewrite_cache_misses_total",
    "Total number of cache misses",
    registry=cache_registry,
)

def get_metrics():
    """Generate Prometheus metrics."""
    return generate_latest(cache_registry)
