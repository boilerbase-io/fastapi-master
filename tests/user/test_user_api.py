import pytest

from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.seed_data(
    (
        "user", [
            {
                "id": pytest.id_for("USER_ID_1")
            },
            {
                "id": pytest.id_for("USER_ID_2")
            },
            ]
    )
)
def test_get_all_user(client: TestClient, seed, persisted_admin_user):
    response = client.get(
        '/v1/users',
        headers={
            "session-token" : persisted_admin_user.id
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


@pytest.mark.seed_data(
    (
        "user", [
            {
                "id": pytest.id_for("USER_ID_1")
            },
            {
                "id": pytest.id_for("USER_ID_2")
            },
            ]
    )
)
def test_fail_get_all_user(client: TestClient, seed, persisted_user):
    response = client.get(
        '/v1/users',
        headers={
            "session-token" : persisted_user.id
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user(client: TestClient, persisted_user):
    response = client.get(
        '/v1/user',
        headers={
            "session-token" : persisted_user.id
        }
    )
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["firstname"] == persisted_user.firstname
    assert user["lastname"] == persisted_user.lastname
    assert user["email"] == persisted_user.email
    assert str(user["phone_number"]) == persisted_user.phone_number


@pytest.mark.skip(reason="No way to test, Right now check it manually")
def test_create_user():
    # FIXME: Right now check it manually
    pass


@pytest.mark.skip(reason="No way to test, Right now check it manually")
def test_user_login():
    # FIXME: Right now check it manually
    pass


@pytest.mark.skip(reason="No way to test, Right now check it manually")
def test_user_logout():
    # FIXME: Right now check it manually
    pass


@pytest.mark.skip(reason="No way to test, Right now check it manually")
def test_user_auth():
    # FIXME: Right now check it manually
    pass


def test_update_user(client: TestClient, persisted_user):
    response = client.put(
        '/v1/user',
        headers={
            "session-token" : persisted_user.id
        },
        json={
                "firstname": "new_firstname",
                "image_url": "https://userprofile.url",
            }
    )
    assert response.status_code == status.HTTP_201_CREATED
    user = response.json()
    assert user["firstname"] == "new_firstname"
    assert user["lastname"] == persisted_user.lastname
    assert user["email"] == persisted_user.email
    assert user["image_url"] == "https://userprofile.url"
    assert str(user["phone_number"]) == persisted_user.phone_number


@pytest.mark.seed_data(
    (
        "user", {
            "id": pytest.id_for("USER_ID_1"),
        }
    ),
    (
        "preferences", {
            "id": pytest.id_for("USER_PREF_ID_1"),
            "created_by": pytest.id_for("USER_ID_1"),
            "enable_nsfw": True,
            "make_privet_generation": True,
        }
    )
)
def test_get_user_preferences(client: TestClient, seed):
    response = client.get(
        '/v1/user/preferences',
        headers={
            "session-token" : pytest.id_for("USER_ID_1")
        }
    )
    assert response.status_code == status.HTTP_200_OK
    user_pref = response.json()
    assert user_pref["enable_nsfw"] == True
    assert user_pref["make_privet_generation"] == True

@pytest.mark.seed_data(
    (
        "user", {
            "id": pytest.id_for("USER_ID_1"),
        }
    ),
    (
        "preferences", {
            "id": pytest.id_for("USER_PREF_ID_1"),
            "created_by": pytest.id_for("USER_ID_1"),
            "enable_nsfw": True,
            "make_privet_generation": True,
        }
    )
)
def test_update_user_preferences(client: TestClient, seed):
    response = client.put(
        '/v1/user/preferences',
        headers={
            "session-token" : pytest.id_for("USER_ID_1")
        },
        json={
                "enable_nsfw": False
            }
    )
    assert response.status_code == status.HTTP_201_CREATED
    user_pref = response.json()
    assert user_pref["enable_nsfw"] == False
    assert user_pref["make_privet_generation"] == True


@pytest.mark.seed_data(
    (
        "user", {
            "id": pytest.id_for("USER_ID_1"),
        }
    ),
    (
        "user_log", [
            {
                "id": pytest.id_for("USER_LOG_ID_1"),
                "user_id": pytest.id_for("USER_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
            },
            {
                "id": pytest.id_for("USER_LOG_ID_2"),
                "user_id": pytest.id_for("USER_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
            },
            {
                "id": pytest.id_for("USER_LOG_ID_3"),
                "user_id": pytest.id_for("USER_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
            },
            {
                "id": pytest.id_for("USER_LOG_ID_4"),
                "user_id": pytest.id_for("USER_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
            }
        ]
    )
)
def test_get_user_logs(client: TestClient, seed):
    response = client.get(
        '/v1/user/logs',
        headers={
            "session-token" : pytest.id_for("USER_ID_1")
        }
    )
    assert response.status_code == status.HTTP_200_OK
    user_logs = response.json()
    assert len(user_logs) == 4


@pytest.mark.seed_data(
    (
        "user", {
            "id": pytest.id_for("USER_ID_1"),
        }
    ),
    (
        "services", {
                "id": pytest.id_for("SERVICES_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
            }
    ),
    (
        "generation", [
            {
                "id": pytest.id_for("GENERATION_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
                "service_id": pytest.id_for("SERVICES_ID_1"),
            },
            {
                "id": pytest.id_for("GENERATION_ID_2"),
                "created_by": pytest.id_for("USER_ID_1"),
                "service_id": pytest.id_for("SERVICES_ID_1"),
            },
        ]
    ),
    (
        "like", [
            {
                "id": pytest.id_for("USER_LIKE_ID_1"),
                "created_by": pytest.id_for("USER_ID_1"),
                "generation_id": pytest.id_for("GENERATION_ID_1"),
            },
            {
                "id": pytest.id_for("USER_LIKE_ID_2"),
                "created_by": pytest.id_for("USER_ID_1"),
                "generation_id": pytest.id_for("GENERATION_ID_2"),
            },
        ]
    )
)
def test_get_user_like(client: TestClient, seed):
    response = client.get(
        '/v1/user/likes',
        headers={
            "session-token" : pytest.id_for("USER_ID_1")
        }
    )
    assert response.status_code == status.HTTP_200_OK
    user_likes = response.json()
    assert len(user_likes) == 2
    assert all([ pytest.id_for("USER_ID_1") == like["created_by"] for like in user_likes ])
