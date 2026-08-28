import time


def start_timer():
    """Start a timer for measuring request duration."""
    return time.perf_counter()


def calculate_latency(start_time):
    """Return request latency in seconds."""
    return round(time.perf_counter() - start_time, 4)


def log_request(
    user_input: str,
    route: str,
    latency: float,
    cached: bool = False,
):
    """
    Record basic information about an AI request.
    """

    return {
        "input_length": len(user_input),
        "route": route,
        "latency_seconds": latency,
        "cached": cached,
    }
