from app.repository.analytics import AnalyticsRepository
from app.repository.auth import AuthRepository
from app.repository.companies import CompanyRepository
from app.repository.export_data import ExportDataRepository
from app.repository.questions import QuestionRepository
from app.repository.quizzes import QuizRepository
from app.repository.score import ScoreRepository
from app.repository.users import UsersRepository
from app.services.analytics import AnalyticsService
from app.services.companies import CompanyService
from app.services.company_actions import CompanyActionsService
from app.services.export_data import ExportDataService
from app.services.questions import QuestionService
from app.services.quizzes import QuizService
from app.services.scores import ScoreService
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


def quiz_service():
    return QuizService(QuizRepository)


def question_service():
    return QuestionService(QuestionRepository)


def score_service():
    return ScoreService(ScoreRepository)


def export_service():
    return ExportDataService(ExportDataRepository)


def analytics_service():
    return AnalyticsService(AnalyticsRepository)
