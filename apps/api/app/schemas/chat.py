from pydantic import BaseModel, HttpUrl, field_validator
import re


class ChatCreateRequest(BaseModel):
    source_url: HttpUrl
    source_type: str = "YOUTUBE"

    @field_validator('source_url')
    @classmethod
    def validate_youtube_url(cls, v):
        """Validate that the URL is a YouTube URL."""
        url_str = str(v)
        # Regular expression to match YouTube URLs
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        
        if not re.match(youtube_regex, url_str):
            raise ValueError('Invalid YouTube URL')
            
        return v