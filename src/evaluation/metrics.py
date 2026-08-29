import re


def normalize_text(text: str) -> str:
    """Normalize text before comparison."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def calculate_keyword_score(expected: str, actual: str) -> float:
    """Calculate the percentage of expected words found in the actual response."""
    expected_words = set(normalize_text(expected).split())
    actual_words = set(normalize_text(actual).split())

    if not expected_words:
        return 0.0

    matched_words = expected_words.intersection(actual_words)

    return round(len(matched_words) / len(expected_words), 2)


def evaluate_response(expected: str, actual: str) -> dict:
    """Evaluate one AI response against its expected answer."""
    score = calculate_keyword_score(expected, actual)

    return {
        "score": score,
        "passed": score >= 0.5,
    }
