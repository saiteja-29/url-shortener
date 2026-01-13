from app.core.redis import redis_client


def get_cached_url(short_code: str):
    return redis_client.get(f"url:{short_code}")
