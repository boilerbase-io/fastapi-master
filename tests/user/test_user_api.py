import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.sheared_data.seed_data import USER_DATA
from src.user.models import User


def test_create_user(client: TestClient):
    response = client.post(
        "/signup",
        json={
            "firstname": "test",
            "lastname": "user",
            "email": "test@demo.com",
            "phone_number_country_code": "+1",
            "phone_number": "1234567890",
            "password": "test@123",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    # test response
    response_json = response.json()
    assert response_json["firstname"] == "test"
    assert response_json["lastname"] == "user"
    assert response_json["email"] == "test@demo.com"
    assert response_json["phone_number_country_code"] == "+1"
    assert response_json["phone_number"] == '1234567890'
    assert response_json["email_verified"] is False
    assert response_json["phone_number_verified"] is False
    assert response_json["role"] == "USER"
    assert response_json["is_active"] is True
    assert response_json["is_banned"] is False
    assert response_json.get("id") is None


@pytest.mark.seed_data(
    ("user", USER_DATA[0])
)
def test_login(client: TestClient, seed: None):
    response = client.post(
        "/login",
        json={
            "email": "john@doe.com",
            "password": "test@123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["token"] is not None


def test_get_me(client: TestClient, persisted_user: User):
    response = client.get(
        "/me",
        headers={
            "Authorization": "Bearer " + persisted_user.create_token()
        }
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json["firstname"] == persisted_user.firstname
    assert response_json["lastname"] == persisted_user.lastname
    assert response_json["email"] == persisted_user.email
    assert response_json["phone_number_country_code"] == persisted_user.phone_number_country_code
    assert response_json["phone_number"] == persisted_user.phone_number
    assert response_json["email_verified"] == persisted_user.email_verified
    assert response_json["phone_number_verified"] == persisted_user.phone_number_verified
    assert response_json["role"] == persisted_user.role
    assert response_json["is_active"] == persisted_user.is_active
    assert response_json["is_banned"] == persisted_user.is_banned


@pytest.mark.seed_data(
    ("user", USER_DATA[0])
)
def test_get_users(client: TestClient, seed, persisted_admin_user: User):
    response = client.get(
        "/users",
        headers={
            "Authorization": "Bearer " + persisted_admin_user.create_token()
        }
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 2


@pytest.mark.seed_data(
    ("user", USER_DATA[0])
)
def test_fail_get_users(client: TestClient, seed, persisted_user: User):
    response = client.get(
        "/users",
        headers={
            "Authorization": "Bearer " + persisted_user.create_token()
        }
    )
    breakpoint()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Unauthorized"
