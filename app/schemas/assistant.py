from typing import Dict
from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


# Define Pydantic models for the various tool types
class CodeInterpreterTool(BaseModel):
    type: str = "code_interpreter"


class RetrievalTool(BaseModel):
    type: str = "retrieval"


class FunctionParameters(BaseModel):
    # Since parameters are described as a JSON Schema object, we can represent
    # them with a dict. More specific models can be created if there's a known
    # structure to validate against
    pass  # Placeholder for any specific fields, if necessary


class FunctionTool(BaseModel):
    type: str = "function"
    description: str
    name: str = Field(..., pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    parameters: FunctionParameters | None


ToolType = Union[CodeInterpreterTool, RetrievalTool, FunctionTool]


class AssistantAPIPostParams(BaseModel):
    url: HttpUrl = Field(..., description="The URL to crawl")
    depth_limit: int = Field(1000, gt=0, description="The depth limit for the crawl")
    model: str = Field(
        "gpt-3.5-turbo-1106", description="The GPT model to use for the assistant"
    )


# request body to create an assistant
class AssistantCreationRequest(BaseModel):
    api_key: str
    model: str = "gpt-3.5-turbo-1106"
    name: str | None = None
    description: str | None = None
    file_ids: List[str] | None = None
    tools: List[Dict[str, str]] | None = None
    instructions: str | None = None
