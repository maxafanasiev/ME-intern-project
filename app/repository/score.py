from app.db.db_connect import get_db
from app.services.result_services import results


class ScoreRepository:

    async def get_user_score_in_company(self, user_id, company_id):
        async for session in get_db():
            return await results.calculate_user_average_score_in_company(user_id, company_id, session)

    async def get_user_score_global(self, user_id):
        async for session in get_db():
            return await results.calculate_user_average_score_global(user_id, session)
