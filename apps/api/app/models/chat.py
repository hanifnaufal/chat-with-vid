from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_url = Column(Text, nullable=False)
    source_type = Column(String(50), nullable=False)
    video_id = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="processing")
    title = Column(Text)
    channel_name = Column(String(255))
    publication_date = Column(DateTime)
    view_count = Column(Integer)
    thumbnail_url = Column(Text)
    transcript = Column(Text)
    generated_summary = Column(Text)
    actionable_items = Column(JSON)  # JSONB in PostgreSQL
    suggested_questions = Column(JSON)  # JSONB in PostgreSQL
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False, onupdate=func.now())
