from fastapi import FastAPI

from app.presentation.api import user, auth


def include_routers(app: FastAPI) -> None:
    app.include_router(user.router)
    app.include_router(auth.router)
