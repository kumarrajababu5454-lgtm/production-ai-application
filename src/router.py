def route_request(user_input: str) -> str:
    """
    Decide which application path should handle the request.
    """

    text = user_input.lower().strip()

    if any(word in text for word in ["calculate", "add", "subtract", "multiply", "divide"]):
        return "calculator"

    if any(word in text for word in ["summarize", "summary"]):
        return "summarization"

    if any(word in text for word in ["translate", "translation"]):
        return "translation"

    return "general"
