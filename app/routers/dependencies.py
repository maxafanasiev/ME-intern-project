from app.repository.auth import AuthRepository
from app.repository.companies import CompanyRepository
from app.repository.users import UsersRepository
from app.services.companies import CompanyService
from app.services.company_actions import CompanyActionsService
from app.services.user_actions import UserActionsService
from app.services.users import UserService
from app.services.auth import AuthService


def user_service():
    return UserService(UsersRepository)


def auth_service():
    return AuthService(AuthRepository)


def company_service():
    return CompanyService(CompanyRepository)


def company_actions_service():
    return CompanyActionsService()


def user_actions_service():
    return UserActionsService()
