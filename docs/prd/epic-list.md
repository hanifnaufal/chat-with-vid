# Epic List
### Epic 1: Foundation & Core Video Chat
**Epic Goal**: To establish the complete project foundation, process a YouTube video to retrieve its transcript and metadata, and enable a user to have a live, context-aware conversation with its content. By the end of this epic, a user can input a URL, receive an initial analysis, and have a complete chat session.

#### Story 1.1: Project Scaffolding & Setup
As a developer,
I want a complete project structure with all necessary dependencies and a local database,
so that I can begin developing features in a consistent and reproducible environment.

**Acceptance Criteria**:
- A monorepo is created containing separate packages for the api (FastAPI) and web (Next.js) applications.
- All dependencies listed in the technical assumptions (Next.js, FastAPI, etc.) are installed.
- A docker-compose.yml file is created to run a PostgreSQL database locally.
- The web and api applications can be started successfully with a single command.
- A README.md file is created with clear instructions for the initial setup (as per FR8).

#### Story 1.2: Continuous Integration Workflow
As a developer,
I want a GitHub Actions workflow that automatically runs checks on every pull request,
so that I can ensure code quality, maintainability, and prevent regressions from being merged into the main branch.

**Acceptance Criteria**
- A new GitHub Actions workflow file is created in .github/workflows/.
- The workflow automatically triggers on any pull request targeting the main branch.
- The workflow installs dependencies for both the api (Python) and web (Next.js) applications.
- The workflow runs all linter checks (e.g., Ruff/Black for Python, ESLint/Prettier for the frontend).
- The workflow executes the complete unit and integration test suite (as defined in your Technical Assumptions).
- The workflow must successfully pass before a pull request is permitted to be merged (requires configuration of branch protection rules in GitHub).



#### Story 1.3: Backend API for Video Chat Creation
As an Efficient Learner,
I want to submit a YouTube URL to the application,
so that a new chat can be created and processed.

**Acceptance Criteria**:
- A FastAPI endpoint POST /api/chats is created that accepts a YouTube URL.
-  The endpoint creates a new chat record, kicks off an asynchronous job to process the video, and immediately returns a unique chat_id.
- The asynchronous job retrieves the video's transcript (FR2) and metadata (FR3).
- The job saves the transcript and metadata associated with the chat record.
- The endpoint handles errors gracefully (e.g., invalid URL) and returns an appropriate error message.

#### Story 1.4: Frontend URL Submission & Asynchronous Polling
As an Efficient Learner,
I want to paste a YouTube URL into the app and get immediate feedback,
so that I can see my request is being handled without blocking the interface.

**Acceptance Criteria**:
- The home page contains a single input field for a YouTube URL and a "Process" button (FR1).
- When the "Process" button is clicked, a POST request is sent to the /api/chats endpoint.
- Upon receiving a chat_id, the application navigates to the analysis page (/chat/{chat_id}).
- The analysis page immediately displays a loading state and begins polling a new endpoint, GET /api/chats/{chat_id},  to check the processing status.
- The loading state must be descriptive, showing the user the current stage of the process (e.g., "Step 1/3: Fetching transcript...", "Step 2/3: Analyzing content...", "Step 3/3: Generating summary...").
- If the API returns an error during submission, a user-friendly error message is displayed.

#### Story 1.5: Display Initial Analysis & Video Player
As an Efficient Learner,
I want to see the initial summary, suggested questions, and the video player when processing is complete,
so that I can get immediate value and have context for my chat.

**Acceptance Criteria**:
- A new backend endpoint GET /api/chats/{chat_id} returns the chat status (processing, complete, or failed) and, if  complete, the full analysis payload.
- A new backend job uses the Gemini API to generate a summary, actionable items (FR4), and suggested questions (FR9) and saves them to the chat record.
- The analysis page displays an embedded YouTube video player snippet for the current video.
- When the polling status becomes complete, the loading state is replaced with the video's metadata, the insightful summary, actionable items, and a list of clickable, suggested questions.
- The information on the page must have a clear visual hierarchy: the insightful summary and suggested questions should be the most prominent elements, followed by the chat interface, with the video player and metadata servingas secondary contextual information.

#### Story 1.6: Implement Core Chat Functionality
As an Efficient Learner,
I want to ask questions in a chat interface and receive answers based on the video,
so that I can interactively explore the content.

**Acceptance Criteria**:
- A chat input field is available on the analysis screen (FR5).
- A new backend endpoint POST /api/chats/{chat_id}/messages is created that accepts a user's question.
- The endpoint sends a properly formatted prompt to the Gemini API, using the chat's transcript for context and instructing it to only answer based on that context (FR10).
- The response from the Gemini API is streamed back to the frontend and displayed in the chat window (FR6).
- The conversation history of the current session is displayed in a scrolling view.
- A clear visual cue (e.g., a pulsing input field or a temporary message like "Ask me anything!") prompts the user to begin the chat.
- While the AI response is streaming, a "Stop Generating" button is visible and functional, allowing the user to interrupt the response.

### Epic 2: Local Chat Persistence and History
**Epic Goal**: To build the persistence layer for the application, allowing users to save their conversations and analysis locally. This involves setting up the database schema, creating backend APIs to save and retrieve chats, and building the frontend interface to browse and reopen past conversations.

#### Story 2.1: Backend Persistence Logic & Schema
As a developer,
I want to define the database schema and save a completed video analysis and chat history to the local PostgreSQL database,
so that user conversations are not lost between application sessions.

Acceptance Criteria:
- A database schema is created in PostgreSQL for storing chats (including all video metadata, the transcript, and the generated analysis) and chat_messages.
- After a video's analysis is successfully generated, the complete chat data is saved to the chats table.
- Each individual user question and AI response from a chat is saved to the chat_messages table, linked to the correct chat.

#### Story 2.2: Backend API for Retrieving Chat History
As an Efficient Learner,
I want to retrieve a list of all my past conversations,
so that I can see my history at a glance.

Acceptance Criteria:
- A new endpoint, GET /api/chats, is created.
- The endpoint retrieves all saved chats from the database.
- The endpoint returns a JSON array of chats, with each object containing the rich metadata required for the history list (thumbnail, title, channel name, view count, and relative published date, as per FR7).

#### Story 2.3: Frontend History UI & Navigation
As an Efficient Learner,
I want to view a history page with all my past chats,
so that I can easily find and select a previous conversation to review.

Acceptance Criteria:
- A new "History" page is created in the frontend application, accessible from the main navigation.
- When the page loads, it calls the GET /api/chats endpoint to fetch the list of past conversations.
- The list is displayed in a user-friendly format, rendering the thumbnail, title, channel name, etc., for each item as required by FR7.
- Each item in the list is a link that navigates the user to the analysis/chat page for that specific chat (e.g., /chat/{chat_id}).

#### Story 2.4: Hydrating the Chat View with Past Conversations
As an Efficient Learner,
I want to click on a past chat in my history and see the full conversation,
so that I can continue where I left off or review the information.

Acceptance Criteria:
- The GET /api/chats/{chat_id} endpoint is updated to also return the saved chat messages for that chat.
- When the analysis/chat page loads with a chat_id, it fetches the complete chat data, including the past conversation.
- The chat view is pre-populated with the entire saved conversation history, appearing exactly as it did when the session was last active.
