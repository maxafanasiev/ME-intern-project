from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import company_actions_service
from app.schemas.pagination_schemas import PaginationQueryParams
from app.services.auth_services import auth
from app.services.company_actions import CompanyActionsService
from app.schemas.user_schemas import User as UserModel
from app.schemas.action_schemas import ActionDetailResponse, CompanyInvitationListResponse, \
    CompanyJoinRequestListResponse

router = APIRouter(tags=["company-actions"])


@router.post("/send-invitation/{company_id}/{user_id}",
             response_model=ActionDetailResponse,
             status_code=status.HTTP_201_CREATED)
async def send_invitation(company_id: int,
                          user_id: int,
                          company_actions_service: Annotated[CompanyActionsService, Depends(company_actions_service)],
                          current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.create_invitation(company_id, user_id, current_user)


@router.delete("/reject-invitation/{invitation_id}", response_model=ActionDetailResponse)
async def reject_invitation(company_actions_service: Annotated[CompanyActionsService, Depends(company_actions_service)],
                            invitation_id: int,
                            current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.reject_invitation(invitation_id, current_user)


@router.get("/invitations/{company_id}", response_model=CompanyInvitationListResponse)
async def get_all_invitations(
        company_actions_service: Annotated[CompanyActionsService, Depends(company_actions_service)],
        company_id: int,
        current_user: User = Depends(auth.get_current_user),
        params: PaginationQueryParams = Depends()):
    return await company_actions_service.get_all_invitations(company_id, current_user, params.page, params.size)


@router.get("/join-requests/{company_id}", response_model=CompanyJoinRequestListResponse)
async def get_all_join_requests(
        company_actions_service: Annotated[CompanyActionsService, Depends(company_actions_service)],
        company_id: int,
        current_user: User = Depends(auth.get_current_user),
        params: PaginationQueryParams = Depends()):
    return await company_actions_service.get_all_join_requests(company_id, current_user, params.page, params.size)


@router.post("/accept-join-request/{join_request_id}", response_model=ActionDetailResponse)
async def accept_join_requests(join_request_id: int,
                               company_actions_service: Annotated[
                                   CompanyActionsService, Depends(company_actions_service)],
                               current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.accept_join_request(join_request_id, current_user)


@router.post("/reject-join-request/{join_request_id}", response_model=ActionDetailResponse)
async def reject_join_requests(join_request_id: int,
                               company_actions_service: Annotated[
                                   CompanyActionsService, Depends(company_actions_service)],
                               current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.reject_join_request(join_request_id, current_user)


@router.post("/remove-user-from-company/{company_id}/{user_id}", response_model=UserModel)
async def remove_user_from_company(user_id: int,
                                   company_id: int,
                                   company_actions_service: Annotated[
                                       CompanyActionsService, Depends(company_actions_service)],
                                   current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.remove_user_from_company(user_id, company_id, current_user)


@router.post("/set-admin/{company_id}/{user_id}", response_model=UserModel)
async def set_admin_in_company(user_id: int,
                               company_id: int,
                               company_actions_service: Annotated[
                                   CompanyActionsService, Depends(company_actions_service)],
                               current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.set_admin_from_member(user_id, company_id, current_user)


@router.post("/remove-admin/{company_id}/{user_id}", response_model=UserModel)
async def remove_admin_in_company(user_id: int,
                               company_id: int,
                               company_actions_service: Annotated[
                                   CompanyActionsService, Depends(company_actions_service)],
                               current_user: User = Depends(auth.get_current_user)):
    return await company_actions_service.remove_admin_from_company(user_id, company_id, current_user)