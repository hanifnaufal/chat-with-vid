from sqlalchemy.orm import Session
from ..core.logging import setup_logging
from ..repository.chat import ChatRepository
from .video import extract_video_id, get_youtube_transcript, get_youtube_metadata
from ..core.exceptions import VideoProcessingError
from uuid import UUID

logger = setup_logging()


class ChatService:
    def __init__(self, db: Session):
        self.chat_repository = ChatRepository(db)

    def start_new_chat(self, source_url: str, source_type: str = "YOUTUBE") -> str:
        """
        Start a new chat by creating a chat record.
        Returns the chat ID as a string.
        """
        logger.info(
            "Starting new chat",
            extra={"source_url": source_url, "source_type": source_type},
        )
        # Extract video ID for storage
        try:
            video_id = extract_video_id(source_url)
        except VideoProcessingError:
            video_id = "unknown"

        # Create chat with video_id
        chat = self.chat_repository.create_chat(source_url, source_type, video_id)
        chat_id = str(chat.id)
        logger.info(
            "Chat record created", extra={"chat_id": chat_id, "video_id": video_id}
        )
        return chat_id

    def get_chat_by_id(self, chat_id: str):
        """
        Retrieve a chat by its ID.
        """
        logger.info("Retrieving chat", extra={"chat_id": chat_id})
        try:
            # Validate UUID format
            UUID(chat_id)
        except ValueError:
            logger.error("Invalid chat ID format", extra={"chat_id": chat_id})
            raise ValueError("Invalid chat ID format")

        chat = self.chat_repository.get_chat_by_id(chat_id)

        if not chat:
            logger.error("Chat not found", extra={"chat_id": chat_id})
            raise ValueError("Chat not found")

        logger.info("Chat retrieved successfully", extra={"chat_id": chat_id})
        return chat

    async def process_video_async(self, chat_id: str, source_url: str):
        """
        Asynchronously process the video to retrieve transcript and metadata.
        """
        logger.info(
            "Starting asynchronous video processing",
            extra={"chat_id": chat_id, "source_url": source_url},
        )
        try:
            video_id = extract_video_id(source_url)
            logger.debug(
                "Extracted video ID", extra={"chat_id": chat_id, "video_id": video_id}
            )
            transcript = get_youtube_transcript(video_id)
            logger.debug(
                "Retrieved YouTube transcript",
                extra={"chat_id": chat_id, "transcript_length": len(transcript)},
            )
            metadata = get_youtube_metadata(video_id)
            logger.debug(
                "Retrieved YouTube metadata",
                extra={"chat_id": chat_id, "metadata_keys": list(metadata.keys())},
            )

            # Update chat record with results
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="complete",
                transcript=transcript,
                title=metadata["title"],
                channel_name=metadata["channel_name"],
                publication_date=metadata["publication_date"],
                view_count=metadata["view_count"],
                thumbnail_url=metadata["thumbnail_url"],
            )
            logger.info(
                "Chat record updated successfully",
                extra={"chat_id": chat_id, "status": "complete"},
            )
        except VideoProcessingError as e:
            logger.error(
                "Video processing error",
                extra={"chat_id": chat_id, "error": str(e)},
                exc_info=True,
            )
            # Update chat record with error status
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="error",
                transcript=f"Error processing video: {str(e)}",
            )
        except Exception as e:
            logger.error(
                "Unexpected error during video processing",
                extra={"chat_id": chat_id, "error": str(e)},
                exc_info=True,
            )
            # Handle any other unexpected errors
            self.chat_repository.update_chat(
                chat_id=chat_id,
                status="error",
                transcript=f"Unexpected error: {str(e)}",
            )
