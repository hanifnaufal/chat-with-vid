# 8. REST API Spec
This OpenAPI 3.0 specification serves as the formal contract between the frontend and the backend.

```yaml
openapi: 3.0.1
info:
  title: "Chat with YouTube Video API"
  version: "1.0.0"
  description: "API for processing YouTube videos and interacting with them via chat."
servers:
  - url: http://localhost:8000
    description: Local development server

paths:
  /api/v1/chats:
    post:
      summary: "Submit a new source URL for processing"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                source_url:
                  type: string
                  format: uri
                  example: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                source_type:
                  type: string
                  example: "YOUTUBE"
      responses:
        '202':
          description: "Accepted for processing. Returns the new chat ID."
          content:
            application/json:
              schema:
                type: object
                properties:
                  chat_id:
                    type: string
                    format: uuid
    get:
      summary: "Get chat history"
      responses:
        '200':
          description: "A list of past chat sessions."
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ChatSummary'

  /api/v1/chats/{chat_id}:
    get:
      summary: "Get a specific chat session"
      parameters:
        - name: chat_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: "The full chat object, including messages."
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Chat'

  /api/v1/chats/{chat_id}/messages:
    post:
      summary: "Send a message to a chat session"
      parameters:
        - name: chat_id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      responses:
        '200':
          description: "A streaming response from the LLM."
          content:
            text/event-stream:
              schema:
                type: string

components:
  schemas:
    ChatMessage:
      type: object
      properties:
        id:
          type: string
          format: uuid
        role:
          type: string
          enum: [user, ai]
        content:
          type: string
        created_at:
          type: string
          format: date-time

    Chat:
      type: object
      properties:
        id:
          type: string
          format: uuid
        status:
          type: string
          enum: [processing, completed, failed]
        title:
          type: string
        channel_name:
          type: string
        publication_date:
          type: string
          format: date-time
        view_count:
          type: integer
        thumbnail_url:
          type: string
          format: uri
        generated_summary:
          type: string
        actionable_items:
          type: array
          items:
            type: string
        suggested_questions:
          type: array
          items:
            type: string
        messages:
          type: array
          items:
            $ref: '#/components/schemas/ChatMessage'

    ChatSummary:
      type: object
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
        channel_name:
          type: string
        publication_date:
          type: string
          format: date-time
        view_count:
          type: integer
        thumbnail_url:
          type: string
          format: uri
```
