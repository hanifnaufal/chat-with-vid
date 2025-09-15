# 7. Core Workflows
### Workflow 1: Processing a New Video
This diagram shows the end-to-end process from a user submitting a URL to the asynchronous processing and analysis being completed.

```mermaid
sequenceDiagram
    participant FE as Next.js Frontend
    participant API as FastAPI Backend
    participant BG_Task as Async Processing Task
    participant DB as PostgreSQL DB

    FE->>+API: 1. POST /api/chats (url)
    API->>+DB: 2. Create Chat record (status: 'processing')
    DB-->>-API: chat_id
    API-->>-FE: 3. Respond with { chat_id }
    API-)BG_Task: 4. Trigger background task(chat_id)

    loop 5. Poll for status
        FE->>+API: GET /api/chats/{chat_id}
        API->>+DB: Check status
        DB-->>-API: status
        API-->>-FE: { status: 'processing' }
    end

    BG_Task->>External: 6. Fetch transcript & call Gemini API
    alt Processing Successful
        BG_Task->>+DB: 7a. Update Chat record (status: 'complete', summary, etc.)
        DB-->>-BG_Task: Success
    else Processing Failed
        BG_Task->>+DB: 7b. Update Chat record (status: 'failed')
        DB-->>-BG_Task: Success
    end

    FE->>+API: 8. GET /api/chats/{chat_id}
    API->>+DB: Check status
    DB-->>-API: status, summary, metadata
    API-->>-FE: 9. { status: 'complete', ...data }
```

### Workflow 2: Continuing a Saved Chat
This diagram shows the simpler flow for a user accessing a previously analyzed video from their history.

```mermaid
sequenceDiagram
    participant FE as Next.js Frontend
    participant API as FastAPI Backend
    participant DB as PostgreSQL DB

    FE->>+API: 1. GET /api/chats
    API->>+DB: 2. Query for all chats
    DB-->>-API: List of chats
    API-->>-FE: 3. Return chat history

    Note over FE: User selects a chat

    FE->>+API: 4. GET /api/chats/{chat_id}
    API->>+DB: 5. Query for chat and all its messages
    DB-->>-API: Chat data + messages
    API-->>-FE: 6. Return full conversation
```
