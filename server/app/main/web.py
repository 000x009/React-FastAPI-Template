from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from app.presentation.api import include_routers
from app.main.ioc import get_async_container
from app.main.config import load_config
from app.services.jwt_token_processor import TokenProcessor


def singleton(dependency):
    def _singleton():
        return dependency
    return _singleton


def get_app() -> FastAPI:
    config = load_config()
    fastapi = FastAPI(title="App")

    token_processor = TokenProcessor(
        key=config.token.key,
        algorythm=config.token.algorithm,
    )

    fastapi.dependency_overrides.update({
        TokenProcessor: singleton(token_processor),
    })
    include_routers(fastapi)

    container = get_async_container(config)
    setup_dishka(container=container, app=fastapi)

    return fastapi
