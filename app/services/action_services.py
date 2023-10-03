from fastapi import HTTPException, status
from sqlalchemy import select, insert, and_, delete

from app.db.models import Company, User, members_association_table as Member, UsersCompaniesActions as Action, \
    admins_association_table as Admin
from app.services.exceptions import ActionPermissionException, AlreadyMemberException


class ActionService:

    async def get_action(self, action_id, session):
        query = select(Action).where(Action.id == action_id)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    async def validate_action(self, user_id, company_id, session):
        query = select(Action).where(
            and_(Action.user_id == user_id, Action.company_id == company_id))
        action = await session.execute(query)
        if not action.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Action not found")

    async def validate_action_exist(self, user_id, company_id, session):
        query = select(Action).where(
            and_(Action.user_id == user_id, Action.company_id == company_id))
        action = await session.execute(query)
        if action.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Action already sent")

    async def validate_action_from_company(self, company_id, action_id: int, session):
        query = select(Action).where(and_(Action.company_id == company_id, Action.id == action_id))
        res = await session.execute(query)
        company = res.scalar_one_or_none()
        if not company:
            raise HTTPException(status_code=404, detail="Not valid action")

    async def validate_action_from_user(self, user_id, action_id, session):
        action = await self.get_action(action_id, session)
        query = select().where(
            and_(
                Member.c.user_id == user_id,
                Member.c.company_id == action.company_id
            )
        )
        member = await session.execute(query)
        if member.scalar_one_or_none():
            raise AlreadyMemberException

    async def check_company_is_exist(self, company_id, session):
        query = select(Company).where(Company.id == company_id)
        company = await session.execute(query)
        if not company.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Company not found")

    async def check_user_is_exist(self, user_id, session):
        query = select(User).where(User.id == user_id)
        user = await session.execute(query)
        if not user.scalar_one_or_none():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    async def validate_company_owner(self, company_id: int, user_id: int, session):
        query = select(Company).where(and_(Company.id == company_id, Company.owner_id == user_id))
        company = await session.execute(query)
        if not company.scalar_one_or_none():
            raise ActionPermissionException

    async def get_company_users_by_group(self, group, company_id, session):
        query = (
            select(User.id)
            .join(group, User.id == group.c.user_id)
            .where(group.c.company_id == company_id)
        )
        res = await session.execute(query)
        users = res.scalars().all()
        return users

    async def get_company_members(self, company_id, session):
        return await self.get_company_users_by_group(Member, company_id, session)

    async def get_company_admins(self, company_id, session):
        return await self.get_company_users_by_group(Admin, company_id, session)

    async def validate_user_is_member(self, user_id, company_id, session):
        if user_id in await self.get_company_members(company_id, session):
            return True
        return False

    async def validate_user_is_admin(self, user_id, company_id, session):
        if user_id in await self.get_company_admins(company_id, session):
            return True
        return False

    async def add_user_to_company(self, group, user_id, company_id, session):
        query = insert(group).values(user_id=user_id, company_id=company_id).returning(
            group)
        db_member = await session.execute(query)
        session.commit()
        res = db_member.scalar_one_or_none()
        return res

    async def add_member_to_company(self, user_id, company_id, session):
        return await self.add_user_to_company(Member, user_id, company_id, session)

    async def add_admin_to_company(self, user_id, company_id, session):
        return await self.add_user_to_company(Admin, user_id, company_id, session)

    async def accept_action(self, action_id, session):
        action = await actions.get_action(action_id, session)
        await self.add_member_to_company(action.user_id, action.company_id, session)
        await session.delete(action)
        await session.commit()
        return action

    async def decline_action(self, action_id, session):
        action = await actions.get_action(action_id, session)
        await session.delete(action)
        await session.commit()
        return action

    async def remove_user_from_company(self, table, user_id, company_id, session):
        query = delete(table).where(
            and_(
                table.c.company_id == company_id,
                table.c.user_id == user_id
            )
        )
        await session.execute(query)
        await session.commit()

    async def remove_member_from_company(self, user_id, company_id, session):
        return await self.remove_user_from_company(Member, user_id, company_id, session)

    async def remove_admin_from_company(self, user_id, company_id, session):
        return await self.remove_user_from_company(Admin, user_id, company_id, session)


actions = ActionService()
