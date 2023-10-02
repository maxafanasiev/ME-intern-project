from sqlalchemy import insert, select, and_

from app.db.db_connect import get_db
from app.db.models import UsersCompaniesActions as Action, User as UserModel
from app.services.action_services import actions


class UserActionsRepository:
    async def create_join_request(self, company_id, current_user: UserModel):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            await actions.validate_action_exist(current_user.id, company_id, session)

            data_dict = {"action": "request_join", "company_id": company_id, "user_id": current_user.id}
            query = insert(Action).values(**data_dict).returning(Action)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def reject_join_request(self, join_request_id, current_user: UserModel):
        async for session in get_db():
            action = await actions.get_action(join_request_id, session)
            await actions.validate_action(current_user.id, action.company_id, session)
            action = await actions.decline_action(join_request_id, session)
            return action

    async def get_all_action_to_user(self, action, current_user: UserModel, page, size):
        async for session in get_db():
            offset = (page - 1) * size
            query = select(Action).where(
                and_(Action.user_id == current_user.id, Action.action == action)).offset(
                offset).limit(size)
            res = await session.execute(query)
            return res.scalars().all()

    async def get_all_user_join_requests(self, current_user: UserModel, page, size):
        res = await self.get_all_action_to_user("request_join", current_user, page, size)
        return {"user_join_request": res}

    async def get_all_user_invitations(self, current_user: UserModel, page, size):
        res = await self.get_all_action_to_user("request_invitation", current_user, page, size)
        return {"user_invitation": res}

    async def accept_invitation(self, invitation_id, current_user: UserModel):
        async for session in get_db():
            await actions.validate_action_from_user(current_user.id, invitation_id, session)
            action = await actions.get_action(invitation_id, session)
            await actions.accept_action(invitation_id, session)
            return action

    async def reject_invitation(self, invitation_id, current_user: UserModel):
        async for session in get_db():
            await actions.validate_action_from_user(current_user.id, invitation_id, session)
            action = await actions.get_action(invitation_id, session)
            await actions.validate_action(current_user.id, action.company_id, session)
            await actions.decline_action(invitation_id, session)
            return action

    async def leave_from_company(self, company_id, current_user: UserModel):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            if await actions.validate_user_is_member(current_user.id, company_id, session):
                await actions.remove_member_from_company(current_user.id, company_id, session)
                await session.commit()
                return current_user



