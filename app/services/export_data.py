from fastapi.responses import JSONResponse, FileResponse

from app.db.models import User
from app.repository.export_data import ExportDataRepository
from app.utils.Enum import FileExtension


class ExportDataService:
    def __init__(self, export_repo: ExportDataRepository = ExportDataRepository):
        self.export_repo = export_repo()

    async def export_self_user_results_to_json(self, current_user: User) -> JSONResponse:
        return await self.export_repo.export_self_user_result(FileExtension.JSON.value, current_user)

    async def export_self_user_results_to_csv(self, current_user: User) -> FileResponse:
        return await self.export_repo.export_self_user_result(FileExtension.CSV.value, current_user)

    async def export_user_result_in_company_json(self, user_id: int, company_id: int,
                                                 current_user: User) -> JSONResponse:
        return await self.export_repo.export_user_result_in_company(user_id, company_id, FileExtension.JSON.value,
                                                                    current_user)

    async def export_user_result_in_company_csv(self, user_id: int, company_id: int,
                                                current_user: User) -> FileResponse:
        return await self.export_repo.export_user_result_in_company(user_id, company_id, FileExtension.CSV.value,
                                                                    current_user)

    async def export_all_users_result_in_company_json(self, company_id: int, current_user: User) -> JSONResponse:
        return await self.export_repo.export_all_users_result_in_company(company_id, FileExtension.JSON.value,
                                                                         current_user)

    async def export_all_users_result_in_company_csv(self, company_id: int, current_user: User) -> FileResponse:
        return await self.export_repo.export_all_users_result_in_company(company_id, FileExtension.CSV.value,
                                                                         current_user)

    async def export_users_in_quiz_json(self, quiz_id: int, current_user: User) -> JSONResponse:
        return await self.export_repo.export_users_in_quiz(quiz_id, FileExtension.JSON.value, current_user)

    async def export_users_in_quiz_csv(self, quiz_id: int, current_user: User) -> FileResponse:
        return await self.export_repo.export_users_in_quiz(quiz_id, FileExtension.CSV.value, current_user)
