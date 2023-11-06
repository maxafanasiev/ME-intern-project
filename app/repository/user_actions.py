from typing import Optional, List, Dict

from sqlalchemy import select

from app.db.db_connect import get_db
from app.db.models import User as UserModel, UsersCompaniesActions as Action, Notification
from app.services.action_services import actions
from app.services.exceptions import ActionPermissionException, NotMemberException, EmptyResponseException


class UserActionsRepository:
    async def create_join_request(self, company_id: int, current_user: UserModel) -> Action:
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            await actions.validate_action_exist(current_user.id, company_id, session)

            data_dict = {"action": "request_join", "company_id": company_id, "user_id": current_user.id}
            return await actions.add_action(data_dict, session)

    async def reject_join_request(self, join_request_id: int, current_user: UserModel) -> Optional[Action]:
        async for session in get_db():
            return await actions.decline_action(join_request_id, current_user, session)

    async def get_all_user_join_requests(self, current_user: UserModel, page: int, size: int) -> Optional[List[Action]]:
        async for session in get_db():
            res = await actions.get_all_action_to_user("request_join", current_user, page, size, session)
            return {"user_join_request": res}

    async def get_all_user_invitations(self, current_user: UserModel, page: int, size: int) -> Optional[List[Action]]:
        async for session in get_db():
            res = await actions.get_all_action_to_user("request_invitation", current_user, page, size, session)
            return {"user_invitation": res}

    async def accept_invitation(self, invitation_id: int, current_user: UserModel) -> Optional[Action]:
        async for session in get_db():
            return await actions.accept_action(invitation_id, current_user, session)

    async def reject_invitation(self, invitation_id: int, current_user: UserModel) -> Optional[Action]:
        async for session in get_db():
            return await actions.decline_action(invitation_id, current_user, session)

    async def leave_from_company(self, company_id: int, current_user: UserModel) -> Optional[UserModel]:
        async for session in get_db():
            await actions.check_company_is_exist(company_id, session)
            if await actions.validate_user_is_member(current_user.id, company_id, session):
                await actions.remove_member_from_company(current_user.id, company_id, session)
                await session.commit()
                return current_user
            raise NotMemberException

    async def get_all_notifications(self, current_user: UserModel) -> Dict:
        async for session in get_db():
            query = select(Notification).where(Notification.user_id == current_user.id)
            notifications = await session.execute(query)
            return {"notifications": notifications.scalars().all()}

    async def read_notification(self, notification_id: int, current_user: UserModel) -> Optional[Notification]:
        async for session in get_db():
            notification = await session.get(Notification, notification_id)
            if not notification:
                raise EmptyResponseException
            if not notification.user_id == current_user.id:
                raise ActionPermissionException
            notification.status = "read"
            await session.commit()
            return notification




