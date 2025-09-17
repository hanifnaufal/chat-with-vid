# 13. Coding Standards
### Core Standards
- **Languages & Runtimes**: All backend code must be written in Python ~3.12.
- **Style & Linting**: All code must be formatted with Black and pass all linting checks from Ruff.
- **Test Organization**: All tests must be located in the apps/api/tests directory and follow the naming convention test_*.py.

### Naming Conventions
All Python code must strictly adhere to the PEP 8 style guide.

### Critical Rules
- **Use the Repository Pattern**: All database interactions MUST go through the repository layer.
- **Centralized Exception Handling**: Raise specific, custom business exceptions; do not use generic try...except blocks in the API layer.
- **Structured Logging Only**: All logging MUST use the configured structured logger. Do not use print().
  - **Logger Access**: Use `from app.core.logging import setup_logging` and `logger = setup_logging()` to get a configured logger instance in your modules.
  - **Log Levels**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) based on the severity of the message.
  - **Contextual Information**: Include relevant context in log messages using the `extra` parameter to the logging methods.
- **Secure API Key Handling**: The Gemini API key MUST only be accessed via a secure configuration service
- **Use LangChain Chains**: All LLM interactions MUST be constructed as LangChain chains (e.g., using LLMChain or Runnables) within the LLM Service. Do not invoke the base LLM directly from the langchain-google-genai package.
