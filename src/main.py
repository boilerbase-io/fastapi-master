import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import Config

format = "%(levelname)s:%(funcName)s:%(message)s"
logging.basicConfig(level=Config.LOG_LEVEL, format=format)


def create_app():
    app = FastAPI(
        title=Config.PROJECT_NAME,
        description=Config.PROJECT_DESCRIPTION,
        version=Config.PROJECT_VERSION,
        contact={"email": Config.CONTACT_EMAIL},
        termsOfService=Config.TERMS_OF_SERVICE,
        host=Config.SERVER_HOST,
    )

    # add CORS
    if Config.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in Config.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include API handler router
    from src.api_handler import api_router

    # include main router
    app.include_router(api_router)

    # controller routes
    @app.get("/", tags=["API ModelBase"])
    def _get():
        return f"Welcome to {Config.PROJECT_NAME} APIs"

    return app
