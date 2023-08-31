from fastapi.routing import APIRouter

from .auth import router as auth_router
from .chat import router as chat_router
from .docs import router as docs_router
from .monitoring import router as monitoring_router
from .tasks import router as tasks_router
from .users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(monitoring_router)
api_router.include_router(docs_router)
