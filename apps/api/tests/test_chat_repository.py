import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.repository.chat import ChatRepository
from app.models.chat import Chat
from uuid import uuid4, UUID
from datetime import datetime


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def chat_repository(mock_db):
    """Create a ChatRepository instance with a mock database."""
    return ChatRepository(mock_db)


def test_create_chat(chat_repository):
    """Test creating a new chat."""
    source_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Mock the database operations
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = uuid4()
    mock_chat.source_url = source_url
    mock_chat.source_type = "YOUTUBE"
    mock_chat.status = "processing"
    
    chat_repository.db.add = MagicMock()
    chat_repository.db.commit = MagicMock()
    chat_repository.db.refresh = MagicMock()
    
    with patch('app.repository.chat.Chat', return_value=mock_chat):
        result = chat_repository.create_chat(source_url)
        
        # Assertions
        assert result == mock_chat
        assert result.source_url == source_url
        assert result.source_type == "YOUTUBE"
        assert result.status == "processing"
        chat_repository.db.add.assert_called_once_with(mock_chat)
        chat_repository.db.commit.assert_called_once()
        chat_repository.db.refresh.assert_called_once_with(mock_chat)


def test_get_chat_by_id(chat_repository):
    """Test retrieving a chat by ID."""
    chat_id = str(uuid4())
    mock_chat = MagicMock(spec=Chat)
    
    # Mock the database query
    mock_query = MagicMock()
    chat_repository.db.query = MagicMock(return_value=mock_query)
    mock_query.filter = MagicMock(return_value=mock_query)
    mock_query.first = MagicMock(return_value=mock_chat)
    
    result = chat_repository.get_chat_by_id(chat_id)
    
    # Assertions
    assert result == mock_chat
    chat_repository.db.query.assert_called_once_with(Chat)
    mock_query.filter.assert_called_once()
    mock_query.first.assert_called_once()


def test_update_chat(chat_repository):
    """Test updating a chat."""
    chat_id = str(uuid4())
    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = UUID(chat_id)
    
    # Mock the get_chat_by_id method
    chat_repository.get_chat_by_id = MagicMock(return_value=mock_chat)
    chat_repository.db.commit = MagicMock()
    chat_repository.db.refresh = MagicMock()
    
    # Test updating status and transcript
    result = chat_repository.update_chat(
        chat_id=chat_id,
        status="processed",
        transcript="Test transcript",
        title="Test Video",
        channel_name="Test Channel",
        publication_date=datetime(2023, 1, 1),
        view_count=1000,
        thumbnail_url="https://example.com/thumbnail.jpg"
    )
    
    # Assertions
    assert result == mock_chat
    assert mock_chat.status == "processed"
    assert mock_chat.transcript == "Test transcript"
    assert mock_chat.title == "Test Video"
    assert mock_chat.channel_name == "Test Channel"
    assert mock_chat.publication_date == datetime(2023, 1, 1)
    assert mock_chat.view_count == 1000
    assert mock_chat.thumbnail_url == "https://example.com/thumbnail.jpg"
    chat_repository.db.commit.assert_called_once()
    chat_repository.db.refresh.assert_called_once_with(mock_chat)


def test_update_chat_not_found(chat_repository):
    """Test updating a chat that doesn't exist."""
    chat_id = str(uuid4())
    
    # Mock the get_chat_by_id method to return None
    chat_repository.get_chat_by_id = MagicMock(return_value=None)
    
    result = chat_repository.update_chat(chat_id=chat_id, status="processed")
    
    # Assertions
    assert result is None
    chat_repository.db.commit.assert_not_called()
    chat_repository.db.refresh.assert_not_called()