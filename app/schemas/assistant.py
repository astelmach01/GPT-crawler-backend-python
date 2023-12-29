from typing import List, Union

from pydantic import BaseModel, Field

from .response import Response


# Define Pydantic models for the various tool types
class CodeInterpreterTool(BaseModel):
    type: str = Field("code_interpreter", regex="code_interpreter")


class RetrievalTool(BaseModel):
    type: str = Field("retrieval", regex="retrieval")


class FunctionParameters(BaseModel):
    # Since parameters are described as a JSON Schema object, we can represent them with a dict
    # More specific models can be created if there's a known structure to validate against
    pass  # Placeholder for any specific fields, if necessary


class FunctionTool(BaseModel):
    type: str = Field("function", regex="function")
    description: str
    name: str = Field(..., regex=r"^[a-zA-Z0-9_-]{1,64}$")
    parameters: FunctionParameters | None


# Union type for tools as they can be of different types
ToolType = Union[CodeInterpreterTool, RetrievalTool, FunctionTool]


class AssistantResponse(Response):
    id: str
    object: str
    created_at: int
    name: str | None = Field(None, max_length=256)
    description: str | None = Field(None, max_length=512)
    model: str
    instructions: str | None = Field(None, max_length=32768)
    tools: List[ToolType] = Field(..., max_items=128)
