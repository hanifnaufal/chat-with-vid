# Chat with Video

This project is a web application that allows users to engage in a conversational chat with any YouTube video. By submitting a video URL, users can ask questions, request summaries, and extract key information directly from the video's content, transforming a passive viewing experience into an interactive knowledge base.

## Core Features

-   **Process YouTube Videos**: Submit any public YouTube URL to begin.
-   **AI-Powered Analysis**: Automatically generates a concise summary, a list of actionable items, and suggested questions based on the video's transcript.
-   **Interactive Chat**: Engage in a conversation with the video's content. The AI uses the transcript as its context, providing relevant and focused answers.
-   **Streaming Responses**: AI responses are streamed in real-time for a dynamic, conversational feel.
-   **Local Chat History**: All conversations are saved on your local machine, allowing you to review or continue them later.

## Tech Stack

The project is a full-stack application built with a modern, decoupled architecture.

#### Backend

| Category | Technology |
| --- | --- |
| Language | Python 3.12 |
| Framework | FastAPI |
| LLM Integration | LangChain, Google Gemini |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Dependency Mgmt | Poetry |

#### Frontend

| Category | Technology |
| --- | --- |
| Framework | Next.js (App Router) |
| Language | TypeScript |
| UI Components | Shadcn/ui, Radix UI |
| Styling | Tailwind CSS |
| State Management | TanStack Query, Zustand |
| Icons | Lucide Icons |

## Project Structure

This project is a monorepo containing the `api` and `web` applications.

```
chat-with-vid/
├── apps/
│   ├── api/                  # Python/FastAPI Backend
│   └── web/                  # Next.js Frontend
├── packages/
│   └── shared-types/         # (Optional) For sharing types between FE/BE
├── .gitignore
├── docker-compose.yml        # For PostgreSQL database
└── README.md
```

## Future Vision

This project serves as a strong foundation. Future plans include:
-   Deploying a publicly accessible live demo.
-   Linking AI answers to specific video timestamps.
-   Supporting additional content sources beyond YouTube.

## Contributing

Contributions are welcome! If you have suggestions or want to improve the project, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.