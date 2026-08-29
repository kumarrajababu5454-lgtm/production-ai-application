# Production AI Application

A production-style AI application built with Python, Streamlit, and Google Gemini.

The project is designed to demonstrate how a simple AI chatbot can be improved with production-oriented components such as guardrails, routing, model selection, prompt adaptation, caching, monitoring, and error handling.

---

## Project Overview

This application provides a simple chat interface where a user can send a message and receive an AI-generated response from Google Gemini.

Instead of sending every request directly to Gemini, the application processes the request through several layers.

The main idea is:

```text
User
  ↓
Guardrails
  ↓
Cache Check
  ↓
Router
  ↓
Model Selection
  ↓
Prompt Adaptation
  ↓
Gemini API
  ↓
Response
  ↓
Cache
  ↓
Monitoring
  ↓
User



What the Application Does

When a user enters a message, the application processes it through the following steps.

1. User Input

The user enters a question or request through the Streamlit chat interface.

Example:

What is machine learning?
2. Guardrails

The request is checked before it continues through the AI pipeline.

This helps the application handle invalid or unacceptable input safely.

3. Cache Check

The application checks whether a response for the same normalized request is already available in the cache.

If a valid cached response exists, the application can return it without making another Gemini API request.

4. Router

The router determines how the request should move through the application.

5. Model Selection

The application selects a model based on the complexity of the request.

Simple requests can use the lightweight model, while more complex requests can use the stronger model.

6. Prompt Adaptation

The request is prepared using the application's prompt adaptation layer before being sent to Gemini.

7. Gemini API

The processed request is sent to Google Gemini.

8. Response

Gemini generates the response.

9. Cache

The response can be stored in the cache so that repeated requests can avoid unnecessary API calls.

10. Monitoring

The application records information about requests and application behavior through its monitoring layer.

11. User

The final response is displayed in the Streamlit interface.

Main Features
Streamlit Chat Interface

The project uses Streamlit to provide a simple browser-based chat interface.

The user can:

Enter a message
Send it to the AI application
View the AI response
Continue using the chat interface

The frontend is located in:

frontend/app.py
Guardrails

The application contains a guardrails layer that checks user input before processing.

This provides a controlled entry point for requests and allows invalid or unacceptable requests to be handled without sending them directly to the AI model.

The implementation is located in:

src/guardrails.py
Request Routing

The router separates request-processing logic from the rest of the application.

This allows the application to decide how a request should be processed without putting all of the logic inside the Streamlit frontend.

The implementation is located in:

src/router.py
Model Selection

The project contains a dedicated model-selection layer.

The purpose is to avoid treating every request in exactly the same way.

Simple requests can use a lightweight and faster model.

More complex requests can use the stronger model.

Examples of complex requests include requests containing concepts such as:

analyze
compare
reason
architecture
debug
step-by-step
deep analysis

The model-selection logic is implemented in:

src/model_selector.py

The model names used by the application are configured in:

src/config.py

The exact model names are intentionally controlled by the application configuration instead of being hard-coded throughout the application.

Prompt Adaptation

The application contains a prompt adaptation layer.

Its purpose is to prepare the request before it is sent to the selected Gemini model.

This keeps prompt-related logic separate from the main application flow.

Implementation:

src/adaptation.py
Response Caching

Caching is used to reduce unnecessary calls to the Gemini API.

The cache works with normalized user input.

For example:

"What is AI?"

and:

"  What   is AI? "

can be treated as the same request after normalization.

Cache TTL

The cache uses a 5-minute time-to-live (TTL).

After the TTL expires, the cached response is no longer treated as a valid cached response.

Cache Size

The cache is limited to 100 entries.

This prevents the cache from growing without a limit.

Oldest Entry Removal

When the cache reaches its maximum size, the oldest entry is removed so that a new entry can be stored.

Why Caching Is Useful

Without caching:

User
 ↓
Gemini API
 ↓
Response

With caching:

User
 ↓
Cache
 ├── Cached response → Return response
 │
 └── No cached response
          ↓
       Gemini API
          ↓
       Response
          ↓
         Cache

Caching can reduce unnecessary API requests when users repeat the same request within the cache lifetime.

The implementation is located in:

src/cache.py
Quota and Error Handling

The application includes error handling for Gemini API failures.

One important case is API quota or rate-limit exhaustion.

Instead of exposing a large raw API exception to the user, the application converts the error into a simpler user-friendly message.

For example:

The AI service has temporarily reached its API quota.
Please try again later.

This gives the user a useful message without exposing internal API error details.

Project Structure

The current project is organized into separate frontend, application, testing, and configuration components.

production-ai-application/
│
├── frontend/
│   └── app.py
│
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
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── render.yaml
└── requirements.txt
Important files
File	Purpose
frontend/app.py	Streamlit user interface
src/app.py	Main application logic
src/config.py	Application configuration and model settings
src/model_selector.py	Selects the appropriate model
src/cache.py	Handles response caching
src/guardrails.py	Handles input validation/guardrails
src/router.py	Handles request routing
src/adaptation.py	Handles prompt adaptation
src/monitoring.py	Application monitoring
src/optimization.py	Application optimization logic
src/health.py	Health-related application functionality
src/models.py	Application data models
tests/test_app.py	Automated tests
requirements.txt	Python dependencies
render.yaml	Render deployment configuration
.env.example	Example environment-variable configuration
.env	Local secrets/configuration
Installation

Clone or open the project and move into the project directory:

cd production-ai-application

Install the dependencies from requirements.txt:

pip install -r requirements.txt

The project uses the dependencies defined in requirements.txt.

Environment Variables

The application requires a Gemini API key.

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

The application reads the API key from the environment.

Important Security Rule

Never commit your real .env file to GitHub.

Your .gitignore should prevent secrets from being committed.

The project also contains:

.env.example

This file provides an example of the required environment-variable structure without exposing the real API key.

A real API key should never be placed inside:

README.md
Python source code
GitHub repositories
screenshots
public documentation
Run Locally

Start the Streamlit frontend with:

streamlit run frontend/app.py

Streamlit will provide a local URL in the terminal.

Open that URL in your browser to use the application.

Testing

The project uses pytest for automated testing.

Run the tests from the project root:

pytest

The current test suite contains 15 tests.

The tests are located in:

tests/test_app.py

Automated tests help verify that application behavior continues to work after code changes.

Local Testing Performed

The Streamlit application has been tested locally.

The local testing included:

Normal request

A normal conversational request was sent through the application and produced an AI response.

Complex request

A more complex request such as:

Compare machine learning and deep learning step by step.

was sent to test the model-selection path.

Guardrail behavior

Invalid/empty-type input was tested to verify that the guardrails provide controlled handling instead of allowing every request to proceed normally.

Cache behavior

Repeated requests can be processed through the caching layer so that an existing valid cached response can be reused.

Quota/Error handling

The Gemini API quota condition was also observed during local testing.

Instead of displaying the raw API exception, the application displayed:

The AI service has temporarily reached its API quota.
Please try again later.

This confirms that the application has user-facing handling for this type of API failure.

Production Architecture

This project is intentionally designed as more than a basic Gemini chatbot.

A basic chatbot could look like:

User
 ↓
Gemini
 ↓
Response

This project adds several application layers:

                 USER
                   ↓
              GUARDRAILS
                   ↓
              CACHE CHECK
                   ↓
                ROUTER
                   ↓
            MODEL SELECTION
                   ↓
           PROMPT ADAPTATION
                   ↓
              GEMINI API
                   ↓
               RESPONSE
                   ↓
                 CACHE
                   ↓
              MONITORING
                   ↓
                 USER
Separation of Concerns

Different parts of the application have different responsibilities.

For example:

Guardrails handle input checks.
The router handles request routing.
Model selection handles model choice.
Prompt adaptation handles prompt preparation.
Cache handles repeated requests.
Monitoring handles application observations.
The frontend handles user interaction.

This makes the code easier to understand and maintain.

Model Routing

Not every request requires the same level of model capability.

The application can route simple requests to a lightweight model and more complex requests to a stronger model.

Optimization

Caching and model selection are examples of optimization techniques used in the project.

The goal is to avoid unnecessary work where possible.

Monitoring

The project contains a monitoring layer so application behavior can be observed separately from the main request-processing logic.

Guardrails

The guardrails layer provides an initial control point before requests are processed by the AI model.

Error Handling

API failures, including quota-related failures, are handled so that users receive understandable messages instead of raw internal exceptions.

Testing

Automated tests provide a repeatable way to check application behavior after changes.

Deployment

The project contains a Render deployment configuration:

render.yaml

This file defines the deployment configuration used by Render.

The repository should be connected to Render so that the deployment can use the configuration in render.yaml.

No production URL is documented here because a production URL should only be added when it is confirmed and available.

Technology Stack

The project uses the following technologies:

Python — application programming language
Streamlit — web-based chat interface
Google Gemini API — AI model service
pytest — automated testing
python-dotenv — environment-variable loading
Pydantic — data validation/model structures

Additional packages used by the project are defined in:

requirements.txt
Future Improvements

Possible future improvements include:

Add more detailed monitoring and metrics
Add stronger automated test coverage
Add more advanced request classification
Improve caching strategies
Add authentication and user management
Add persistent conversation storage
Add production logging and observability

These are future improvements and are not currently claimed as implemented features.

Disclaimer

This is a production-style learning/project implementation.

The project demonstrates concepts commonly used when building production-oriented AI applications, including routing, model selection, caching, guardrails, monitoring, error handling, and automated testing.

However, "production-style" does not mean that the application is guaranteed to be production-ready for enterprise-scale workloads.

Before using a system like this for a real production environment, additional work may be required for areas such as:

Security
Authentication
Authorization
Scalability
Reliability
Persistent storage
Observability
Cost controls
Privacy
Compliance
Load testing
Disaster recovery

The purpose of this project is to learn and demonstrate how these concepts can be combined into a structured AI application.


### One thing before you save it

Because you specifically asked for the README to **match the code exactly**, I would **not yet trust the sections for the exact model names, exact guardrail rules, or exact Render start command** until we have the actual files available.

If you have the project files attached to this chat, send/upload them and I can verify those exact details and give







Project 4 -

@'
# Production AI Application + AI Evaluation Platform

A production-style AI application built with Python, Streamlit, and Google Gemini.

The project demonstrates two connected parts:

1. A production-oriented AI application.
2. An evaluation and continuous-improvement platform built around that application.

The production application includes guardrails, routing, model selection, prompt adaptation, caching, monitoring, optimization, and error handling.

The evaluation platform measures AI quality using automated evaluation, LLM-as-Judge evaluation, human feedback, failure analysis, A/B testing, monitoring, and continuous improvement.

---

## Project Overview

The project starts with a simple AI application and adds production-oriented engineering layers around it.

The main application flow is:

```text
User
  ↓
Guardrails
  ↓
Cache Check
  ↓
Router
  ↓
Model Selection
  ↓
Prompt Adaptation
  ↓
Gemini API
  ↓
Response
  ↓
Cache
  ↓
Monitoring
  ↓
User

Project 4 adds an evaluation loop around the application:

AI Application
      ↓
Evaluation Dataset
      ↓
Automated Evaluation
      ↓
LLM-as-Judge
      ↓
Human Feedback
      ↓
Failure Analysis
      ↓
A/B Testing
      ↓
Continuous Improvement
      ↓
Evaluate Again

The purpose is not only to build an AI application, but also to measure its quality and create a repeatable improvement process.

Part 1 — Production AI Application
Main Features
Streamlit Chat Interface

The frontend provides a browser-based chat interface.

The user can:

Enter a message
Send it to the AI application
View the AI response
Continue using the application

Frontend:

frontend/app.py
Guardrails

The application validates user input before sending it to the AI model.

The current validation includes:

Empty input handling
Input length checking

Implementation:

src/guardrails.py
Request Routing

The router separates requests into application routes.

Current routes include:

calculator
summarization
translation
general

Implementation:

src/router.py
Model Selection

The application selects a Gemini model based on request complexity.

Complex-request indicators include terms such as:

analyze
analyse
explain in detail
compare
reason
complex
step by step
deep analysis
architecture
design a system
debug

Implementation:

src/model_selector.py

Model configuration:

src/config.py

The model names are controlled through the application configuration.

Prompt Adaptation

The application changes the prompt instructions based on the selected route.

For example:

Calculator requests focus on mathematical accuracy.
Summarization requests focus on important information.
Translation requests focus on preserving meaning.
General requests use the general assistant behavior.

Implementation:

src/adaptation.py
Response Caching

The application caches responses for repeated requests.

The cache:

Normalizes user input
Uses a 5-minute TTL
Supports up to 100 entries
Removes the oldest entry when the cache reaches its limit

Implementation:

src/cache.py

Caching helps avoid unnecessary Gemini API requests for repeated requests.

Monitoring

The monitoring layer records information about application requests.

The recorded information includes:

Input length
Route
Request latency
Whether the response came from cache

Implementation:

src/monitoring.py

The monitoring data is also used by the Project 4 evaluation platform.

Error and Quota Handling

The application handles Gemini API quota/rate-limit errors.

Instead of exposing the raw API exception, the user receives a simpler message:

The AI service has temporarily reached its API quota.
Please try again later.

This behavior was observed during local testing.

Part 2 — AI Evaluation & Continuous Improvement Platform

Project 4 is built on top of the production AI application.

Its purpose is to answer an important question:

How do we know whether an AI application is working well, and how do we improve it when it does not?

The evaluation platform provides a repeatable process for measuring AI quality.

Evaluation Dataset

The project contains evaluation cases used to test the AI application.

The dataset is stored in:

data/evaluation_dataset.json

Each evaluation case contains information such as:

User question
Expected answer
Category

The evaluation dataset allows the same test cases to be run repeatedly.

Automated Evaluation

The first evaluation layer compares the generated answer against the expected answer using automated scoring.

Results are stored in:

data/evaluation_results.json
data/evaluation_scored_results.json

The current evaluation contains:

Total tests: 5
Passed: 5
Failed: 0
Average score: 0.80

Automated evaluation is useful for repeatable checks, but it does not completely describe the quality of an AI response.

LLM-as-Judge

The project also uses an LLM-based judge to evaluate generated answers.

The judge evaluates dimensions such as:

Correctness
Relevance
Completeness
Instruction following

Results are stored in:

data/evaluation_judge_results.json

The current evaluation produced:

Total tests: 5
Average judge score: 5.00/5

This provides a second quality signal in addition to automated scoring.

Human Feedback

The platform supports human feedback for individual evaluation results.

A reviewer can provide:

Rating
Approval/rejection
Optional comment

Human feedback is stored in:

data/human_feedback.json

Human feedback is useful because automated metrics and LLM judges cannot capture every aspect of user experience.

Failure Analysis

The project analyzes evaluation results to identify failed cases.

Implementation:

src/evaluation/failure_analysis.py

Results:

data/failure_analysis.json

The current evaluation produced:

Failure cases: 0
All current evaluation cases passed.

When failures exist, the failure report can identify information such as:

Test ID
Category
Automated score
LLM judge score
Failure reasons
Judge explanation
A/B Testing

The project includes A/B testing for comparing two prompt variants.

The purpose is to determine whether an alternative prompt/configuration performs better.

Results are stored in:

data/ab_test_results.json

The completed A/B test produced:

Variant A: 5.00/5
Variant B: 4.80/5
Winner: Variant A

This demonstrates how an AI system can compare alternative approaches instead of changing prompts based only on intuition.

Online Monitoring

The evaluation platform also reads application monitoring information.

Monitoring can show:

Total requests
Average latency
Cache hits
Cache hit rate
Route usage

Monitoring results are based on:

data/monitoring_log.json

The monitoring layer connects application behavior with the evaluation process.

Continuous Improvement

The platform combines the evaluation components into a continuous-improvement workflow.

The workflow is:

Run AI Application
        ↓
Collect Evaluation Results
        ↓
Automated Evaluation
        ↓
LLM-as-Judge
        ↓
Human Feedback
        ↓
Failure Analysis
        ↓
A/B Testing
        ↓
Choose Better Variant
        ↓
Evaluate Again

The continuous improvement analysis is implemented in:

src/evaluation/continuous_improvement.py

Results are stored in:

data/continuous_improvement.json

The current analysis reports:

Failure cases: 0
A/B Variant A: 5.0/5
A/B Variant B: 4.8/5
A/B Winner: Variant A

There is currently not enough historical evaluation data to calculate a quality change between two evaluation runs.

This is expected because quality-change measurement requires at least two evaluation runs.

Evaluation Dashboard

Project 4 includes a separate Streamlit dashboard:

evaluation_app/app.py

The dashboard brings the evaluation information together in one place.

It displays areas such as:

Latest evaluation
Evaluation history
Evaluation results
Human feedback
A/B testing
Online monitoring
Failure analysis
Continuous improvement

Run the dashboard with:

streamlit run evaluation_app/app.py
Project 4 Architecture

The overall Project 4 architecture is:

                    PRODUCTION AI APPLICATION
                              │
                              ▼
                     Evaluation Dataset
                              │
                              ▼
                    Automated Evaluation
                              │
                              ▼
                       LLM-as-Judge
                              │
                              ▼
                       Human Feedback
                              │
                              ▼
                       Failure Analysis
                              │
                              ▼
                         A/B Testing
                              │
                              ▼
                    Continuous Improvement
                              │
                              ▼
                       Evaluate Again

This creates a feedback loop instead of treating evaluation as a one-time activity.

Project Structure
production-ai-application/
│
├── frontend/
│   └── app.py
│
├── evaluation_app/
│   └── app.py
│
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
│   ├── router.py
│   │
│   └── evaluation/
│       ├── ab_test.py
│       ├── continuous_improvement.py
│       ├── failure_analysis.py
│       └── ...
│
├── data/
│   ├── evaluation_dataset.json
│   ├── evaluation_results.json
│   ├── evaluation_scored_results.json
│   ├── evaluation_judge_results.json
│   ├── evaluation_history.json
│   ├── ab_test_results.json
│   ├── human_feedback.json
│   ├── monitoring_log.json
│   ├── failure_analysis.json
│   └── continuous_improvement.json
│
├── tests/
│   └── test_app.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── render.yaml
└── requirements.txt
Important Files
File	Purpose
frontend/app.py	Production AI Streamlit interface
evaluation_app/app.py	Evaluation and monitoring dashboard
src/app.py	Main AI application pipeline
src/config.py	Gemini configuration and model settings
src/guardrails.py	Input validation
src/router.py	Request routing
src/model_selector.py	Model selection
src/adaptation.py	Prompt adaptation
src/cache.py	Response caching
src/monitoring.py	Application monitoring
src/evaluation/	Evaluation and improvement components
data/	Evaluation and monitoring results
tests/test_app.py	Application tests
requirements.txt	Python dependencies
render.yaml	Render deployment configuration
Installation

Move into the project directory:

cd production-ai-application

Install the dependencies:

pip install -r requirements.txt

This project does not require creating a separate Python virtual environment.

Environment Variables

The application requires a Gemini API key.

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

The application loads the key from the environment.

Important Security Rule

Never commit the real .env file to GitHub.

The project includes:

.env.example

The real API key should never be placed inside:

README.md
Python source code
GitHub repositories
Screenshots
Public documentation
Run the Production Application

Start the main Streamlit application:

streamlit run frontend/app.py

Streamlit will provide a local URL.

Open that URL in a browser to use the production AI application.

Run the Evaluation Dashboard

Start the Project 4 dashboard:

streamlit run evaluation_app/app.py

The dashboard provides a visual view of evaluation, A/B testing, monitoring, failure analysis, and continuous improvement.

Testing

The project uses pytest.

Run the application test suite explicitly with:

pytest -q tests

The verified test result is:

15 passed

Python compilation was also verified successfully with:

python -m compileall -q src tests evaluation_app
Evaluation Commands
Failure Analysis
python -m src.evaluation.failure_analysis

Current result:

Failure cases: 0
Continuous Improvement
python -m src.evaluation.continuous_improvement

Current result:

A/B Variant A: 5.0/5
A/B Variant B: 4.8/5
A/B Winner: Variant A
A/B Testing
python -m src.evaluation.ab_test

The completed experiment selected Variant A as the winner.

Evaluation Results

The current completed evaluation produced:

Automated Evaluation
--------------------
Total tests: 5
Average score: 0.80
Passed: 5
Failed: 0

LLM-as-Judge
------------
Total tests: 5
Average score: 5.00/5

A/B Testing
-----------
Variant A: 5.00/5
Variant B: 4.80/5
Winner: Variant A

Failure Analysis
----------------
Failure cases: 0

These values describe the current evaluation run and should not be treated as permanent benchmark results.

Production Architecture

A basic AI application could look like:

User
  ↓
Gemini
  ↓
Response

This project adds production-oriented layers:

                 USER
                   ↓
              GUARDRAILS
                   ↓
              CACHE CHECK
                   ↓
                ROUTER
                   ↓
            MODEL SELECTION
                   ↓
           PROMPT ADAPTATION
                   ↓
              GEMINI API
                   ↓
               RESPONSE
                   ↓
                 CACHE
                   ↓
              MONITORING
                   ↓
                 USER

Project 4 then evaluates this application:

Production AI Application
          ↓
      Evaluation
          ↓
    Quality Signals
          ↓
   Failure Analysis
          ↓
     A/B Testing
          ↓
     Improvement
          ↓
     Evaluation
Separation of Concerns

Different components have different responsibilities.

Guardrails handle input validation.
Router handles request routing.
Model selection handles model choice.
Prompt adaptation handles prompt preparation.
Cache handles repeated requests.
Monitoring records application behavior.
Evaluation measures AI quality.
LLM-as-Judge provides an additional quality signal.
Human feedback captures reviewer input.
Failure analysis identifies problems.
A/B testing compares alternatives.
Continuous improvement connects these components.
Streamlit provides the user interfaces.

This separation keeps the project easier to understand and maintain.

Deployment

The project contains:

render.yaml

This provides Render deployment configuration.

The application should be connected to Render and configured with the required environment variables.

No production URL is documented here unless it has been confirmed.

Technology Stack

The project uses:

Python
Streamlit
Google Gemini API
pytest
python-dotenv
Pydantic

Additional dependencies are listed in:

requirements.txt
What This Project Demonstrates

This project demonstrates how an AI system can be developed in stages:

AI Model
   ↓
Application
   ↓
Production Engineering
   ↓
Evaluation
   ↓
Monitoring
   ↓
Failure Analysis
   ↓
A/B Testing
   ↓
Continuous Improvement

The important lesson is that building an AI application does not end when the model produces an answer.

The system also needs ways to:

Measure quality
Detect failures
Collect feedback
Monitor behavior
Compare alternatives
Improve over time
Future Improvements

Possible future improvements include:

Larger evaluation datasets
More evaluation categories
More detailed monitoring
More human feedback
More A/B experiments
Historical quality tracking across many runs
Stronger observability
Authentication
Persistent user data
Production-scale infrastructure

These are future improvements and are not claimed as currently implemented features.

Disclaimer

This is a production-style learning and portfolio project.

It demonstrates concepts used when building production-oriented AI applications and AI evaluation systems.

"Production-style" does not mean that the project is guaranteed to be production-ready for enterprise-scale workloads.

A real production deployment may require additional work for areas such as:

Security
Authentication
Authorization
Scalability
Reliability
Persistent storage
Observability
Cost controls
Privacy
Compliance
Load testing
Disaster recovery

The purpose of this project is to demonstrate how these concepts can be combined into a structured AI application and continuous evaluation workflow.
'@ | Set-Content README.md -Encoding UTF8

git diff --stat README.md
