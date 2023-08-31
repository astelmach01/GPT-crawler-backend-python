import logging
from datetime import datetime
from functools import wraps
from typing import Sequence

from fastapi import APIRouter, HTTPException
from services.aws.models import Task as TaskModel

from app.schemas.response import TaskResponse
from app.schemas.task import Task as TaskSchema
from app.services.aws.rds import (
    create_task,
    delete_task,
    read_tasks_by_user_id,
    update_task,
)

router = APIRouter()


def task_response_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> TaskResponse:
        try:
            task_result: Sequence[TaskModel | None]
            task_result, log_msg = await func(*args, **kwargs)

            logging.info(f"Executed {func.__name__} with result: {task_result}")

            if None in task_result:
                return TaskResponse(success=False, reason=log_msg)

            tasks = [
                TaskSchema(task=task.description, date=task.date)
                for task in task_result
                if task
            ]
            return TaskResponse(success=True, tasks=tasks)

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return wrapper


@router.post("/create_task/{user_id}", response_model=TaskResponse)
@task_response_decorator
async def create_new_task(user_id: str, description: str, date: datetime):
    task: TaskModel = create_task(description, date, user_id)
    return [task], f"Task for user_id: {user_id} not created"


@router.get("/get_user_tasks/{user_id}", response_model=TaskResponse)
@task_response_decorator
async def get_user_tasks(user_id: str):
    tasks: Sequence[TaskModel | None] = read_tasks_by_user_id(user_id)
    if not tasks:
        tasks = [None]
    return tasks, f"No tasks found for user: {user_id}"


@router.put("/update_task/{task_id}", response_model=TaskResponse)
@task_response_decorator
async def _update_task(task_id: str, description: str, date: datetime):
    task: TaskModel = update_task(task_id, description, date)
    return [task], f"Task with task_id: {task_id} not updated"


@router.delete("/delete_task/{task_id}", response_model=TaskResponse)
@task_response_decorator
async def _delete_task(task_id: str):
    task: TaskModel = delete_task(task_id)
    return [task], f"Task with task_id: {task_id} not deleted"
