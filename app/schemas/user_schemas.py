from typing import Optional, List

from pydantic import BaseModel, EmailStr, SecretStr, Field


class User(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str


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
    user_firstname: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_lastname: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_status: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_city: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_phone: Optional[str] = Field(min_length=1, max_length=50, default=None)
    user_links: Optional[List[str]] = None
    user_avatar: Optional[str] = None
    password: Optional[str] = Field(min_length=8, max_length=50, default=None)


class UserDetailResponse(BaseModel):
    user_id: int
    user_email: str
    user_firstname: str
    user_lastname: str
    user_status: str
    user_city: str
    user_phone: str
    user_links: List[str]
    user_avatar: str
    is_superuser: bool


class UsersListResponse(BaseModel):
    users: List[User]
