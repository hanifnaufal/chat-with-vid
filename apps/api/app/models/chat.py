from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(Text, nullable=False)
    source_type = Column(String(50), nullable=False)
    video_id = Column(String(255))
    status = Column(String, default="processing")
    title = Column(Text)
    channel_name = Column(String)
    publication_date = Column(DateTime)
    view_count = Column(Integer)
    thumbnail_url = Column(Text)
    transcript = Column(Text)
    generated_summary = Column(Text)
    actionable_items = Column(Text)  # JSONB in DB, but Text in model for simplicity
    suggested_questions = Column(Text)  # JSONB in DB, but Text in model for simplicity
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
