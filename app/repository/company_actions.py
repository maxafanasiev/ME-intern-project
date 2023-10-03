from fastapi import HTTPException, status

from app.db.db_connect import get_db
from app.services.action_services import actions
from app.services.exceptions import AlreadyMemberException, NotMemberException


class CompanyActionsRepository:

    async def create_invitation(self, company_id, user_id, current_user):
        async for session in get_db():
            await actions.check_user_is_exist(user_id, session)
            await actions.validate_action_exist(current_user.id, company_id, session)
            data_dict = {"action": "request_invitation", "company_id": company_id, "user_id": user_id}
            return await actions.add_action(data_dict, session)

    async def reject_invitation(self, invitation_id, current_user):
        async for session in get_db():
            action = await actions.get_action(invitation_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            await actions.decline_action(invitation_id, session)
            return action

    async def get_all_company_join_requests(self, company_id, current_user, page, size):
        async for session in get_db():
            res = await actions.get_all_action_to_company("request_join", company_id, current_user, page, size, session)
            return {"company_join_request": res}

    async def get_all_company_invitations(self, company_id, current_user, page, size):
        async for session in get_db():
            res = await actions.get_all_action_to_company("request_invitation", company_id, current_user, page, size,
                                                          session)
            return {"company_invitation": res}

    async def accept_join_request(self, join_request_id, current_user):
        async for session in get_db():
            action = await actions.get_action(join_request_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            if not await actions.validate_user_is_member(action.user_id, action.company_id, session):
                return await actions.accept_action(join_request_id, session)
            raise AlreadyMemberException

    async def reject_join_request(self, join_request_id, current_user):
        async for session in get_db():
            action = await actions.get_action(join_request_id, session)
            await actions.validate_company_owner(action.company_id, current_user.id, session)
            await actions.decline_action(join_request_id, session)
            return action

    async def remove_user_from_company(self, user_id, company_id, current_user):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            user = await actions.check_user_is_exist(user_id, session)
            await actions.validate_company_owner(company_id, current_user.id, session)
            if await actions.validate_user_is_member(user_id, company_id, session):
                await actions.remove_member_from_company(user_id, company_id, session)
                await session.commit()
                return user
            raise NotMemberException

    async def set_admin_from_member(self, user_id, company_id, current_user):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            await actions.validate_company_owner(company_id, current_user.id, session)
            user = await UsersRepository().get_one(user_id)
            if (await actions.validate_user_is_member(user_id, company_id, session)
                    and not await actions.validate_user_is_admin(user_id, company_id, session)):
                await actions.add_admin_to_company(user_id, company_id, session)
                await session.commit()
                return user
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not a member of company")

    async def remove_admin_from_company(self, user_id, company_id, current_user):
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            await actions.validate_company_owner(company_id, current_user.id, session)
            user = await UsersRepository().get_one(user_id)
            if await actions.validate_user_is_admin(user_id, company_id, session):
                await actions.remove_admin_from_company(user_id, company_id, session)
                return user
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not a admin of company")
        