from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.user import UserDTO, CreateUserDTO
from app.data.models import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: UUID) -> UserDTO | None:
        query = (
            select(UserModel)
            .where(UserModel.id == user_id)
        )
        result = await self.session.execute(query)
        user_model = result.unique().scalar_one_or_none()

        if not user_model:
            return None

        return UserDTO(
            id=user_model.id,
            full_name=user_model.full_name,
            email=user_model.email,
            joined_at=user_model.joined_at,
        )

    async def create_user(self, data: CreateUserDTO) -> UserDTO:
        user_model = UserModel(
            id=data.id,
            full_name=data.full_name,
            joined_at=data.joined_at,
            email=data.email,
        )

        self.session.add(user_model)
        await self.session.commit()

        return UserDTO(
            id=user_model.id,
            full_name=user_model.full_name,
            email=user_model.email,
            joined_at=user_model.joined_at,
        )
