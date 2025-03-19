from uuid import uuid4
from datetime import datetime, UTC, timedelta
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import JSONResponse, Response

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dto.user import CreateUserDTO, GetUserDTO, UserDTO
from app.presentation.schemas.auth import RegisterSchema
from app.services.jwt_token_processor import TokenProcessor, TokenIdProvider
from app.services.user_service import UserService
from app.presentation.dependencies.stub import Stub
from app.presentation.dependencies.id_provider import id_provider

router = APIRouter(
    prefix='/auth',
    tags=["Auth"],
    route_class=DishkaRoute,
)

@router.post('/register')
async def register(
    data: RegisterSchema,
    user_service: FromDishka[UserService],
    response: Response,
    token_processor: Annotated[TokenProcessor, Depends(Stub(TokenProcessor))],
) -> str:
    user = await user_service.create_user(CreateUserDTO(
        id=uuid4(),
        joined_at=datetime.now(UTC),
        full_name=data.full_name,
        email=data.email,
    ))

    token = token_processor.create_token(data=dict(user_id=str(user.id)), expires_in=timedelta(days=1))
    response.set_cookie('token', token, httponly=True)

    return "ok"
