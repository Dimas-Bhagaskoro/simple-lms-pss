from django.core.cache import cache
from ninja.errors import HttpError


def rate_limit(request, limit=60):
    ip = request.META.get("REMOTE_ADDR", "unknown")

    key = f"rate_limit:{ip}"

    count = cache.get(key, 0)

    if count >= limit:
        raise HttpError(429, "Rate limit exceeded")

    cache.set(key, count + 1, timeout=60)