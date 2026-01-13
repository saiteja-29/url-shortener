from fastapi import HTTPException, Request
from app.core.redis import redis_client

RATE_LIMIT = 10      # max requests
WINDOW_SIZE = 60     # seconds


def rate_limiter(request: Request):
    ip = request.client.host
    path = request.url.path

    key = f"rate:{ip}:{path}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, WINDOW_SIZE)

    if current > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )
