import json
import logging

import openai

from .functions import function_descriptions, function_names
from .memory import convert_message_buffer_to_openai, get_memory

MODEL = "gpt-3.5-turbo"


async def _handle_function_call(response: dict, user_id) -> str:
    response_message = response["message"]

    function_name = response_message["function_call"]["name"]
    function_to_call = function_names[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])

    function_args["user_id"] = user_id

    function_response = await function_to_call(**function_args)
    return function_response


async def chatgpt_response(prompt, username: str, model=MODEL) -> str:
    memory = get_memory(username)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory: {messages}")
    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
    )

    answer = response["choices"][0]["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer


async def chatgpt_function_response(
    prompt: str,
    username: str,
    functions=function_descriptions,
    model=MODEL,
    **kwargs,
) -> str:
    memory = get_memory(username)
    memory.chat_memory.add_user_message(prompt)

    messages = convert_message_buffer_to_openai(memory)

    logging.info(f"Memory for function response: {messages}")

    response = await openai.ChatCompletion.acreate(
        model=model,
        messages=messages,
        functions=functions,
    )
    response = response["choices"][0]

    if response["finish_reason"] == "function_call":
        answer = await _handle_function_call(response, **kwargs)

    else:
        answer = response["message"]["content"]

    memory.chat_memory.add_ai_message(answer)
    return answer
