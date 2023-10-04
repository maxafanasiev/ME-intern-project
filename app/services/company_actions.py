from app.db.models import User as UserModel
from app.repository.company_actions import CompanyActionsRepository
from app.schemas.action_schemas import ActionDetailResponse, CompanyInvitationListResponse, \
    CompanyJoinRequestListResponse
from app.schemas.user_schemas import UserDetailResponse


class CompanyActionsService:
    def __init__(self, company_action_repo=CompanyActionsRepository):
        self.company_action_repo = company_action_repo()

    async def create_invitation(self,
                                company_id: int,
                                user_id: int,
                                current_user: UserModel
                                ) -> ActionDetailResponse:
        return await self.company_action_repo.create_invitation(company_id, user_id, current_user)

    async def reject_invitation(self, invitation_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.company_action_repo.reject_invitation(invitation_id, current_user)

    async def get_all_invitations(self,
                                  company_id: int,
                                  current_user: UserModel,
                                  page: int,
                                  size: int
                                  ) -> CompanyInvitationListResponse:
        return await self.company_action_repo.get_all_company_invitations(company_id, current_user, page, size)

    async def get_all_join_requests(self,
                                    company_id: int,
                                    current_user: UserModel,
                                    page: int,
                                    size: int
                                    ) -> CompanyJoinRequestListResponse:
        return await self.company_action_repo.get_all_company_join_requests(company_id, current_user, page, size)

    async def accept_join_request(self, join_request_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.company_action_repo.accept_join_request(join_request_id, current_user)

    async def reject_join_request(self, join_request_id: int, current_user: UserModel) -> ActionDetailResponse:
        return await self.company_action_repo.reject_join_request(join_request_id, current_user)

    async def remove_user_from_company(self,
                                       user_id: int,
                                       company_id: int,
                                       current_user: UserModel
                                       ) -> UserDetailResponse:
        return await self.company_action_repo.remove_user_from_company(user_id, company_id, current_user)
