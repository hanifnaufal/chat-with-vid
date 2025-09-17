import pytest
from app.schemas.chat import ChatCreateRequest
from pydantic import ValidationError


def test_youtube_url_validator():
    """Test the YouTube URL validator logic."""
    # Valid YouTube URLs should pass validation
    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtube.com/embed/dQw4w9WgXcQ",
    ]

    for url in valid_urls:
        chat_request = ChatCreateRequest(source_url=url)
        assert chat_request.source_url.scheme in ["http", "https"]
        assert (
            "youtube" in chat_request.source_url.host
            or "youtu.be" in chat_request.source_url.host
        )


def test_non_youtube_url_validator():
    """Test that non-YouTube URLs are rejected."""
    invalid_urls = [
        "https://www.google.com",
        "https://vimeo.com/123456789",
        "https://www.youtubee.com/watch?v=dQw4w9WgXcQ",  # Misspelled
    ]

    for url in invalid_urls:
        with pytest.raises(ValidationError):
            ChatCreateRequest(source_url=url)
