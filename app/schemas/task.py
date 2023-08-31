from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    """Generic task request."""

    task: str
    date: datetime
