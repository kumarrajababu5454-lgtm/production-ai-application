def build_adapted_prompt(user_input: str, route: str) -> str:
    """
    Adapt the model behavior based on the application route.
    """

    base_instruction = """
You are a reliable production AI assistant.

Rules:
- Be clear and concise.
- Do not invent facts.
- If the request is unclear, ask for clarification.
"""

    route_instruction = {
        "calculator": """
Focus on mathematical accuracy.
Explain the calculation clearly.
""",
        "summarization": """
Focus on extracting the most important information.
Keep the summary concise.
""",
        "translation": """
Preserve the meaning of the original text.
Do not add unnecessary information.
""",
        "general": """
Answer the user's question clearly and helpfully.
""",
    }

    selected_instruction = route_instruction.get(
        route,
        route_instruction["general"],
    )

    return f"""
{base_instruction}

{selected_instruction}

User request:
{user_input}
"""
