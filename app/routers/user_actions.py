from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import user_actions_service
from app.schemas.pagination_schemas import PaginationQueryParams
from app.services.auth_services import auth
from app.services.user_actions import UserActionsService
from app.routers.dependencies import user_actions_service
from app.schemas.user_schemas import User as UserModel
from app.schemas.action_schemas import ActionDetailResponse, UserInvitationListResponse, UserJoinRequestListResponse, \
    ListNotificationsResponse, NotificationResponse

router = APIRouter(tags=["user-actions"])


@router.post("/send-join-request/{company_id}",
             response_model=ActionDetailResponse,
             status_code=status.HTTP_201_CREATED)
async def send_join_request(company_id: int,
                            user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                            current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.create_join_request(company_id, current_user)


@router.delete("/reject-join-request/{join_request_id}", response_model=ActionDetailResponse)
async def reject_join_request(user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                              join_request_id: int,
                              current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.reject_join_request(join_request_id, current_user)


@router.get("/invitations", response_model=UserInvitationListResponse)
async def get_all_invitations_to_user(
        user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
        current_user: User = Depends(auth.get_current_user),
        params: PaginationQueryParams = Depends()):
    return await user_actions_service.get_all_invitations_to_user(current_user, params.page, params.size)


@router.get("/join-requests", response_model=UserJoinRequestListResponse)
async def get_all_user_join_requests(
        user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
        current_user: User = Depends(auth.get_current_user),
        params: PaginationQueryParams = Depends()):
    return await user_actions_service.get_all_user_join_requests(current_user, params.page, params.size)


@router.post("/accept-invitation/{invitation_id}", response_model=ActionDetailResponse)
async def accept_invitation(invitation_id: int,
                            user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                            current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.accept_invitation(invitation_id, current_user)


@router.post("/reject-invitation/{invitation_id}", response_model=ActionDetailResponse)
async def reject_invitation(invitation_id: int,
                            user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                            current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.reject_invitation(invitation_id, current_user)


@router.post("/leave-from-company/{company_id}", response_model=UserModel)
async def leave_from_company(company_id: int,
                             user_actions_service: Annotated[
                                 UserActionsService, Depends(user_actions_service)],
                             current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.leave_from_company(company_id, current_user)


@router.get("/notifications", response_model=ListNotificationsResponse)
async def get_all_notification(user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                             current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.get_all_notifications(current_user)


@router.post("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(notification_id: int,
                             user_actions_service: Annotated[UserActionsService, Depends(user_actions_service)],
                             current_user: User = Depends(auth.get_current_user)):
    return await user_actions_service.read_notification(notification_id, current_user)
