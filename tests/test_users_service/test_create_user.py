import pytest

from .fixtures.data_factories import UserFactory
from users_service.app.graphql.types.enums import UserRole


@pytest.mark.asyncio
async def test_create_user(async_client):
    test_user_data = UserFactory()

    query = """
        mutation CreateUser($input: UserCreateInput!) {
            createUser(input: $input) {
                id
                email
                username
                role
            }
        }
    """

    variables = {
        "input": {
            "email": test_user_data.email,
            "username": test_user_data.username,
            "password": test_user_data.hashed_password,
        }
    }

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["createUser"]["id"] is not None
    assert data["data"]["createUser"]["email"] == test_user_data.email
    assert data["data"]["createUser"]["username"] == test_user_data.username
    assert data["data"]["createUser"]["role"] == UserRole.USER.name


@pytest.mark.asyncio
async def test_create_wrong_user(async_client):
    bad_user_data = UserFactory(email="abcdefgh")

    query = """
        mutation CreateUser($input: UserCreateInput!) {
            createUser(input: $input) {
                id
                email
                username
                role
            }
        }
    """

    variables = {
        "input": {
            "email": bad_user_data.email,
            "username": bad_user_data.username,
            "password": bad_user_data.hashed_password,
        }
    }

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["createUser"] is None
    assert "errors" in data
    assert data["errors"][0]["extensions"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_create_unfulfilled_user(async_client):
    test_user_data = UserFactory()

    query = """
        mutation CreateUser($input: UserCreateInput!) {
            createUser(input: $input) {
                id
                email
                username
                role
            }
        }
    """

    variables = {
        "input": {
            "email": test_user_data.email,
            "username": test_user_data.username,
        }
    }

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert "errors" in data
