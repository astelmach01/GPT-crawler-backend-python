from fastapi import APIRouter

from app.schemas.chat import ChatBase

from .core import chatgpt_call

router = APIRouter()


@router.post("/request")
async def chat(chat_request: ChatBase) -> str:
    """Generic chat request.

    A generic chat request.
    :param chat_request: chat request.
    :return: chat response.
    """

    prompt = chat_request.prompt
    return chatgpt_call(prompt)
