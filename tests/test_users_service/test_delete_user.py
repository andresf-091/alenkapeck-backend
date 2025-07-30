import strawberry
import pytest
import uuid
from sqlalchemy import select
from .fixtures.data_factories import UserFactory

from users_service.app.models import User


@pytest.mark.asyncio
async def test_delete_user(async_client, db_session):
    test_user = UserFactory()

    db_session.add(test_user)
    await db_session.commit()

    assert test_user.id is not None

    result = await db_session.execute(
        select(User).where(User.username == test_user.username)
    )
    assert result.scalars().first() is not None

    query = """
        mutation DeleteUser($userId: UUID!) {
            deleteUser(userId: $userId) {
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
    assert data["data"]["deleteUser"]["id"] == str(test_user.id)

    result = await db_session.execute(
        select(User).where(User.username == test_user.username)
    )
    assert result.scalars().first() is None


@pytest.mark.asyncio
async def test_delete_user_not_found(async_client, db_session):
    query = """
        mutation DeleteUser($userId: UUID!) {
            deleteUser(userId: $userId) {
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
    assert data["data"]["deleteUser"] is None
    assert "errors" in data
    assert data["errors"][0]["extensions"]["code"] == "NOT_FOUND_ERROR"
