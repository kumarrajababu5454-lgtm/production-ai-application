import time


_CACHE = {}

CACHE_TTL = 300
MAX_CACHE_SIZE = 100


def _make_cache_key(user_input: str) -> str:
    return " ".join(user_input.strip().lower().split())


def get_cached_response(user_input: str):
    """
    Return a cached response if it exists and has not expired.
    """

    key = _make_cache_key(user_input)

    if key not in _CACHE:
        return None

    response, timestamp = _CACHE[key]

    if time.time() - timestamp > CACHE_TTL:
        del _CACHE[key]
        return None

    return response


def set_cached_response(user_input: str, response: str):
    """
    Store an AI response in the cache.
    """

    key = _make_cache_key(user_input)

    # Prevent unlimited cache growth.
    if len(_CACHE) >= MAX_CACHE_SIZE and key not in _CACHE:
        oldest_key = min(
            _CACHE,
            key=lambda item: _CACHE[item][1],
        )
        del _CACHE[oldest_key]

    _CACHE[key] = (
        response,
        time.time(),
    )


def clear_cache():
    """
    Clear all cached responses.
    """

    _CACHE.clear()
