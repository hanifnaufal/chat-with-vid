# 3. Tech Stack
### Cloud Infrastructure
- **Provider**: For the MVP, the primary deployment target is Local, utilizing Docker to ensure a consistent environment that meets the "zero operational budget" requirement. The architecture will be designed to be cloud-ready.
- **Future Recommendation**: Amazon Web Services (AWS).
- **Key Future Services**:
    - **AWS Fargate**: For deploying the containerized FastAPI application without managing servers.
    - **Amazon RDS for PostgreSQL**: For a fully managed, scalable PostgreSQL database.
    - **AWS Secrets Manager**: For securely handling the Gemini API key and other credentials.
- **Deployment Regions**: N/A for local MVP.

### Technology Stack Table
This table outlines the specific technologies chosen for the backend.

| Category | Technology | Version | Purpose | Rationale |
| --- | --- | --- | --- | --- |
| Language | Python | ~3.12 | Primary backend language | Modern, stable version with broad library compatibility. |
| Framework | FastAPI | ~0.111.0 | Web framework for building APIs | Required by PRD; offers high performance and native async support . |
| LLM Framework | LangChain | ~0.2.0 | High-level framework for orchestrating LLM interactions. | Provides abstractions for chains, prompts, and memory to simplify complex LLM workflows. |
| LLM Integration | langchain-google-genai | ~1.0.0 | LangChain integration for the Gemini API. | The official package for connecting LangChain to our chosen LLM provider. |
| ORM / DB Client | SQLAlchemy | ~2.0 | Database toolkit and Object Relational Mapper | Industry standard for Python; version 2.0 has excellent async support that pairs perfectly with FastAPI. |
| DB Driver | psycopg (v3) | ~3.1 | Modern PostgreSQL driver for Python | Offers superior performance and native async support compared to its predecessor (psycopg2). |
| Data Validation | Pydantic | ~2.7 | Data validation and settings management | Natively integrated into FastAPI for robust, type-hint-based validation of API requests. |
| Dependency Mgmt | Poetry | ~1.8 | Dependency management and packaging | Creates a deterministic, lock-file-based environment, which is superior for reproducibility (supports NFR7) . |
| Testing | pytest | ~8.2 | Testing framework | The de-facto standard for testing in Python; large ecosystem of plugins. |
| Linting/Formatting | Ruff & Black | latest | Code linting and formatting | Ruff is an extremely fast, all-in-one linter. Black is the standard, opinionated code formatter. Together they ensure code quality and consistency. |
