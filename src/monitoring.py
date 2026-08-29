import json
import time
from pathlib import Path


LOG_PATH = Path("data/monitoring_log.json")


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
    Record and persist basic information about an AI request.
    """

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "input_length": len(user_input),
        "route": route,
        "latency_seconds": latency,
        "cached": cached,
    }

    logs = []

    if LOG_PATH.exists():
        try:
            with LOG_PATH.open(
                "r",
                encoding="utf-8-sig",
            ) as file:
                logs = json.load(file)

            if not isinstance(logs, list):
                logs = []

        except (json.JSONDecodeError, OSError):
            logs = []

    logs.append(record)

    with LOG_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            logs,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return record
