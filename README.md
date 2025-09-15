# Chat with Video

This project is a web application that allows users to engage in a conversational chat with any YouTube video. By submitting a video URL, users can ask questions, request summaries, and extract key information directly from the video's content, transforming a passive viewing experience into an interactive knowledge base.

## Features
- **Process YouTube Videos**: Submit any public YouTube URL to begin.
- **AI-Powered Analysis**: Automatically generates a concise summary, a list of actionable items, and suggested questions based on the video's transcript.
- **Interactive Chat**: Engage in a conversation with the video's content. The AI uses the transcript as its context, providing relevant and focused answers.
- **Streaming Responses**: AI responses are streamed in real-time for a dynamic, conversational feel.
- **Local Chat History**: All conversations are saved on your local machine, allowing you to review or continue them later.

## Technology Stack

- **Frontend**: Next.js 14 with React Server Components
- **Backend**: FastAPI with Python 3.12
- **Database**: PostgreSQL 16
- **AI**: Google Gemini API via LangChain
- **Containerization**: Docker and Docker Compose
- **Dependency Management**: Poetry (backend), npm (frontend)

## Prerequisites

- Docker and Docker Compose
- Google Gemini API key (for AI features)

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd chat-with-vid
   ```

2. **Set up environment variables:**
   ```bash
   # Copy and configure backend environment variables
   cp apps/api/.env.example apps/api/.env
   
   # Copy and configure frontend environment variables
   cp apps/web/.env.local.example apps/web/.env.local
   ```
   
   Edit `apps/api/.env` and configure your environment variables:
   ```
   POSTGRES_PASSWORD=your_secure_database_password_here
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

3. **Start all services:**
   ```bash
   ./start.sh
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: postgresql://postgres:${POSTGRES_PASSWORD}@localhost:5432/chat_with_vid

### Development Mode

For development with hot reloading:

```bash
./dev.sh
```

This will start services using `docker-compose.dev.yml` with volume mounts for live code updates.

## Project Structure

```
chat-with-vid/
├── apps/
│   ├── api/                  # Python/FastAPI Backend
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py         # FastAPI app instance and middleware
│   │   │   ├── api/            # API Routers (Endpoints)
│   │   │   │   └── v1/
│   │   │   │       └── chats.py
│   │   │   ├── core/           # Core logic (config, db session)
│   │   │   ├── models/         # SQLAlchemy ORM models
│   │   │   ├── schemas/        # Pydantic schemas (for API validation)
│   │   │   ├── services/       # Business logic (Chat, LLM, Video Processing)
│   │   │   └── repository/     # Data access layer
│   │   ├── tests/              # Pytest tests
│   │   ├── .env.example
│   │   └── pyproject.toml      # Poetry config for backend
│   │
│   └── web/                  # Next.js Frontend
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   └── lib/
│       ├── .env.local.example
│       └── package.json
│
├── packages/
│   └── shared-types/         # (Optional) For sharing types between FE/BE
│
├── .gitignore
├── docker-compose.yml        # Production services
├── docker-compose.dev.yml    # Development services with hot reloading
├── start.sh                  # Production startup script
├── dev.sh                    # Development startup script
└── README.md
```

## Manual Installation (Alternative)

If you prefer to run services directly without Docker:

### Backend Setup

1. Navigate to the API directory:
   ```bash
   cd apps/api
   ```

2. Install Poetry (if not already installed):
   ```bash
   pip install poetry
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google Gemini API key
   ```

5. Run the development server:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the web directory:
   ```bash
   cd apps/web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local if needed
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

### Backend (.env)
- `GOOGLE_API_KEY`: Your Google Gemini API key
- `DATABASE_URL`: PostgreSQL connection string (automatically set in Docker)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL (automatically set in Docker)

## API Endpoints

- `POST /api/v1/chats/`: Create a new chat session with a YouTube URL
- `GET /api/v1/chats/{chat_id}/messages/`: Get all messages for a chat session
- `POST /api/v1/chats/{chat_id}/messages/`: Send a message to the chat session

## Development

### Code Quality

- **Backend**: Code is formatted with Black and linted with Ruff
- **Frontend**: Code is formatted with Prettier and linted with ESLint

### Testing

- **Backend**: Uses pytest for testing
- Run tests with: `poetry run pytest`

### Database

The PostgreSQL database is automatically set up with Docker. For direct access:
```bash
docker-compose exec db psql -U postgres -d chat_with_vid
```

## Deployment

The application is designed to run in Docker containers. For production deployment:

1. Build and push Docker images to your container registry
2. Deploy using your preferred orchestration platform (Kubernetes, AWS ECS, etc.)
3. Set up appropriate environment variables and secrets management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

For issues and feature requests, please [create an issue](link-to-issues) on GitHub.
