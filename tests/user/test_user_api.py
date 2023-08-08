from fastapi import status
from fastapi.testclient import TestClient


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
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
