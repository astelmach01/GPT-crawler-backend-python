from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from app.settings import settings
from app.web.api.chat.prompts import intro

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

system_prompt = SystemMessagePromptTemplate.from_template(intro)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_message_prompt])

chain = LLMChain(llm=llm, prompt=chat_prompt, memory=memory)


def main():
    # Run the chain
    print(chain.run("I would like to book a flight to London."))

    # Print the output
    print(memory.chat_memory.messages)
    print(message_history.messages)
