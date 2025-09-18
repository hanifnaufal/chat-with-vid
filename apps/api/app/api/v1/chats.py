from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import ValidationError

from ...schemas.chat import ChatCreateRequest, ChatResponse
from ...services.chat import ChatService
from ...core.database import get_db
from ...core.exceptions import InvalidURLException
from ...core.logging import setup_logging

logger = setup_logging()

router = APIRouter()


@router.post("/chats", status_code=status.HTTP_202_ACCEPTED)
def create_chat(
    chat_request: ChatCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new chat for processing a YouTube video.
    """
    logger.info(
        "Creating new chat",
        extra={
            "source_url": str(chat_request.source_url),
            "source_type": chat_request.source_type,
        },
    )
    try:
        chat_service = ChatService(db)
        chat_id = chat_service.start_new_chat(
            str(chat_request.source_url), chat_request.source_type
        )
        # Add the video processing as a background task
        background_tasks.add_task(
            chat_service.process_video_async, chat_id, str(chat_request.source_url)
        )
        logger.info("Chat creation initiated successfully", extra={"chat_id": chat_id})
        return {"chat_id": chat_id}
    except InvalidURLException as e:
        logger.error("Invalid URL provided", extra={"error": str(e)}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "INVALID_URL", "message": str(e)},
        )
    except ValidationError as e:
        logger.error("Validation error", extra={"error": e.errors()}, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "VALIDATION_ERROR", "message": e.errors()},
        )
    except Exception as e:
        logger.error(
            "Unexpected error during chat creation",
            extra={"error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
        )


@router.get("/chats/{chat_id}")
def read_chat(chat_id: str, db: Session = Depends(get_db)):
    """
    Retrieve chat details by ID.
    """
    try:
        chat_service = ChatService(db)
        chat = chat_service.get_chat_by_id(chat_id)

        # Convert to Pydantic model
        chat_response = ChatResponse(
            id=str(chat.id),
            source_url=chat.source_url,
            source_type=chat.source_type,
            video_id=chat.video_id,
            status=chat.status,
            title=chat.title,
            channel_name=chat.channel_name,
            publication_date=chat.publication_date,
            view_count=chat.view_count,
            thumbnail_url=chat.thumbnail_url,
            transcript=chat.transcript,
            generated_summary=chat.generated_summary,
            actionable_items=chat.actionable_items,
            suggested_questions=chat.suggested_questions,
            created_at=chat.created_at,
            updated_at=chat.updated_at,
        )

        return chat_response
    except ValueError as e:
        if "Invalid chat ID format" in str(e):
            logger.error("Invalid chat ID format", extra={"chat_id": chat_id})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_code": "INVALID_CHAT_ID",
                    "message": "Invalid chat ID format",
                },
            )
        elif "Chat not found" in str(e):
            logger.error("Chat not found", extra={"chat_id": chat_id})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error_code": "CHAT_NOT_FOUND", "message": "Chat not found"},
            )
        else:
            logger.error(
                "Unexpected error during chat retrieval",
                extra={"chat_id": chat_id, "error": str(e)},
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error_code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                },
            )
    except Exception as e:
        logger.error(
            "Unexpected error during chat retrieval",
            extra={"chat_id": chat_id, "error": str(e)},
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
        )


@router.get("/chats")
def read_chats():
    return {"chats": []}
