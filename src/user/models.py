from enum import Enum

import jwt
from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Boolean, String

from src.config import Config
from utils.db.base import ModelBase


class UserRoles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class User(ModelBase):
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    image_url = Column(String, nullable=True)

    email = Column(String, unique=True)
    phone_number_country_code = Column(String)
    phone_number = Column(String, unique=True, nullable=True)

    email_verified = Column(Boolean, default=False)
    phone_number_verified = Column(Boolean, default=False)

    password = Column(String, nullable=False)

    role = Column(String, default=UserRoles.USER.value)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    def __repr__(self):
        return f"""
            User INFO:
                ID: {self.id}
                Email: {self.email}
                role: {self.role}
                First Name: {self.firstname}
                Last Name: {self.lastname}
        """

    def set_password(self, password):
        """Hash a password for storing."""
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user"""
        return pbkdf2_sha256.verify(provided_password, self.password)

    def create_token(self):
        return jwt.encode(
            {
                "id": self.id,
                "email": self.email,
                "role": self.role,
                "is_active": self.is_active,
                "is_banned": self.is_banned,
                "exp": Config.JWT_EXPIRATION_TIME,
            },
            key=Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM,
        ).decode("utf-8")
