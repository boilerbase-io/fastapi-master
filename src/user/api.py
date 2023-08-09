import uuid
from typing import List

from fastapi import APIRouter, HTTPException, status

from src.user.crud import user_crud
from src.user.models import UserRoles
from src.user.schemas import LoginRequest, Token, UserBase, UserRequest, UserResponse
from src.user.utils.deps import authenticated_user, is_authorized_for
from utils.db.session import get_db

user_router = APIRouter()


@user_router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(user_req: UserRequest, db: get_db):
    user_id = str(uuid.uuid4())
    return user_crud.create(
        db,
        obj_in=UserBase(
            id=user_id, created_by=user_id, updated_by=user_id, **user_req.model_dump()
        ),
    )


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


@user_router.patch(
    "/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def update_user(user_req: UserRequest, user_db: authenticated_user):
    user, db = user_db
    return user_crud.update(db, db_obj=user, obj_in=user_req)


@user_router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_db: authenticated_user):
    user, db = user_db
    user_crud.soft_del(db, db_obj=user)
    return None
