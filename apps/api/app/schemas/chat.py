from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
from typing import Optional
import re


class ChatCreateRequest(BaseModel):
    source_url: HttpUrl
    source_type: str = "YOUTUBE"

    @field_validator("source_url")
    @classmethod
    def validate_youtube_url(cls, v):
        """Validate that the URL is a YouTube URL."""
        url_str = str(v)
        # Regular expression to match YouTube URLs
        youtube_regex = (
            r"(https?://)?(www\.)?"
            r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
            r"(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        )

        if not re.match(youtube_regex, url_str):
            raise ValueError("Invalid YouTube URL")

        return v


class ChatResponse(BaseModel):
    id: str
    source_url: HttpUrl
    source_type: str
    video_id: str
    status: str
    title: Optional[str] = None
    channel_name: Optional[str] = None
    publication_date: Optional[datetime] = None
    view_count: Optional[int] = None
    thumbnail_url: Optional[HttpUrl] = None
    transcript: Optional[str] = None
    generated_summary: Optional[str] = None
    actionable_items: Optional[list] = None
    suggested_questions: Optional[list] = None
    created_at: datetime
    updated_at: datetime
