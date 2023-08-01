from fastapi import APIRouter
from src.config import settings

from src.user.api import router as user_router


# Router
api_router = APIRouter()


# User
api_router.include_router(user_router, include_in_schema=True, prefix=settings.API_LATEST_VERSION_PREFIX, tags=["User APIs"])
