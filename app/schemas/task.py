from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    """Generic task request."""

    id: int
    task: str
    date: datetime
