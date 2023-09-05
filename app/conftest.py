from datetime import datetime
from typing import Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.aws.models import Base, Task, User
from app.settings import settings

from .web.api.dependencies import get_db
from .web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: app name.
    """
    return "asyncio"


@pytest.fixture
def fastapi_app(test_db_session) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db] = lambda: test_db_session
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


test_task_params = {
    "description": "test task",
    "date": datetime(2021, 1, 1, 12, 0),
    "user_id": 1,
}

test_user_params = {"name": "test user", "id": 1}


@pytest.fixture(scope="function")
def test_db_session():
    engine = create_engine(
        settings.get_db_url("test_user_task_db"), connect_args={"wait_timeout": 1}
    )
    Base.metadata.create_all(engine)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = session_local()

    # Insert a test user
    test_user = User(**test_user_params)
    db.add(test_user)
    db.commit()

    # insert a test task with a date of 12:30 on 1st Jan 2021
    test_task = Task(**test_task_params)
    db.add(test_task)
    db.commit()

    yield db  # this is where the testing happens

    db.close()

    Base.metadata.drop_all(engine)
