from datetime import datetime
from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import insert, select, and_, Table

from app.core.logger import logger
from app.db.db_connect import get_db
from app.db.models import Company, members_association_table, User, admins_association_table
from app.schemas.company_schemas import CompanyMembersResponse, CompanyAdminsResponse, CompanyUpdateRequestModel, \
    CreateCompanyRequestModel
from app.utils.repository import SQLAlchemyRepository


class CompanyRepository(SQLAlchemyRepository):
    model = Company

    async def add_one(self, data: CreateCompanyRequestModel, current_user: User) -> Company:
        async for session in get_db():
            data_dict = dict(data)
            query = insert(self.model).values(**data_dict).returning(self.model)
            res = await session.execute(query)
            db_company = res.scalar_one()
            db_company.owner_id = current_user.id
            await session.commit()
            return db_company

    async def update_one(self,
                         company_id: int,
                         data: CompanyUpdateRequestModel,
                         current_user: User
                         ) -> Optional[Company]:
        async for session in get_db():
            query = select(Company).where(and_(Company.id == company_id, Company.owner_id == current_user.id))
            result = await session.execute(query)
            db_company = result.scalar_one_or_none()
            if db_company is None:
                logger.error(f"Error updating company")
                raise HTTPException(status_code=404, detail="Company not found")
            for field, value in data.model_dump().items():
                if value is not None:
                    setattr(db_company, field, value)
            db_company.updated_at = datetime.now()
            await session.commit()
            await session.refresh(db_company)
            return db_company

    async def delete_one(self, company_id: int, current_user: User) -> Optional[Company]:
        async for session in get_db():
            query = select(Company).where(and_(Company.id == company_id, Company.owner_id == current_user.id))
            result = await session.execute(query)
            db_company = result.scalar_one_or_none()
            if db_company is None:
                logger.error(f"Error deleting company")
                raise HTTPException(status_code=404, detail="Company not found")
            await session.delete(db_company)
            await session.commit()
            return db_company

    async def _get_company_users(self, company_id: int, association_table: Table, page: int, size: int) -> List[User]:
        async for session in get_db():
            offset = (page - 1) * size
            query = (
                select(User)
                .join(association_table, User.id == association_table.c.user_id)
                .where(association_table.c.company_id == company_id)
                .offset(offset)
                .limit(size)
            )
            res = await session.execute(query)
            return res.scalars().all()

    async def get_company_members(self, company_id: int, page: int, size: int) -> CompanyMembersResponse:
        return {"company_members": await self._get_company_users(company_id, members_association_table, page, size)}

    async def get_company_admins(self, company_id: int, page: int, size: int) -> CompanyAdminsResponse:
        return {"company_admins": await self._get_company_users(company_id, admins_association_table, page, size)}



