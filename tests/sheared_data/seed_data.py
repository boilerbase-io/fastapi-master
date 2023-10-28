import pytest
from passlib.hash import pbkdf2_sha256

USER_DATA = [
    {
        "id": pytest.id_for("USER_ID_!"),
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@doe.com",
        "phone_number_country_code": "+1",
        "phone_number": "1234567890",
        "password": pbkdf2_sha256.hash("test@123"),
    }
]
