import jwt
from typing import Tuple
from config import Config
from typing import Annotated
from sqlalchemy.orm import Session
from src.user.models import User
from fastapi import HTTPException, status, Request

from fastapi import Depends
from utils.db.session import get_db

from src.user.crud import user_crud


def _authenticated(request: Request):
    try:
        access_token = request.headers.get("Authorization")
        jwt.decode(
            access_token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )

        return True

    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


def _authenticated_user(
    request: Request, db: Session = Depends(get_db)
) -> Tuple[User, Session]:
    try:
        access_token = request.headers.get("Authorization")
        user = None
        if access_token:
            payload = jwt.decode(
                access_token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
            )
            
            user_id = payload["id"]
            if not user_id:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

            user = user_crud.get(db, id=user_id)
            if not user:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid User")
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authorization not found")

        return user, db

    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


is_authorized = Annotated[bool, Depends(_authenticated)]
authenticated_user = Annotated[Tuple[User, Session], Depends(_authenticated_user)]


def _is_authorized_for(roles: list):
    def _is_authorized(user_db: authenticated_user):
        user, _ = user_db
        if user.role in roles:
            return True
        return False

    return _is_authorized


is_authorized_for = lambda _roles: Annotated[bool, Depends(_is_authorized_for(_roles))]
