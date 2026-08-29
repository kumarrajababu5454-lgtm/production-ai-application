import json
from pathlib import Path
from collections import Counter


LOG_PATH = Path("data/monitoring_log.json")


def load_monitoring_logs():
    """Load monitoring records from disk."""

    if not LOG_PATH.exists():
        return []

    with LOG_PATH.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def analyze_monitoring(logs):
    """Create monitoring and observability metrics."""

    if not logs:
        return {
            "total_requests": 0,
            "average_latency": 0.0,
            "cache_hits": 0,
            "cache_hit_rate": 0.0,
            "routes": {},
        }

    latencies = [
        record.get("latency", 0)
        for record in logs
    ]

    cache_hits = sum(
        1
        for record in logs
        if record.get("cached", False)
    )

    routes = Counter(
        record.get("route", "unknown")
        for record in logs
    )

    total_requests = len(logs)

    return {
        "total_requests": total_requests,
        "average_latency": round(
            sum(latencies) / len(latencies),
            4,
        ) if latencies else 0.0,
        "cache_hits": cache_hits,
        "cache_hit_rate": round(
            cache_hits / total_requests,
            2,
        ) if total_requests else 0.0,
        "routes": dict(routes),
    }


if __name__ == "__main__":

    logs = load_monitoring_logs()
    analysis = analyze_monitoring(logs)

    print()
    print("Online Monitoring Analysis")
    print("--------------------------")
    print(
        f"Total requests: "
        f"{analysis['total_requests']}"
    )

    print(
        f"Average latency: "
        f"{analysis['average_latency']:.4f}s"
    )

    print(
        f"Cache hits: "
        f"{analysis['cache_hits']}"
    )

    print(
        f"Cache hit rate: "
        f"{analysis['cache_hit_rate']:.0%}"
    )

    print()
    print("Routes")

    for route, count in analysis["routes"].items():
        print(f"{route}: {count}")
