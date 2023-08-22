import openai

from app.settings import settings

openai_api_key = settings.OPENAI_API_KEY
openai.api_key = openai_api_key

MODEL = "gpt-3.5-turbo"


def chatgpt_call(prompt, model=MODEL) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response["choices"][0]["message"]["content"]
