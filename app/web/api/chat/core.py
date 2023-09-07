from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage

from app.settings import settings

from .functions import tools
from .memory import get_memory
from .prompts import intro

llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, model=settings.MODEL_NAME)


def get_response(prompt: str, session_id):
    agent = initialize_agent(
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        tools=tools,
        memory=get_memory(session_id=session_id),
        agent_kwargs={"SystemMessage": SystemMessage(content=intro)},
    )
    return agent.run(prompt)
