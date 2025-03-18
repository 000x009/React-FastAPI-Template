from typing import Annotated

from fastapi import Depends, Cookie

from app.services.jwt_token_processor import TokenProcessor, TokenIdProvider
from app.presentation.dependencies.stub import Stub


def id_provider(
    token_processor: Annotated[TokenProcessor, Depends(Stub(TokenProcessor))],
    token: Annotated[str, Cookie()],
) -> TokenIdProvider:
    return TokenIdProvider(token, token_processor)
