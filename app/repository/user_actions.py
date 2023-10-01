from fastapi import HTTPException
from sqlalchemy import insert, select, and_

from app.core.logger import logger
from app.db.db_connect import get_db
from app.db.models import UsersCompaniesActions as Action, User as UserModel
from app.services.action_services import actions
from app.services.companies import CompanyService
from app.services.exceptions import ActionPermissionException, AlreadyMemberException


class UserActionsRepository:
    async def create_join_request(self, company_id, current_user: UserModel):
        async for session in get_db():
            if await actions.is_user_member_of_company(current_user.id, company_id, session):
                raise AlreadyMemberException
            if not await actions.has_permission(company_id, current_user, session):
                raise ActionPermissionException

            existing_request = await actions.get_existing_request(company_id, current_user.id, "request_join", session)
            if existing_request:
                raise HTTPException(status_code=400, detail="Invitation request already exists")

            data_dict = {"action": "request_join", "company_id": company_id, "user_id": current_user.id}
            query = insert(Action).values(**data_dict).returning(Action)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def reject_join_request(self, join_request_id, current_user: UserModel):
        async for session in get_db():
            query = select(Action).where(Action.id == join_request_id)
            result = await session.execute(query)
            db_join = result.scalar_one_or_none()
            if db_join is None:
                logger.error("Error join request")
                raise HTTPException(status_code=404, detail="Join request not found")
            if current_user.id == db_join.user_id:
                await session.delete(db_join)
                await session.commit()
                return db_join
            else:
                logger.error(
                    f"Error reject join request: User {current_user.id} is not the sender "
                    f"of the join request {db_join.id}")
                raise ActionPermissionException

    async def get_all_invitations_to_user(self, current_user: UserModel, page, size):
        async for session in get_db():
            offset = (page - 1) * size
            query = select(Action).where(
                and_(Action.user_id == current_user.id, Action.action == "request_invitation")).offset(
                offset).limit(size)
            res = await session.execute(query)
            name = "user_invitation"
            return {name: res.scalars().all()}

    async def get_all_user_join_requests(self, current_user: UserModel, page, size):
        async for session in get_db():
            offset = (page - 1) * size
            query = select(Action).where(
                and_(Action.user_id == current_user.id, Action.action == "request_join")).offset(offset).limit(size)
            res = await session.execute(query)
            name = "user_join_request"
            return {name: res.scalars().all()}

    async def accept_invitation(self, invitation_id, current_user: UserModel):
        async for session in get_db():
            query = select(Action).where(Action.id == invitation_id)
            result = await session.execute(query)
            db_invite = result.scalar_one_or_none()
            if db_invite is None:
                logger.error("Error invitation request")
                raise HTTPException(status_code=404, detail="Join request not found")
            if current_user.id == db_invite.user_id:
                await session.delete(db_invite)
                await actions.add_member_to_company(db_invite.user_id, db_invite.company_id, session)
                await session.commit()
                return db_invite
            else:
                logger.error(
                    f"Error accept join request: User {current_user.id} is not the receiver "
                    f"of the invitation {db_invite.id}")
                raise ActionPermissionException

    async def reject_invitation(self, invitation_id, current_user: UserModel):
        async for session in get_db():
            query = select(Action).where(Action.id == invitation_id)
            result = await session.execute(query)
            db_invite = result.scalar_one_or_none()
            if db_invite is None:
                logger.error("Error reject invitation")
                raise HTTPException(status_code=404, detail="Invitation not found")
            if not await actions.has_permission(db_invite.company_id, current_user, session):
                logger.error(
                    f"Error accept join request: User {current_user.id} is not the receiver "
                    f"of the invitation {db_invite.id}")
                raise ActionPermissionException
            await session.delete(db_invite)
            await session.commit()
            return db_invite

    async def leave_from_company(self, company_id, current_user: UserModel):
        async for session in get_db():
            await CompanyService().get_company_by_id(company_id)
            company_members_id = await actions.get_company_members(company_id, session)
            if current_user.id in company_members_id:
                await actions.remove_member_from_company(current_user.id, company_id, session)
                await session.commit()
                return current_user
            else:
                logger.error(
                    f"Error leave company: User {current_user.id} is not the member "
                    f"of the company {company_id}")
                raise ActionPermissionException



