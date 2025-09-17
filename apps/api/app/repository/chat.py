from sqlalchemy.orm import Session
from uuid import uuid4
from ..models.chat import Chat


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, source_url: str, source_type: str = "YOUTUBE") -> Chat:
        """Create a new chat record with processing status."""
        db_chat = Chat(
            id=uuid4(),
            source_url=source_url,
            source_type=source_type,
            status="processing"
        )
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return db_chat

    def get_chat_by_id(self, chat_id: str) -> Chat:
        """Retrieve a chat by its ID."""
        return self.db.query(Chat).filter(Chat.id == chat_id).first()