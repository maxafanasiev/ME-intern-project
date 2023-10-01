from fastapi import HTTPException
from sqlalchemy import select, insert, and_, delete

from app.core.logger import logger
from app.db.models import Company, User, members_association_table, UsersCompaniesActions as Action


class ActionService:

    async def has_permission(self, company_id, current_user, session):
        company = await self.get_company(company_id, session)
        company_owner_id = company.owner_id
        return current_user.id == company_owner_id

    async def get_company(self, company_id, session):
        query = select(Company).where(Company.id == company_id)
        result = await session.execute(query)
        db_company = result.scalar_one_or_none()
        if db_company is None:
            logger.error(f"Company id:{company_id} not found")
            raise HTTPException(status_code=404, detail="Company not found")
        return db_company

    async def is_user_member_of_company(self, user_id, company_id, session):
        query = select().where(
            and_(
                members_association_table.c.user_id == user_id,
                members_association_table.c.company_id == company_id
            )
        )
        result = await session.execute(query)
        return result.scalar() is not None

    async def get_company_members(self, company_id, session):
        query = (
            select(User.id)
            .join(members_association_table, User.id == members_association_table.c.user_id)
            .where(members_association_table.c.company_id == company_id)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def add_member_to_company(self, user_id, company_id, session):
        data = {"user_id": user_id, "company_id": company_id}
        query = insert(members_association_table).values(**data).returning(members_association_table)
        result = await session.execute(query)
        db_member = result.scalar_one_or_none()
        session.commit()
        return db_member

    async def remove_member_from_company(self, user_id, company_id, session):
        query = delete(members_association_table).where(
            and_(
                members_association_table.c.company_id == company_id,
                members_association_table.c.user_id == user_id
            )
        )
        await session.execute(query)
        await session.commit()

    async def get_existing_request(self, company_id, user_id, action, session):
        query = select(Action).where(
            and_(Action.company_id == company_id, Action.user_id == user_id, Action.action == action)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()


actions = ActionService()
