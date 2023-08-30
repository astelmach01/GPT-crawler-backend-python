from typing import List

from fastapi import APIRouter

from app.schemas.chat import ChatBase, ChatResponse
from app.schemas.task import Task
from app.services.aws.dynamodb import append_task, get_user_tasks

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


@router.post("/create_task")
async def _create_task(user_id, task: Task) -> str:
    if append_task(user_id, task.task, task.date):
        return f"Reminder: {task.task} at {task.date}"
    return "Failed to create reminder"


@router.get("/get_tasks/{user_id}")
async def _get_user_tasks(user_id: str) -> List[Task]:
    tasks = get_user_tasks(user_id)
    return tasks
