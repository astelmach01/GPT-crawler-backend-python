from pydantic import BaseModel

from .task import Task
from .user import User


class Response(BaseModel):
    success: bool
    reason: str | None = None


class TaskResponse(Response):
    tasks: list[Task] = []


class UserResponse(Response):
    user: User | None = None


class ChatResponse(Response):
    """Generic chat response."""

    response: str | None = None
