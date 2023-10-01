from datetime import datetime
from typing import List

from pydantic import BaseModel


class Action(BaseModel):
    id: int
    user_id: int
    company_id: int
    action: str


class ActionDetailResponse(BaseModel):
    id: int
    user_id: int
    company_id: int
    action: str
    created_at: datetime
    updated_at: datetime


class UserInvitationListResponse(BaseModel):
    user_invitation: List[Action]


class UserJoinRequestListResponse(BaseModel):
    user_join_request: List[Action]


class CompanyInvitationListResponse(BaseModel):
    company_invitation: List[Action]


class CompanyJoinRequestListResponse(BaseModel):
    company_join_request: List[Action]


