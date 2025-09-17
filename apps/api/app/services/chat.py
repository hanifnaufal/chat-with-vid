from uuid import UUID
from ..repository.chat import ChatRepository
from sqlalchemy.orm import Session


class ChatService:
    def __init__(self, db: Session):
        self.chat_repository = ChatRepository(db)

    def start_new_chat(self, source_url: str, source_type: str = "YOUTUBE") -> str:
        """
        Start a new chat by creating a chat record.
        Returns the chat ID as a string.
        """
        chat = self.chat_repository.create_chat(source_url, source_type)
        return str(chat.id)