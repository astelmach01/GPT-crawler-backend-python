from pydantic import BaseModel

from .task import Task


class Response(BaseModel):
    success: bool
    reason: str | None = None


class TaskResponse(Response):
    tasks: list[Task] = []


class UserResponse(Response):
    user_id: int | None = None


class ChatResponse(Response):
    """Generic chat response."""

    response: str | None = None


class TokenResponse(Response):
    """Generic token response."""

    access_token: str | None = None
    token_type: str | None = None
