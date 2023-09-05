from datetime import datetime

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


# test adding a task to the "api/tasks/create_task/{user_id}" endpoint
@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, fastapi_app: FastAPI) -> None:
    # create a task
    new_task = {"description": "test task", "date": datetime(2021, 1, 1, 12, 0)}

    response = await client.post(
        fastapi_app.url_path_for("create_new_task", user_id=1),
        params=new_task,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 2,
                "task": new_task["description"],
                "date": new_task["date"].strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ],
        "reason": "Success",
    }


# test creating a task with a non-existent user
@pytest.mark.asyncio
async def test_create_task_non_existent_user(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    # create a task
    new_task = {"description": "test task", "date": datetime(2021, 1, 1, 12, 0)}

    response = await client.post(
        fastapi_app.url_path_for("create_new_task", user_id=1003436),
        params=new_task,
    )
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": False,
        "reason": "Task for user_id: 1003436 not created",
        "tasks": [],
    }


# test creating a task, deleting it, and then getting tasks for the user id 1
# user id 1 already has these tasks in the database
# test_task_params = {
#     "description": "test task",
#     "date": datetime(2021, 1, 1, 12, 0),
#     "user_id": 1,
# }
@pytest.mark.asyncio
async def test_create_task_delete_task_get_tasks(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    # create a task
    new_task = {"description": "test task 2", "date": datetime(2021, 1, 1, 12, 0)}

    response = await client.post(
        fastapi_app.url_path_for("create_new_task", user_id=1),
        params=new_task,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 2,
                "task": new_task["description"],
                "date": new_task["date"].strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ],
        "reason": "Success",
    }

    # get the tasks, assert length is 2
    response = await client.get(
        fastapi_app.url_path_for("get_user_tasks", user_id=1),
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["tasks"]) == 2

    # delete the task
    response = await client.delete(
        fastapi_app.url_path_for("_delete_task", task_id=2),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 2,
                "task": new_task["description"],
                "date": new_task["date"].strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ],
        "reason": "Success",
    }

    # get tasks for user id 1
    response = await client.get(
        fastapi_app.url_path_for("get_user_tasks", user_id=1),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 1,
                "task": "test task",
                "date": "2021-01-01T12:00:00",
            }
        ],
        "reason": "Success",
    }


# test updating a task then getting tasks for the user id 1
@pytest.mark.asyncio
async def test_update_task_get_tasks(client: AsyncClient, fastapi_app: FastAPI) -> None:
    # update the task
    updated_task = {"description": "updated task", "date": datetime(2021, 1, 1, 12, 0)}

    response = await client.put(
        fastapi_app.url_path_for("_update_task", task_id=1),
        params=updated_task,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 1,
                "task": updated_task["description"],
                "date": updated_task["date"].strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ],
        "reason": "Success",
    }

    # get tasks for user id 1
    response = await client.get(
        fastapi_app.url_path_for("get_user_tasks", user_id=1),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "success": True,
        "tasks": [
            {
                "id": 1,
                "task": updated_task["description"],
                "date": updated_task["date"].strftime("%Y-%m-%dT%H:%M:%S"),
            }
        ],
        "reason": "Success",
    }
