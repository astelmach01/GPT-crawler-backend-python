import json

import openai

from .functions import function_descriptions, function_names
from .prompts import intro

MODEL = "gpt-3.5-turbo"


def _handle_function_call(response: dict) -> str:
    response_message = response["message"]

    function_name = response_message["function_call"]["name"]
    function_to_call = function_names[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])

    function_response = function_to_call(**function_args)
    return function_response


def _format_system_message(message: str) -> dict:
    return {"speaker": "system", "text": message}


def _format_user_message(message: str) -> dict:
    return {"speaker": "user", "text": message}


def chatgpt_response(prompt, model=MODEL) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[_format_system_message(intro), _format_user_message(prompt)],
    )

    return response["choices"][0]["message"]["content"]


def chatgpt_function_response(
    prompt: str, functions=function_descriptions, model=MODEL
) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            _format_system_message(intro),
            _format_user_message(prompt),
        ],
        functions=functions,
    )["choices"][0]

    if response["finish_reason"] == "function_call":
        return _handle_function_call(response)

    return response["message"]["content"]
