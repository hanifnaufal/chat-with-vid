from sqlalchemy.orm import Session
from uuid import uuid4, UUID
from ..models.chat import Chat
from typing import Optional
from datetime import datetime


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, source_url: str, source_type: str = "YOUTUBE", video_id: str = "unknown") -> Chat:
        """Create a new chat record with processing status."""
        db_chat = Chat(
            id=uuid4(),
            source_url=source_url,
            source_type=source_type,
            video_id=video_id,
            status="processing",
        )
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return db_chat

    def get_chat_by_id(self, chat_id: str) -> Chat:
        """Retrieve a chat by its ID."""
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def update_chat(
        self,
        chat_id: UUID,
        status: Optional[str] = None,
        transcript: Optional[str] = None,
        title: Optional[str] = None,
        channel_name: Optional[str] = None,
        publication_date: Optional[datetime] = None,
        view_count: Optional[int] = None,
        thumbnail_url: Optional[str] = None,
        video_id: Optional[str] = None,
    ) -> Chat:
        """Update a chat record with processing results."""
        db_chat = self.get_chat_by_id(chat_id)
        if db_chat:
            if status is not None:
                db_chat.status = status
            if transcript is not None:
                db_chat.transcript = transcript
            if title is not None:
                db_chat.title = title
            if channel_name is not None:
                db_chat.channel_name = channel_name
            if publication_date is not None:
                db_chat.publication_date = publication_date
            if view_count is not None:
                db_chat.view_count = view_count
            if thumbnail_url is not None:
                db_chat.thumbnail_url = thumbnail_url
            if video_id is not None:
                db_chat.video_id = video_id
            self.db.commit()
            self.db.refresh(db_chat)
        return db_chat
