import logging

from fastapi import APIRouter
from schemas.response import TaskResponse

from app.schemas.task import Task
from app.services.aws.dynamodb import append_task, get_user_tasks

router = APIRouter()


@router.post("/create_task/{user_id}")
async def _create_task(user_id, task: Task) -> str:
    if append_task(user_id, task.task, task.date):
        return f"Reminder: {task.task} at {task.date}"
    return "Failed to create reminder"


@router.get("/get_tasks/{user_id}")
async def _get_user_tasks(user_id: str) -> TaskResponse:
    logging.info(f"Getting tasks for user {user_id}")
    tasks = get_user_tasks(user_id)
    return tasks
