def validate_input(user_input: str) -> tuple[bool, str]:
    """
    Validate user input before sending it to the AI model.
    """

    # Empty input
    if not user_input or not user_input.strip():
        return False, "Please enter a message."

    # Length limit
    if len(user_input) > 2000:
        return False, "Your message is too long. Please keep it under 2000 characters."

    return True, ""
