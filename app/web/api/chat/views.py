import logging

from fastapi import APIRouter

from app.schemas.chat import ChatBase
from app.schemas.response import ChatResponse

from .core import chatgpt_function_response

router = APIRouter()


@router.post("/request")
async def chat(chat_request: ChatBase) -> ChatResponse:
    """Generic chat request.

    A generic chat request.
    :param chat_request: chat request.
    :return: chat response.
    """
    logging.info(f"Chat request: {chat_request}")
    response = chatgpt_function_response(chat_request.prompt)
    return ChatResponse(success=True, response=response, reason="Success")
