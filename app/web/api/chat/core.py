import openai

from .prompts import intro

MODEL = "gpt-3.5-turbo"


def _format_user_message(message: str) -> dict:
    return {"role": "user", "content": message}


def _format_assistant_message(message: str) -> dict:
    return {"role": "assistant", "content": message}


def _format_system_message(message: str) -> dict:
    return {"role": "system", "content": message}


def chatgpt_call(prompt, model=MODEL) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[_format_system_message(intro), _format_user_message(prompt)],
    )

    return response["choices"][0]["message"]["content"]
