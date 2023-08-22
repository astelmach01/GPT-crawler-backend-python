from pydantic import BaseModel


class ChatBase(BaseModel):
    """Generic chat request."""

    prompt: str


class ChatResponse(BaseModel):
    """Generic chat response."""

    response: str
