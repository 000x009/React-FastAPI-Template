import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(override=True)


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    name: str

    @property
    def connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.name}"


@dataclass
class TokenConfig:
    algorithm: str
    key: str


@dataclass
class WebConfig:
    database: DBConfig
    token: TokenConfig


def load_config() -> WebConfig:
    db_config = DBConfig(
        host=os.environ.get('DB_HOST'),
        password=os.environ.get('DB_PASSWORD'),
        user=os.environ.get('DB_USER'),
        name=os.environ.get('DB_NAME'),
    )
    token_config = TokenConfig(
        algorithm=os.environ.get('TOKEN_ALGORITHM'),
        key=os.environ.get('TOKEN_SECRET_KEY'),
    )

    return WebConfig(
        database=db_config,
        token=token_config,
    )
