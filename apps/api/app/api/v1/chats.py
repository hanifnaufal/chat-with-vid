from fastapi import APIRouter

router = APIRouter()


@router.get("/chats")
def read_chats():
    return {"chats": []}
