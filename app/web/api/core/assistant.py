import os
from typing import Dict
from typing import List
from typing import Literal

from fastapi import HTTPException
from openai import OpenAI
from openai.types import FileObject
from openai.types.beta import Assistant
from pydantic import BaseModel


class AssistantCreationRequest(BaseModel):
    api_key: str
    model: str = "gpt-3.5-turbo-1106"
    name: str | None = None
    description: str | None = None
    file_ids: List[str] | None = None
    tools: List[Dict[str, str]] | None = None
    instructions: str | None = None


async def create_assistant(request: AssistantCreationRequest) -> Assistant:
    """Creates a new assistant."""
    args = request.model_dump()
    api_key = args.pop("api_key")

    client = OpenAI(api_key=api_key)

    try:
        assistant = client.beta.assistants.create(**args)
        return assistant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def upload_file(
    api_key: str,
    file_path: os.PathLike,
    purpose: Literal["fine-tune", "assistants"] = "assistants",
) -> FileObject:
    """Uploads a file to OpenAI's API."""
    try:
        client = OpenAI(api_key=api_key)
        response = client.files.create(file=file_path, purpose=purpose)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
