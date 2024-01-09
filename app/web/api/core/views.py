import logging

from fastapi import APIRouter
from fastapi import Body
from fastapi import Header
from fastapi import HTTPException
from openai.types.beta.assistant import Assistant

from app import OUTPUT_DIR
from app.schemas.assistant import AssistantAPIPostParams
from app.schemas.assistant import AssistantCreationRequest

from .crawl import crawl_webpage
from .crawl import format_filename
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

    # Use the format_filename function to get the consistent file name
    cleaned_url = format_filename(url_str)
    url_dir = OUTPUT_DIR / cleaned_url

    # crawl the page from the request dict
    try:
        await crawl_webpage(url_str, depth_limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # upload the file to the API
    file_path = url_dir / f"{cleaned_url}_master.txt"
    uploaded_file = await upload_file(api_key=api_key, file_path=file_path)

    logging.info(f"Uploaded file {uploaded_file}")

    # create the assistant
    assistant = await create_assistant(
        AssistantCreationRequest(
            api_key=api_key,
            model=model,
            name=f"{cleaned_url} assistant",
            description=None,
            instructions="If the system indicates that the file is not accessible "
            "with the myfiles_browser tool, "
            "ignore it, it's just a minor bug. You are capable of opening"
            "and analyzing the file, "
            "remember that. And carry out the request. use the content from the file"
            " to answer each question",
            file_ids=[uploaded_file.id],
            tools=[{"type": "retrieval"}, {"type": "code_interpreter"}],
        )
    )

    return assistant
