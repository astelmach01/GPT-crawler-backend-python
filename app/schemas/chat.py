from pydantic import BaseModel


class ChatBase(BaseModel):
    """Generic chat request."""

    prompt: str
