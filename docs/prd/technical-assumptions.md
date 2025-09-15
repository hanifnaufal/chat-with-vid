# Technical Assumptions
### Repository Structure: Monorepo
The project will be structured as a monorepo. This approach is recommended in the project brief to keep the Python backend and Next.js frontend code together in a single, portfolio-ready package, simplifying dependency management and cross-platform development.

### Service Architecture: Decoupled Client-Server
The application will be built with a decoupled architecture where the Next.js frontend acts as the client and the Python/FastAPI application serves as the backend API server. The final deployment target (e.g., monolithic server, serverless functions) is deferred and will be decided after the local MVP is complete.

### Testing Requirements: Unit + Integration
The testing strategy for the MVP will focus on a combination of Unit and Integration tests. This ensures that individual components function correctly and that the frontend and backend can communicate as expected. A full end-to-end (E2E) testing suite will be considered a post-MVP addition to maintain a focused initial scope.

### Additional Technical Assumptions and Requests
The following technologies are specified in the project brief and are considered foundational assumptions for the architecture:

- **Frontend**: React with Next.js
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL (specifically managed with Docker for local development)
- **LLM**: Google's Gemini API
