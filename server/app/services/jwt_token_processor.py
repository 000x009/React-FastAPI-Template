import json
from typing import Literal, Any, MutableMapping
from datetime import timedelta, datetime, UTC
from uuid import UUID

from jose import jwt, JWTError

from app.exceptions.auth import NotAuthorizedError

Algorithm = Literal[
    "HS256",
    "HS384",
    "HS512",
    "RS256",
    "RS384",
    "RS512",
    "ES256",
    "ES384",
    "ES512",
]


class TokenProcessor:
    def __init__(self, key: str, algorythm: Algorithm) -> None:
        self.key = key
        self.algorythm = algorythm

    def create_token(
        self,
        data: Any,
        expires_in: timedelta,
    ) -> str:
        now = datetime.now(UTC)
        exp = now + expires_in
        payload = dict(exp=exp, sub=json.dumps(data))

        token = jwt.encode(
            payload,
            key=self.key,
            algorithm=self.algorythm,
        )

        return token

    def validate_token(
        self,
        token: str,
    ) -> MutableMapping[str, Any]:
        try:
            payload = jwt.decode(token, key=self.key, algorithms=self.algorythm)

            return json.loads(payload['sub'])
        except JWTError:
            raise NotAuthorizedError('Not Authorized')
        except KeyError:
            raise NotAuthorizedError('Not Authorized')


class TokenIdProvider:
    def __init__(self, token: str, token_processor: TokenProcessor) -> None:
        self.token = token
        self.token_processor = token_processor

    def get_user_id(self) -> UUID:
        data = self.token_processor.validate_token(self.token)

        return UUID(data['user_id'])
