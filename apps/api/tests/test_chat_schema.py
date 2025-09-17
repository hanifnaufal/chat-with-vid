import pytest
from pydantic import ValidationError
from app.schemas.chat import ChatCreateRequest


def test_valid_youtube_url():
    """Test that valid YouTube URLs are accepted."""
    # Test different valid YouTube URL formats
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "http://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "http://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ"
    ]
    
    for url in valid_urls:
        chat_request = ChatCreateRequest(source_url=url)
        assert str(chat_request.source_url) == url
        assert chat_request.source_type == "YOUTUBE"


def test_invalid_url():
    """Test that invalid URLs raise validation errors."""
    # Test completely invalid URLs
    invalid_urls = [
        "https://www.google.com",
        "https://vimeo.com/123456789",
        "not-a-url",
        "https://www.youtubee.com/watch?v=dQw4w9WgXcQ"
    ]
    
    for url in invalid_urls:
        with pytest.raises(ValidationError):
            ChatCreateRequest(source_url=url)


def test_missing_url():
    """Test that missing URL raises validation error."""
    with pytest.raises(ValidationError):
        ChatCreateRequest()