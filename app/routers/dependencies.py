from app.repository.users import UsersRepository
from app.services.users import UserService


def user_service():
    return UserService(UsersRepository)