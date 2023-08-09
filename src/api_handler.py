from fastapi import APIRouter

from src.user.api import user_router

# Router
api_router = APIRouter()


# User
api_router.include_router(user_router, include_in_schema=True, tags=["User APIs"])
