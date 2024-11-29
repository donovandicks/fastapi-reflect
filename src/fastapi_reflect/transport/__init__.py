from fastapi import FastAPI

from .ai import ai_router as AIRouter
from .songs import songs_router as SongsRouter

routers = [
    SongsRouter,
    AIRouter,
]


def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)


__all__ = ["register_routers"]
