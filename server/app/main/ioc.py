from collections.abc import AsyncGenerator, AsyncIterable

from dishka import Provider, Scope, provide, from_context, AsyncContainer, make_async_container
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.main.config import WebConfig
from app.services.user_service import UserService
from app.data.dao.user import UserDAO


class DatabaseProvider(Provider):
    config = from_context(WebConfig, override=True, scope=Scope.APP)

    @provide(scope=Scope.APP, provides=AsyncEngine)
    async def get_engine(self, config: WebConfig) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(url=config.database.connection_url, pool_pre_ping=True)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_async_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self, sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session


class ServiceProvider(Provider):
    user_service = provide(UserService, scope=Scope.REQUEST, provides=UserService)


class DAOProvider(Provider):
    user_dao = provide(UserDAO, scope=Scope.REQUEST, provides=UserDAO)


def get_async_container(config: WebConfig) -> AsyncContainer:
    providers = [
        DatabaseProvider(),
        ServiceProvider(),
        DAOProvider(),
    ]
    container = make_async_container(*providers, context={WebConfig: config})

    return container
