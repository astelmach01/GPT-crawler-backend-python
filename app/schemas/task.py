from pydantic import BaseModel


class Task(BaseModel):
    """Generic task request."""

    task: str
    date: str
