"""Chat API."""
import openai

from app.settings import settings

from .views import router

openai.api_key = settings.OPENAI_API_KEY
openai.organization = settings.OPENAI_ORGANIZATION

__all__ = ["router"]
