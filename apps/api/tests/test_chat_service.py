import pytest
import asyncio
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.services.chat import ChatService
from app.repository.chat import ChatRepository
from app.models.chat import Chat
from app.core.exceptions import VideoProcessingError
from uuid import uuid4, UUID
from datetime import datetime


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_chat_repository(mock_db):
    """Create a mock ChatRepository instance."""
    return MagicMock(spec=ChatRepository)


@pytest.fixture
def chat_service(mock_db, mock_chat_repository):
    """Create a ChatService instance with a mock database and repository."""
    service = ChatService(mock_db)
    service.chat_repository = mock_chat_repository
    return service


@patch("app.services.chat.extract_video_id")
@patch("app.services.chat.get_youtube_transcript")
@patch("app.services.chat.get_youtube_metadata")
def test_process_video_async_success(
    mock_get_metadata, mock_get_transcript, mock_extract_id, chat_service
):
    """Test successful asynchronous video processing."""
    # Setup mocks
    chat_id = str(uuid4())
    source_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = "dQw4w9WgXcQ"

    mock_extract_id.return_value = video_id
    mock_get_transcript.return_value = "This is a test transcript."
    mock_get_metadata.return_value = {
        "title": "Test Video",
        "channel_name": "Test Channel",
        "publication_date": datetime(2023, 1, 1),
        "view_count": 1000,
        "thumbnail_url": "https://example.com/thumbnail.jpg",
    }

    # Run the async function
    asyncio.run(chat_service.process_video_async(chat_id, source_url))

    # Assertions
    mock_extract_id.assert_called_once_with(source_url)
    mock_get_transcript.assert_called_once_with(video_id)
    mock_get_metadata.assert_called_once_with(video_id)

    # Verify that update_chat was called with the correct parameters
    chat_service.chat_repository.update_chat.assert_called_once_with(
        chat_id=chat_id,
        status="processed",
        transcript="This is a test transcript.",
        title="Test Video",
        channel_name="Test Channel",
        publication_date=datetime(2023, 1, 1),
        view_count=1000,
        thumbnail_url="https://example.com/thumbnail.jpg",
    )


@patch("app.services.chat.extract_video_id")
def test_process_video_async_video_processing_error(mock_extract_id, chat_service):
    """Test handling VideoProcessingError during video processing."""
    # Setup mocks
    chat_id = str(uuid4())
    source_url = "https://www.youtube.com/watch?v=invalid"

    mock_extract_id.side_effect = VideoProcessingError("Invalid YouTube URL")

    # Run the async function
    asyncio.run(chat_service.process_video_async(chat_id, source_url))

    # Assertions
    mock_extract_id.assert_called_once_with(source_url)

    # Verify that update_chat was called with error status
    chat_service.chat_repository.update_chat.assert_called_once_with(
        chat_id=chat_id,
        status="error",
        transcript="Error processing video: Invalid YouTube URL",
    )


@patch("app.services.chat.extract_video_id")
@patch("app.services.chat.get_youtube_transcript")
def test_process_video_async_unexpected_error(
    mock_get_transcript, mock_extract_id, chat_service
):
    """Test handling unexpected errors during video processing."""
    # Setup mocks
    chat_id = str(uuid4())
    source_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = "dQw4w9WgXcQ"

    mock_extract_id.return_value = video_id
    mock_get_transcript.side_effect = Exception("Unexpected error")

    # Run the async function
    asyncio.run(chat_service.process_video_async(chat_id, source_url))

    # Assertions
    mock_extract_id.assert_called_once_with(source_url)
    mock_get_transcript.assert_called_once_with(video_id)

    # Verify that update_chat was called with error status
    chat_service.chat_repository.update_chat.assert_called_once_with(
        chat_id=chat_id, status="error", transcript="Unexpected error: Unexpected error"
    )


def test_start_new_chat(chat_service):
    """Test starting a new chat."""
    # Setup mocks
    source_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = uuid4()

    chat_service.chat_repository.create_chat = MagicMock(return_value=mock_chat)

    # Call the method
    chat_id = chat_service.start_new_chat(source_url)

    # Assertions
    assert chat_id == str(mock_chat.id)
    chat_service.chat_repository.create_chat.assert_called_once_with(
        source_url, "YOUTUBE", "dQw4w9WgXcQ"
    )


@patch("app.services.chat.extract_video_id")
def test_start_new_chat_extract_video_id_error(mock_extract_id, chat_service):
    """Test starting a new chat when extract_video_id fails."""
    # Setup mocks
    source_url = "https://www.youtube.com/watch?v=invalid"
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = uuid4()

    mock_extract_id.side_effect = VideoProcessingError("Invalid YouTube URL")
    chat_service.chat_repository.create_chat = MagicMock(return_value=mock_chat)

    # Call the method
    chat_id = chat_service.start_new_chat(source_url)

    # Assertions
    assert chat_id == str(mock_chat.id)
    chat_service.chat_repository.create_chat.assert_called_once_with(
        source_url, "YOUTUBE", "unknown"
    )


def test_get_chat_by_id_success(chat_service):
    """Test successful retrieval of a chat by ID."""
    # Setup mocks
    chat_id = str(uuid4())
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = UUID(chat_id)

    chat_service.chat_repository.get_chat_by_id.return_value = mock_chat

    # Call the method
    result = chat_service.get_chat_by_id(chat_id)

    # Assertions
    assert result == mock_chat
    chat_service.chat_repository.get_chat_by_id.assert_called_once_with(chat_id)


def test_get_chat_by_id_invalid_uuid(chat_service):
    """Test handling of invalid UUID format."""
    # Setup
    invalid_chat_id = "invalid-uuid"

    # Call the method and assert exception
    with pytest.raises(ValueError, match="Invalid chat ID format"):
        chat_service.get_chat_by_id(invalid_chat_id)

    # Verify repository method was not called
    chat_service.chat_repository.get_chat_by_id.assert_not_called()


def test_get_chat_by_id_not_found(chat_service):
    """Test handling of non-existent chat ID."""
    # Setup
    chat_id = str(uuid4())
    chat_service.chat_repository.get_chat_by_id.return_value = None

    # Call the method and assert exception
    with pytest.raises(ValueError, match="Chat not found"):
        chat_service.get_chat_by_id(chat_id)

    # Verify repository method was called
    chat_service.chat_repository.get_chat_by_id.assert_called_once_with(chat_id)
