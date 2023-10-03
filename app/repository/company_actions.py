from sqlalchemy import insert, select, and_

from app.db.db_connect import get_db
from app.db.models import UsersCompaniesActions as Action
from app.repository.users import UsersRepository
from app.services.action_services import actions


class CompanyActionsRepository:

    async def create_invitation(self, company_id, user_id, current_user):
        async for session in get_db():
            await actions.check_user_is_exist(user_id, session)
            await actions.validate_action_exist(current_user.id, company_id, session)

            data_dict = {"action": "request_invitation", "company_id": company_id, "user_id": user_id}
            query = insert(Action).values(**data_dict).returning(Action)
            res = await session.execute(query)
            await session.commit()
            return res.scalar_one()

    async def reject_invitation(self, invitation_id, current_user):
        async for session in get_db():
            action = await actions.get_action(invitation_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            await actions.validate_action_from_company(action.company_id, invitation_id, session)
            await actions.decline_action(invitation_id, session)
            return action

    async def get_all_action_to_company(self, action, company_id, current_user, page, size):
        async for session in get_db():
            await actions.validate_company_owner(company_id, current_user.id, session)
            offset = (page - 1) * size
            query = select(Action).where(
                and_(Action.company_id == company_id, Action.action == action)).offset(
                offset).limit(size)
            res = await session.execute(query)
            return res.scalars().all()

    async def get_all_company_join_requests(self, company_id, current_user, page, size):
        res = await self.get_all_action_to_company("request_join", company_id, current_user, page, size)
        return {"company_join_request": res}

    async def get_all_company_invitations(self, company_id, current_user, page, size):
        res = await self.get_all_action_to_company("request_invitation", company_id, current_user, page, size)
        return {"company_invitation": res}

    async def accept_join_request(self, join_request_id, current_user):
        async for session in get_db():
            action = await actions.get_action(join_request_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            await actions.validate_action_from_company(action.company_id, join_request_id, session)
            await actions.accept_action(join_request_id, session)
            return action

    async def reject_join_request(self, join_request_id, current_user):
        async for session in get_db():
            action = await actions.get_action(join_request_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            await actions.validate_action_from_company(action.company_id, join_request_id, session)
            await actions.decline_action(join_request_id, session)
            return action

    async def remove_user_from_company(self, user_id, company_id, current_user):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            await actions.validate_company_owner(company_id, current_user.id, session)
            await actions.check_user_is_exist(user_id, session)
            user = await UsersRepository().get_one(user_id)
            if await actions.validate_user_is_member(user_id, company_id, session):
                await actions.remove_member_from_company(user_id, company_id, session)
                await session.commit()
                return user

