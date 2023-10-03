from app.repository.user_actions import UserActionsRepository
from app.db.models import User as UserModel
from app.schemas.action_schemas import ActionDetailResponse, UserInvitationListResponse, \
    UserJoinRequestListResponse
from app.schemas.user_schemas import UserDetailResponse


class UserActionsService:
    def __init__(self, user_actions_repo=UserActionsRepository):
        self.user_actions_repo = user_actions_repo()

    async def create_join_request(self, company_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.user_actions_repo.create_join_request(company_id, current_user)

    async def reject_join_request(self, join_request_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.user_actions_repo.reject_join_request(join_request_id, current_user)

    async def get_all_invitations_to_user(self,
                                          current_user: UserModel,
                                          page: int,
                                          size: int) -> UserInvitationListResponse:
        return await self.user_actions_repo.get_all_user_invitations(current_user, page, size)

    async def get_all_user_join_requests(self,
                                         current_user: UserModel,
                                         page: int,
                                         size: int) -> UserJoinRequestListResponse:
        return await self.user_actions_repo.get_all_user_join_requests(current_user, page, size)

    async def accept_invitation(self, invitation_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.user_actions_repo.accept_invitation(invitation_id, current_user)

    async def reject_invitation(self, invitation_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.user_actions_repo.reject_invitation(invitation_id, current_user)

    async def leave_from_company(self, company_id, current_user: UserModel) -> UserDetailResponse:
        return await self.user_actions_repo.leave_from_company(company_id, current_user)
