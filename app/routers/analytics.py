from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.models import User
from app.schemas.analytic_schemas import UserGlobalAnalytics, UserQuizzesScoreAnalytics, ListQuizLastAttemptAnalytics, \
    ListUserResultAnalytics, ListQuizResultAnalytics, ListUserLastCompletionTimeAnalytics
from app.services.auth_services import auth

from app.services.analytics import AnalyticsService
from app.routers.dependencies import analytics_service

router = APIRouter(tags=['analytics'])


@router.get("/user/global-score/{user_id}", response_model=UserGlobalAnalytics)
async def user_global_analytics(
        user_id: int,
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)]):
    return await analytics_service.get_user_analytics(user_id)


@router.get("/user/quizzes-score/self", response_model=UserQuizzesScoreAnalytics)
async def list_of_average_scores_by_quizzes(
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await analytics_service.get_user_quizzes_analytics(current_user)


@router.get("/user/quizzes-time-passing/self", response_model=ListQuizLastAttemptAnalytics)
async def quizzes_list_with_time_of_passing_analytics(
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await analytics_service.get_user_quizzes_by_time_passing(current_user)


@router.get("/admin/all-users-scores/{company_id}", response_model=ListUserResultAnalytics)
async def users_scores_analytics_in_company(
        company_id: int,
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await analytics_service.get_users_scores_analytics_in_company(company_id, current_user)


@router.get("/admin/user-scores-all-quizzes/{company_id}/{user_id}", response_model=ListQuizResultAnalytics)
async def get_user_average_scores_all_quizzes_in_company_over_time(
        user_id: int,
        company_id: int,
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await analytics_service.get_user_average_scores_in_company_over_time(user_id, company_id, current_user)


@router.get("/admin/users-last-completion-time/{company_id}/", response_model=ListUserLastCompletionTimeAnalytics)
async def get_users_last_completion_time_in_company(
        company_id: int,
        analytics_service: Annotated[AnalyticsService, Depends(analytics_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await analytics_service.get_users_last_completion_time_in_company(company_id, current_user)
