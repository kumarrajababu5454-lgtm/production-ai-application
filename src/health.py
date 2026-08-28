def health_check() -> dict:
    """
    Basic application health check.
    """

    return {
        "status": "healthy",
        "service": "production-ai-application",
    }
