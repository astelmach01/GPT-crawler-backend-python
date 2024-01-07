import logging
from urllib.parse import urlparse

from fastapi import APIRouter
from fastapi import Body
from fastapi import Header
from openai.types.beta.assistant import Assistant

from app import OUTPUT_DIR
from app.schemas.assistant import AssistantAPIPostParams
from app.schemas.assistant import AssistantCreationRequest

from .crawl import crawl_webpage
from .openai import create_assistant
from .openai import upload_file


router = APIRouter()


@router.post("/assistant")
async def make_assistant(
    api_key: str = Header(..., description="OpenAI API key for authentication"),
    params: AssistantAPIPostParams = Body(...),
) -> Assistant:
    """Create a new assistant from a URL."""
    url = params.url
    depth_limit = params.depth_limit
    model = params.model

    url_str = str(url)
    cleaned_url = urlparse(url_str).netloc.replace(".", "_")
    url_dir = OUTPUT_DIR / cleaned_url

    # crawl the page from the request dict
    await crawl_webpage(url_str, depth_limit)

    # upload the file to the API
    file_path = url_dir / f"{cleaned_url}_master_combined.txt"
    uploaded_file = await upload_file(api_key=api_key, file_path=file_path)

    logging.info(f"Uploaded file {uploaded_file}")

    # create the assistant
    assistant = await create_assistant(
        AssistantCreationRequest(
            api_key=api_key,
            model=model,
            name=f"{cleaned_url} assistant",
            description=None,
            file_ids=[uploaded_file.id],
            tools=[{"type": "retrieval"}],
        )
    )

    return assistant
