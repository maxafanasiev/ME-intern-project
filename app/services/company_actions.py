from app.db.models import User as UserModel
from app.repository.company_actions import CompanyActionsRepository


class CompanyActionsService:
    def __init__(self, company_action_repo=CompanyActionsRepository):
        self.company_action_repo = company_action_repo()

    async def create_invitation(self, company_id, user_id, current_user: UserModel):
        return await self.company_action_repo.create_invitation(company_id, user_id, current_user)

    async def reject_invitation(self, invitation_id, current_user: UserModel):
        return await self.company_action_repo.reject_invitation(invitation_id, current_user)

    async def get_all_invitations(self, company_id, current_user: UserModel, page, size):
        return await self.company_action_repo.get_all_invitations(company_id, current_user, page, size)

    async def get_all_join_requests(self, company_id, current_user: UserModel, page, size):
        return await self.company_action_repo.get_all_join_requests(company_id, current_user, page, size)

    async def accept_join_request(self, join_request_id, current_user: UserModel):
        return await self.company_action_repo.accept_join_request(join_request_id, current_user)

    async def reject_join_request(self, join_request_id, current_user: UserModel):
        return await self.company_action_repo.reject_join_request(join_request_id, current_user)

    async def remove_user_from_company(self, user_id, company_id, current_user: UserModel):
        return await self.company_action_repo.remove_user_from_company(user_id, company_id, current_user)
