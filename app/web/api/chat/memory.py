import logging
from typing import List

from langchain.adapters.openai import convert_message_to_dict
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory
from langchain.schema.messages import SystemMessage

from app.services.aws.dynamodb import TABLE_NAME, session

from .prompts import system_prompt


def get_memory(session_id: str):
    """Get a conversation buffer with chathistory saved to dynamodb

    Returns:
        ConversationBufferMemory: A memory object with chat history saved to dynamodb
    """

    # Define the necessary components with the dynamodb endpoint
    message_history = DynamoDBChatMessageHistory(
        table_name=TABLE_NAME,
        session_id=session_id,
        boto3_session=session,
    )

    if len(message_history.messages) == 0:
        message_history.add_message(SystemMessage(content=system_prompt))

    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history, return_messages=True
    )

    logging.info(f"Memory: {memory}")

    return memory


def convert_message_buffer_to_openai(memory: ConversationBufferMemory) -> List[dict]:
    """Convert a message buffer to a list of messages that OpenAI can understand

    Args:
        memory (ConversationBufferMemory): A memory object with chat history saved
        to dynamodb

    Returns:
        List[dict]: A list of messages that OpenAI can understand
    """
    messages = []
    for message in memory.buffer_as_messages:
        messages.append(convert_message_to_dict(message))

    return messages
