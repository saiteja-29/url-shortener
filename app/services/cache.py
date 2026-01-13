from app.core.redis import redis_client
from app.utils.cache import calculate_ttl


def cache_url(short_code: str, original_url: str, expires_at=None):
    ttl = calculate_ttl(expires_at)

    redis_client.set(
        name=f"url:{short_code}",
        value=original_url,
        ex=ttl
    )
