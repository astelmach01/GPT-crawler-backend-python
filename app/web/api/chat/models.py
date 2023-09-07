from pydantic.v1 import BaseModel, Field


class ReminderInput(BaseModel):
    task: str = Field(..., description="The task to be reminded of")
    days: int = Field(..., description="The number of days to wait")
    hours: int = Field(..., description="The number of hours to wait")
    minutes: int = Field(..., description="The number of minutes to wait")
