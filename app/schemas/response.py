from pydantic import BaseModel

from .task import Task


class Response(BaseModel):
    success: bool


class TaskResponse(Response):
    tasks: list[Task] = []


class ChatResponse(Response):
    """Generic chat response."""

    response: str
