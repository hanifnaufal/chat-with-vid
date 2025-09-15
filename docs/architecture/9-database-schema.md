# 9. Database Schema
This schema is for PostgreSQL and includes tables, relationships, indexes, and a trigger for managing update timestamps.

```sql
-- The 'uuid-ossp' extension is required for generating UUIDs.
-- This should be enabled in the database: CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table to store the main chat session and its associated source/analysis data
CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_url TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    video_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'processing',
    title TEXT,
    channel_name VARCHAR(255),
    publication_date TIMESTAMPTZ,
    view_count INTEGER,
    thumbnail_url TEXT,
    transcript TEXT,
    generated_summary TEXT,
    actionable_items JSONB,
    suggested_questions JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Table to store individual messages within a chat session
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user' or 'ai'
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_chats_video_id ON chats(video_id);
CREATE INDEX idx_chat_messages_chat_id ON chat_messages(chat_id);

-- Trigger to automatically update the 'updated_at' timestamp on the 'chats' table
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON chats
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();
```
