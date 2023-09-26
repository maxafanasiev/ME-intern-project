from app.repository.auth import AuthRepository
from app.repository.users import UsersRepository
from app.services.users import UserService
from app.services.auth import AuthService


def user_service():
    return UserService(UsersRepository)


def auth_service():
    return AuthService(AuthRepository)
