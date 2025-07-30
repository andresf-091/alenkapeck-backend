import pytest
import uuid
from sqlalchemy import select
from .fixtures.data_factories import UserFactory

from users_service.app.models import User


@pytest.mark.asyncio
async def test_update_user(async_client, db_session):
    test_user_before = UserFactory()
    username_before = test_user_before.username
    email_before = test_user_before.email

    db_session.add(test_user_before)
    await db_session.commit()

    assert test_user_before.id is not None

    query = """
        mutation UpdateUser($userId: UUID!, $input: UserUpdateInput!) {
            updateUser(userId: $userId, input: $input) {
                id
                email
                username
                role
            }
        }
    """

    test_user_after = UserFactory(
        username=username_before + "_new", email="new_" + email_before
    )

    variables = {
        "userId": str(test_user_before.id),
        "input": {
            "email": test_user_after.email,
            "username": test_user_after.username,
        },
    }

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["updateUser"]["email"] == test_user_after.email
    assert data["data"]["updateUser"]["email"] != email_before
    assert data["data"]["updateUser"]["username"] == test_user_after.username


@pytest.mark.asyncio
async def test_update_user_not_found(async_client):
    query = """
        mutation UpdateUser($userId: UUID!, $input: UserUpdateInput!) {
            updateUser(userId: $userId, input: $input) {
                id
                email
                username
                role
            }
        }
    """

    variables = {
        "userId": str(uuid.uuid4()),
        "input": {
            "email": "test@gmail.com",
            "username": "testusername",
        },
    }

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["updateUser"] is None
    assert "errors" in data
    assert data["errors"][0]["extensions"]["code"] == "NOT_FOUND_ERROR"
