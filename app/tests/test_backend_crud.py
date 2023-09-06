import asyncio
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


@pytest.mark.asyncio
async def test_stale_data_after_update(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    # Create a task
    new_task = {"description": "test task 3", "date": datetime(2021, 1, 1, 12, 0)}
    response = await client.post(
        fastapi_app.url_path_for("create_new_task", user_id=1),
        params=new_task,
    )
    assert response.status_code == status.HTTP_200_OK

    # Update the task
    updated_task = {"description": "updated test task 3"}
    response = await client.put(
        fastapi_app.url_path_for(
            "_update_task", task_id=response.json()["tasks"][0]["id"]
        ),
        params=updated_task,
    )
    assert response.status_code == status.HTTP_200_OK

    # Fetch the task and ensure it reflects the update
    response = await client.get(
        fastapi_app.url_path_for("get_user_tasks", user_id=1),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["tasks"][-1]["task"] == "updated test task 3"


@pytest.mark.asyncio
async def test_stale_data_after_delete(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    # Create a task
    new_task = {"description": "test task 4", "date": datetime(2021, 1, 1, 12, 0)}
    response = await client.post(
        fastapi_app.url_path_for("create_new_task", user_id=1),
        params=new_task,
    )
    assert response.status_code == status.HTTP_200_OK

    # Delete the task
    response = await client.delete(
        fastapi_app.url_path_for(
            "_delete_task", task_id=response.json()["tasks"][0]["id"]
        ),
    )
    assert response.status_code == status.HTTP_200_OK

    # Fetch tasks and ensure the deleted task is not returned
    response = await client.get(
        fastapi_app.url_path_for("get_user_tasks", user_id=1),
    )
    assert response.status_code == status.HTTP_200_OK
    assert not any(task["task"] == "test task 4" for task in response.json()["tasks"])


@pytest.mark.asyncio
async def test_create_tasks_multi(client: AsyncClient, fastapi_app: FastAPI) -> None:
    # create a task
    new_task = {"description": "test task", "date": datetime(2021, 1, 1, 12, 0)}

    num_tasks = 100
    # Create multiple tasks that make requests to the API
    tasks = [
        asyncio.create_task(
            client.post(
                fastapi_app.url_path_for("create_new_task", user_id=1),
                params=new_task,
            )
        )
        for _ in range(
            num_tasks
        )  # Change this to the number of concurrent requests you want to make
    ]

    # Gather the results of all tasks
    responses = await asyncio.gather(*tasks)

    # Check that all responses are the same
    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json["success"] == True
        assert response_json["reason"] == "Success"
        assert len(response_json["tasks"]) == 1
        task = response_json["tasks"][0]
        assert task["task"] == new_task["description"]
        assert task["date"] == new_task["date"].strftime("%Y-%m-%dT%H:%M:%S")
        assert task["id"] > 0 and task["id"] <= num_tasks + 1


@pytest.mark.asyncio
async def test_update_task_multi_get(client: AsyncClient, fastapi_app: FastAPI) -> None:
    # update a task
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

    num_requests = 100
    # Create multiple tasks that make requests to the API
    tasks = [
        asyncio.create_task(
            client.get(
                fastapi_app.url_path_for("get_user_tasks", user_id=1),
            )
        )
        for _ in range(num_requests)
    ]

    # Gather the results of all tasks
    responses = await asyncio.gather(*tasks)

    # Check that all responses are the same
    for response in responses:
        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()
        assert response_json["success"] == True
        assert response_json["reason"] == "Success"
        assert len(response_json["tasks"]) >= 1
        task = response_json["tasks"][0]
        assert task["task"] == updated_task["description"]
        assert task["date"] == updated_task["date"].strftime("%Y-%m-%dT%H:%M:%S")
        assert task["id"] == 1


@pytest.mark.asyncio
async def test_crud_tasks_intertwined(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    num_tasks = 100
    new_task = {"description": "test task", "date": datetime(2021, 1, 1, 12, 0)}
    updated_task = {"description": "updated task", "date": datetime(2021, 1, 1, 12, 0)}

    tasks = []
    for i in range(num_tasks):
        # Create a task
        tasks.append(
            asyncio.create_task(
                client.post(
                    fastapi_app.url_path_for("create_new_task", user_id=1),
                    params=new_task,
                )
            )
        )

        # Update the task
        tasks.append(
            asyncio.create_task(
                client.put(
                    fastapi_app.url_path_for("_update_task", task_id=i + 1),
                    params=updated_task,
                )
            )
        )

        # Get the task
        tasks.append(
            asyncio.create_task(
                client.get(
                    fastapi_app.url_path_for("get_user_tasks", user_id=1),
                )
            )
        )

        # Delete the task
        tasks.append(
            asyncio.create_task(
                client.delete(
                    fastapi_app.url_path_for("_delete_task", task_id=i + 1),
                )
            )
        )

    # Gather the results of all tasks
    responses = await asyncio.gather(*tasks)

    # Check that all responses are successful
    for response in responses:
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_crud_tasks_intertwined(
    client: AsyncClient, fastapi_app: FastAPI
) -> None:
    num_tasks = 100
    new_task = {"description": "test task", "date": datetime(2021, 1, 1, 12, 0)}
    updated_task = {"description": "updated task", "date": datetime(2021, 1, 1, 12, 0)}

    for i in range(num_tasks):
        # Create a task
        response = await client.post(
            fastapi_app.url_path_for("create_new_task", user_id=1),
            params=new_task,
        )
        assert response.status_code == status.HTTP_200_OK

        # Update the task
        response = await client.put(
            fastapi_app.url_path_for("_update_task", task_id=i + 1),
            params=updated_task,
        )
        assert response.status_code == status.HTTP_200_OK

        # Get the task
        response = await client.get(
            fastapi_app.url_path_for("get_user_tasks", user_id=1),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["tasks"][0]["task"] == updated_task["description"]

        # Delete the task
        response = await client.delete(
            fastapi_app.url_path_for("_delete_task", task_id=i + 1),
        )
        assert response.status_code == status.HTTP_200_OK

        # Get the task
        response = await client.get(
            fastapi_app.url_path_for("get_user_tasks", user_id=1),
        )
        assert response.status_code == status.HTTP_200_OK
        assert not any(task["id"] == i + 1 for task in response.json()["tasks"])
