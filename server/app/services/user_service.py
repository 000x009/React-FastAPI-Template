from app.data.dao.user import UserDAO
from app.dto.user import UserDTO, GetUserDTO, CreateUserDTO


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    async def get_user(self, data: GetUserDTO) -> UserDTO:
        return await self.dao.get_user_by_id(user_id=data.id)

    async def create_user(self, data: CreateUserDTO) -> UserDTO:
        return await self.dao.create_user(data)
