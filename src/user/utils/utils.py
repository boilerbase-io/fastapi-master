import random
import string
import uuid

from sqlalchemy.orm import Session

from src.user.crud import user_crud
from src.user.schemas import UserBase


def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def get_sso_user(
    db: Session, email: str, given_name: str, family_name: str, picture: str = None
):
    # check if user already exists
    email = email.lower()
    user = user_crud.get_by_email(db, email)
    if user:
        return user

    # create user if not exists
    user_id = str(uuid.uuid4())
    extra_fields = {}
    if picture:
        extra_fields = {"image_url": picture}
    user = user_crud.create(
        db,
        obj_in=UserBase(
            id=user_id,
            email=email,
            password=generate_random_password(),
            firstname=given_name,
            lastname=family_name,
            email_verified=True,
            created_by=user_id,
            updated_by=user_id,
            **extra_fields,
        ),
    )

    return user
