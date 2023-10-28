from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.user.models import UserRoles
from utils.schemas.base import BaseSchema


class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    image_url: Optional[str] = None

    email: Optional[str] = None
    phone_number_country_code: Optional[str] = None
    phone_number: Optional[str] = None


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

    # model config for orm models
    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseSchema, UserResponse):
    id: Optional[str]
    updated_by: Optional[str]
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    user: UserResponse
    token: str
