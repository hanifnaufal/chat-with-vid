# 6. External APIs
### Google Gemini API
- **Purpose**: Provides the core generative AI capabilities for video summarization, identifying action items, and powering the interactive chat.
- **Documentation**: https://ai.google.dev/docs
- **Authentication**: API Key. As specified in the PRD, this key must be stored securely in an environment variable on the backend and never exposed to the frontend.
- **Rate Limits**: The free tier of the Gemini API has rate limits (e.g., requests per minute). Our application must handle potential 429 Too Many Requests errors gracefully.
- **Key Endpoints Used**: We will use the gemini-1.5-flash model via the following methods in the Python SDK
    - **generateContent**: For the initial, one-off analysis.
    - **streamGenerateContent**: For the interactive chat to provide a real-time response.
- **Integration Notes**: All interaction with the Gemini API will be encapsulated within the LLM Service component.

### YouTube Transcript Service
- **Purpose**: To retrieve the machine-generated or user-provided transcript for a given YouTube video. This is the primary context source for the LLM.

- **Documentation**: This will be implemented via a library such as youtube-transcript-api (https://pypi.org/project/youtube-transcript-api/).

- **Authentication**: None required for publicly available videos.

- **Rate Limits**: There are no official, published rate limits. However, making an excessive number of requests in a short period can lead to temporary IP-based blocking. We must consider this a potential operational risk.

- **Key Endpoints Used**: N/A (Library-based). The primary function will be similar to:
  ```python
  ytt_api = YouTubeTranscriptApi()
  transcript = ytt_api.fetch(video_id)
  ```

- **Integration Notes**: This functionality will be encapsulated within the Video Processing Service component and run as an asynchronous background task.
