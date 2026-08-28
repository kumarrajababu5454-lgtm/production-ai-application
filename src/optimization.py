def optimize_request(user_input: str) -> str:
    """
    Prepare the user request for efficient inference.

    Removes unnecessary whitespace while preserving the
    meaning of the request.
    """

    return " ".join(user_input.split())
