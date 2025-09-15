# Requirements
### Functional
- **FR1**: The system must provide an interface for a user to submit a YouTube video URL.

- **FR2**: The backend must process a submitted URL to retrieve the video's transcript and prepare it for analysis by the Gemini API.

- **FR3**: In addition to the transcript, the backend must retrieve the video's metadata, including its title, thumbnail URL, channel name, view count, and publication date.

- **FR4**: Upon successful video processing, the application must automatically generate and display an ** and a list of actionable items derived from the video's content.

- **FR5**: The system must feature an interactive chat interface that displays the conversation history and allows the user to submit new questions.

- **FR6**: The system must integrate with the Gemini API, sending the video transcript as context along with the user's question, and stream the generated response back to the chat interface.

- **FR7**: The application must persist conversations on the user's local machine. The UI must display a list of past chats, with each entry showing the video's thumbnail, title, channel name, view count, and relative published date (e.g., '2 months ago'). Users must be able to reopen a conversation from this list.

- **FR8**: The project must include a README.md file with clear, step-by-step instructions for setting up the local development environment and configuring the necessary Gemini API key.

- **FR9**: After a video is processed, the system should suggest a few relevant questions the user can ask to start the conversation, based on the video's title and transcript.

- **FR10**: The LLM's responses during the chat must be based solely on the context provided by the video's transcript and should not answer questions on unrelated topics.

### Non-Functional
- **NFR1**: The application must be responsive and function correctly on modern desktop and mobile web browsers (Chrome, Firefox, Safari, Edge).

- **NFR2**: For a 10-minute video, the initial summary must be generated in under 10 seconds, and chat responses must begin streaming in under 3 seconds.

- **NFR3**: The system must be built using React/Next.js for the frontend, Python/FastAPI for the backend, and PostgreSQL for the database.

- **NFR4**: The Gemini API key must be managed securely via an environment variable (.env file) and must not be exposed in the frontend code.

- **NFR5**: The MVP must be capable of running entirely on a user's local machine, with an operational budget of zero.

- **NFR6**: The system must include safeguards and safety measures to mitigate prompt injection attacks at the API level.

- **NFR7**: A new contributor must be able to set up the local development environment and run all tests successfully in under 30 minutes by following the project documentation.
