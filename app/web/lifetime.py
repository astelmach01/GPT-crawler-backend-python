from typing import Awaitable, Callable

from fastapi import FastAPI

from app.services.aws.rds import DatabaseSession

DB_NAME = "user_task_db"


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        DatabaseSession.initialize()
        app.state.db_session = DatabaseSession.get_session()
        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    @app.on_event("shutdown")
    async def _shutdown() -> None:
        DatabaseSession.close()

    return _shutdown
