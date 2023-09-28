from app.utils.repository import AbstractRepository
from app.schemas.company_schemas import CompanyListResponse, CompanyDetailResponse, CompanyUpdateRequestModel, \
    CreateCompanyRequestModel
from app.db.models import User as UserModel


class CompanyService:
    def __init__(self, company_repo: AbstractRepository):
        self.user_repo: AbstractRepository = company_repo()

    async def create_company(self, company: CreateCompanyRequestModel,
                             current_user: UserModel) -> CompanyDetailResponse:
        return await self.user_repo.add_one(company, current_user)

    async def get_company_by_id(self, company_id: int) -> CompanyDetailResponse:
        return await self.user_repo.get_one(company_id)

    async def get_all_companies(self, page: int, size: int) -> CompanyListResponse:
        return await self.user_repo.get_all(page, size)

    async def update_company(self, company_id: int, company: CompanyUpdateRequestModel,
                             current_user: UserModel) -> CompanyDetailResponse:
        return await self.user_repo.update_one(company_id, company, current_user)

    async def delete_company(self, company_id: int, current_user: UserModel) -> CompanyDetailResponse:
        return await self.user_repo.delete_one(company_id, current_user)
