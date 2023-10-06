import csv
import json

from fastapi.responses import FileResponse, JSONResponse

from app.db.db_connect import get_db
from app.db.models import User
from app.db.redis_utils import redis_db
from app.repository.quizzes import QuizRepository
from app.services.action_services import actions
from app.services.exceptions import ActionPermissionException, EmptyResponseException


class ExportDataRepository:
    async def __export_results(self, extension: str, results):
        if extension == "json":
            return await self.__export_results_to_json(results)
        if extension == "csv":
            return await self.__export_results_to_csv(results)
        raise ValueError("Invalid extension")

    async def __export_results_to_json(self, results):
        return JSONResponse(results)

    async def __export_results_to_csv(self, results):
        csv_filename = 'export/results.csv'

        with open(csv_filename, mode='w', newline='') as csv_file:
            try:
                fieldnames = results[0].keys()
            except IndexError:
                raise EmptyResponseException
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for row in results:
                writer.writerow(row)

        return FileResponse(csv_filename,
                            headers={"Content-Disposition": f"attachment; filename={csv_filename}"})

    async def __get_user_results_from_redis(self, search_key: str):
        redis = await redis_db.create_redis_connection()

        matching_keys = await redis.keys(search_key)

        user_results = []
        for key in matching_keys:
            data = await redis_db.get_data(redis, key)
            if data:
                user_results.append(json.loads(data))

        return user_results

    async def export_user_result_in_company(self, user_id: int, company_id: int, extension: str, current_user: User):
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                search_key = f'*user_{user_id}*company_{company_id}*'
                results = await self.__get_user_results_from_redis(search_key)
                return await self.__export_results(extension, results)
            raise ActionPermissionException

    async def export_all_users_result_in_company(self, company_id: int, extension: str, current_user: User):
        async for session in get_db():
            if (await actions.validate_user_is_owner(current_user.id, company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, company_id, session)):
                search_key = f'*:company_{company_id}:*'
                results = await self.__get_user_results_from_redis(search_key)
                return await self.__export_results(extension, results)
            raise ActionPermissionException

    async def export_users_in_quiz(self, quiz_id: int, extension: str, current_user: User):
        async for session in get_db():
            quiz = await QuizRepository().get_one(quiz_id)
            if (await actions.validate_user_is_owner(current_user.id, quiz.quiz_company_id, session)
                    or await actions.validate_user_is_admin(current_user.id, quiz.quiz_company_id, session)):
                search_key = f'*quiz_{quiz_id}*'
                results = await self.__get_user_results_from_redis(search_key)
                return await self.__export_results(extension, results)
            raise ActionPermissionException

    async def export_self_user_result(self, extension: str, current_user: User):
        search_key = f'*:user_{current_user.id}:*'
        results = await self.__get_user_results_from_redis(search_key)
        return await self.__export_results(extension, results)


