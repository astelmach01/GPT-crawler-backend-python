from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import DynamoDBChatMessageHistory

TABLE_NAME = "SessionTable"


def get_memory(session_id: str):
    """Get a conversation buffer with chathistory saved to dynamodb

    Returns:
        ConversationBufferMemory: A memory object with chat history saved to dynamodb
    """

    # Define the necessary components
    message_history = DynamoDBChatMessageHistory(
        table_name=TABLE_NAME,
        session_id=session_id,
        endpoint_url="https://dynamodb.us-east-2.amazonaws.com",
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history, return_messages=True
    )

    return memory
