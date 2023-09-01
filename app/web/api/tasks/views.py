import logging
from datetime import datetime
from functools import wraps
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.response import TaskResponse
from app.schemas.task import Task as TaskSchema
from app.services.aws.models import Task as TaskModel
from app.services.aws.rds import (
    create_task,
    delete_task,
    read_tasks_by_user_id,
    update_task,
)

from ..dependencies import get_db

router = APIRouter()


def task_response_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> TaskResponse:
        try:
            task_result: List[TaskModel | None]
            task_result, log_msg = await func(*args, **kwargs)

            logging.info(f"Executed {func.__name__} with result: {task_result}")

            if None in task_result:
                return TaskResponse(success=False, reason=log_msg)

            tasks = [
                TaskSchema(id=task.id, task=task.description, date=task.date)
                for task in task_result
                if task
            ]
            return TaskResponse(success=True, tasks=tasks, reason="Success")

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return wrapper


@router.post("/create_task/{user_id}", response_model=TaskResponse)
@task_response_decorator
async def create_new_task(
    description: str,
    date: datetime,
    user_id: int,
    session=Depends(get_db),
):
    task: TaskModel = create_task(description, date, user_id, session)
    return [task], f"Task for user_id: {user_id} not created"


@router.get("/get_user_tasks/{user_id}", response_model=TaskResponse)
@task_response_decorator
async def get_user_tasks(user_id: int, session=Depends(get_db)):
    tasks = read_tasks_by_user_id(user_id, session)
    return tasks, f"No tasks found for user: {user_id}"


@router.put("/update_task/{task_id}", response_model=TaskResponse)
@task_response_decorator
async def _update_task(
    task_id: int,
    description: str,
    date: datetime | None = None,
    session=Depends(get_db),
):
    task: TaskModel | None = update_task(
        task_id, description, new_date=date, session=session
    )
    return [task], f"Task with task_id: {task_id} not updated"


@router.delete("/delete_task/{task_id}", response_model=TaskResponse)
@task_response_decorator
async def _delete_task(task_id: int, session=Depends(get_db)):
    task: TaskModel | None = delete_task(task_id, session)
    return [task], f"Task with task_id: {task_id} not deleted"
