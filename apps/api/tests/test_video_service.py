import pytest
from unittest.mock import patch, MagicMock
from app.services.video import (
    extract_video_id,
    get_youtube_transcript,
    get_youtube_metadata,
    VideoProcessingError,
)


def test_extract_video_id_valid_url():
    """Test extracting video ID from a valid URL."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    expected_id = "dQw4w9WgXcQ"
    assert extract_video_id(url) == expected_id


def test_extract_video_id_invalid_url():
    """Test extracting video ID from an invalid URL."""
    url = "https://www.example.com"
    with pytest.raises(VideoProcessingError):
        extract_video_id(url)


@patch("app.services.video.TextFormatter")
@patch("app.services.video.YouTubeTranscriptApi")
def test_get_youtube_transcript(mock_youtube_transcript_api, mock_text_formatter):
    """Test retrieving YouTube transcript."""
    # Create a mock for the YouTubeTranscriptApi instance
    mock_ytt_api_instance = MagicMock()
    mock_transcript_list = [{"text": "Hello"}, {"text": "World"}]
    mock_ytt_api_instance.fetch.return_value = mock_transcript_list
    mock_youtube_transcript_api.return_value = mock_ytt_api_instance
    
    # Mock the TextFormatter to return a specific formatted string
    mock_formatter_instance = MagicMock()
    mock_formatter_instance.format_transcript.return_value = "Hello World"
    mock_text_formatter.return_value = mock_formatter_instance

    video_id = "dQw4w9WgXcQ"
    expected_transcript = "Hello World"

    assert get_youtube_transcript(video_id) == expected_transcript
    mock_youtube_transcript_api.assert_called_once()
    mock_ytt_api_instance.fetch.assert_called_once_with(video_id)
    mock_text_formatter.assert_called_once()
    mock_formatter_instance.format_transcript.assert_called_once_with(mock_transcript_list)


@patch("app.services.video.YouTubeTranscriptApi")
def test_get_youtube_transcript_error(mock_youtube_transcript_api):
    """Test handling errors when retrieving YouTube transcript."""
    # Create a mock for the YouTubeTranscriptApi instance
    mock_ytt_api_instance = MagicMock()
    mock_ytt_api_instance.fetch.side_effect = Exception("API Error")
    mock_youtube_transcript_api.return_value = mock_ytt_api_instance

    video_id = "dQw4w9WgXcQ"

    with pytest.raises(VideoProcessingError):
        get_youtube_transcript(video_id)


@patch("app.services.video.YouTube")
def test_get_youtube_metadata(mock_youtube):
    """Test retrieving YouTube metadata."""
    mock_yt = MagicMock()
    mock_yt.title = "Test Video"
    mock_yt.author = "Test Author"
    mock_yt.publish_date = "2023-01-01"
    mock_yt.views = 1000
    mock_yt.thumbnail_url = "https://example.com/thumbnail.jpg"

    mock_youtube.return_value = mock_yt

    video_id = "dQw4w9WgXcQ"
    expected_metadata = {
        "title": "Test Video",
        "channel_name": "Test Author",
        "publication_date": "2023-01-01",
        "view_count": 1000,
        "thumbnail_url": "https://example.com/thumbnail.jpg",
    }

    assert get_youtube_metadata(video_id) == expected_metadata
    mock_youtube.assert_called_once_with(f"https://www.youtube.com/watch?v={video_id}")


@patch("app.services.video.YouTube")
def test_get_youtube_metadata_error(mock_youtube):
    """Test handling errors when retrieving YouTube metadata."""
    mock_youtube.side_effect = Exception("API Error")

    video_id = "dQw4w9WgXcQ"

    with pytest.raises(VideoProcessingError):
        get_youtube_metadata(video_id)
