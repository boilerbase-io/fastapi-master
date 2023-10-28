import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.user.models import User
from tests.sheared_data.seed_data import USER_DATA


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
    user_info = response_json["user"]
    assert user_info["firstname"] == "test"
    assert user_info["lastname"] == "user"
    assert user_info["email"] == "test@demo.com"
    assert user_info["phone_number_country_code"] == "+1"
    assert user_info["phone_number"] == "1234567890"
    assert user_info["email_verified"] is False
    assert user_info["phone_number_verified"] is False
    assert user_info["role"] == "USER"
    assert user_info["is_active"] is True
    assert user_info["is_banned"] is False
    assert user_info.get("id") is None
    assert response_json["token"] is not None


@pytest.mark.seed_data(("user", USER_DATA[0]))
def test_fail_create_user_email_exists(client: TestClient, seed: None):
    response = client.post(
        "/signup",
        json={
            "firstname": "test",
            "lastname": "user",
            "email": "john@doe.com",
            "phone_number_country_code": "+1",
            "phone_number": "1234567890",
            "password": "test@123",
        },
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "User with this email already exists"


@pytest.mark.seed_data(("user", USER_DATA[0]))
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


@pytest.mark.seed_data(("user", USER_DATA[0]))
def test_fail_login(client: TestClient, seed: None):
    response = client.post(
        "/login",
        json={
            "email": "john@doe.com",
            "password": "wrong-password",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"


def test_get_me(client: TestClient, persisted_user: User):
    response = client.get(
        "/me", headers={"Authorization": "Bearer " + persisted_user.create_token()}
    )
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json["firstname"] == persisted_user.firstname
    assert response_json["lastname"] == persisted_user.lastname
    assert response_json["email"] == persisted_user.email
    assert (
        response_json["phone_number_country_code"]
        == persisted_user.phone_number_country_code
    )
    assert response_json["phone_number"] == persisted_user.phone_number
    assert response_json["email_verified"] == persisted_user.email_verified
    assert (
        response_json["phone_number_verified"] == persisted_user.phone_number_verified
    )
    assert response_json["role"] == persisted_user.role
    assert response_json["is_active"] == persisted_user.is_active
    assert response_json["is_banned"] == persisted_user.is_banned


@pytest.mark.seed_data(("user", USER_DATA[0]))
def test_get_users(client: TestClient, seed, persisted_admin_user: User):
    response = client.get(
        "/users",
        headers={"Authorization": "Bearer " + persisted_admin_user.create_token()},
    )

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert len(response_json) == 2


@pytest.mark.seed_data(("user", USER_DATA[0]))
def test_fail_get_users(client: TestClient, seed, persisted_user: User):
    response = client.get(
        "/users", headers={"Authorization": "Bearer " + persisted_user.create_token()}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Unauthorized"


def test_update_user(client: TestClient, persisted_user: User):
    response = client.patch(
        "/user",
        json={"firstname": "test 123", "lastname": "user 123"},
        headers={"Authorization": "Bearer " + persisted_user.create_token()},
    )

    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["firstname"] == "test 123"
    assert response_json["lastname"] == "user 123"
    assert response_json["email"] == persisted_user.email
    assert (
        response_json["phone_number_country_code"]
        == persisted_user.phone_number_country_code
    )
    assert response_json["phone_number"] == persisted_user.phone_number
    assert response_json["email_verified"] == persisted_user.email_verified
    assert (
        response_json["phone_number_verified"] == persisted_user.phone_number_verified
    )
    assert response_json["role"] == persisted_user.role
    assert response_json["is_active"] == persisted_user.is_active
    assert response_json["is_banned"] == persisted_user.is_banned


def test_fail_update_user(client: TestClient, persisted_user: User):
    response = client.patch(
        "/user",
        json={"firstname": "test 123", "lastname": "user 123"},
        headers={"Authorization": "Bearer " + "1234567890"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid token"


def test_delete_user(client: TestClient, persisted_user: User, db_session: Session):
    response = client.delete(
        "/user", headers={"Authorization": "Bearer " + persisted_user.create_token()}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    user = db_session.query(User).filter(User.id == persisted_user.id).first()
    print(user)
    assert user.is_deleted is True
