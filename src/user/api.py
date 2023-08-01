from src.user.schemas import (
    LoginRequest,
    Token,
    UserRequest,
    UserResponse,
)
from fastapi import APIRouter, status, HTTPException
from src.user.crud import user_crud
from user.models import UserRoles
from user.utils.deps import is_authorized_for, authenticated_user
from utils.db.session import get_db
from typing import List

user_router = APIRouter()


@user_router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(user_req: UserRequest, db: get_db):
    return user_crud.create(db, obj_in=user_req)


@user_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(login_creds: LoginRequest, db: get_db):
    user = user_crud.get_by_email(db, login_creds.email)
    if not user and (not user.check_password(login_creds.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return Token(token=user.create_token())


@user_router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def me(user_db: authenticated_user):
    user, _ = user_db
    return user


@user_router.get(
    "/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK
)
def get_users(
    user_db: is_authorized_for([UserRoles.ADMIN.value, UserRoles.SUPER_ADMIN.value])
):
    _, db = user_db

    return user_crud.get_multi(db)


@user_router.patch("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def update_user(
    user_req: UserRequest,
    user_db: authenticated_user
):
    user, db = user_db
    return user_crud.update(db, db_obj=user, obj_in=user_req)

@user_router.delete("/user", status_code=status.HTTP_204_NO_CONTENT, status_code=status.HTTP_201_CREATED)
def delete_user(
    user_db: authenticated_user
):
    user, db = user_db
    return user_crud.soft_del(db, db_obj=user)