# 10. Source Tree
This structure is based on a modern full-stack monorepo approach, separating applications (apps) from shared code (packages).

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
│   │   │   ├── models/       # SQLAlchemy ORM models
│   │   │   ├── schemas/        # Pydantic schemas (for API validation)
│   │   │   ├── services/       # Business logic (Chat, LLM, Video Processing)
│   │   │   └── repository/     # Data access layer
│   │   ├── tests/              # Pytest tests
│   │   ├── .env.example
│   │   └── pyproject.toml      # Poetry config for backend
│   │
│   └── web/                  # Next.js Frontend (as per ui-architecture.md)
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
├── docker-compose.yml        # For PostgreSQL database
└── README.md
```
