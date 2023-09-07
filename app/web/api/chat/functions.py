from langchain.tools import StructuredTool

from app.web.api.tasks.core import create_reminder

from .models import ReminderInput

create_reminder_tool = StructuredTool.from_function(
    func=create_reminder,
    name="create_reminder",
    description="This function handles the logic for creating a reminder for a "
    "generic task at a given date and time. Integer parameters should be greater "
    "than or equal to zero.",
    args_schema=ReminderInput,
)

tools = [create_reminder_tool]
