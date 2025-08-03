import uuid
import pytest

from .fn.factories import UserFactory


@pytest.mark.asyncio
async def test_get_user(async_client, db_session):
    test_user = UserFactory()

    db_session.add(test_user)
    await db_session.commit()

    assert test_user.id is not None

    query = """
        query GetUser($userId: UUID!) {
            user(userId: $userId) {
                id
                email
                username
                role
            }
        }
    """

    variables = {"userId": str(test_user.id)}

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["user"]["id"] == str(test_user.id)
    assert data["data"]["user"]["email"] == test_user.email
    assert data["data"]["user"]["username"] == test_user.username
    assert data["data"]["user"]["role"] == test_user.role.name


@pytest.mark.asyncio
async def test_get_wrong_user(async_client):
    query = """
        query GetUser($userId: UUID!) {
            user(userId: $userId) {
                id
                email
                username
                role
            }
        }
    """

    variables = {"userId": str(uuid.uuid4())}

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["user"] is None
    assert data["errors"][0]["extensions"]["code"] == "NOT_FOUND_ERROR"


@pytest.mark.asyncio
async def test_get_users(async_client, db_session):
    test_users = [UserFactory() for _ in range(10)]

    for test_user in test_users:
        db_session.add(test_user)

    await db_session.commit()

    query = """
        query GetUsers {
            users {
                id
                email
                username
                role
            }
        }
    """

    response = await async_client.post(
        "/graphql",
        json={"query": query},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    for test_user in test_users:
        assert any(
            user["id"] == str(test_user.id)
            and user["email"] == test_user.email
            and user["username"] == test_user.username
            and user["role"] == test_user.role.name
            for user in data["data"]["users"]
        )


@pytest.mark.asyncio
async def test_get_users_empty(async_client):
    query = """
        query GetUsers {
            users {
                id
                email
                username
                role
            }
        }
    """

    response = await async_client.post(
        "/graphql",
        json={"query": query},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["users"] == []
