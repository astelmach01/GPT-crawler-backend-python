from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.schema import SystemMessage
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel, Field

from app.settings import settings
from app.web.api.tasks.core import create_reminder

from .prompts import intro

TABLE_NAME = "SessionTable"
session_id = "0"

# Define the necessary components
message_history = DynamoDBChatMessageHistory(
    table_name=TABLE_NAME, session_id=session_id
)

memory = ConversationBufferMemory(
    memory_key="chat_history", chat_memory=message_history, return_messages=True
)
llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY)


class ReminderInput(BaseModel):
    task: str = Field(..., description="The task to be reminded of")
    days: int = Field(..., description="The number of days to wait")
    hours: int = Field(..., description="The number of hours to wait")
    minutes: int = Field(..., description="The number of minutes to wait")


tools = [
    StructuredTool.from_function(
        func=create_reminder,
        name="create_reminder",
        description="This function handles the logic for creating a reminder for a "
        "generic task at a given date and time. Integer parameters should be greater "
        "than or equal to zero.",
        args_schema=ReminderInput,
    )
]

agent = initialize_agent(
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=tools,
    memory=memory,
    agent_kwargs={"SystemMessage": SystemMessage(content=intro)},
)


def main():
    # Run the chain
    print(agent.run(input("Enter a message: ")))

    # Print the output
    print(memory.chat_memory.messages)
    print(message_history.messages)
