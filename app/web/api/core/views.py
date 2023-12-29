import logging
from urllib.parse import urlparse

from fastapi import APIRouter, Header, Body
from openai.types.beta.assistant import Assistant
from pydantic import HttpUrl

from app import OUTPUT_DIR
from .assistant import create_assistant, upload_file, AssistantCreationRequest
from .crawl import crawl_webpage

router = APIRouter()


@router.post("/assistant")
async def make_assistant(
    api_key: str = Header(..., description="API key for authentication"),
    url: HttpUrl = Body(..., embed=True, description="The URL to crawl")) -> Assistant:
    """Create a new assistant from a URL."""

    url_str = str(url)
    cleaned_url = urlparse(url_str).netloc.replace(".", "_")
    url_dir = OUTPUT_DIR / cleaned_url

    # crawl the page from the request dict
    crawl_webpage(url_str)

    # upload the file to the API
    file_path = url_dir / f"{cleaned_url}_master_combined.txt"
    uploaded_file = await upload_file(api_key=api_key, file_path=file_path)

    logging.info(f"Uploaded file {uploaded_file}")

    # create the assistant
    assistant = await create_assistant(
        AssistantCreationRequest(
            api_key=api_key,
            model="gpt-3.5-turbo-1106",
            name="Math Tutor",
            description=None,
            file_ids=[uploaded_file.id],
            tools=[{"type": 'code_interpreter'}],
            instructions="You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        )
    )

    return assistant
