from src.models import AIResponse, UserMessage
from src.guardrails import validate_input
from src.router import route_request
from src.cache import (
    get_cached_response,
    set_cached_response,
    clear_cache,
)
from src.monitoring import log_request
from src.model_selector import select_model


def test_user_message_schema():
    message = UserMessage(message="Hello")
    assert message.message == "Hello"


def test_ai_response_schema():
    response = AIResponse(response="Hello!")
    assert response.response == "Hello!"


def test_empty_input_is_rejected():
    valid, message = validate_input("")
    assert valid is False
    assert message == "Please enter a message."


def test_long_input_is_rejected():
    long_message = "a" * 2001
    valid, message = validate_input(long_message)
    assert valid is False


def test_valid_input_is_allowed():
    valid, message = validate_input("What is AI?")
    assert valid is True
    assert message == ""


def test_calculator_route():
    assert route_request("Calculate 25 multiplied by 40") == "calculator"


def test_summarization_route():
    assert route_request("Summarize this text") == "summarization"


def test_translation_route():
    assert route_request("Translate this to Hindi") == "translation"


def test_general_route():
    assert route_request("What is artificial intelligence?") == "general"


def test_cache():
    clear_cache()

    assert get_cached_response("Hello") is None

    set_cached_response("Hello", "Hi there!")

    assert get_cached_response("Hello") == "Hi there!"

    clear_cache()

    assert get_cached_response("Hello") is None


def test_monitoring_log():
    log = log_request(
        user_input="Hello",
        route="general",
        latency=0.25,
        cached=False,
    )

    assert log["input_length"] == 5
    assert log["route"] == "general"
    assert log["latency_seconds"] == 0.25
    assert log["cached"] is False


def test_model_selection():
    model = select_model("Explain artificial intelligence in detail")

    assert isinstance(model, str)
    assert len(model) > 0
from src.adaptation import build_adapted_prompt


def test_adapted_prompt():
    prompt = build_adapted_prompt(
        user_input="Summarize this document",
        route="summarization",
    )

    assert "production AI assistant" in prompt
    assert "Summarize this document" in prompt
from src.optimization import optimize_request


def test_request_optimization():
    result = optimize_request(
        "   What   is   artificial   intelligence?   "
    )

    assert result == "What is artificial intelligence?"

from src.health import health_check


def test_health_check():
    result = health_check()

    assert result["status"] == "healthy"
    assert result["service"] == "production-ai-application"
