from src.config import FAST_MODEL, MODEL_NAME


def select_model(user_input: str) -> str:
    """
    Select the Gemini model based on request complexity.

    Simple requests:
        Gemini 3.5 Flash-Lite
        -> optimized for low latency and high-volume tasks

    Complex requests:
        Gemini 3.6 Flash
        -> stronger model for more demanding requests
    """

    text = user_input.lower().strip()

    complex_words = [
        "analyze",
        "analyse",
        "explain in detail",
        "compare",
        "reason",
        "complex",
        "step by step",
        "deep analysis",
        "architecture",
        "design a system",
        "debug",
    ]

    if any(word in text for word in complex_words):
        return MODEL_NAME

    return FAST_MODEL
