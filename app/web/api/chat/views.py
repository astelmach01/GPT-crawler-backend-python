import logging

from fastapi import APIRouter, Depends

from app.schemas.chat import ChatBase
from app.schemas.response import ChatResponse
from app.schemas.user import User
from app.web.api.auth.core import get_current_user

from .core import chatgpt_function_response

router = APIRouter()


@router.post("/request")
async def chat(
    chat_request: ChatBase, current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """Generic chat request.

    A generic chat request.
    :param chat_request: chat request.
    :return: chat response.
    """
    logging.info(f"Chat request from user {current_user.username}: {chat_request}")

    response = await chatgpt_function_response(
        chat_request.prompt, username=current_user.username, user_id=current_user.id
    )
    return ChatResponse(success=True, response=response, reason="Success")
