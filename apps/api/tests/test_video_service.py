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
    mock_formatter_instance.format_transcript.assert_called_once_with(
        mock_transcript_list
    )


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


@patch("app.services.video.yt_dlp.YoutubeDL")
def test_get_youtube_metadata(mock_youtube_dl):
    """Test retrieving YouTube metadata."""
    # Create a mock for the YoutubeDL context manager
    mock_ydl_instance = MagicMock()
    mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance

    # Mock the extract_info method to return metadata
    mock_info = {
        "title": "Test Video",
        "uploader": "Test Author",
        "upload_date": "20230101",
        "view_count": 1000,
        "thumbnail": "https://example.com/thumbnail.jpg",
    }
    mock_ydl_instance.extract_info.return_value = mock_info

    video_id = "dQw4w9WgXcQ"
    expected_metadata = {
        "title": "Test Video",
        "channel_name": "Test Author",
        "publication_date": "2023-01-01",  # This will be converted by the function
        "view_count": 1000,
        "thumbnail_url": "https://example.com/thumbnail.jpg",
    }

    result = get_youtube_metadata(video_id)
    assert result["title"] == expected_metadata["title"]
    assert result["channel_name"] == expected_metadata["channel_name"]
    assert result["view_count"] == expected_metadata["view_count"]
    assert result["thumbnail_url"] == expected_metadata["thumbnail_url"]
    # Check that publication_date is a date object when timestamp is available
    # Since our mock doesn't include a timestamp, the publication_date will be None
    assert result["publication_date"] is None
    mock_youtube_dl.assert_called_once_with(
        {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True,
            "extract_flat": "in_playlist",
        }
    )
    mock_ydl_instance.extract_info.assert_called_once_with(
        f"https://www.youtube.com/watch?v={video_id}", download=False
    )


@patch("app.services.video.yt_dlp.YoutubeDL")
def test_get_youtube_metadata_error(mock_youtube_dl):
    """Test handling errors when retrieving YouTube metadata."""
    # Create a mock for the YoutubeDL context manager
    mock_ydl_instance = MagicMock()
    mock_youtube_dl.return_value.__enter__.return_value = mock_ydl_instance

    # Mock the extract_info method to raise an exception
    mock_ydl_instance.extract_info.side_effect = Exception("API Error")

    video_id = "dQw4w9WgXcQ"

    with pytest.raises(VideoProcessingError):
        get_youtube_metadata(video_id)
