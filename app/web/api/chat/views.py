from app.schemas.chat import ChatBase
from fastapi import APIRouter

router = APIRouter()


@router.post("/request")
async def chat(chat_request: ChatBase):
    """Generic chat request.

    A generic chat request.
    :param chat_request: chat request.
    :return: chat response.
    """
    return {"chat": chat_request.prompt}
