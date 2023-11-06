from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, field_validator


class User(BaseModel):
    id: int
    user_email: str
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None


class SingInRequestModel(BaseModel):
    user_email: str
    password: str


class SignUpRequestModel(BaseModel):
    user_email: EmailStr
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_status: Optional[str] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_links: Optional[List[str]] = None
    user_avatar: Optional[str] = None
    password: str


class UserUpdateRequestModel(BaseModel):
    user_email: Optional[str] = Field(examples=[None], default=None)
    user_firstname: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_lastname: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_status: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_city: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_phone: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_links: Optional[List[str]] = None
    user_avatar: Optional[str] = None
    password: Optional[str] = Field(min_length=8, max_length=50, default=None)

    @field_validator("user_email")
    def prevent_email_change(cls, value):
        if value is not None:
            raise ValueError("changing email is prohibited")
        return value


class UserDetailResponse(BaseModel):
    id: int
    user_email: str
    user_firstname: Optional[str] = None
    user_lastname: Optional[str] = None
    user_status: Optional[str] = None
    user_city: Optional[str] = None
    user_phone: Optional[str] = None
    user_links: Optional[List[str]] = None
    user_avatar: Optional[str] = None
    is_superuser: Optional[bool] = False
    created_at: datetime
    updated_at: datetime


class UsersListResponse(BaseModel):
    users: List[User]
