from app.utils.repository import AbstractRepository
from app.schemas.user_schemas import SignUpRequestModel, UserUpdateRequestModel, User, UsersListResponse, \
    UserDetailResponse
from app.db.models import User as UserModel


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo: AbstractRepository = user_repo()

    async def create_user(self, user: SignUpRequestModel) -> UserDetailResponse:
        return await self.user_repo.add_one(user)

    async def get_user_by_id(self, user_id: int) -> UserDetailResponse:
        return await self.user_repo.get_one(user_id)

    async def get_all_users(self, page: int, size: int) -> UsersListResponse:
        return await self.user_repo.get_all(page, size)

    async def update_user(self, user: UserUpdateRequestModel,
                          current_user: UserModel) -> UserDetailResponse:
        return await self.user_repo.update_one(user, current_user)

    async def delete_user(self, current_user: UserModel) -> User:
        return await self.user_repo.delete_one(current_user)
