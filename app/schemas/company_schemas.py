from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from app.schemas.user_schemas import User, UserDetailResponse


class Company(BaseModel):
    id: int
    company_name: str
    company_title: Optional[str] = None
    owner_id: int


class CreateCompanyRequestModel(BaseModel):
    company_name: str
    company_title: Optional[str] = None
    company_description: Optional[str] = None
    company_city: Optional[str] = None
    company_phone: Optional[str] = None
    company_links: Optional[List[str]] = None
    company_avatar: Optional[str] = None
    is_visible: Optional[bool] = True


class CompanyUpdateRequestModel(BaseModel):
    company_name: Optional[str] = Field(min_length=1, max_length=255, default=None)
    company_title: Optional[str] = Field(min_length=1, max_length=100, default=None)
    company_description: Optional[str] = Field(min_length=1, default=None)
    company_city: Optional[str] = Field(min_length=1, max_length=50, default=None)
    company_phone: Optional[str] = Field(min_length=1, max_length=50, default=None)
    company_links: Optional[List[str]] = None
    company_avatar: Optional[str] = None
    is_visible: Optional[bool] = True


class CompanyDetailResponse(BaseModel):
    id: int
    company_name: str
    company_title: Optional[str] = None
    company_description: Optional[str] = None
    company_city: Optional[str] = None
    company_phone: Optional[str] = None
    company_links: Optional[List[str]] = None
    company_avatar: Optional[str] = None
    is_visible: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int


class CompanyListResponse(BaseModel):
    companies: List[Company]


class CompanyMembersResponse(BaseModel):
    company_members: List[User]


class CompanyAdminsResponse(BaseModel):
    company_admins: List[User]
