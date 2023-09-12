import json
import logging

import openai

from .functions import function_descriptions, function_names
from .memory import convert_message_buffer_to_openai, get_memory

MODEL = "gpt-3.5-turbo"
SESSION_ID = "0"


def _handle_function_call(response: dict) -> str:
    response_message = response["message"]

    function_name = response_message["function_call"]["name"]
    function_to_call = function_names[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])

    function_response = function_to_call(**function_args)
    return function_response


def chatgpt_response(prompt, model=MODEL, session_id: str = SESSION_ID) -> str:
    memory = get_memory(session_id)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory: {messages}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    answer = response["choices"][0]["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer


def chatgpt_function_response(
    prompt: str,
    functions=function_descriptions,
    model=MODEL,
    session_id: str = SESSION_ID,
) -> str:
    memory = get_memory(session_id)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory for function response: {messages}")

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
    )["choices"][0]

    if response["finish_reason"] == "function_call":
        answer = _handle_function_call(response)

    else:
        answer = response["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer
