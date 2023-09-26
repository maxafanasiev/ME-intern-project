from fastapi import Depends

from app.services.app_services import app_service
from app.utils.repository import AbstractRepository
from app.schemas.user_schemas import SignUpRequestModel, UserUpdateRequestModel, User, UsersListResponse, \
    UserDetailResponse


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()

    async def create_user(self, user: SignUpRequestModel) -> User:
        new_user = await self.user_repo.add_one(user)
        return new_user

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repo.get_one(user_id)
        return user

    async def get_all_users(self, page: int, size: int) -> UsersListResponse:
        users = await self.user_repo.get_all(page, size)
        return users

    async def update_user(self, user_id: int, user: UserUpdateRequestModel,
                          current_user: User) -> UserDetailResponse:
        updated_user = await self.user_repo.update_one(user_id, user, current_user)
        return updated_user

    async def delete_user(self, user_id: int, current_user: User) -> User:
        user = await self.user_repo.delete_one(user_id, current_user)
        return user
