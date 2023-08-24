from fastapi import APIRouter

from app.schemas.chat import ChatBase, ChatResponse

from .core import chatgpt_function_response

router = APIRouter()


@router.post("/request")
async def chat(chat_request: ChatBase) -> ChatResponse:
    """Generic chat request.

    A generic chat request.
    :param chat_request: chat request.
    :return: chat response.
    """

    response = chatgpt_function_response(chat_request.prompt)
    return ChatResponse(response=response)
