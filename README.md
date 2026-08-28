Update the existing README.md for this production-ai-application project.

IMPORTANT:
- Do NOT modify application code.
- Do NOT create new files.
- Do NOT remove existing useful documentation.
- Only update README.md.
- Keep the language simple so a beginner can understand the project.
- Do not claim features that are not actually implemented.

First inspect the entire project structure and existing README.md.

Then rewrite/update README.md so it accurately documents the current application.

Include these sections:

1. Project Title
   Production AI Application

2. Project Overview
   Explain in simple language that this is a production-style AI application built with Python, Streamlit, Google Gemini, routing, model selection, guardrails, caching, monitoring, and error handling.

3. What the Application Does
   Explain the complete user journey:
   User enters a message
   → Guardrails
   → Cache check
   → Router
   → Model selection
   → Prompt adaptation
   → Gemini API
   → Response
   → Cache
   → Monitoring
   → User

4. Main Features
   Explain:
   - Streamlit chat interface
   - Guardrails
   - Request routing
   - Model selection
   - Prompt adaptation
   - Response caching
   - Cache TTL
   - Cache size limit
   - Monitoring
   - Gemini API integration
   - Friendly quota/error handling
   - Automated tests

5. Model Selection
   Clearly explain the current model-selection logic.
   Simple requests should use the lightweight/fast model.
   Complex requests such as analyze, compare, reason, architecture, debug, step-by-step, and deep analysis should use the stronger model.

   IMPORTANT:
   Read model_selector.py and config.py and use the EXACT model names currently present in the code.
   Do not invent model names.

6. Cache
   Explain:
   - input normalization
   - 5-minute TTL if that is what the current code actually uses
   - maximum 100 entries if that is what the current code actually uses
   - oldest-entry removal when the cache is full
   - why caching reduces unnecessary API calls

7. Guardrails
   Explain how invalid/unsafe/empty-type requests are handled.
   Read guardrails.py and document the actual behavior instead of guessing.

8. Quota and Error Handling
   Explain that Gemini API quota/rate-limit errors are converted into a user-friendly message instead of exposing the raw API exception.
   Mention the type of error only if it is confirmed by the code.

9. Project Structure
   Document the actual current structure:

   production-ai-application/
   ├── frontend/
   │   └── app.py
   ├── src/
   │   ├── adaptation.py
   │   ├── app.py
   │   ├── cache.py
   │   ├── config.py
   │   ├── guardrails.py
   │   ├── health.py
   │   ├── models.py
   │   ├── model_selector.py
   │   ├── monitoring.py
   │   ├── optimization.py
   │   └── router.py
   ├── tests/
   │   └── test_app.py
   ├── .env
   ├── .env.example
   ├── .gitignore
   ├── README.md
   ├── render.yaml
   └── requirements.txt

   Verify this against the actual project before documenting it.

10. Installation
    Explain how to install dependencies using requirements.txt.

11. Environment Variables
    Explain GEMINI_API_KEY.
    Explain that .env should never be committed to GitHub.
    Explain .env.example.

12. Run Locally
    Give the exact command currently required to start the Streamlit frontend.

13. Testing
    Explain how to run pytest.
    Document the current test count only after checking the actual tests.

14. Local Testing Performed
    Document that the Streamlit application was tested locally.
    Mention normal requests, complex requests, guardrail behavior, caching, and quota/error handling only if supported by the current project/testing evidence.

15. Production Architecture
    Explain why the project is more than a basic Gemini chatbot:
    - separation of concerns
    - model routing
    - optimization
    - caching
    - monitoring
    - guardrails
    - error handling
    - testing

16. Deployment
    Document the Render deployment configuration using the actual render.yaml.
    Do not invent deployment URLs.
    If a production URL is not present in the repository, do not make one up.

17. Technology Stack
    Include only technologies actually used:
    Python
    Streamlit
    Google Gemini API
    pytest
    and any other dependency actually used by the project.

18. Future Improvements
    Keep this short and realistic.

19. Disclaimer
    Clearly state that this is a production-style learning/project implementation and not a guarantee of production readiness at enterprise scale.

IMPORTANT:
Before writing the README, inspect:
- frontend/app.py
- src/app.py
- src/config.py
- src/model_selector.py
- src/cache.py
- src/guardrails.py
- src/router.py
- src/adaptation.py
- src/monitoring.py
- src/optimization.py
- src/health.py
- src/models.py
- tests/test_app.py
- requirements.txt
- render.yaml
- .env.example

Make the README match the code exactly.
Do not expose API keys or secrets.