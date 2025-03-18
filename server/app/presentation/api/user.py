from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from dishka.integrations.fastapi import FromDishka, DishkaRoute

from app.dto.user import GetUserDTO, UserDTO

from app.services.jwt_token_processor import TokenIdProvider
from app.services.user_service import UserService
from app.presentation.dependencies.id_provider import id_provider

router = APIRouter(
    prefix='/user',
    tags=["User"],
    route_class=DishkaRoute,
)


@router.get('/')
async def get_user(
    user_service: FromDishka[UserService],
    identity_provider: Annotated[TokenIdProvider, Depends(id_provider)],
) -> UserDTO:
    user_id = identity_provider.get_user_id()
    user = await user_service.get_user(GetUserDTO(user_id))

    return user
