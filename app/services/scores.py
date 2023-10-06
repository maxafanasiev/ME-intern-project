from app.repository.score import ScoreRepository
from app.schemas.quiz_workflow_schemas import RatingGlobal, RatingInCompany


class ScoreService:
    def __init__(self, score_repo: ScoreRepository):
        self.score_repo: ScoreRepository = score_repo()

    async def get_user_score_in_company(self, user_id: int, company_id: int) -> RatingInCompany:
        return await self.score_repo.get_user_score_in_company(user_id, company_id)

    async def get_user_score_global(self, user_id: int) -> RatingGlobal:
        return await self.score_repo.get_user_score_global(user_id)
