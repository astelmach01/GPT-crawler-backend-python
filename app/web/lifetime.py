from typing import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.aws.models import Base  # Import models from models.py
from app.settings import settings

DB_NAME = "user_task_db"


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    @app.on_event("startup")
    async def _startup() -> None:
        app.middleware_stack = None
        engine = create_engine(settings.get_db_url(DB_NAME))
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)
        app.state.db_engine = engine
        app.state.db_session = session()
        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    @app.on_event("shutdown")
    async def _shutdown() -> None:
        app.state.db_session.close()
        app.state.db_engine.dispose()

    return _shutdown
