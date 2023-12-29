from pydantic import BaseModel


class Response(BaseModel):
    success: bool
    reason: str | None = None
