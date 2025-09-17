import asyncio
from ..repository.chat import ChatRepository
from sqlalchemy.orm import Session
from .video import extract_video_id, get_youtube_transcript, get_youtube_metadata
from ..core.exceptions import VideoProcessingError


class ChatService:
    def __init__(self, db: Session):
        self.chat_repository = ChatRepository(db)

    def start_new_chat(self, source_url: str, source_type: str = "YOUTUBE") -> str:
        """
        Start a new chat by creating a chat record.
        Returns the chat ID as a string.
        """
        chat = self.chat_repository.create_chat(source_url, source_type)
        # Start asynchronous video processing
        asyncio.create_task(self.process_video_async(str(chat.id), source_url))
        return str(chat.id)

    async def process_video_async(self, chat_id: str, source_url: str):
        """
        Asynchronously process the video to retrieve transcript and metadata.
        """
        try:
            video_id = extract_video_id(source_url)
            transcript = get_youtube_transcript(video_id)
            metadata = get_youtube_metadata(video_id)

            # Update chat record with results
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="processed",
                transcript=transcript,
                title=metadata["title"],
                channel_name=metadata["channel_name"],
                publication_date=metadata["publication_date"],
                view_count=metadata["view_count"],
                thumbnail_url=metadata["thumbnail_url"],
            )
        except VideoProcessingError as e:
            # Update chat record with error status
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="error",
                transcript=f"Error processing video: {str(e)}",
            )
        except Exception as e:
            # Handle any other unexpected errors
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="error",
                transcript=f"Unexpected error: {str(e)}",
            )
