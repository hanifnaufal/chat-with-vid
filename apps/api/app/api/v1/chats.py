from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from ...schemas.chat import ChatCreateRequest
from ...services.chat import ChatService
from ...core.database import get_db
from ...core.exceptions import InvalidURLException
from ...core.logging import setup_logging

logger = setup_logging()

router = APIRouter()


@router.post("/chats", status_code=status.HTTP_202_ACCEPTED)
def create_chat(chat_request: ChatCreateRequest, db: Session = Depends(get_db)):
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


@router.get("/chats")
def read_chats():
    return {"chats": []}
