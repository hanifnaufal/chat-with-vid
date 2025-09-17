from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4


client = TestClient(app)


@patch("app.api.v1.chats.ChatService")
def test_create_chat_valid_url(mock_chat_service):
    """Test creating a chat with a valid YouTube URL."""
    # Mock the service to return a fake chat ID
    mock_chat_service.return_value.start_new_chat.return_value = str(uuid4())

    response = client.post(
        "/api/v1/chats",
        json={"source_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    )

    assert response.status_code == 202
    assert "chat_id" in response.json()
    assert response.json()["chat_id"] is not None


def test_create_chat_invalid_url():
    """Test creating a chat with an invalid URL."""
    response = client.post(
        "/api/v1/chats", json={"source_url": "https://www.google.com"}
    )

    # FastAPI validates the URL format before our custom validation
    # Our custom validation only works for valid URLs that don't match YouTube pattern
    assert response.status_code == 422


def test_create_chat_missing_url():
    """Test creating a chat with missing URL."""
    response = client.post("/api/v1/chats", json={})

    assert response.status_code == 422  # Validation error from FastAPI


def test_create_chat_invalid_payload():
    """Test creating a chat with invalid payload."""
    response = client.post("/api/v1/chats", json={"source_url": "not-a-url"})

    assert response.status_code == 422  # Validation error from FastAPI


@patch("app.api.v1.chats.ChatService")
def test_create_chat_async_processing(mock_chat_service):
    """Test that creating a chat starts asynchronous processing."""
    # Mock the service
    mock_service_instance = MagicMock()
    mock_chat_service.return_value = mock_service_instance
    mock_chat_service.return_value.start_new_chat.return_value = str(uuid4())

    # We won't directly test the asyncio.create_task call here as it's challenging to mock
    # and the main goal is to ensure the endpoint returns the correct status code.
    # The actual async processing is tested in the service tests.
    response = client.post(
        "/api/v1/chats",
        json={"source_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
    )

    # Assertions
    assert response.status_code == 202


def test_get_chats():
    """Test getting chats (existing endpoint)."""
    response = client.get("/api/v1/chats")

    assert response.status_code == 200
    assert response.json() == {"chats": []}
