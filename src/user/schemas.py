from typing import Optional
from pydantic import BaseModel
from user.models import UserRoles
from utils.schemas.base import BaseSchema


class UserUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    image_url: Optional[str] = None

    email: Optional[str]
    phone_number_country_code: Optional[str]
    phone_number: Optional[int] = None


class UserRequest(UserUpdate):
    firstname: str
    lastname: str
    email: str
    password: str


class UserResponse(UserUpdate):
    email_verified: Optional[bool] = False
    phone_number_verified: Optional[bool] = False

    role: str = UserRoles.USER.value
    is_active: bool = True
    is_banned: bool = False

    class Config:
        orm_mode = True


class UserBase(BaseSchema, UserResponse):
    id: Optional[str]
    updated_by: Optional[str]
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
