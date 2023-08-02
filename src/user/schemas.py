from typing import Optional
from pydantic import BaseModel
from utils.schemas.base import BaseSchema


class UserUpdate(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    image_url: Optional[str]

    email: Optional[str]
    phone_number_country_code: Optional[str]
    phone_number: Optional[int] = None


class UserRequest(UserUpdate):
    firstname: str
    lastname: str
    email: str
    password: str


class UserResponse(UserRequest):
    email_verified: bool
    phone_number_verified: bool

    role: str
    is_active: bool
    is_banned: bool

    class Config:
        orm_mode = True


class UserBase(BaseSchema, UserResponse):
    id: Optional[str]
    updated_by: Optional[str]


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    token: str
