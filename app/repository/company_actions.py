from fastapi import HTTPException
from sqlalchemy import insert, select, and_

from app.core.logger import logger
from app.db.db_connect import get_db
from app.db.models import UsersCompaniesActions as Action, Company
from app.repository.users import UsersRepository
from app.services.action_services import actions
from app.services.exceptions import ActionPermissionException, AlreadyMemberException
from app.services.users import UserService


class CompanyActionsRepository:
    async def create_invitation(self, company_id, user_id, current_user):
        async for session in get_db():
            if not await actions.has_permission(company_id, current_user, session):
                raise ActionPermissionException
            if await actions.is_user_member_of_company(current_user.id, company_id, session):
                raise AlreadyMemberException
            existing_request = await actions.get_existing_request(company_id, user_id, 'request_invitation', session)
            if existing_request:
                raise HTTPException(status_code=400, detail="Invitation request already exists")

            data_dict = {"action": "request_invitation", "company_id": company_id, "user_id": user_id}
            query = insert(Action).values(**data_dict).returning(Action)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def reject_invitation(self, invitation_id, current_user):
        async for session in get_db():
            db_invite = await self.get_invitation(invitation_id)
            if not await actions.has_permission(db_invite.company_id, current_user, session):
                raise ActionPermissionException

            await session.delete(db_invite)
            await session.commit()
            return db_invite

    async def get_all_invitations(self, company_id, current_user, page, size):
        async for session in get_db():
            if not await actions.has_permission(company_id, current_user, session):
                raise ActionPermissionException

            offset = (page - 1) * size
            query = select(Action).where(
                and_(Action.company_id == company_id, Action.action == "request_invitation")).offset(offset).limit(size)
            res = await session.execute(query)
            name = "company_invitation"
            return {name: res.scalars().all()}

    async def get_all_join_requests(self, company_id, current_user, page, size):
        async for session in get_db():
            if not await actions.has_permission(company_id, current_user, session):
                raise ActionPermissionException

            offset = (page - 1) * size
            query = select(Action).where(and_(Action.company_id == company_id, Action.action == "request_join")).offset(
                offset).limit(size)
            res = await session.execute(query)
            name = "company_join_request"
            return {name: res.scalars().all()}

    async def accept_join_request(self, join_request_id, current_user):
        async for session in get_db():
            db_join = await self.get_join_request(join_request_id)
            if not await actions.has_permission(db_join.company_id, current_user, session):
                raise ActionPermissionException

            await session.delete(db_join)
            await actions.add_member_to_company(db_join.user_id, db_join.company_id, session)
            await session.commit()
            return db_join

    async def reject_join_request(self, join_request_id, current_user):
        async for session in get_db():
            db_join = await self.get_join_request(join_request_id)
            if not await actions.has_permission(db_join.company_id, current_user, session):
                raise ActionPermissionException

            await session.delete(db_join)
            await session.commit()
            return db_join

    async def remove_user_from_company(self, user_id, company_id, current_user):
        async for session in get_db():
            db_company = await actions.get_company(company_id, session)
            db_user = await UserService(UsersRepository).get_user_by_id(user_id)
            if not await actions.has_permission(company_id, current_user, session):
                raise ActionPermissionException

            await actions.remove_member_from_company(user_id, company_id, session)
            await session.commit()
            return db_user

    async def get_invitation(self, invitation_id):
        async for session in get_db():
            query = select(Action).where(Action.id == invitation_id)
            result = await session.execute(query)
            db_invite = result.scalar_one_or_none()
            if db_invite is None:
                logger.error("Error reject invitation")
                raise HTTPException(status_code=404, detail="Invitation not found")
            return db_invite

    async def get_join_request(self, join_request_id):
        async for session in get_db():
            query = select(Action).where(Action.id == join_request_id)
            result = await session.execute(query)
            db_join = result.scalar_one_or_none()
            if db_join is None:
                logger.error("Error accept join request")
                raise HTTPException(status_code=404, detail="Join request not found")
            return db_join

