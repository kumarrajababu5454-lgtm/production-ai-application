from src.config import client
from src.models import AIResponse
from src.guardrails import validate_input
from src.router import route_request
from src.cache import get_cached_response, set_cached_response
from src.monitoring import start_timer, calculate_latency, log_request
from src.model_selector import select_model
from src.adaptation import build_adapted_prompt


def generate_response(user_input: str) -> AIResponse:
    """
    Production-style AI response pipeline.

    Flow:
    Guardrails
        ?
    Cache
        ?
    Router
        ?
    Model Selection
        ?
    Prompt Adaptation
        ?
    Gemini
        ?
    Cache
        ?
    Monitoring
    """

    start_time = start_timer()

    # 1. Guardrails
    is_valid, error_message = validate_input(user_input)

    if not is_valid:
        return AIResponse(response=error_message)

    # 2. Cache
    cached_response = get_cached_response(user_input)

    if cached_response is not None:
        latency = calculate_latency(start_time)

        log_request(
            user_input=user_input,
            route="cache",
            latency=latency,
            cached=True,
        )

        return AIResponse(response=cached_response)

    # 3. Router
    route = route_request(user_input)

    # 4. Model Selection
    model_name = select_model(user_input)

    # 5. Model Adaptation
    prompt = build_adapted_prompt(
        user_input=user_input,
        route=route,
    )

    # 6. Generate response
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        result = response.text or "The AI returned an empty response."

    except Exception as error:
        error_text = str(error)

        # Friendly handling for Gemini quota/rate-limit errors.
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            result = (
                "The AI service has temporarily reached its API quota. "
                "Please try again later."
            )
        else:
            raise

    # 7. Cache successful responses
    if not (
        "temporarily reached its API quota" in result
    ):
        set_cached_response(user_input, result)

    # 8. Monitoring
    latency = calculate_latency(start_time)

    log_request(
        user_input=user_input,
        route=route,
        latency=latency,
        cached=False,
    )

    return AIResponse(response=result)
