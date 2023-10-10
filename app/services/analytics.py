from app.db.models import User
from app.repository.analytics import AnalyticsRepository
from app.schemas.analytic_schemas import UserGlobalAnalytics, UserQuizzesScoreAnalytics, ListQuizLastAttemptAnalytics, \
    ListUserResultAnalytics, ListQuizResultAnalytics, ListUserLastCompletionTimeAnalytics


class AnalyticsService:

    def __init__(self, analytic_repo=AnalyticsRepository):
        self.analytic_repo: AnalyticsRepository = analytic_repo()

    async def get_user_analytics(self, user_id: int) -> UserGlobalAnalytics:
        return await self.analytic_repo.get_user_analytics(user_id)

    async def get_user_quizzes_analytics(self, current_user: User) -> UserQuizzesScoreAnalytics:
        return await self.analytic_repo.get_user_quizzes_analytics(current_user)

    async def get_user_quizzes_by_time_passing(self, current_user: User) -> ListQuizLastAttemptAnalytics:
        return await self.analytic_repo.get_latest_quiz_completion_times_for_user(current_user)

    async def get_users_scores_analytics_in_company(self, company_id: int,
                                                    current_user: User) -> ListUserResultAnalytics:
        return await self.analytic_repo.get_users_scores_analytics_in_company(company_id, current_user)

    async def get_user_average_scores_in_company_over_time(self, user_id: int, company_id: int,
                                                           current_user: User) -> ListQuizResultAnalytics:
        return await self.analytic_repo.get_user_average_scores_in_company_over_time(user_id, company_id, current_user)

    async def get_users_last_completion_time_in_company(self, company_id: int,
                                                        current_user: User) -> ListUserLastCompletionTimeAnalytics:
        return await self.analytic_repo.get_users_last_completion_time_in_company(company_id, current_user)
