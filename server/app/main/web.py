from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from app.presentation.api import include_routers
from app.main.ioc import get_async_container
from app.main.config import load_config


def get_app() -> FastAPI:
    config = load_config()
    fastapi = FastAPI(title="App")

    include_routers(fastapi)

    container = get_async_container(config)
    setup_dishka(container=container, app=fastapi)

    return fastapi
